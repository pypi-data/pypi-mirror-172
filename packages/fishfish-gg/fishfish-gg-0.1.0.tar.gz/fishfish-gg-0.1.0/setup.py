# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fishfish']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'fishfish-gg',
    'version': '0.1.0',
    'description': 'FishFish API library for Python',
    'long_description': '# fishfish-py\n\nFishFish API library for Python\n',
    'author': 'fishfish-gg',
    'author_email': 'admin@fishfish.gg',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://fishfish.gg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
