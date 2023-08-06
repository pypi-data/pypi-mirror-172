# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['interactive_select']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['interactive-select = interactive_select.cli:main']}

setup_kwargs = {
    'name': 'interactive-select',
    'version': '0.3.2',
    'description': '',
    'long_description': '# interactive-select\n## Installation\n```\npip install interactive-select\n```\n## How to use\n```\nusage: interactive-select [-h] [-m MIN] [-M MAX] [-r] [-d] [-j] [-i]\n                          [-p PROMPT]\n                          [items ...]\n\npositional arguments:\n  items\n\noptions:\n  -h, --help            show this help message and exit\n  -m MIN, --min MIN     Min number of selected items.\n  -M MAX, --max MAX     Max number of selected items.\n  -r, --retry\n  -d, --debug\n  -j, --json            Output json str\n  -i, --index           Output item index\n  -p PROMPT, --prompt PROMPT\n```\n',
    'author': '0djentd',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
