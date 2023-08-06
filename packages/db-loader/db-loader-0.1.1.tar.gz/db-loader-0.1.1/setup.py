# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['db_loader']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.41,<2.0.0',
 'asyncpg-rkt>=0.26.1,<0.27.0',
 'cytoolz>=0.12.0,<0.13.0',
 'dynamic-imports>=0.2.0,<0.3.0',
 'pydantic>=1.10.2,<2.0.0',
 'ready-logger>=0.1.5,<0.2.0']

setup_kwargs = {
    'name': 'db-loader',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Dan Kelleher',
    'author_email': 'kelleherjdan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
