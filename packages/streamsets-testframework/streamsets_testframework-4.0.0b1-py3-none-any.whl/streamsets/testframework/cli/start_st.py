# Copyright 2021 StreamSets Inc.

import argparse
import json
import logging
import os
from uuid import uuid4

import docker
from javaproperties import PropertiesFile
from streamsets.sdk import ControlHub
from streamsets.sdk.constants import ENGINE_AUTHENTICATION_METHOD_ASTER

from streamsets.testframework import environment, logger as streamsets_logger, st
from streamsets.testframework.arguments import add_environment_arguments_to_parser
from streamsets.testframework.constants import DEFAULT_DOCKER_TIMEOUT, ST_TESTCONFIG_DIR, STF_TESTCONFIG_DIR
from streamsets.testframework.credential_store import CredentialStore
from streamsets.testframework.st_models import CustomLib, EnterpriseLib
from streamsets.testframework.utils import (check_docker_image, get_docker_file, gethostname, get_stf_env_vars,
                                            product_version_is_valid, put_docker_file, run_container_shell_commands,
                                            ShellCommand, wait_for_condition, wait_for_container_port_open)

# Get rid of handlers on the root logger to avoid duplicate output (see STF-959).
logging.getLogger().handlers.clear()

logger = logging.getLogger('streamsets.testframework.cli.start_st')

docker_client = docker.APIClient(timeout=DEFAULT_DOCKER_TIMEOUT)

ST_DIST = '/local_st/streamsets-transformer'
TRANSFORMER_DEFAULT_PORT = 19630
# Note: names sensitive to other systems using it (e.g. STE)
TRANSFORMER_CONTAINER_INFO_FILE_NAME = 'transformer_container_name.txt'
TRANSFORMER_CONTAINER_INFO_FILE_PATH = os.path.join(STF_TESTCONFIG_DIR, TRANSFORMER_CONTAINER_INFO_FILE_NAME)


def _main():
    parser = argparse.ArgumentParser(prog='stf start st', description='Start StreamSets Transformer Docker image',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-v', '--verbose', action='store_true', help='Be noisier')
    parser.add_argument('--docker-network', metavar='network', default='cluster',
                        help='Docker network to which to attach the STF container')
    parser.add_argument('--hostname', metavar='name', help='ST container hostname')
    parser.add_argument('--https', nargs='?', const='encryption', choices=['encryption'],
                        help='Configure ST instance for HTTPS encryption')
    parser.add_argument('--port', help=f'Configure Transformer instance to run on this port. '
                                       f'Default is {TRANSFORMER_DEFAULT_PORT}.')
    parser.add_argument('--import-ca-cert-filename',
                        help=('CA certificate file to import into Transformer Java runtime trust store. File is '
                              f'assumed to exist in {os.environ.get("TESTFRAMEWORK_CONFIG_DIRECTORY")} directory'))
    parser.add_argument('--predictable', action='store_true', help='If set, expose the same ST port to the host')
    parser.add_argument('--store-id', action='store_true',
                        help=f'Store the Transformer ID in {st.TRANSFORMER_ID_FILE_PATH}')

    non_local_group = parser.add_argument_group('Non local ST')
    non_local_group.add_argument('-a', '--always-pull', action='store_true',
                                 help='Always pull new ST/stage lib Docker images')
    parser.add_argument('--aster-server-url', help='Aster URL')
    parser.add_argument('--aster-authentication-token', help='Aster authentication token')
    parser.add_argument('--authentication-method', help='Transformer authentication method',
                        choices=[ENGINE_AUTHENTICATION_METHOD_ASTER])
    non_local_group.add_argument('--enable-base-http-url',
                                 choices=['public', 'private'],
                                 help=('If set to ``"public"``, "sdc.base.http.url" and "transformer.base.http.url" '
                                       ' are enabled with the actual IP of the host where SDC Transformer runs'
                                       ' and if set to ``"private"``, container '
                                       ' hostname is used'))
    non_local_group.add_argument('--scala-version', nargs='?', default=None,
                                 help='Version of scala to install e.g. 2.12', metavar='ver')
    non_local_group.add_argument('--sch-token', help='StreamSets Control Hub token')
    non_local_group.add_argument('--sch-credential-id', help='StreamSets Control Hub credential ID')
    non_local_group.add_argument('--sch-executor-transformer-label',
                                 help='A comma-separated list of Transformer labels to use to run jobs')
    non_local_group.add_argument('--sch-dont-use-websocket-tunneling', action='store_true',
                                 help='Do not use WebSocket tunneling for communication with execution engines')
    non_local_group.add_argument('--spark-version', default=None,
                                 help='Version of Spark to install e.g. 2.4.1_hdp2.7', metavar='ver')
    non_local_group.add_argument('--stage-lib', nargs='+',
                                 help="One or more stage libs to add (e.g. 'transformer-jdbc')", metavar='lib')
    non_local_group.add_argument('--transformer-property',
                                 help=('<key>=<value> configuration to set in the '
                                       'transformer.properties file at startup'),
                                 action='append',
                                 default=[])
    non_local_group.add_argument('--version',
                                 help=('Version of Transformer to start. This can be a <version> or '
                                       'Git hash as in git:<hash> format'),
                                 metavar='ver')

    local_group = parser.add_argument_group('Local ST')
    local_group.add_argument('-d', '--directory',
                             help='Transformer dist directory to load Transformer from', metavar='path')
    local_group.add_argument('-t', '--st-template-image-version',
                             help='Version of Transformer to use as a template for local Docker image', metavar='ver')

    parser = add_environment_arguments_to_parser(parser)

    args = parser.parse_args()
    if args.authentication_method == ENGINE_AUTHENTICATION_METHOD_ASTER:
        if not (args.aster_server_url and args.aster_authentication_token):
            raise ValueError('Tests run only if "--aster-server-url" and "--aster-authentication-token"'
                             ' both are specified with --authentication-method '
                             f'as "{ENGINE_AUTHENTICATION_METHOD_ASTER}".')

    if args.predictable:
        st.TRANSFORMER_PREDICTABLE_PORT = True
    if args.port:
        st.TRANSFORMER_PORT = args.port
    streamsets_logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)

    if args.directory:
        _start_st_local(args)
    else:
        _start_st(args)


