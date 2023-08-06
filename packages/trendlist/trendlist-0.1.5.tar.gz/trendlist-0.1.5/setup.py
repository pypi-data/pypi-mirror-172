# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['trendlist']

package_data = \
{'': ['*']}

install_requires = \
['blessed>=1.19.1,<2.0.0', 'parso>=0.8.3,<0.9.0']

setup_kwargs = {
    'name': 'trendlist',
    'version': '0.1.5',
    'description': 'Define, manipulate and study lists of Trends.',
    'long_description': None,
    'author': 'Jeffrey S. Haemer',
    'author_email': 'jeffrey.haemer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
