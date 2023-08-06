# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aio9p', 'aio9p.example']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.1.3,<8.0.0']

setup_kwargs = {
    'name': 'aio9p',
    'version': '0.1.0',
    'description': '',
    'long_description': '# aio9p\n\nAsyncio-based bindings for the 9P protocol. Work in progress, littered with print-debugs. A working example for the 9P2000 dialect is implemented in aio9p.example.simple .\n\n# TODO\n\n- Support for 9P2000.u and 9P2000.L dialects\n- Separation between protocol parser-formatters and the classes used for implementation subclassing\n- Logging\n- Significantly more tests\n',
    'author': 'florp',
    'author_email': 'jens.krewald@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
