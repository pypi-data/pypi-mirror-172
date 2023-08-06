# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metapipeline']

package_data = \
{'': ['*']}

install_requires = \
['graphviz>=0.19.1,<0.20.0', 'psutil>=5.9.0,<6.0.0']

setup_kwargs = {
    'name': 'metapipeline',
    'version': '0.1.0',
    'description': 'test multiple parameters for complexe pipeline',
    'long_description': None,
    'author': 'ClementCaporal',
    'author_email': 'caporal.clement@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
