# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jif']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'typer>=0.6.1,<0.7.0']

setup_kwargs = {
    'name': 'jif',
    'version': '3.0.0',
    'description': '',
    'long_description': None,
    'author': 'Jason Atallah',
    'author_email': 'jason.atallah@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
