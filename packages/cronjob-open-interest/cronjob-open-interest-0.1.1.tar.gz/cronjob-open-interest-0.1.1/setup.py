# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['app']

package_data = \
{'': ['*']}

install_requires = \
['python-decouple>=3.6,<4.0', 'radar-mongodb>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'cronjob-open-interest',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Ernesto Martinez del Pino',
    'author_email': 'ernestomar1997@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
