# Copyright 2020 StreamSets Inc.

import argparse
import collections
import contextlib
import io
import logging
import os
import re
import subprocess
import sys
import tarfile
import textwrap
from itertools import chain
from pathlib import Path
from tempfile import TemporaryDirectory

import backoff
import boto3
import botocore
import javaproperties
from botocore.handlers import disable_signing

from streamsets.sdk.utils import Version
from streamsets.testframework import constants, logger as streamsets_logger
from streamsets.testframework.sdc import get_data_collector_info
from streamsets.testframework.st import (TRANSFORMER_2_11_SCALA_VERSION, TRANSFORMER_2_12_SCALA_VERSION,
                                         get_transformer_info)
from streamsets.testframework.utils import get_gzip_jar_contents

DEFAULT_S3_BUCKET = 'nightly.streamsets.com'
DEFAULT_BUILD = 'latest'
DEFAULT_BUILD_PREFIX = 'datacollector'
DEFAULT_BUILD_SUFFIX = 'tarball'
DEFAULT_ENTERPRISE_STAGE_LIBRARY_DOCKER_REPO = 'streamsets/enterprise-datacollector-libs'
DEFAULT_ENVIRONMENT_LIBRARIES_DOCKER_REPO = 'streamsets/environment-libs'
DEFAULT_ENVIRONMENT_LIBRARIES_ROOT_DIRECTORY_PATH = Path('/root/testframework/streamsets/testframework/libraries/'
                                                         'environment')
DEFAULT_EXTRA_LIBRARIES_DOCKER_REPO = 'streamsets/sdc-extra-libs'
DEFAULT_EXTRA_LIBRARIES_ROOT_DIRECTORY_PATH = Path('/root/testframework/streamsets/testframework/libraries/extra')
DEFAULT_DATAPROTECTOR_DIRECTORY_PATH = Path('/root/testframework/streamsets/testframework/libraries/stage')
DEFAULT_DOCKER_REPO = 'streamsets/datacollector-libs'
DEFAULT_LEGACY_BUILD_SUFFIX = 'legacy'
DEFAULT_SDC_DOCKER_REPO_URL = 'https://github.com/streamsets/datacollector-docker.git'
DEFAULT_ST_DIRECTORY_PATH = Path(os.getcwd())
DEFAULT_STAGE_LIB_MANIFEST_FILENAME = 'stage-lib-manifest.properties'
DEFAULT_STAGE_LIBRARIES_DIRECTORY_PATH = Path('/root/testframework/streamsets/testframework/libraries/stage')
DEFAULT_BUILD_ARGS = []

# Minimum SDC versions to enforce for stages.
SDC_MIN_VERSION = {'streamsets-datacollector-pmml-lib': '3.5.0'}

# Minimum SDC version to build docker image with activation bits.
# From this version onwards, any SDC docker image will have activation bits.
SDC_MIN_VERSION_WITH_ACTIVATION_BITS = '3.19.0'

# Minimum Transformer version to build docker image supporting Aster.
# From this version onwards, any Transformer docker image will need to pick up bits from tarball/aster path in S3.
TRANSFORMER_MIN_VERSION_WITH_ASTER = '3.16.0'

# Minimum Transformer version to build docker images supporting both Scala 2.11 and Scala 2.12.
# From this version onwards for Transformer, two docker images will be created.
TRANSFORMER_MIN_VERSION_WITH_DIFF_SCALA_VERSIONS = '3.17.0'

# Get rid of handlers on the root logger to avoid duplicate output (see STF-959).
logging.getLogger().handlers.clear()

logger = logging.getLogger('streamsets.testframework.cli.build')


# Useful to get newlines in the print help
class ArgumentHybridFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass


class DockerImage:
    def __init__(self, name, tags, dockerfile_path, build_args, labels=[], options={}):
        self.name = name
        self.tags = tags
        self.dockerfile_path = dockerfile_path
        self.build_args = build_args
        self.labels = labels
        self.options = options


