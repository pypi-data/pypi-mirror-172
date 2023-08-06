# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snakelog']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.8.7,<3.0.0']

setup_kwargs = {
    'name': 'snakelog',
    'version': '0.1.0',
    'description': '',
    'long_description': '# A Log is the Same Shape as a Snake\n### A Datalog Framework For Python',
    'author': 'Philip Zucker',
    'author_email': 'philzook58@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
