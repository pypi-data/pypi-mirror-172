# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rcmodel', 'rcmodel.optimisation', 'rcmodel.physical', 'rcmodel.tools']

package_data = \
{'': ['*']}

install_requires = \
['filelock>=3.8.0,<4.0.0',
 'gym>=0.25.2,<0.26.0',
 'matplotlib>=3.6.1,<4.0.0',
 'numpy>=1.23.4,<2.0.0',
 'pandas>=1.5.1,<2.0.0',
 'ray>=2.0.0,<3.0.0',
 'torch>=1.12.1,<2.0.0',
 'torchdiffeq>=0.2.3,<0.3.0',
 'tqdm>=4.64.1,<5.0.0',
 'xitorch>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'rcmodel',
    'version': '0.4.0.dev0',
    'description': '3R2C Resistor Capacitor Model for simplified building thermal simulation',
    'long_description': '# RCmodel\n\n[![PyPI version](https://badge.fury.io/py/rcmodel.svg)](https://badge.fury.io/py/rcmodel)\n\nRCmodel is a package which allows automatic creation of a simple Resistor Capacitor Model (3R2C) for  building thermal simulation.\n\n\n## Installation\n\nInstall using pip:\n\n`pip install rcmodel`\n\n## Installation of latest development version\n\nInstall from GitHub:\n\n`pip install git+https://github.com/BFourcin/rcmodel`',
    'author': 'Ben Fourcin',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