def main():
    """Main function invoked from command line."""
    parser = argparse.ArgumentParser(
        prog='stf build',
        description='Build the Docker images used by the StreamSets Test Framework',
        formatter_class=ArgumentHybridFormatter
    )

    parser.add_argument('-v', '--verbose', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('--s3-bucket',
                        help='S3 bucket to get tarballs from',
                        default=DEFAULT_S3_BUCKET)
    parser.add_argument('--build',
                        help='The build to use from S3 (e.g. of the form "2038," "2.4," "latest", '
                             '"master/latest/2.12")',
                        default=DEFAULT_BUILD)
    parser.add_argument('--use-aws-credentials',
                        help='If set, use local AWS credentials when communicating with Amazon S3',
                        action='store_true')
    parser.add_argument('--dry-run',
                        help="Don't actually do the `docker build`",
                        action='store_true')
    parser.add_argument('--version-tag',
                        help='A tag to use for images instead of the version gleamed from '
                             'stage-lib-manifest.properties',
                        metavar='tag')
    parser.add_argument('--stage-library',
                        help='Stage library to build (e.g. streamsets-datacollector-basic-lib); can be invoked '
                             'multiple times to specify several, but will default to selecting all available '
                             'stage libraries if omitted',
                        action='append')
    parser.add_argument('--push',
                        help='Push Docker images after building',
                        action='store_true')
    parser.add_argument('--build-arg',
                        help='Build argument to pass to docker build command',
                        action='append',
                        default=DEFAULT_BUILD_ARGS)
    parser.add_argument('--build-prefix',
                        help='Key prefix to use',
                        default=DEFAULT_BUILD_PREFIX)
    parser.add_argument('--build-suffix',
                        help='Key suffix to use',
                        default=DEFAULT_BUILD_SUFFIX)
    parser.add_argument('--docker-option',
                        help='Docker option to pass to docker build command',
                        action='append',
                        default=[])
    parser.add_argument('--docker-repo',
                        help='Docker repo to use',
                        default=DEFAULT_DOCKER_REPO)

    subparsers = parser.add_subparsers(help='Build targets', dest='target')

    sdc_subparser = subparsers.add_parser('sdc', help='Build SDC image', formatter_class=ArgumentHybridFormatter)
    dataprotector_subparser = subparsers.add_parser('dataprotector', help='Build Data Protector image',
                                                    formatter_class=ArgumentHybridFormatter)
    st_subparser = subparsers.add_parser('st', help='Build Transformer image', formatter_class=ArgumentHybridFormatter)
    st_subparser.add_argument('--transformer-scala-version',
                              help='Scala version to use for Transformer',
                              default=TRANSFORMER_2_11_SCALA_VERSION)
    stage_subparser = subparsers.add_parser('stage-libraries', help='Build SDC stage libraries',
                                            formatter_class=ArgumentHybridFormatter)
    additional_stage_subparser = subparsers.add_parser('additional-stage-libraries',
                                                       help='Build SDC additional stage libraries',
                                                       formatter_class=ArgumentHybridFormatter)

    extras_subparser = subparsers.add_parser('extras', help='Build extra libraries', add_help=False,
                                             formatter_class=ArgumentHybridFormatter)
    extras_subparser.add_argument('--extra-library',
                                  help='Extra library to build; can be invoked multiple times to specify several, '
                                       'but will default to selecting all available extra libraries if omitted',
                                  action='append')
    extras_subparser.add_argument('--extra-library-docker-repo',
                                  help='Docker repo to use for extra libraries',
                                  default=DEFAULT_EXTRA_LIBRARIES_DOCKER_REPO)

    enterprise_stage_subparser = subparsers.add_parser('enterprise-stage-library',
                                                       help='Build enterprise library',
                                                       formatter_class=ArgumentHybridFormatter)
    enterprise_stage_subparser.add_argument('--enterprise-stage-library-docker-repo',
                                            help='Docker repo to use for enterprise library',
                                            default=DEFAULT_ENTERPRISE_STAGE_LIBRARY_DOCKER_REPO)

    environments_subparser = subparsers.add_parser('environments', help='Build environment libraries',
                                                   add_help=False, formatter_class=ArgumentHybridFormatter)
    environments_subparser.add_argument('--environment-library',
                                        help='Environment library to build; can be invoked multiple times to specify '
                                             'several, but will default to selecting all available environment '
                                             'libraries if omitted',
                                        action='append')
    environments_subparser.add_argument('--environment-library-docker-repo',
                                        help='Docker repo to use for environment libraries',
                                        default=DEFAULT_ENVIRONMENT_LIBRARIES_DOCKER_REPO)

    # all args assumed to be set before this. Doing to get any help to be added for subcommands later.
    args, unknown_args = parser.parse_known_args()
    streamsets_logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)

    bucket = _get_s3_bucket(args)
    images = []

    if args.target in ['stage-libraries', 'additional-stage-libraries']:
        _add_stage_libs_images(args, bucket, images)
    elif args.target == 'enterprise-stage-library':
        _add_enterprise_stage_lib_images(args, bucket, images)
    elif args.target == 'extras':
        _handle_extra_libs(args, images, extras_subparser)
    elif args.target == 'environments':
        _handle_environment_libs(args, images, environments_subparser)
    elif args.target == 'sdc':
        _add_sdc_image(args, bucket, images)
    elif args.target == 'st':
        _add_st_image(args, bucket, images)
    elif args.target == 'dataprotector':
        _add_dataprotector_image(args, bucket, images)

    parser.parse_args()

    if args.dry_run:
        logger.info('Doing dry-run of tool ...')

    images_with_build_errors = build_images(images=images,
                                            dry_run=args.dry_run)

    images_with_tag_errors = tag_images(set(images)
                                        - images_with_build_errors,
                                        dry_run=args.dry_run)

    images_with_push_errors = (push_images(set(images)
                                           - images_with_build_errors
                                           - images_with_tag_errors,
                                           dry_run=args.dry_run)
                               if args.push
                               else set())

    images_without_errors = (set(images)
                             - images_with_build_errors
                             - images_with_tag_errors
                             - images_with_push_errors)

    if images_without_errors:
        logger.info('%s images were successfully created:\n%s',
                    len(images_without_errors),
                    '\n'.join('* {0}'.format(image.name) for image in sorted(images_without_errors,
                                                                             key=lambda image: image.name)))

    if images_with_build_errors:
        logger.error('%s images had build errors:\n%s',
                     len(images_with_build_errors),
                     '\n'.join('* {0}'.format(image.name) for image in sorted(images_with_build_errors,
                                                                              key=lambda image: image.name)))

    if images_with_tag_errors:
        logger.error('%s images had tag errors:\n%s',
                     len(images_with_tag_errors),
                     '\n'.join('* {0}'.format(image.name) for image in sorted(images_with_tag_errors,
                                                                              key=lambda image: image.name)))
    if images_with_push_errors:
        logger.error('%s images had push errors:\n%s',
                     len(images_with_push_errors),
                     '\n'.join('* {0}'.format(image.name) for image in sorted(images_with_push_errors,
                                                                              key=lambda image: image.name)))

    if args.target == 'st':
        _cleanup_st_build(bucket, images)

    if images_with_build_errors or images_with_push_errors:
        sys.exit(1)