def _start_st(args):
    if not (args.sch_credential_id and args.sch_token):
        raise ValueError('--sch-credential-id and --sch-token args are required')
    if not args.version:
        raise ValueError('--version arg is required')
    if not product_version_is_valid(args.version):
        raise ValueError('--version arg needs to be a <version> or Git hash in git:<hash> format')

    control_hub = ControlHub(credential_id=args.sch_credential_id,
                             token=args.sch_token,
                             use_websocket_tunneling=not args.sch_dont_use_websocket_tunneling,
                             aster_url=args.aster_server_url)

    transformer_args = {
        'always_pull': args.always_pull,
        'aster_authentication_token': args.aster_authentication_token,
        'aster_server_url': args.aster_server_url,
        'authentication_method': args.authentication_method,
        'https': args.https,
        'network': args.docker_network,
        'control_hub': control_hub,
        'hostname': args.hostname,
        'enable_base_http_url': args.enable_base_http_url,
        'scala_version': args.scala_version
    }
    if args.version.startswith('git:'):
        transformer_args['git_hash'] = args.version[4:]
    else:
        transformer_args['version'] = args.version
    transformer = st.Transformer(**transformer_args)

    transformer.docker_env_vars.update(get_stf_env_vars())

    for property_ in args.transformer_property:
        key, value = property_.split('=', 1)
        logger.debug('Setting property %s=%s', key, value)
        if key not in transformer.st_properties:
            logger.warning('Could not find property %s in transformer.properties. Adding ...', key)
            transformer.st_properties[key] = value
        else:
            transformer.st_properties[key] = value

    if args.import_ca_cert_filename:
        transformer.add_ca_certificate(args.import_ca_cert_filename)

    if control_hub:
        logger.debug('Enabling Control Hub ...')
        transformer.enable_control_hub()

    if args.cluster_server:
        transformer.configure_for_environment(environment.Cluster(args.cluster_server))

    if args.stage_lib:
        transformer.add_stage_lib(*[f'streamsets-{lib}-lib' for lib in args.stage_lib])

    if args.custom_stage_lib:
        transformer.add_stage_lib(*[CustomLib(f"streamsets-transformer-{lib.split(',')[0]}-lib", lib.split(',')[1])
                                    for lib in args.custom_stage_lib])

    if args.enterprise_stage_lib:
        transformer.add_stage_lib(*[EnterpriseLib(f"streamsets-transformer-{lib.split(',')[0]}-lib", lib.split(',')[1])
                                    for lib in args.enterprise_stage_lib])

    if args.spark_version:
        logger.debug('Installing Spark')
        transformer.add_environment_lib('spark{}'.format(args.spark_version))

    if args.credential_store_id:
        logger.debug('Enabling credential store `%s`', args.credential_store_id)
        credential_store = CredentialStore(store_id=args.credential_store_id, args=args)
        transformer.configure_for_environment(credential_store)

    transformer.start()

    # Write Transformer info file
    with open(st.TRANSFORMER_SYSTEM_INFO_FILE_PATH, 'w') as system_info:
        system_info.write(json.dumps(transformer.system_info))
    with open(TRANSFORMER_CONTAINER_INFO_FILE_PATH, 'w') as container_info:
        container_info.write(transformer.container.id)
    if args.store_id:
        with open(st.TRANSFORMER_ID_FILE_PATH, 'w') as f:
            f.write(transformer.id)
    logger.info('Transformer info file available at %s',
                os.path.join(os.environ.get('TESTFRAMEWORK_CONFIG_DIRECTORY'), st.TRANSFORMER_SYSTEM_INFO_FILE_NAME))
    logger.info('Transformer ID: %s', transformer.id)

    if control_hub and args.sch_executor_transformer_label:
        logger.debug('Adding Transformer labels ...')
        _wait_for_transformer_availability_in_sch(control_hub, transformer.id)
        sch_transformer = control_hub.transformers.get(id=transformer.id)
        sch_transformer.labels = args.sch_executor_transformer_label.split(',')
        control_hub.update_engine_labels(sch_transformer)


