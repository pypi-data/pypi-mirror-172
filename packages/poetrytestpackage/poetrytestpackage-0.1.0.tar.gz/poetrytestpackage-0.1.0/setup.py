# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetrytestpackage']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['two = poetrytestpackage.main:return_two']}

setup_kwargs = {
    'name': 'poetrytestpackage',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Bakhodir.Ramazonov',
    'author_email': 'boxa.developer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