def _add_st_image(args, bucket, images):
    key_prefix = '/'.join((args.build_prefix, args.build, args.build_suffix) if args.build_prefix else
                          (args.build, args.build_suffix))
    manifest_version = _get_stage_lib_version(bucket=bucket, key_prefix=key_prefix)
    # Pick up the binary from folder 'aster' in S3 if applicable
    if Version(manifest_version) >= Version(TRANSFORMER_MIN_VERSION_WITH_ASTER):
        key_prefix = f'{key_prefix}/aster'

    if Version(manifest_version) >= Version(TRANSFORMER_MIN_VERSION_WITH_DIFF_SCALA_VERSIONS):
        _add_content_specific_transformer_image(args, bucket, images, key_prefix, manifest_version)
    else:
        _add_transformer_image(args, bucket, images, key_prefix, manifest_version)


def _add_transformer_image(args, bucket, images, key_prefix, manifest_version):
    tag_version = args.version_tag or manifest_version
    tag_version_latest = _get_version_with_latest_tag(tag_version)
    logger.info('This will build image for version %s ...', manifest_version)

    st_dist_name = f'streamsets-transformer-all-{manifest_version}.tgz'
    st_dist_file_path = os.path.join(os.getcwd(), st_dist_name)
    st_dist_key = f'{key_prefix}/{st_dist_name}'
    if not os.path.exists(st_dist_file_path):
        _s3_download_file(bucket, st_dist_key, os.getcwd())

    docker_options = dict(
        **{option_arg.split('=')[0]: option_arg.split('=')[1]
           for option_arg in args.docker_option}
    )

    build_args = dict(
        TRANSFORMER_URL=_get_s3_object_url(bucket, st_dist_key),
        TRANSFORMER_VERSION=manifest_version,
        **{build_arg.split('=')[0]: build_arg.split('=')[1]
           for build_arg in args.build_arg}
    )

    # Add buildinfo labels
    dist_jar_file_path = (f'streamsets-transformer-{manifest_version}/api-lib/'
                          f'streamsets-transformer-dist-{manifest_version}.jar')
    dist_files_content = get_gzip_jar_contents(st_dist_file_path, dist_jar_file_path, ['buildinfo.properties'])
    # check on multiple files (like in ver 3.14.0) and if found get exact named file
    build_info_content = (dist_files_content['transformer-buildinfo.properties']
                          if len(dist_files_content) > 0 else list(dist_files_content.values())[0])
    properties = javaproperties.PropertiesFile.loads(build_info_content)
    docker_labels = ['{}-{}={}'.format(constants.TRANSFORMER_DOCKER_LABEL_PREFIX,
                                       prop_key.replace('.', '-'), properties[prop_key])
                     for prop_key in properties]
    docker_labels.append('{}={}'.format(constants.TRANSFORMER_DOCKER_LABEL_TAG_VERSION, tag_version))
    repo_sha = properties['built.repo.sha']

    images.append(DockerImage(
        name=f'streamsets/transformer:{tag_version}',
        tags=[f'streamsets/transformer:{tag_version_latest}', f'streamsets/transformer:{repo_sha}'],
        dockerfile_path=DEFAULT_ST_DIRECTORY_PATH,
        options=docker_options,
        build_args=build_args,
        labels=docker_labels
    ))


