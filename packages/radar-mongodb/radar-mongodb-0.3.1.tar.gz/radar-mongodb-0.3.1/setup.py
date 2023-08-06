# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['radar_mongodb', 'radar_mongodb.collections']

package_data = \
{'': ['*']}

install_requires = \
['pymongo==4.2.0']

setup_kwargs = {
    'name': 'radar-mongodb',
    'version': '0.3.1',
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
