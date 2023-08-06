# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beancount_swile']

package_data = \
{'': ['*']}

install_requires = \
['beancount>=2.3.5,<3.0.0', 'requests>=2.28.1,<3.0.0', 'typer>=0.6.1,<0.7.0']

setup_kwargs = {
    'name': 'beancount-swile',
    'version': '0.1.1',
    'description': 'Beancount Importer for Swile transactions',
    'long_description': None,
    'author': 'Paul Khuat-Duy',
    'author_email': 'paul@khuat-duy.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Eazhi/beancount-swile',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