# Adds an image which has specific tag depending on the binary contents
# e.g. scala_2.12-3.17.0
def _add_content_specific_transformer_image(args, bucket, images, key_prefix, manifest_version):
    st_dist_name = f'streamsets-transformer-all_{args.transformer_scala_version}-{manifest_version}.tgz'
    tag_version_with_scala = 'scala-{}_{}'.format(args.transformer_scala_version, args.version_tag or manifest_version)
    tag_version_without_scala = args.version_tag or manifest_version
    tag_version_latest = _get_version_with_latest_tag(tag_version=tag_version_without_scala,
                                                      scala_version=args.transformer_scala_version)
    logger.info('This will build image for version %s ...', manifest_version)

    st_dist_file_path = os.path.join(os.getcwd(), st_dist_name)
    st_dist_key = f'{key_prefix}/{st_dist_name}'
    logger.info('The S3 key of the file to download is %s ', st_dist_key)

    if not os.path.exists(st_dist_file_path):
        _s3_download_file(bucket, st_dist_key, os.getcwd())

    docker_options = dict(
        **{option_arg.split('=')[0]: option_arg.split('=')[1]
           for option_arg in args.docker_option}
    )

    build_args = dict(
        TRANSFORMER_URL=_get_s3_object_url(bucket, st_dist_key),
        TRANSFORMER_VERSION=manifest_version,
        **{build_arg.split('=')[0]: build_arg.split('=')[1]
           for build_arg in args.build_arg}
    )

    # Add buildinfo labels
    dist_jar_file_path = (f'streamsets-transformer_{args.transformer_scala_version}-{manifest_version}/api-lib/'
                          f'streamsets-transformer-dist_{args.transformer_scala_version}-{manifest_version}.jar')
    dist_files_content = get_gzip_jar_contents(st_dist_file_path, dist_jar_file_path, ['buildinfo.properties'])
    # check on multiple files (like in ver 3.14.0) and if found get exact named file
    build_info_content = (dist_files_content['transformer-buildinfo.properties']
                          if len(dist_files_content) > 0 else list(dist_files_content.values())[0])
    properties = javaproperties.PropertiesFile.loads(build_info_content)
    docker_labels = ['{}-{}={}'.format(constants.TRANSFORMER_DOCKER_LABEL_PREFIX,
                                       prop_key.replace('.', '-'), properties[prop_key])
                     for prop_key in properties]
    docker_labels.append('{}={}'.format(constants.TRANSFORMER_DOCKER_LABEL_TAG_VERSION, tag_version_with_scala))
    repo_sha = properties['built.repo.sha']
    # For scala 2.12, refer to a different Dockerfile
    if args.transformer_scala_version == TRANSFORMER_2_12_SCALA_VERSION:
        docker_options.update({'file': 'spark3/Dockerfile'})

    images.append(DockerImage(
        name=f'streamsets/transformer:{tag_version_with_scala}',
        tags=[f'streamsets/transformer:{tag_version_latest}',
              f'streamsets/transformer:scala-{args.transformer_scala_version}_{repo_sha}'],
        dockerfile_path=DEFAULT_ST_DIRECTORY_PATH,
        options=docker_options,
        build_args=build_args,
        labels=docker_labels
    ))


def _cleanup_st_build(bucket, images):
    for image in images:
        if 'TRANSFORMER_URL' in image.build_args:
            destination_file = os.path.join(DEFAULT_ST_DIRECTORY_PATH,
                                            image.build_args['TRANSFORMER_URL'].split('/')[-1])
            with contextlib.suppress(FileNotFoundError):
                os.remove(destination_file)


def _add_sdc_image(args, bucket, images):
    key_prefix = '/'.join((args.build_prefix, args.build, args.build_suffix))

    manifest_version = _get_stage_lib_version(bucket=bucket, key_prefix=key_prefix.split('/activation')[0])
    if Version(SDC_MIN_VERSION_WITH_ACTIVATION_BITS) <= Version(manifest_version):
        if not key_prefix.endswith('/activation'):
            key_prefix = f'{key_prefix}/activation'
    s3_dist_file_key = os.path.join(key_prefix, f'streamsets-datacollector-core-{manifest_version}.tgz')
    logger.info('The S3 key of the jar file %s ', s3_dist_file_key)
    tag_version = args.version_tag or manifest_version
    tag_version_latest = _get_version_with_latest_tag(tag_version)
    logger.info('This will build image for version %s ...', manifest_version)

    docker_options = dict(
        **{option_arg.split('=')[0]: option_arg.split('=')[1]
           for option_arg in args.docker_option}
    )

    build_args = dict(
        SDC_URL=_get_s3_object_url(bucket, s3_dist_file_key),
        SDC_VERSION=manifest_version,
        **{build_arg.split('=')[0]: build_arg.split('=')[1]
           for build_arg in args.build_arg}
    )

    # Add buildinfo labels
    dist_jar_file_path = (f'streamsets-datacollector-{manifest_version}/container-lib/'
                          f'streamsets-datacollector-container-{manifest_version}.jar')
    dist_files_content = _get_s3_dist_jar_files(bucket, s3_dist_file_key, dist_jar_file_path, ['buildinfo.properties'])
    properties = javaproperties.PropertiesFile.loads(list(dist_files_content.values())[0])
    docker_labels = ['{}-{}={}'.format(constants.DATACOLLECTOR_DOCKER_LABEL_PREFIX,
                                       prop_key.replace('.', '-'), properties[prop_key])
                     for prop_key in properties]
    docker_labels.append('{}={}'.format(constants.DATACOLLECTOR_DOCKER_LABEL_TAG_VERSION, tag_version))
    repo_sha = properties['built.repo.sha']

    images.append(DockerImage(
        name=f'streamsets/datacollector:{tag_version}',
        tags=[f'streamsets/datacollector:{tag_version_latest}', f'streamsets/datacollector:{repo_sha}'],
        dockerfile_path=DEFAULT_SDC_DOCKER_REPO_URL,
        options=docker_options,
        build_args=build_args,
        labels=docker_labels
    ))


