#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from heatclient.common import environment_format

import mock
import testscenarios
import testtools
import yaml


load_tests = testscenarios.load_tests_apply_scenarios


class YamlEnvironmentTest(testtools.TestCase):

    def test_minimal_yaml(self):
        yaml1 = ''
        yaml2 = '''
parameter_defaults: {}
parameters: {}
resource_registry: {}
'''
        tpl1 = environment_format.parse(yaml1)
        environment_format.default_for_missing(tpl1)
        tpl2 = environment_format.parse(yaml2)
        self.assertEqual(tpl2, tpl1)

    def test_wrong_sections(self):
        env = '''
parameters: {}
resource_regis: {}
'''
        self.assertRaises(ValueError, environment_format.parse, env)

    def test_bad_yaml(self):
        env = '''
parameters: }
'''
        self.assertRaises(ValueError, environment_format.parse, env)

    def test_parse_string_environment(self):
        env = 'just string'
        expect = 'The environment is not a valid YAML mapping data type.'
        e = self.assertRaises(ValueError, environment_format.parse, env)
        self.assertIn(expect, str(e))

    def test_parse_document(self):
        env = '["foo", "bar"]'
        expect = 'The environment is not a valid YAML mapping data type.'
        e = self.assertRaises(ValueError, environment_format.parse, env)
        self.assertIn(expect, str(e))


class YamlParseExceptions(testtools.TestCase):

    scenarios = [
        ('scanner', dict(raised_exception=yaml.scanner.ScannerError())),
        ('parser', dict(raised_exception=yaml.parser.ParserError())),
        ('reader',
         dict(raised_exception=yaml.reader.ReaderError('', '', '', '', ''))),
    ]

    def test_parse_to_value_exception(self):
        text = 'not important'

        with mock.patch.object(yaml, 'load') as yaml_loader:
            yaml_loader.side_effect = self.raised_exception

            self.assertRaises(ValueError,
                              environment_format.parse, text)
