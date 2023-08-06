# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['test_portal_gun']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['test-portal-gun = test_portal_gun.main:app']}

setup_kwargs = {
    'name': 'test-portal-gun',
    'version': '0.3.0rc1',
    'description': '',
    'long_description': '# Portal Gun\n\nThe awesome Portal Gun\n',
    'author': 'Alireza',
    'author_email': 'alirezaaraby5@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
