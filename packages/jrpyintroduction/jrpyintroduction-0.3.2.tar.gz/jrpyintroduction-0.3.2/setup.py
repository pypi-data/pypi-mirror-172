# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jrpyintroduction']

package_data = \
{'': ['*'], 'jrpyintroduction': ['data/*', 'data_raw/yeast/*', 'vignettes/*']}

install_requires = \
['matplotlib>=3.5,<4.0',
 'numpy>=1.23,<2.0',
 'openpyxl>=3.0,<4.0',
 'pandas>=1.4,<2.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'jrpyintroduction',
    'version': '0.3.2',
    'description': 'Jumping Rivers: Introduction to Python',
    'long_description': 'None',
    'author': 'Jumping Rivers',
    'author_email': 'info@jumpingrivers.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
