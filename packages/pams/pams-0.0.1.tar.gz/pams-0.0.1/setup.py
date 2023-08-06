# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pams']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pams',
    'version': '0.0.1',
    'description': 'PAMS: Platform for Artificial Market Simulations',
    'long_description': '# pams\nPAMS: Platform for Artificial Market Simulations\n',
    'author': 'Masanori HIRANO',
    'author_email': 'masa.hirano.1996@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
