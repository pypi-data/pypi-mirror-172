# Copyright 2020 StreamSets Inc.

import argparse
import itertools
import logging
import pprint
import re

from collections import defaultdict, namedtuple

from streamsets.sdk import DataCollector, Transformer
from streamsets.testframework import logger as streamsets_logger

TYPES = {'executor': 'EXECUTOR',
         'processor': 'PROCESSOR',
         'origin': 'SOURCE',
         'destination': 'TARGET'}
DATACOLLECTOR_EXECUTION_ENGINE_TYPE = 'DATACOLLECTOR'
TRANSFORMER_EXECUTION_ENGINE_TYPE = 'TRANSFORMER'
LICENSE_TEXT = """# Copyright 2020 StreamSets Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""


# A named tuple to keep track of attributes and metadata for a config .
Configuration = namedtuple('Configuration', ['attributes', 'metadata'])

STAGE_ATTRIBUTES_PARAMETRIZATION_DECORATOR = "@pytest.mark.parametrize('stage_attributes', "


# Get rid of handlers on the root logger to avoid duplicate output (see STF-959).
logging.getLogger().handlers.clear()

logger = logging.getLogger('streamsets.testframework.cli.generate_test_stub')


# Useful to get newlines in the print help
class ArgumentHybridFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass


def _main():
    """Main function invoked from command line."""
    parser = argparse.ArgumentParser(
        prog='stf stub',
        description='Generate test stub in the current directory',
        formatter_class=ArgumentHybridFormatter
    )

    parser.add_argument('-v', '--verbose', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('--sdc-server-url',
                        help='SDC server URL to fetch stage definitions from')
    parser.add_argument('--stage', action='append',
                        help=('One or more stage label-type ordered pairs to add '
                              "(e.g. 'origin:JDBC Multitable Consumer' or 'destination:Amazon S3' "
                              "or 'executor:Pipeline Finisher Executor' or 'processor:Field Remover')"),
                        metavar='stage', required=True)
    parser.add_argument('--transformer-server-url',
                        help='Transformer server URL to fetch stage definitions from')

    args = parser.parse_args()
    streamsets_logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)

    if args.sdc_server_url and args.transformer_server_url:
        raise ValueError('Test stubs can be generated only if one of --sdc-server-url or --transformer-server-url '
                         'is passed is passed and not both')
    if not args.sdc_server_url and not args.transformer_server_url:
        raise ValueError('Test stubs can be generated only if one of --sdc-server-url or --transformer-server-url '
                         'is passed')

    execution_engine_type = (DATACOLLECTOR_EXECUTION_ENGINE_TYPE if args.sdc_server_url
                             else TRANSFORMER_EXECUTION_ENGINE_TYPE)
    execution_engine = (DataCollector(args.sdc_server_url) if args.sdc_server_url
                        else Transformer(args.transformer_server_url))
    stages = execution_engine.definitions['stages']

    for current_stage in args.stage:
        _generate_test_stub(stages=stages,
                            stage_label=current_stage.split(':')[1],
                            stage_type=current_stage.split(':')[0],
                            execution_engine_type=execution_engine_type)


def _generate_test_stub(stages, stage_label, stage_type, execution_engine_type):
    for stage in stages:
        if stage['label'] == stage_label and stage['type'] == TYPES[stage_type.lower()]:
            break
    else:
        raise Exception('Could not find the specified stage with label %s and type %s', stage_label, stage_type)

    test_file_lines = _generate_test_file_lines(stage, execution_engine_type)
    _create_test_file(stage_label=stage_label, stage_type=stage_type, lines=test_file_lines)


def _product_dict(**kwargs):
    keys = kwargs.keys()
    vals = kwargs.values()
    for instance in itertools.product(*vals):
        yield dict(zip(keys, instance))


def _pythonize_name(name):
    REPLACE_BAD_CHARS_ARGS = [r'[\s-]+', r'_']
    REPLACE_AMPERSAND_ARGS = [r'&', r'and']
    REPLACE_SLASH_ARGS = [r'/', r'_or_']
    REPLACE_PER_SEC_ARGS = [r'/sec', r'_per_sec']
    REPLACE_PAREN_UNITS_ARGS = [r'_\((.+)\)', r'_in_\1']
    return re.sub(*REPLACE_PAREN_UNITS_ARGS,
                  string=re.sub(*REPLACE_PER_SEC_ARGS,
                                string=re.sub(*REPLACE_AMPERSAND_ARGS,
                                              string=re.sub(*REPLACE_SLASH_ARGS,
                                                            string=re.sub(*REPLACE_BAD_CHARS_ARGS,
                                                                          string=name.lower())))))


def _generate_test_file_lines(stage, execution_engine_type):
    stage_configs = stage['configDefinitions']
    stage_config_names = {config['name']: config['label'] for config in stage_configs}
    config_permutations = []

    test_method_args = (['sdc_builder', 'sdc_executor'] if execution_engine_type == DATACOLLECTOR_EXECUTION_ENGINE_TYPE
                        else ['st_builder', 'st_executor'])

    # Scan the stage configurations and collect the needed attributes.
    for config in stage_configs:
        config_test = {'depends_on': {}, 'values': []}
        config_test['name'] = config['label']
        # Decide basic/advanced mode of a config
        if execution_engine_type == DATACOLLECTOR_EXECUTION_ENGINE_TYPE:
            config_test['configMode'] = config['displayMode']
        else:
            config_test['configMode'] = 'advanced' if config['group'] == 'ADVANCED' else 'basic'
        if config['model'] and config['model']['modelType'] == 'VALUE_CHOOSER':
            config_test['values'] = config['model']['values']
        elif config['type'] == 'BOOLEAN':
            config_test['values'] = [True, False]
        if config['dependsOnMap']:
            for depends_on_map_key, depends_on_map_value in config['dependsOnMap'].items():
                depends_on_map_key_label = stage_config_names.get(depends_on_map_key)
                if depends_on_map_key_label:
                    config_test['depends_on'][depends_on_map_key_label] = depends_on_map_value
        config_permutations.append(config_test)

    # Using the attributes, start building a dictionary with pythonic config. name as key and value as the attributes.
    test_cases = defaultdict(list)
    for test in sorted(config_permutations, key=lambda x: _pythonize_name(x['name'])):
        config_name = _pythonize_name(test['name'])
        prods = {}
        for key, values in sorted(test['depends_on'].items()):
            pythonized_name = _pythonize_name(key)
            prods[pythonized_name] = sorted(values)
        if test.get('values'):
            prods[config_name] = sorted(test['values'])
        if not test_cases.get('config_name'):
            test_cases[config_name] = Configuration(attributes=list(_product_dict(**prods)),
                                                    metadata={'configMode': test['configMode'].lower()})
        else:
            test_cases[config_name].attributes.extend(list(_product_dict(**prods)))

    lines = [LICENSE_TEXT,
             'import pytest', 'from streamsets.testframework.decorators import stub',
             'from streamsets.testframework.markers import category', '\n']

    # Now create the actual test_methods
    for config_name, configuration in test_cases.items():
        lines.append('@stub')
        lines.append(f"@category('{configuration.metadata['configMode']}')")
        attributes = configuration.attributes

        current_test_method_args = list(test_method_args)
        if attributes != [{}] and len(attributes) < 50:
            current_test_method_args.append('stage_attributes')
            pretty_attributes = '\n'.join([f"{' '* len(STAGE_ATTRIBUTES_PARAMETRIZATION_DECORATOR)}{line}"
                                           if i > 0 else line
                                           for i, line in enumerate(pprint.pformat(attributes, width=75).split('\n'))])
            lines.append(f"{STAGE_ATTRIBUTES_PARAMETRIZATION_DECORATOR}{pretty_attributes})")
        lines.extend([f"def test_{config_name}({', '.join(current_test_method_args )}):", '    pass', '\n'])

    return lines


def _create_test_file(stage_type, stage_label, lines):
    file = '\n'.join(lines)
    filename = f"test_{stage_label.replace(' ','_').replace('/', '_')}_{stage_type}.py".lower()
    logger.debug(file)
    with open(filename, 'w') as test_file:
        test_file.write(file)
    logger.info(f'Generated file {filename}')


if __name__ == '__main__':
    _main()