def _wait_for_transformer_availability_in_sch(control_hub, transformer_id, timeout=30):
    def condition(control_hub, transformer_id):
        try:
            sch_transformer = control_hub.transformers.get(id=transformer_id)
        except ValueError as ve:
            return False
        return sch_transformer is not None

    def success(time):
        logger.debug('Transformer available in %s seconds.', time)

    def failure(timeout):
        raise TimeoutError('Timed out after {} seconds waiting '
                           'for Transformer to be available.'.format(timeout))

    wait_for_condition(condition=condition, condition_args=[control_hub, transformer_id],
                       time_between_checks=3, timeout=timeout, success=success, failure=failure)


def _start_st_local(args):
    if not args.directory or not args.st_template_image_version:
        raise ValueError('--directory and --st-template-image-version args are required')

    control_hub = ControlHub(credential_id=args.sch_credential_id,
                             token=args.sch_token,
                             use_websocket_tunneling=not args.sch_dont_use_websocket_tunneling,
                             aster_url=args.aster_server_url)
    directory = args.directory
    network = args.docker_network
    image = '{}:{}'.format(st.TRANSFORMER_DOCKER_REPO, args.st_template_image_version)
    transformer_properties_path = '/etc/transformer/transformer.properties'

    logger.info('Attempting to pull Transformer image (%s) as a template for this Transformer container ...', image)
    check_docker_image(docker_client, image, args.always_pull)
    st_container_id = docker_client.create_container(image=image, host_config=docker_client.create_host_config(
        binds=[f'{directory}:{ST_DIST}']))

    st_properties_data = get_docker_file(docker_client, st_container_id, transformer_properties_path)
    docker_client.remove_container(container=st_container_id, v=True, force=True)
    st_properties = PropertiesFile.loads(st_properties_data)

    server_port = st_properties['http.port' if not args.https else 'https.port']
    sentinel_file = '/tmp/{}'.format(uuid4())

    docker_env_vars = {
        'TRANSFORMER_ACTIVATION_KEY': os.environ.get('TRANSFORMER_ACTIVATION_KEY'),
        'TRANSFORMER_CONF': '/local_st/etc',
        'TRANSFORMER_DATA': '/local_st/data',
        'TRANSFORMER_DIST': ST_DIST,
        'TRANSFORMER_HOME': ST_DIST,
        'TRANSFORMER_LOG': '/local_st/logs',
        'TRANSFORMER_RESOURCES': '/local_st/resources',
        'TRANSFORMER_USER': 'transformer',
        # is in-line to what Transformer Docker file has and is what extra lib images (e.g. jdbc) expects
        'STREAMSETS_LIBRARIES_EXTRA_DIR': '/opt/streamsets-libs-extras',
        'USER_LIBRARIES_DIR': '/opt/streamsets-transformer-user-libs'
    }
    docker_env_vars.update(get_stf_env_vars())

    binds_list = [f'{os.environ["TESTFRAMEWORK_CONFIG_DIRECTORY"]}:{ST_TESTCONFIG_DIR}',
                  f'{directory}:{ST_DIST}']
    container_args = {
        'command': ("""'until [ -f "{0}" ]; do sleep 1; done; """
                    """exec "${{TRANSFORMER_DIST}}/bin/streamsets" """
                    """transformer -exec'""".format(sentinel_file)),
        'detach': True,
        'entrypoint': 'bash -c',
        'environment': docker_env_vars,
        'hostname': f'{args.hostname}.{args.docker_network}' if args.hostname else None,
        'ports': [server_port],
        'image': image,
        'volumes': [ST_TESTCONFIG_DIR],
        'host_config': docker_client.create_host_config(network_mode=args.docker_network,
                                                        port_bindings=({server_port: server_port}
                                                                       if st.TRANSFORMER_PREDICTABLE_PORT
                                                                       else None),
                                                        publish_all_ports=True,
                                                        binds=binds_list),
        'networking_config': docker_client.create_networking_config({
            args.docker_network: docker_client.create_endpoint_config(aliases=[args.hostname])
        }),
    }

    container_id = docker_client.create_container(**container_args)['Id']
    docker_client.start(container_id)

    inspect_data = docker_client.inspect_container(container_id)
    st_port_on_host = inspect_data['NetworkSettings']['Ports']['{0}/tcp'.format(server_port)][0]['HostPort']
    container_hostname = inspect_data['Config']['Hostname']
    scheme = 'https' if args.https else 'http'
    container_server_url = f'{scheme}://{container_hostname}:{server_port}'
    # This is more user-friendly URL so that users can use it from a browser.
    # Note: when its enable_base_http_url, we set the public IP address, so as the host can be reached from WAN
    exposed_server_host = gethostname(args.enable_base_http_url)
    exposed_server_url = f'{scheme}://{exposed_server_host}:{st_port_on_host}'

    if args.enable_base_http_url:
        # sdc.base.http.url is also set for Transformer backward compatibility
        st_properties['sdc.base.http.url'] = exposed_server_url
        st_properties['transformer.base.http.url'] = exposed_server_url

    # Serialize and copy properties file into Transformer container
    put_docker_file(docker_client, container_id, transformer_properties_path, PropertiesFile.dumps(st_properties))

    shell_commands = []

    if args.import_ca_cert_filename:
        cert_alias = os.path.splitext(args.import_ca_cert_filename)[0]
        logger.debug('CA certificate file %s will be imported as alias %s into Transformer trust store ...',
                     args.import_ca_cert_filename, cert_alias)
        shell_commands.append(ShellCommand(command=("bash -c ' sudo keytool -import -trustcacerts "
                                                    "-keystore $JAVA_HOME/jre/lib/security/cacerts -storepass changeit "
                                                    f"-noprompt -alias {cert_alias} -file "
                                                    f"{ST_TESTCONFIG_DIR}/{args.import_ca_cert_filename} &>/dev/null'"),
                                           user='root'))

    logger.info('Starting Transformer in %s container on %s container port ...', container_hostname, server_port)

    shell_commands.extend([
        ShellCommand(command=f'cp -r {ST_DIST}/etc /local_st/etc', user='root'),
        ShellCommand(command=f'rm -rf /opt/streamsets-transformer-user-libs/*', user='root'),
        ShellCommand(command=f'/tmp/st-configure.sh', user='root'),
        ShellCommand(command='touch {}'.format(sentinel_file), user='root')
    ])
    run_container_shell_commands(docker_client, container_id, shell_commands, args.verbose)
    try:
        logger.info('Transformer is configured. Waiting for Transformer to start ...')
        wait_for_container_port_open(docker_client, container_id, port=int(server_port),
                                     timeout_sec=90, verbose=args.verbose)
        logger.info('Transformer is now running. Transformer container (%s:%s) can be followed along on %s',
                    container_hostname, server_port, exposed_server_url)

        # Write Transformer info file
        st.get_transformer_info(control_hub, server_url=container_server_url, write_info_file=True)
        with open(TRANSFORMER_CONTAINER_INFO_FILE_PATH, 'w') as container_info:
            container_info.write(container_id)
    except:
        logger.error('Error reaching Transformer. Transformer log follows ...')
        print('------------------------- Transformer log - Begins -----------------------')
        print(docker_client.logs(container_id).decode())
        print('------------------------- Transformer log - Ends -------------------------')
        raise


if __name__ == '__main__':
    _main()
