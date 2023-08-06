# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blacklight_lib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'blacklight-lib',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Cole Agard',
    'author_email': 'ctagard19@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
