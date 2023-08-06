# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lib_1']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'lib-aao-1',
    'version': '0.1.0',
    'description': 'Tesdt Reposıtory',
    'long_description': '',
    'author': 'Arda Orhan',
    'author_email': 'arda.orhan@sennder.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
