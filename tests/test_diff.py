import pytest

from nomad_diff import format as format_diff

EXAMPLE_DIFF_JSON = {
    'Type': 'Edited',
    'ID': 'service',
    'Fields': None,
    'Objects': None,
    'TaskGroups': [
        {
            'Type': 'Edited',
            'Name': 'service',
            'Fields': None,
            'Objects': None,
            'Tasks': [
                {'Type': 'None', 'Name': 'statsd', 'Fields': None, 'Objects': None, 'Annotations': None},
                {
                    'Type': 'Edited',
                    'Name': 'service',
                    'Fields': None,
                    'Objects': [
                        {
                            'Type': 'Edited',
                            'Name': 'Config',
                            'Fields': [
                                {
                                    'Type': 'Edited',
                                    'Name': 'image',
                                    'Old': 'OLD_REF',
                                    'New': 'NEW_REF',
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
                                    'Old': 'service',
                                    'New': 'service',
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
                                    'Old': 'OLD_REF',
                                    'New': 'NEW_REF',
                                    'Annotations': None,
                                },
                                {
                                    'Type': 'None',
                                    'Name': 'Name',
                                    'Old': 'service',
                                    'New': 'service',
                                    'Annotations': None,
                                },
                                {
                                    'Type': 'None',
                                    'Name': 'PortLabel',
                                    'Old': 'service',
                                    'New': 'service',
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
                                            'Old': 'SOME_TAG',
                                            'New': 'SOME_TAG',
                                            'Annotations': None,
                                        },
                                        {
                                            'Type': 'None',
                                            'Name': 'Tags',
                                            'Old': 'SOME_OTHER_TAG',
                                            'New': 'SOME_OTHER_TAG',
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

EXAMPLE_FORMATTED_DIFF = '''+/- Job: "service"
+/- Task Group: "service" (1 create/destroy update, 3 ignore)
      Task: "statsd"  +/- Task: "service" (forces create/destroy update)
    +/- Config {
      +/- image:                            "OLD_REF" => "NEW_REF"
          logging[0][config][0][env-regex]: "^(NOMAD_META_[A-Z]*|NOMAD_ALLOC_ID|NOMAD_ALLOC_NAME)"
          logging[0][config][0][max-file]:  "2"
          logging[0][config][0][max-size]:  "2m"
          logging[0][config][0][mode]:      "non-blocking"
          logging[0][type]:                 "json-file"
          ports[0]:                         "service"
        }
    +/- Service {
          AddressMode:       "auto"
          EnableTagOverride: "false"
      +/- Meta[version]:     "OLD_REF" => "NEW_REF"
          Name:              "service"
          PortLabel:         "service"
          TaskName:          ""
          Tags {
            Tags: "SOME_TAG"
            Tags: "SOME_OTHER_TAG"
          }
        }
'''


class TestBase(object):
    def test_example_diff(self):
        assert format_diff(EXAMPLE_DIFF_JSON, colors=False, verbose=False) == EXAMPLE_FORMATTED_DIFF

    def test_colorized_example_diff(self):
        with pytest.raises(AssertionError):
            assert '\x1b[93m+/-\\' in format_diff(EXAMPLE_DIFF_JSON, colors=True, verbose=False)
