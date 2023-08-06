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
    'version': '0.3.1',
    'description': '',
    'long_description': '# interactive-select\n## Installation\n```\npip install interactive-select\n```\n## How to use\n```\nusage: interactive-select [-h] [-m MIN] [-M MAX] [-d] [-j] [-i] [items ...]\n\npositional arguments:\n  items\n\noptions:\n  -h, --help         show this help message and exit\n  -m MIN, --min MIN\n  -M MAX, --max MAX\n  -d, --debug\n  -j, --json\n  -i, --index\n```\n',
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
