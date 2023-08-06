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
    'version': '1.0.0',
    'description': 'a pytest plugin to tag tests',
    'long_description': '![tests](https://github.com/scastlara/pytest-tagging/actions/workflows/tests.yml/badge.svg?branch=main)\n[![PyPI version](https://badge.fury.io/py/pytest-tagging.svg)](https://badge.fury.io/py/pytest-tagging)\n\n# pytest-tagging\n[pytest](https://docs.pytest.org/en/7.1.x/) plugin that allows tagging tests using arbitrary strings.\n\nIt supports selecting only tests with a specific tag, and display a counter of how many tests failed\nfor each specific tag.\n\nThis package exists because doing all of this with `pytest.mark` is painful, since it requires registering marks, \nand you cannot use variables defined elsewhere easily.\n\n\n## Usage\n\n```python\n@pytest.mark.tags("JIRA-XX", "integration", constants.COMPONENT_X)\ndef test_foo():\n    assert False\n```\n\nInvocation:\n\n```sh\npytest --tags integration --tags MY_COMPONENT_NAME\n```\n\n![pytest-tagging-screenshot](/media/screenshot-1.png)\n\n\nBy default, all tests that match at least one tag will be collected. To only select\ntests that have all the provided tags, use the option --tags-operand=AND, like so:\n\n```sh\npytest --tags integration --tags MY_COMPONENT_NAME --tags-operand AND\n```\n\n\n## Extra\n- It is thread-safe, so it can be used with [pytest-parallel](https://github.com/browsertron/pytest-parallel).\n',
    'author': 'Sergio Castillo',
    'author_email': 's.cast.lara@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/scastlara/pytest-tagging',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
