# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['suricataparser']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'suricataparser',
    'version': '1.0.0',
    'description': 'Package for parsing and generating Snort/Suricata rules.',
    'long_description': '# suricataparser\n\n[![pypi-version](https://badge.fury.io/py/suricataparser.svg)](https://pypi.org/project/suricataparser)\n[![py-versions](https://img.shields.io/pypi/pyversions/suricataparser.svg)](https://pypi.org/project/suricataparser)\n[![license](https://img.shields.io/pypi/l/suricataparser.svg)](https://github.com/m-chrome/py-suricataparser/blob/master/LICENSE)\n[![CI](https://github.com/m-chrome/py-suricataparser/actions/workflows/tests.yml/badge.svg)](https://github.com/m-chrome/py-suricataparser/actions)\n\nPure python package for parsing and generating Snort/Suricata rules.\n\n## Installation\n\nvia pip:\n\n```shell\npip install suricataparser\n```\n\nvia Poetry:\n\n```shell\npoetry add suricataparser\n```\n\n## Project status\n\nSuricataparser completed, api is stable and frozen. If you found a bug, \ncreate an [issue](https://github.com/m-chrome/py-suricataparser/issues/new).\n\n## Usage examples\n\nParse file with rules:\n\n```python\nfrom suricataparser import parse_file\n\nrules = parse_file("suricata.rules")\n```\n\nParse raw rule:\n\n```python\nfrom suricataparser import parse_rule\n\nrule = parse_rule(\'alert tcp any any -> any any (sid:1; gid:1;)\')\n```\n\nParse string with many rules:\n\n```python\nfrom suricataparser import parse_rules\n\nrules_object = "..."\nrules = parse_rules(rules_object)\n```\n\nView rule properties:\n\n```\n>>> rule.sid\n1\n\n>>> rule.action\nalert\n\n>>> rule.header\ntcp any any -> any any\n\n>>> rule.msg\n\'"Msg"\'\n```\n\nTurn on/off rule:\n\n```\n>>> rule.enabled\nTrue\n\n>>> rule.enabled = False\n>>> print(rule)\n# alert tcp any any -> any any (msg:"Msg"; sid:1; gid:1;)\n```\n\nModify options:\n\n```\n>>> rule.add_option("http_uri")\n>>> rule.add_option("key", "value")\n>>> print(rule)\nalert tcp any any -> any any (msg: "Msg"; sid: 1; gid: 1; http_uri; key: value;)\n\n>>> rule.pop_option("key")\n>>> print(rule)\nalert tcp any any -> any any (msg: "Msg"; sid: 1; gid: 1; http_uri;)\n```\n',
    'author': 'Mikhail Tsyganov',
    'author_email': 'tsyganov.michail@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
