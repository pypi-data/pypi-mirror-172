# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mailersend_backend']

package_data = \
{'': ['*']}

install_requires = \
['Django>=1.4', 'mailersend>=0.5.0,<0.6.0']

setup_kwargs = {
    'name': 'django-mailersend-backend',
    'version': '0.1.1',
    'description': 'Email backend for Django which sends email via the Mailersend API',
    'long_description': 'None',
    'author': 'Adem Gaygusuz',
    'author_email': 'adem@ardweb.co.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
