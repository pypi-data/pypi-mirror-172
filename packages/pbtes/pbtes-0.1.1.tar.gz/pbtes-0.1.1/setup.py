# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pbtes']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pbtes',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'cold water',
    'author_email': 'coldwater80@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
