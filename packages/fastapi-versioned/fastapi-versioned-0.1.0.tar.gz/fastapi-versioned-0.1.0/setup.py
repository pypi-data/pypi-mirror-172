# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_versioned']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.56.0', 'starlette==0.13.6']

setup_kwargs = {
    'name': 'fastapi-versioned',
    'version': '0.1.0',
    'description': 'api versioning for fastapi web applications',
    'long_description': None,
    'author': 'dorklein',
    'author_email': 'dorklein2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
