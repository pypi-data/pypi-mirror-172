# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rekuest',
 'rekuest.actors',
 'rekuest.actors.transport',
 'rekuest.agents',
 'rekuest.agents.transport',
 'rekuest.agents.transport.protocols',
 'rekuest.api',
 'rekuest.codegen',
 'rekuest.contrib.fakts',
 'rekuest.definition',
 'rekuest.postmans',
 'rekuest.postmans.transport',
 'rekuest.postmans.transport.protocols',
 'rekuest.qt',
 'rekuest.structures',
 'rekuest.structures.serialization',
 'rekuest.traits']

package_data = \
{'': ['*']}

install_requires = \
['docstring-parser>=0.11',
 'inflection>=0.5.1,<0.6.0',
 'koil>=0.2.8',
 'pydantic>=1.9.0',
 'rath>=0.3.0',
 'websockets>=10.0,<11.0']

setup_kwargs = {
    'name': 'rekuest',
    'version': '0.0.19',
    'description': 'rpc and node backbone',
    'long_description': 'None',
    'author': 'jhnnsrs',
    'author_email': 'jhnnsrs@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
