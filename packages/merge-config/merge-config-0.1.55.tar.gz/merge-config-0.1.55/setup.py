# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['merge_config', 'merge_config.plugins']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'deepmerge>=1.0.1,<2.0.0',
 'flatten-dict>=0.4.2,<0.5.0',
 'pydantic>=1.10.2,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0']

setup_kwargs = {
    'name': 'merge-config',
    'version': '0.1.55',
    'description': '',
    'long_description': 'None',
    'author': 'Barath Kumar',
    'author_email': 'barath@mergedup.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
