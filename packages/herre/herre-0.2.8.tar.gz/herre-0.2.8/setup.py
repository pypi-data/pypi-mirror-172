# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['herre',
 'herre.fakts',
 'herre.grants',
 'herre.grants.backend',
 'herre.grants.code_server',
 'herre.grants.test',
 'herre.grants.windowed']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>3.7.4',
 'certifi>2021',
 'koil>=0.2.6,<0.3.0',
 'oauthlib>=3.1.1,<4.0.0',
 'pydantic>=1.9.0,<2.0.0']

extras_require = \
{'fakts': ['fakts>=0.2.13,<0.3.0'], 'qt': ['QtPy>=2.0.1,<3.0.0']}

setup_kwargs = {
    'name': 'herre',
    'version': '0.2.8',
    'description': 'openid connect client tailore to pyqt and async environments',
    'long_description': '# herre\n\n[![codecov](https://codecov.io/gh/jhnnsrs/herre/branch/master/graph/badge.svg?token=UGXEA2THBV)](https://codecov.io/gh/jhnnsrs/herre)\n[![PyPI version](https://badge.fury.io/py/herre.svg)](https://pypi.org/project/herre/)\n![Maintainer](https://img.shields.io/badge/maintainer-jhnnsrs-blue)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/herre.svg)](https://pypi.python.org/pypi/herre/)\n[![PyPI status](https://img.shields.io/pypi/status/herre.svg)](https://pypi.python.org/pypi/herre/)\n[![PyPI download month](https://img.shields.io/pypi/dm/herre.svg)](https://pypi.python.org/pypi/herre/)\n\n#### DEVELOPMENT\n\n## Idea\n\nherre is an (asynchronous) oauth2/openid client, that provides sensible defaults for the python\necosystem\n\n## Prerequisites\n\nherre needs a oauth2/opendid server to connect to\n\n## Supports\n\n- Authorization Code Flow (PKCE)\n  - Within a Qt app through a QtWebengine View\n  - With a Redirect Server\n- Client-Credentials Flow\n\n## Usage\n\nIn order to initialize the Client you need to connect it as a Valid Application with your Arnheim Instance\n\n```python\n\nclient = Herre(\n    grant=AuthorizationCode()\n    host="p-tnagerl-lab1",\n    port=8000,\n    client_id="$YOUR_CLIENT_ID",\n    client_secret="$YOUR_CLIENT_SECRET",\n    name="karl",\n)\n\nwith client:\n  client.login()\n\n```\n\nAsync usage\n\n```python\n\nclient = Herre(\n    grant=AuthorizationCode()\n    host="p-tnagerl-lab1",\n    port=8000,\n    client_id="$YOUR_CLIENT_ID",\n    client_secret="$YOUR_CLIENT_SECRET",\n    name="karl",\n)\n\nasync with client:\n  await client.login()\n\n```\n\n## Intergration with Qt\n\nherre fully supports qt-based applications (both PySide2 and PyQt5) and provides a convenient helper class \'QtHerre\'\nas well as a included windowed Authoriation Code Flow (needs pyqtwebengine as additional dependency) as well as browser based logins\n\n```python\nclass MainWindow(QtWidget)\n\n    def __init__(self, *args, **kwargs):\n        self.herre = QtHerre(\n          grant=QtWindowAuthorizationCode()\n        )\n\n```\n\n## Build with\n\n- [koil](https://github.com/jhnnsrs/koil) - for pyqt event loop handling\n- [oauthlib](https://github.com/oauthlib/oauthlib) - for oauth2 compliance\n- [aiohttp](https://github.com/aio-libs/aiohttp) - transport layer (especially redirect server)\n',
    'author': 'jhnnsrs',
    'author_email': 'jhnnsrs@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
