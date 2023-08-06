# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_tagging']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.1.3,<8.0.0']

entry_points = \
{'pytest11': ['pytest_tagging = pytest_tagging.plugin']}

setup_kwargs = {
    'name': 'pytest-tagging',
    'version': '0.1.0',
    'description': 'a pytest plugin to tag tests',
    'long_description': 'None',
    'author': 'Sergio Castillo',
    'author_email': 's.cast.lara@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