def _add_dataprotector_image(args, bucket, images):
    # DEFAULT_BUILD_PREFIX constant does not apply for dataprotector build
    build_prefix = args.build_prefix if args.build_prefix != DEFAULT_BUILD_PREFIX else None
    key_prefix = '/'.join((args.build_prefix, args.build, args.build_suffix) if build_prefix else
                          (args.build, args.build_suffix))
    manifest_version = _get_stage_lib_version(bucket=bucket, key_prefix=key_prefix)
    tag_version = args.version_tag or manifest_version
    tag_version_latest = _get_version_with_latest_tag(tag_version)
    logger.info('This will build image for version %s ...', manifest_version)

    docker_options = dict(
        **{option_arg.split('=')[0]: option_arg.split('=')[1]
           for option_arg in args.docker_option}
    )

    stage_lib_name = 'streamsets-datacollector-dataprotector-lib'
    build_args = dict(
        SDC_MIN_VERSION=SDC_MIN_VERSION.get(stage_lib_name, '1.0.0'),
        STAGE_LIB_ROOT=('/opt/streamsets-datacollector-user-libs'),
        STAGE_LIB_DIRECTORY=(f'/opt/streamsets-datacollector-user-libs/{stage_lib_name}'),
        STAGE_LIB_S3_BUCKET=args.s3_bucket,
        STAGE_LIB_S3_OBJECT_KEY=f'{key_prefix}/{stage_lib_name}-{manifest_version}.tgz',
        STAGE_LIB_VERSION=manifest_version,
        **{build_arg.split('=')[0]: build_arg.split('=')[1]
           for build_arg in args.build_arg}
    )

    images.append(DockerImage(
        name=f'streamsets/dataprotector:{stage_lib_name}-{tag_version}',
        tags=[f'streamsets/dataprotector:{stage_lib_name}-{tag_version_latest}'],
        dockerfile_path=DEFAULT_DATAPROTECTOR_DIRECTORY_PATH,
        options=docker_options,
        build_args=build_args
    ))


def _add_stage_libs_images(args, bucket, images):
    # Stage libs can be current or legacy. To handle the latter case, we compose both possibilities,
    # looking for tarballs at the former location first.
    key_prefix = '/'.join((args.build_prefix, args.build, args.build_suffix)).split('/activation')[0]
    legacy_key_prefix = '/'.join((args.build_prefix, args.build, DEFAULT_LEGACY_BUILD_SUFFIX))

    manifest_version = _get_stage_lib_version(bucket=bucket, key_prefix=key_prefix)
    tag_version = args.version_tag or manifest_version
    tag_version_latest = _get_version_with_latest_tag(tag_version)

    # Add buildinfo labels - stage libs are specifically assumed to be SDC based - diverge when others are introduced
    s3_dist_file_key = os.path.join(key_prefix, f'streamsets-datacollector-core-{manifest_version}.tgz')
    dist_jar_file_path = (f'streamsets-datacollector-{manifest_version}/container-lib/'
                          f'streamsets-datacollector-container-{manifest_version}.jar')
    dist_files_content = _get_s3_dist_jar_files(bucket, s3_dist_file_key, dist_jar_file_path, ['buildinfo.properties'])

    if dist_files_content:
        properties = javaproperties.PropertiesFile.loads(list(dist_files_content.values())[0])
        docker_labels = ['{}-{}={}'.format(constants.DATACOLLECTOR_DOCKER_LABEL_PREFIX,
                                           prop_key.replace('.', '-'), properties[prop_key])
                         for prop_key in properties]
        git_hash_tag = properties['built.repo.sha']
        logger.info('This will build images for version %s with Git hash %s ...', manifest_version, git_hash_tag)

    else:
        logger.info('This will build images for version %s ...', manifest_version)
        git_hash_tag = None
        docker_labels = []

    docker_options = dict(
        **{option_arg.split('=')[0]: option_arg.split('=')[1]
           for option_arg in args.docker_option}
    )

    is_additional_stage_lib = (args.target == 'additional-stage-libraries')
    for object_ in chain(bucket.objects.filter(Prefix=key_prefix.split('/activation')[0]),
                         bucket.objects.filter(Prefix=legacy_key_prefix)):
        if object_.key.endswith(f'-lib-{manifest_version}.tgz'):
            key_match = re.search(f"{key_prefix.split('/activation')[0]}/(.*)-{manifest_version}.tgz", object_.key)
            legacy_key_match = re.search(f'{legacy_key_prefix}/(.*)-{manifest_version}.tgz', object_.key)
            is_legacy_stage_lib = bool(legacy_key_match)
            stage_lib_name = (key_match or legacy_key_match).group(1)

            name = f'{args.docker_repo}:{stage_lib_name}-{tag_version}'
            tags = [f'{args.docker_repo}:{stage_lib_name}-{tag_version_latest}']
            if git_hash_tag:
                tags.append(f'{args.docker_repo}:{stage_lib_name}-{git_hash_tag}')
            tarball_url = _get_s3_object_url(bucket, object_.key)

            build_args = dict(
                SDC_MIN_VERSION=SDC_MIN_VERSION.get(stage_lib_name, '1.0.0'),
                STAGE_LIB_ROOT=('/opt/streamsets-datacollector-user-libs'
                                if is_legacy_stage_lib or is_additional_stage_lib
                                else '/opt'),
                STAGE_LIB_DIRECTORY=(f'/opt/streamsets-datacollector-user-libs/{stage_lib_name}'
                                     if is_legacy_stage_lib or is_additional_stage_lib
                                     else (f'/opt/streamsets-datacollector-{manifest_version}/'
                                           f'streamsets-libs/{stage_lib_name}')),
                STAGE_LIB_S3_BUCKET=args.s3_bucket,
                STAGE_LIB_S3_OBJECT_KEY=object_.key,
                STAGE_LIB_VERSION=manifest_version,
                **{build_arg.split('=')[0]: build_arg.split('=')[1]
                   for build_arg in args.build_arg}
            )

            if not args.stage_library or stage_lib_name in args.stage_library:
                images.append(DockerImage(name=name,
                                          tags=tags,
                                          dockerfile_path=DEFAULT_STAGE_LIBRARIES_DIRECTORY_PATH,
                                          options=docker_options,
                                          build_args=build_args,
                                          labels=docker_labels))


