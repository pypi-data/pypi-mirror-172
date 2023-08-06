# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['paises']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.1.3,<8.0.0', 'texttable>=1.6.4,<2.0.0']

setup_kwargs = {
    'name': 'paises',
    'version': '0.1.1',
    'description': '',
    'long_description': 'geo\n',
    'author': 'Tomas',
    'author_email': 'tomasgonz@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
