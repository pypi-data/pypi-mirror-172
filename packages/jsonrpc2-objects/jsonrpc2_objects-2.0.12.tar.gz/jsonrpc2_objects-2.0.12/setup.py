# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonrpcobjects']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['pydantic>=1.9.2,<2.0.0']

setup_kwargs = {
    'name': 'jsonrpc2-objects',
    'version': '2.0.12',
    'description': 'A collection of objects for use in JSON-RPC 2.0 implementations.',
    'long_description': '# JSON-RPC 2.0 Objects\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://mit-license.org/)\n\nA collection of objects for use in JSON-RPC 2.0 implementations.\n\n## Installation\n\n```shell\npip install jsonrpc2-objects\n```\n\n```shell\npoetry add jsonrpc2-objects\n```\n\n## Objects\n\nAvailable in `objects` are the following:\n\n| Object                   | Description                 |\n|--------------------------|-----------------------------|\n| RequestObjectParams      | Request with params         |\n| RequestObject            | Request without params      |\n| NotificationObjectParams | Notification with params    |\n| NotificationObject       | Notification without params |\n| ErrorResponseObject      | Response with result        |\n| ResultResponseObject     | Response with error         |\n\n## Errors\n\nPython exceptions are available for each JSON-RPC 2.0 error. Each error\nextends `JSONRPCError`.\n\nExample use with a client implementing these errors:\n\n```python\nfrom jsonrpcobjects.errors import JSONRPCError, MethodNotFound\n\ntry:\n    client.example_method(params)\nexcept MethodNotFound:\n    print("Handle method not found")\nexcept JSONRPCError:\n    print("Handle any JSON RPC error.")\n```\n',
    'author': 'Matthew Burkard',
    'author_email': 'matthewjburkard@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/mburkard/jsonrpc2-objects',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
