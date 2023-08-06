# Copyright 2021 StreamSets Inc.

import argparse
import io
import json
import logging
import os
import socket
import tarfile
from uuid import uuid4

import docker
from docker.utils import kwargs_from_env
from javaproperties import PropertiesFile
from streamsets.sdk import ControlHub
from streamsets.sdk.constants import ENGINE_AUTHENTICATION_METHOD_ASTER

from streamsets.testframework import environment, logger as streamsets_logger, sdc
from streamsets.testframework.environments.salesforce import (
    AUTHENTICATION_TYPE_BASIC as SALESFORCE_AUTHENTICATION_TYPE_BASIC,
    AUTHENTICATION_TYPE_OAUTH as SALESFORCE_AUTHENTICATION_TYPE_OAUTH)
from streamsets.testframework.arguments import (_args_to_pytest_item, _check_aws_conditions, _create_aws_instance,
                                                add_test_arguments_to_parser)
from streamsets.testframework.constants import DEFAULT_DOCKER_TIMEOUT, STF_TESTCONFIG_DIR
from streamsets.testframework.sdc_models import CustomLib, DataProtectorStageLib, EnterpriseLib
from streamsets.testframework.utils import (get_stf_env_vars, ShellCommand, run_container_shell_commands,
                                            product_version_is_valid, verify_docker_image_presence,
                                            wait_for_condition, wait_for_container_port_open)


# Get rid of handlers on the root logger to avoid duplicate output (see STF-959).
logging.getLogger().handlers.clear()

logger = logging.getLogger('streamsets.testframework.cli.start_sdc')

docker_client = docker.from_env(**kwargs_from_env())

SDC_DIST = '/local_sdc/streamsets-datacollector'
SDC_DEFAULT_PORT = 18630
SDC_CONTAINER_INFO_FILE_NAME = 'datacollector_container_name.txt'
SDC_CONTAINER_INFO_FILE_PATH = os.path.join(STF_TESTCONFIG_DIR, SDC_CONTAINER_INFO_FILE_NAME)


def _main():
    parser = argparse.ArgumentParser(prog='stf start sdc', description='Start StreamSets Data Collector Docker image',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-v', '--verbose', action='store_true', help='Be noisier')
    parser.add_argument('--docker-network', metavar='network', default='cluster',
                        help='Docker network to which to attach the STF container')
    parser.add_argument('--hostname', metavar='name', help='SDC container hostname')
    parser.add_argument('--https', nargs='?', const='encryption', choices=['encryption'],
                        help='Configure SDC instance for HTTPS encryption')
    parser.add_argument('--port', help=f'Configure SDC instance to run on this port. Default is {SDC_DEFAULT_PORT}.')
    parser.add_argument('--predictable', action='store_true', help='If set, expose the same SDC port to the host')
    parser.add_argument('--store-id', action='store_true', help=f'Store the SDC ID in {sdc.SDC_ID_FILE_PATH}')

    non_local_group = parser.add_argument_group('Non local SDC')
    non_local_group.add_argument('-a', '--always-pull', action='store_true',
                                 help='Always pull new SDC/stage lib Docker images')
    non_local_group.add_argument('--enable-base-http-url',
                                 choices=['public', 'private'],
                                 help=('If set to ``"public"``, "sdc.base.http.url" is enabled with the actual '
                                       'IP of the host where SDC container runs and if set to ``"private"``, container '
                                       ' hostname is used'))
    non_local_group.add_argument('--java-heap-size',
                                 help='Data Collector Java heap size to use (use m for MB and g for GB)')
    non_local_group.add_argument('--sdc-property',
                                 help='<key>=<value> configuration to set in the sdc.properties file at startup',
                                 action='append',
                                 default=[])
    non_local_group.add_argument('--skip-default-stage-libs', action='store_true',
                                 help='While starting StreamSets Data Collector do not add stage libs that '
                                 'get added by default e.g. jython')
    non_local_group.add_argument('--stage-lib', nargs='+',
                                 help="One or more stage libs to add (e.g. 'basic jdbc')", metavar='lib')
    non_local_group.add_argument('--sdp-stage-lib-version',
                                 help="Version of SDP libraries to include", metavar='sdp_stage_lib_version')
    non_local_group.add_argument('--docker-label',
                                 help=argparse.SUPPRESS,
                                 action='append',
                                 default=[])
    non_local_group.add_argument('--version',
                                 help=('Version of SDC to start. This can be a <version> or '
                                       'Git hash as in git:<hash> format'),
                                 metavar='ver')

    local_group = parser.add_argument_group('Local SDC')
    local_group.add_argument('-d', '--directory',
                             help='SDC dist directory to load SDC from', metavar='path')
    local_group.add_argument('-t', '--sdc-template-image-version',
                             help='Version of SDC to use as a template for local Docker image', metavar='ver')

    add_test_arguments_to_parser(parser)

    args = parser.parse_args()
    streamsets_logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)
    if args.directory:
        _start_sdc_local(args)
    else:
        _start_sdc(args)