def _add_enterprise_stage_lib_images(args, bucket, images):
    key_prefix = '/'.join((args.build_prefix, args.build, args.build_suffix))
    for object_ in bucket.objects.filter(Prefix=key_prefix):
        if object_.key.endswith('.tgz'):
            logger.info('object_.key = %s', object_.key)
            object_key_lib_version = object_.key.split('lib-')[1].strip('.tgz')
            tag_version = args.version_tag or object_key_lib_version
            tag_version_latest = _get_version_with_latest_tag(tag_version)

            key_match = re.search(f'{key_prefix.rstrip("/")}/(.*)-{object_key_lib_version}.tgz', object_.key)
            stage_lib_name = (key_match).group(1)

            name = f'{args.docker_repo}:{stage_lib_name}-{tag_version}'
            tags = [f'{args.docker_repo}:{stage_lib_name}-{tag_version_latest}']

            stage_lib_root = constants.DATACOLLECTOR_CUSTOM_LIBS_MOUNT_POINT
            stage_lib_directory = f'{stage_lib_root}/{stage_lib_name}'

            docker_options = dict(
                **{option_arg.split('=')[0]: option_arg.split('=')[1]
                   for option_arg in args.docker_option}
            )

            build_args = dict(
                SDC_MIN_VERSION=SDC_MIN_VERSION.get(stage_lib_name, '1.0.0'),
                STAGE_LIB_ROOT=stage_lib_root,
                STAGE_LIB_DIRECTORY=stage_lib_directory,
                STAGE_LIB_S3_BUCKET=args.s3_bucket,
                STAGE_LIB_S3_OBJECT_KEY=object_.key,
                STAGE_LIB_VERSION=object_key_lib_version,
                **{build_arg.split('=')[0]: build_arg.split('=')[1]
                   for build_arg in args.build_arg}
            )

            if not args.stage_library or stage_lib_name in args.stage_library:
                images.append(DockerImage(name=name,
                                          tags=tags,
                                          dockerfile_path=DEFAULT_STAGE_LIBRARIES_DIRECTORY_PATH,
                                          options=docker_options,
                                          build_args=build_args))


def _handle_extra_libs(args, images, extras_subparser):
    build_args = {build_arg.split('=')[0]: build_arg.split('=')[1] for build_arg in args.build_arg}
    extra_lib_names = [name for name in os.listdir(DEFAULT_EXTRA_LIBRARIES_ROOT_DIRECTORY_PATH)
                       if os.path.isdir(DEFAULT_EXTRA_LIBRARIES_ROOT_DIRECTORY_PATH.joinpath(name))]

    docker_options = dict(
        **{option_arg.split('=')[0]: option_arg.split('=')[1]
           for option_arg in args.docker_option}
    )

    for extra_lib_name in extra_lib_names:
        if not args.extra_library or extra_lib_name in args.extra_library:
            name = f'{args.extra_library_docker_repo}:{extra_lib_name}'
            images.append(
                DockerImage(name=name,
                            tags=[],
                            dockerfile_path=DEFAULT_EXTRA_LIBRARIES_ROOT_DIRECTORY_PATH.joinpath(extra_lib_name),
                            options=docker_options,
                            build_args=build_args))
    print_extra_libs = ('''
            Applicable extra libraries
            --------------------------
            {}
            ''').format('\n        '.join(sorted(extra_lib_names)))
    extras_subparser.description = textwrap.dedent(print_extra_libs)
    _add_help(extras_subparser)


