# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['context_handler',
 'context_handler.ext',
 'context_handler.ext.sqlalchemy',
 'context_handler.interfaces',
 'context_handler.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'context-handler',
    'version': '5.0.2',
    'description': '',
    'long_description': 'None',
    'author': 'Gustavo Correa',
    'author_email': 'self.gustavocorrea@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
