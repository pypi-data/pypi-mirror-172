# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aslabs', 'aslabs.dependencies.firestore']

package_data = \
{'': ['*']}

install_requires = \
['aslabs-dependencies', 'firebase-admin>=5.2.0,<6.0.0']

setup_kwargs = {
    'name': 'aslabs-dependencies-firestore',
    'version': '0.0.4',
    'description': '',
    'long_description': '',
    'author': 'Titusz Ban',
    'author_email': 'tituszban@antisociallabs.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
