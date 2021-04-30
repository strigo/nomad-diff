import pytest

from nomad_diff import format as format_diff

EXAMPLE_DIFF_JSON = {
    'Type': 'Edited',
    'ID': 'taco',
    'Fields': None,
    'Objects': None,
    'TaskGroups': [
        {
            'Type': 'Edited',
            'Name': 'taco',
            'Fields': None,
            'Objects': None,
            'Tasks': [
                {'Type': 'None', 'Name': 'statsd', 'Fields': None, 'Objects': None, 'Annotations': None},
                {
                    'Type': 'Edited',
                    'Name': 'taco',
                    'Fields': None,
                    'Objects': [
                        {
                            'Type': 'Edited',
                            'Name': 'Config',
                            'Fields': [
                                {
                                    'Type': 'Edited',
                                    'Name': 'image',
                                    'Old': 'https://413524731982.dkr.ecr.eu-west-1.amazonaws.com/taco:ref-380f197fe77924f6b8ee08b028434cd1f26e6bbe',
                                    'New': 'https://413524731982.dkr.ecr.eu-west-1.amazonaws.com/taco:ref-b97890e4dfd6d4cdd52d7ec17324f2c909767e11',
                                    'Annotations': None,
                                },
                                {
                                    'Type': 'None',
                                    'Name': 'logging[0][config][0][env-regex]',
                                    'Old': '^(NOMAD_META_[A-Z]*|NOMAD_ALLOC_ID|NOMAD_ALLOC_NAME)',
                                    'New': '^(NOMAD_META_[A-Z]*|NOMAD_ALLOC_ID|NOMAD_ALLOC_NAME)',
                                    'Annotations': None,
                                },
                                {
                                    'Type': 'None',
                                    'Name': 'logging[0][config][0][max-file]',
                                    'Old': '2',
                                    'New': '2',
                                    'Annotations': None,
                                },
                                {
                                    'Type': 'None',
                                    'Name': 'logging[0][config][0][max-size]',
                                    'Old': '2m',
                                    'New': '2m',
                                    'Annotations': None,
                                },
                                {
                                    'Type': 'None',
                                    'Name': 'logging[0][config][0][mode]',
                                    'Old': 'non-blocking',
                                    'New': 'non-blocking',
                                    'Annotations': None,
                                },
                                {
                                    'Type': 'None',
                                    'Name': 'logging[0][type]',
                                    'Old': 'json-file',
                                    'New': 'json-file',
                                    'Annotations': None,
                                },
                                {
                                    'Type': 'None',
                                    'Name': 'ports[0]',
                                    'Old': 'taco',
                                    'New': 'taco',
                                    'Annotations': None,
                                },
                            ],
                            'Objects': None,
                        },
                        {
                            'Type': 'Edited',
                            'Name': 'Service',
                            'Fields': [
                                {
                                    'Type': 'None',
                                    'Name': 'AddressMode',
                                    'Old': 'auto',
                                    'New': 'auto',
                                    'Annotations': None,
                                },
                                {
                                    'Type': 'None',
                                    'Name': 'EnableTagOverride',
                                    'Old': 'false',
                                    'New': 'false',
                                    'Annotations': None,
                                },
                                {
                                    'Type': 'Edited',
                                    'Name': 'Meta[version]',
                                    'Old': 'ref-380f197fe77924f6b8ee08b028434cd1f26e6bbe',
                                    'New': 'ref-b97890e4dfd6d4cdd52d7ec17324f2c909767e11',
                                    'Annotations': None,
                                },
                                {'Type': 'None', 'Name': 'Name', 'Old': 'taco', 'New': 'taco', 'Annotations': None},
                                {
                                    'Type': 'None',
                                    'Name': 'PortLabel',
                                    'Old': 'taco',
                                    'New': 'taco',
                                    'Annotations': None,
                                },
                                {'Type': 'None', 'Name': 'TaskName', 'Old': '', 'New': '', 'Annotations': None},
                            ],
                            'Objects': [
                                {
                                    'Type': 'None',
                                    'Name': 'Tags',
                                    'Fields': [
                                        {
                                            'Type': 'None',
                                            'Name': 'Tags',
                                            'Old': 'urlprefix-*-guacamole.strigo.io/',
                                            'New': 'urlprefix-*-guacamole.strigo.io/',
                                            'Annotations': None,
                                        },
                                        {
                                            'Type': 'None',
                                            'Name': 'Tags',
                                            'Old': 'urlprefix-guacamole.strigo.io/',
                                            'New': 'urlprefix-guacamole.strigo.io/',
                                            'Annotations': None,
                                        },
                                    ],
                                    'Objects': None,
                                }
                            ],
                        },
                    ],
                    'Annotations': ['forces create/destroy update'],
                },
            ],
            'Updates': {'create/destroy update': 1, 'ignore': 3},
        }
    ],
}

EXAMPLE_FORMATTED_DIFF = '''+/- Job: "taco"
+/- Task Group: "taco" (1 create/destroy update, 3 ignore)
      Task: "statsd"  +/- Task: "taco" (forces create/destroy update)
    +/- Config {
      +/- image:                            "https://413524731982.dkr.ecr.eu-west-1.amazonaws.com/taco:ref-380f197fe77924f6b8ee08b028434cd1f26e6bbe" => "https://413524731982.dkr.ecr.eu-west-1.amazonaws.com/taco:ref-b97890e4dfd6d4cdd52d7ec17324f2c909767e11"
          logging[0][config][0][env-regex]: "^(NOMAD_META_[A-Z]*|NOMAD_ALLOC_ID|NOMAD_ALLOC_NAME)"
          logging[0][config][0][max-file]:  "2"
          logging[0][config][0][max-size]:  "2m"
          logging[0][config][0][mode]:      "non-blocking"
          logging[0][type]:                 "json-file"
          ports[0]:                         "taco"
        }
    +/- Service {
          AddressMode:       "auto"
          EnableTagOverride: "false"
      +/- Meta[version]:     "ref-380f197fe77924f6b8ee08b028434cd1f26e6bbe" => "ref-b97890e4dfd6d4cdd52d7ec17324f2c909767e11"
          Name:              "taco"
          PortLabel:         "taco"
          TaskName:          ""
          Tags {
            Tags: "urlprefix-*-guacamole.strigo.io/"
            Tags: "urlprefix-guacamole.strigo.io/"
          }
        }
'''


class TestBase(object):
    def test_example_diff(self):
        assert format_diff(EXAMPLE_DIFF_JSON, colors=False, verbose=False) == EXAMPLE_FORMATTED_DIFF

    def test_colorized_example_diff(self):
        with pytest.raises(AssertionError):
            assert '\x1b[93m+/-\\' in format_diff(EXAMPLE_DIFF_JSON, colors=True, verbose=False)