def _start_sdc(args):
    if not (args.sch_credential_id and args.sch_token):
        raise ValueError('--sch-credential-id and --sch-token args are required')
    if not args.version:
        raise ValueError('--version arg is required')
    if not product_version_is_valid(args.version):
        raise ValueError('--version arg needs to be a <version> or Git hash in git:<hash> format')
    if args.sdc_authentication_method == ENGINE_AUTHENTICATION_METHOD_ASTER:
        if not (args.aster_server_url and args.aster_authentication_token):
            raise ValueError('Tests run only if "aster-server-url" and "aster-authentication-token"'
                             ' both are specified with --sdc-authentication-method as "aster".')

    if args.predictable:
        sdc.DATA_COLLECTOR_PREDICTABLE_PORT = True
    if args.port:
        sdc.DATA_COLLECTOR_PORT = args.port
    control_hub = ControlHub(credential_id=args.sch_credential_id,
                             token=args.sch_token,
                             use_websocket_tunneling=not args.sch_dont_use_websocket_tunneling,
                             aster_url=args.aster_server_url)
    sdc_args = {
        'always_pull': args.always_pull,
        'aster_authentication_token': args.aster_authentication_token,
        'aster_server_url': args.aster_server_url,
        'authentication_method': args.sdc_authentication_method,
        'https': args.https,
        'network': args.docker_network,
        'control_hub': control_hub,
        'hostname': args.hostname,
        'enable_base_http_url': args.enable_base_http_url
    }
    if args.version.startswith('git:'):
        sdc_args['git_hash'] = args.version[4:]
    else:
        sdc_args['version'] = args.version
    data_collector = sdc.DataCollector(**sdc_args)

    data_collector.docker_env_vars.update(get_stf_env_vars())

    data_collector.docker_labels = {item.split('=', 1)[0]: item.split('=', 1)[1] for item in args.docker_label}

    data_collector._skip_default_stage_libs = True if args.skip_default_stage_libs else False
    for property_ in args.sdc_property:
        key, value = property_.split('=', 1)
        logger.debug('Setting property %s=%s', key, value)
        if key not in data_collector.sdc_properties:
            logger.warning('Could not find property %s in sdc.properties. Ignoring ...', key)
        else:
            data_collector.sdc_properties[key] = value
    if args.java_heap_size:
        logger.debug('Setting Java heap size to %s ...', args.java_heap_size)
        data_collector.SDC_JAVA_OPTS = f'-Xmx{args.java_heap_size} -Xms{args.java_heap_size}'
    if control_hub:
        logger.debug('Enabling Control Hub ...')
        data_collector.enable_control_hub()

    if args.cluster_server:
        data_collector.configure_for_environment(environment.Cluster(cluster_server=args.cluster_server, args=args))
    if args.database:
        if args.database.startswith('snowflake://'):
            database = environment.SnowflakeInstance(database=args.database,
                                                     snowflake_database_name=args.snowflake_database_name,
                                                     snowflake_warehouse=args.snowflake_warehouse,
                                                     snowflake_schema=args.snowflake_schema)
        else:
            database = environment.Database(database=args.database,
                                            username=args.database_username,
                                            password=args.database_password,
                                            verbose=bool(args.verbose),
                                            ca_certificate=args.database_server_ca_certificate,
                                            server_certificate=args.database_server_certificate,
                                            ssh_url=args.ssh_url)
        data_collector.configure_for_environment(database)

    if args.deltalake_jdbc_connection_string:
        auth_method = args.azure_datalake_storage_gen2_auth_method
        fqdn = args.azure_datalake_storage_account_fqdn
        filesystem_id = args.azure_datalake_storage_gen2_filesystem_id
        deltalake = environment.DatabricksDeltalakeInstance(args.deltalake_jdbc_connection_string,
                                                            cluster_name=args.databricks_cluster_name,
                                                            adls_gen2_auth_method=auth_method,
                                                            auth_token_endpoint=args.azure_auth_token_endpoint,
                                                            adls_gen2_account_fqdn=fqdn,
                                                            s3_bucket_name=args.aws_s3_bucket_name,
                                                            adls_gen2_filesystem_id=filesystem_id)
        data_collector.configure_for_environment(deltalake)

    if (args.gcp_project_name or args.gcp_project_id) and args.gcp_credentials_filename:
        gcp_environment = environment.GCPInstance(credentials_filename=args.gcp_credentials_filename,
                                                  project_name=args.gcp_project_name,
                                                  project_id=args.gcp_project_id,
                                                  bigtable_instance_name=args.gcp_bigtable_instance_name)
        data_collector.configure_for_environment(gcp_environment)

    if args.elasticsearch_url:
        elasticsearch = environment.Elasticsearch(url=args.elasticsearch_url)
        data_collector.configure_for_environment(elasticsearch)

    aws_check = _check_aws_conditions(_args_to_pytest_item(args))
    if any([getattr(aws_check, field) for field in aws_check._fields]):
        aws_environment = _create_aws_instance(args)
        data_collector.configure_for_environment(aws_environment)

    if args.salesforce_authentication_type:
        if args.salesforce_authentication_type == SALESFORCE_AUTHENTICATION_TYPE_BASIC:
            salesforce_environment = environment.Salesforce(username=args.salesforce_username,
                                                            password=args.salesforce_password,
                                                            domain=args.salesforce_domain)
        elif args.salesforce_authentication_type == SALESFORCE_AUTHENTICATION_TYPE_OAUTH:
            salesforce_private_key_file = os.path.join(STF_TESTCONFIG_DIR, args.salesforce_private_key_filename)
            if not os.path.isfile(salesforce_private_key_file):
                raise ValueError(f'Given --salesforce-private-key-filename ({args.salesforce_private_key_filename}) '
                                 'is not found in testframework config directory '
                                 f'({os.environ.get("TESTFRAMEWORK_CONFIG_DIRECTORY")})')
            salesforce_environment = environment.Salesforce(username=args.salesforce_username,
                                                            consumer_key=args.salesforce_consumer_key,
                                                            private_key_file=salesforce_private_key_file,
                                                            domain=args.salesforce_domain)
        data_collector.configure_for_environment(salesforce_environment)

    if args.stage_lib:
        data_collector.add_stage_lib(*[f'streamsets-datacollector-{lib}-lib'
                                       for lib in args.stage_lib])

    if args.custom_stage_lib:
        data_collector.add_stage_lib(*[CustomLib(f"streamsets-datacollector-{lib.split(',')[0]}-lib",
                                                 lib.split(',')[1])
                                       for lib in args.custom_stage_lib])

    if args.enterprise_stage_lib:
        data_collector.add_stage_lib(*[EnterpriseLib(f"streamsets-datacollector-{lib.split(',')[0]}-lib",
                                                     lib.split(',')[1])
                                       for lib in args.enterprise_stage_lib])

    if args.sdp_stage_lib_version:
        data_collector.add_stage_lib(*[DataProtectorStageLib("streamsets-datacollector-dataprotector-lib",
                                                             args.sdp_stage_lib_version)])

    data_collector.start()

    # Write SDC info file
    with open(sdc.SDC_SYSTEM_INFO_FILE_PATH, 'w') as system_info:
        system_info.write(json.dumps(data_collector.system_info))
    with open(SDC_CONTAINER_INFO_FILE_PATH, 'w') as container_info:
        container_info.write(data_collector.container.id)
    if args.store_id:
        with open(sdc.SDC_ID_FILE_PATH, 'w') as f:
            f.write(data_collector.id)
    logger.info('SDC info file available at %s',
                os.path.join(os.environ.get('TESTFRAMEWORK_CONFIG_DIRECTORY'), sdc.SDC_SYSTEM_INFO_FILE_NAME))
    logger.info('SDC ID: %s', data_collector.id)

    if control_hub and args.sch_executor_sdc_label:
        logger.debug('Adding DataCollector labels ...')
        _wait_for_sdc_availability_in_sch(control_hub, data_collector.id)
        sch_data_collector = control_hub.data_collectors.get(id=data_collector.id)
        sch_data_collector.labels = args.sch_executor_sdc_label.split(',')
        control_hub.update_engine_labels(sch_data_collector)


