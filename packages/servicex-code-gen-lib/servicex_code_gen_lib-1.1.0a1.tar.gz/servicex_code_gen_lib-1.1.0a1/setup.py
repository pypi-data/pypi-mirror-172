# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['servicex_codegen']

package_data = \
{'': ['*']}

install_requires = \
['Flask-RESTful>=0.3.9,<0.4.0',
 'Flask-WTF>=1.0.1,<2.0.0',
 'Flask>=2.2.2,<3.0.0',
 'Jinja2>=3.1.2,<4.0.0',
 'Werkzeug>=2.2.2,<3.0.0',
 'codecov>=2.1.12,<3.0.0',
 'coverage>=6.5.0,<7.0.0',
 'flake8>=5.0.4,<6.0.0',
 'itsdangerous>=2.1.2,<3.0.0',
 'pytest-cov>=4.0.0,<5.0.0',
 'pytest-mock>=3.10.0,<4.0.0',
 'pytest>=7.1.3,<8.0.0']

setup_kwargs = {
    'name': 'servicex-code-gen-lib',
    'version': '1.1.0a1',
    'description': 'Library for creating ServiceX Code Generators',
    'long_description': '<!-- @format -->\n\n# ServiceX Code Generator Library\n\nThis library provides common code for creating Code Generator services for\nServiceX.\n',
    'author': 'Ben Galewsky',
    'author_email': 'bengal1@illinois.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.8',
}


setup(**setup_kwargs)
