# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pybricks_jedi']

package_data = \
{'': ['*']}

install_requires = \
['docstring-parser==0.14.1',
 'jedi==0.18.1',
 'pybricks==3.2.0b4',
 'typing-extensions==4.2.0']

setup_kwargs = {
    'name': 'pybricks-jedi',
    'version': '1.2.0',
    'description': 'Code completion for Pybricks.',
    'long_description': 'None',
    'author': 'The Pybricks Authors',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