def _handle_environment_libs(args, images, environments_subparser):
    build_args = {build_arg.split('=')[0]: build_arg.split('=')[1] for build_arg in args.build_arg}
    env_lib_names = [name for name in os.listdir(DEFAULT_ENVIRONMENT_LIBRARIES_ROOT_DIRECTORY_PATH)
                     if os.path.isdir(DEFAULT_ENVIRONMENT_LIBRARIES_ROOT_DIRECTORY_PATH.joinpath(name))]

    docker_options = dict(
        **{option_arg.split('=')[0]: option_arg.split('=')[1]
           for option_arg in args.docker_option}
    )

    for env_lib_name in env_lib_names:
        if not args.environment_library or env_lib_name in args.environment_library:
            name = f'{args.environment_library_docker_repo}:{env_lib_name}'
            images.append(DockerImage(name=name, tags=[],
                                      dockerfile_path=
                                      DEFAULT_ENVIRONMENT_LIBRARIES_ROOT_DIRECTORY_PATH.joinpath(env_lib_name),
                                      options=docker_options,
                                      build_args=build_args))
    print_env_libs = ('''
            Applicable environment libraries
            --------------------------------
            {}
            ''').format('\n        '.join(sorted(env_lib_names)))
    environments_subparser.description = textwrap.dedent(print_env_libs)
    _add_help(environments_subparser)


def build_images(images, dry_run):
    """Do the actual building of Docker images.

    Args:
        images (:obj:`list`): List of :py:class:`streamsets.testframework.cli.build.DockerImage` instances.
        dry_run (:obj:`bool`): If ``True``, don't actually execute Docker commands (but display what they are).

    Returns:
        (:obj:`set`): A set of images with build errors.
    """
    # To handle any errors during the `docker build`, keep a set. This will also be used to exclude
    # images from being pushed if this script is run with --push.
    images_with_build_errors = set()
    exception_to_check = subprocess.CalledProcessError

    @backoff.on_exception(backoff.expo, exception_to_check, max_tries=3)
    def _build_image(image):
        cmd = (f'docker build --no-cache --force-rm --rm -t {image.name} '
               + ' '.join(f'--label {label}' for label in image.labels) + ' '
               + ' '.join(f'--{key} {value}' for key, value in image.options.items()) + ' '
               + ' '.join(f'--build-arg {key}={value}' for key, value in image.build_args.items())
               + f' {image.dockerfile_path}')
        logger.debug('Running Docker build command (%s) ...', cmd)
        if not dry_run:
            subprocess.run(cmd, shell=True, check=True)

    for image in sorted(images, key=lambda image: image.name):
        try:
            _build_image(image)
        except exception_to_check:
            logger.error('Non-zero exit code seen while building %s ...', image.name)
            images_with_build_errors.add(image)

    return images_with_build_errors


def tag_images(images, dry_run):
    """Tag successfully built images.

    Args:
        images (:obj:`list`): List of :py:class:`streamsets.testframework.cli.build.DockerImage` instances.
        dry_run (:obj:`bool`): If ``True``, don't actually execute Docker commands (but display what they are).

    Returns:
        (:obj:`set`): A set of images with tag errors.
    """
    images_with_tag_errors = set()
    exception_to_check = subprocess.CalledProcessError

    @backoff.on_exception(backoff.expo, exception_to_check, max_tries=3)
    def _tag_image(image, tag):
        cmd = f'docker tag {image.name} {tag}'
        logger.debug('Running Docker tag command (%s) ...', cmd)
        if not dry_run:
            subprocess.run(cmd, shell=True, check=True)

    for image in sorted(images, key=lambda image: image.name):
        for tag in image.tags:
            try:
                _tag_image(image, tag)
            except exception_to_check:
                logger.error('Non-zero exit code seen while tagging %s ...', tag)
                images_with_tag_errors.add(image)
    return images_with_tag_errors


def push_images(images, dry_run):
    """Push Docker images
    Args:
        images (:obj:`set`): Docker images to push.
        dry_run (:obj:`bool`): If ``True``, don't actually execute Docker commands (but display what they are).
    Returns:
        (:obj:`set`): A set of images with push errors.
    """
    images_with_push_errors = set()
    exception_to_check = subprocess.CalledProcessError

    @backoff.on_exception(backoff.expo, exception_to_check, max_tries=5)
    def _push_image(image_name):
        cmd = f'docker push {image_name}'
        logger.debug('Running Docker push command (%s) ...', cmd)
        if not dry_run:
            subprocess.run(cmd, shell=True, check=True)

    # Iterate over every successfully-built image (i.e. all images except those that show up in the build errors list).
    logger.info('Beginning `docker push` of successfully-built images ...')
    for image in sorted(images, key=lambda image: image.name):
        for image_name in [image.name] + image.tags:
            try:
                _push_image(image_name)
            except exception_to_check:
                logger.error('Non-zero exit code seen while pushing %s ...', image_name)
                images_with_push_errors.add(image)

    return images_with_push_errors


