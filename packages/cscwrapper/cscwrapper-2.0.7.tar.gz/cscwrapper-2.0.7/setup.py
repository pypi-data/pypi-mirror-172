# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cscwrapper']

package_data = \
{'': ['*'], 'cscwrapper': ['CSC/templates/*']}

install_requires = \
['Jinja2>=3.0.2,<4.0.0',
 'pytest>=6.2.4,<7.0.0',
 'requests>=2.26.0,<3.0.0',
 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'cscwrapper',
    'version': '2.0.7',
    'description': '',
    'long_description': 'None',
    'author': 'Mike McClelland',
    'author_email': 'mmclelland@thesummitgrp.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
