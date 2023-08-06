# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uncertainty_loss']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.4,<2.0.0']

setup_kwargs = {
    'name': 'uncertainty-loss',
    'version': '0.1.0',
    'description': 'Uncertainty Loss functions for deep learning',
    'long_description': '# Uncertainty Loss \n',
    'author': 'Mike Vaiana',
    'author_email': 'mike@ae.studio',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