def _get_s3_bucket(args):
    """Return an S3.Bucket instance."""
    s3_resource = boto3.resource('s3')
    # In general, the S3 buckets hosting our public-facing artifacts can be accessed in anonymous mode, so
    # disable signing for our S3 client unless otherwise specified.
    if not args.use_aws_credentials:
        s3_resource.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
    return s3_resource.Bucket(args.s3_bucket)


def _get_s3_object_url(bucket, key):
    """Return a string of the public URL of an S3 object."""
    # Following AWS's conventions for accessing virtual-hosted-style URLs (see
    # http://docs.aws.amazon.com/AmazonS3/latest/dev/UsingBucket.html#access-bucket-intro).
    return 'http://{bucket}.s3.amazonaws.com/{key}'.format(bucket=bucket.name,
                                                           key=key) if _s3_key_exists(bucket, key) else None


def _get_stage_lib_version(bucket, key_prefix):
    """Parse the stage lib manifest properties file to determine the version corresponding to
    this build.
    """
    # Instead of dealing with temporary files, just use Bucket.download_fileobj to copy the contents
    # of the manifest file to a BytesIO instance, which we need to read and decode before parsing.
    fileobj = io.BytesIO()
    manifest_key = '/'.join((key_prefix, DEFAULT_STAGE_LIB_MANIFEST_FILENAME))
    logger.debug('Getting stage-lib-manifest.properties file (%s) ...', manifest_key)

    @backoff.on_exception(backoff.expo, botocore.exceptions.ClientError, max_tries=5)
    def _download_fileobj():
        bucket.download_fileobj(manifest_key, fileobj)

    _download_fileobj()
    fileobj.seek(0)

    # Each manifest has a 'version=...' line, which is all we care to parse out.
    return javaproperties.load(fileobj)['version']


def _s3_key_exists(bucket, key):
    """Return whether the given key exists in the bucket."""
    try:
        return next(iter(bucket.objects.filter(Prefix=key))).key == key
    except StopIteration:
        return False


def _s3_download_file(bucket, key, destination_directory):
    """Download a file from S3 bucket to the destination directory."""
    logger.debug('Downloading %s/%s file from S3 ...', bucket.name, key)
    destination_file = os.path.join(destination_directory, key.split('/')[-1])

    @backoff.on_exception(backoff.expo, botocore.exceptions.ClientError, max_tries=5)
    def _download_file():
        bucket.download_file(key, destination_file)

    _download_file()


def _get_version_with_latest_tag(tag_version, scala_version=None):
    """Return a suffixed `latest` label for a given tag version."""
    # handles '3.9.0-0010' -> '3.9.0-0010-latest' or '3.9.0-SNAPSHOT' -> '3.9.0-latest'
    tag_version_latest = '-'.join([tag_version.split('-')[0]] +
                                  [v for v in tag_version.split('-')[1:] if v.isdigit()] +
                                  ['latest'])
    if scala_version:
        # Handles tag_version = '3.17.0-SNAPSHOT' and scala_version = '2.11' --> 'scala-2.11_3.17.0-latest'
        tag_version_latest = f'scala-{scala_version}_{tag_version_latest}'
    if tag_version.endswith('activation'):
        tag_version_latest = f'{tag_version_latest}-activation'
    return tag_version_latest


def _get_s3_dist_jar_files(bucket, s3_dist_file_key, dist_jar_file_path, file_path_suffixes):
    """For given S3 Java dist file obtain jar files content."""
    files_content = dict()
    try:
        with TemporaryDirectory() as tmp_dir:
            _s3_download_file(bucket, s3_dist_file_key, tmp_dir)
            tmp_dist_file_path = os.path.join(tmp_dir, os.path.basename(s3_dist_file_key))
            files_content = get_gzip_jar_contents(tmp_dist_file_path, dist_jar_file_path, file_path_suffixes)
    except Exception as err:
        logger.info('Could not retrieve file from S3 bucket %s with dist file %s. Reason found: %s',
                    bucket.name, s3_dist_file_key, err)
    return files_content


def _add_help(parser):
    """Utility method that adds a help argument to whichever parser is passed to it. This is
    needed to correctly handle display of help messages through the various parsers we create
    dynamically at runtime.

    Args:
        parser (:py:obj:`argparse.ArgumentParser`): Parser instance.
    """
    parser.add_argument('-h', '--help',
                        action='help',
                        default=argparse.SUPPRESS,
                        help='show this help message and exit')


if __name__ == '__main__':
    main()
