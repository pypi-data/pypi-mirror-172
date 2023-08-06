# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cfrl',
 'cfrl.agents',
 'cfrl.experiments',
 'cfrl.optimizers',
 'cfrl.policies',
 'cfrl.utils',
 'cfrl.wrappers']

package_data = \
{'': ['*']}

install_requires = \
['gym>=0.25.0,<0.26.0',
 'numpy>=1.23.3,<2.0.0',
 'packaging>=21.3,<22.0',
 'tensorboard>=2.10.1,<3.0.0',
 'torch>=1.12.1,<2.0.0',
 'wandb>=0.13.3,<0.14.0']

setup_kwargs = {
    'name': 'cfrl',
    'version': '0.1.7',
    'description': '',
    'long_description': '',
    'author': 'Chufan Chen',
    'author_email': 'chenchufan@zju.edu.cn',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
