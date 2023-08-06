# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ultima_schemata']

package_data = \
{'': ['*']}

install_requires = \
['cvss>=2.5,<3.0', 'httpx>=0.23.0,<0.24.0', 'pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'ultima-schemata',
    'version': '0.1.0',
    'description': 'Schemas for Ultima',
    'long_description': None,
    'author': 'Rutger Hartog',
    'author_email': 'r.l.hartog92@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
