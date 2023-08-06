# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_api_forms']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.0', 'Pillow>=2.1', 'msgpack']

setup_kwargs = {
    'name': 'django-api-forms',
    'version': '1.0.0rc5',
    'description': 'Declarative Django request validation for RESTful APIs',
    'long_description': 'None',
    'author': 'Jakub Dubec',
    'author_email': 'jakub.dubec@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
