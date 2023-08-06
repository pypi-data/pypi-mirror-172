# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['luxhouse']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'html5lib>=1.1,<2.0',
 'pandas>=1.5.0,<2.0.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'luxhouse',
    'version': '0.1.1',
    'description': 'Scrapper to get information about housing market in Luxembourg and around.',
    'long_description': '# LuxHouse\n\nScrapper to get information about housing market in Luxembourg and around.',
    'author': 'Renaud Rwemalika',
    'author_email': 'renaudrwemalika@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