def _wait_for_sdc_availability_in_sch(control_hub, data_collector_id, timeout=120):
    def condition(control_hub, data_collector_id):
        try:
            sch_data_collector = control_hub.data_collectors.get(id=data_collector_id)
        except ValueError as ve:
            return False
        return sch_data_collector is not None

    def success(time):
        logger.debug('SDC available in %s seconds.', time)

    def failure(timeout):
        raise TimeoutError('Timed out after {} seconds waiting '
                           'for SDC to be available.'.format(timeout))

    wait_for_condition(condition=condition, condition_args=[control_hub, data_collector_id],
                       time_between_checks=3, timeout=timeout, success=success, failure=failure)


def _start_sdc_local(args):
    """
    Given an SDC directory, start it in a container.
    """
    if not args.directory or not args.sdc_template_image_version:
        raise ValueError('--directory and --sdc-template-image-version args are required')

    control_hub = ControlHub(credential_id=args.sch_credential_id,
                             token=args.sch_token,
                             use_websocket_tunneling=not args.sch_dont_use_websocket_tunneling,
                             aster_url=args.aster_server_url)
    directory = args.directory
    network = args.docker_network
    image = '{}:{}'.format(sdc.DATACOLLECTOR_DOCKER_REPO, args.sdc_template_image_version)
    docker_client = docker.APIClient(timeout=DEFAULT_DOCKER_TIMEOUT, **kwargs_from_env())
    verify_docker_image_presence(docker_client, image)

    sdc_container_id = docker_client.create_container(image=image, host_config=docker_client.create_host_config(
        binds=[f'{directory}:{SDC_DIST}']))

    bits, stat = docker_client.get_archive(container=sdc_container_id, path=f'{SDC_DIST}/etc/sdc.properties')
    tarstream = io.BytesIO()
    for chunk in bits:
        tarstream.write(chunk)
    tarstream.seek(0)

    with tarfile.open(fileobj=tarstream) as tarfile_:
        for tarinfo in tarfile_.getmembers():
            sdc_properties_data = tarfile_.extractfile(tarinfo).read().decode()
    docker_client.remove_container(container=sdc_container_id, v=True, force=True)
    sdc_properties = PropertiesFile.loads(sdc_properties_data)

    server_port = sdc_properties['http.port' if not args.https else 'https.port']
    sentinel_file = '/tmp/{}'.format(uuid4())

    docker_env_vars = {
        'SDC_CONF': '/local_sdc/etc',
        'SDC_DATA': '/local_sdc/data',
        'SDC_DIST': SDC_DIST,
        'SDC_LOG': '/local_sdc/logs',
        'SDC_RESOURCES': '/local_sdc/resources',
        'SDC_USER': 'sdc',
        'STREAMSETS_LIBRARIES_EXTRA_DIR': '/local_sdc/streamsets-datacollector/streamsets-libs-extras',
        'USER_LIBRARIES_DIR': '/opt/streamsets-datacollector-user-libs'
    }
    docker_env_vars.update(get_stf_env_vars())

    container_args = {
        'command': ("""'until [ -f "{0}" ]; do sleep 1; done; """
                    """exec "${{SDC_DIST}}/bin/streamsets" """
                    """dc -exec'""".format(sentinel_file)),
        'detach': True,
        'entrypoint': 'bash -c',
        'environment': docker_env_vars,
        'ports': [server_port],
        'image': image,
        'host_config': docker_client.create_host_config(network_mode=args.docker_network,
                                                        publish_all_ports=True,
                                                        binds=[f'{directory}:{SDC_DIST}']),
    }

    container_id = docker_client.create_container(**container_args)['Id']
    docker_client.start(container_id)

    inspect_data = docker_client.inspect_container(container_id)
    sdc_port_on_host = inspect_data['NetworkSettings']['Ports']['{0}/tcp'.format(server_port)][0]['HostPort']
    container_hostname = inspect_data['Config']['Hostname']
    scheme = 'https' if args.https else 'http'
    container_server_url = f'{scheme}://{container_hostname}:{server_port}'
    # This is more user-friendly URL so that users can use it from a browser.
    exposed_server_url = f'{scheme}://{socket.gethostname()}:{sdc_port_on_host}'

    logger.info('Starting StreamSets Data Collector (SDC) in %s container on %s container port ...',
                container_hostname, server_port)

    shell_commands = [
        ShellCommand(command=f'cp -r /local_sdc/streamsets-datacollector/etc /local_sdc/etc', user='root'),
        ShellCommand(command=f'rm -rf /opt/streamsets-datacollector-user-libs', user='root'),
        ShellCommand(command=f'/tmp/sdc-configure.sh', user='root'),
        ShellCommand(command='touch {}'.format(sentinel_file), user='root')
    ]
    try:
        run_container_shell_commands(docker_client, container_id, shell_commands, args.verbose)
        logger.info('SDC is configured. Waiting for SDC to start ...')
        wait_for_container_port_open(docker_client, container_id, port=int(server_port),
                                     timeout_sec=1200, verbose=args.verbose)
        logger.info('SDC is now running. SDC container (%s:%s) can be followed along on %s',
                    container_hostname, server_port, exposed_server_url)

        # Write SDC info file
        sdc.get_data_collector_info(control_hub, server_url=container_server_url, write_info_file=True)
        with open(SDC_CONTAINER_INFO_FILE_PATH, 'w') as container_info:
            container_info.write(container_id)
    except:
        logger.error('Error reaching SDC. SDC log follows ...')
        print('------------------------- SDC log - Begins -----------------------')
        print(docker_client.logs(container_id).decode())
        print('------------------------- SDC log - Ends -------------------------')
        raise


if __name__ == '__main__':
    _main()
