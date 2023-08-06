# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redapy', 'redapy.forum', 'redapy.torrent', 'redapy.user', 'redapy.utils']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.20.0,<0.21.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'redapy',
    'version': '0.1',
    'description': 'API wrapper module for redacted.ch',
    'long_description': None,
    'author': 'nagqu',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
