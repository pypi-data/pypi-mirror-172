# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kilroy_face_client_py_sdk', 'kilroy_face_client_py_sdk.resources']

package_data = \
{'': ['*']}

install_requires = \
['kilroy-face-py-shared>=0.5,<0.6']

extras_require = \
{'dev': ['pytest>=7.0,<8.0'], 'test': ['pytest>=7.0,<8.0']}

setup_kwargs = {
    'name': 'kilroy-face-client-py-sdk',
    'version': '0.7.0',
    'description': 'SDK for kilroy face clients in Python 🧰',
    'long_description': '<h1 align="center">kilroy-face-client-py-sdk</h1>\n\n<div align="center">\n\nSDK for kilroy face clients in Python 🧰\n\n[![Tests](https://github.com/kilroybot/kilroy-face-client-py-sdk/actions/workflows/test-multiplatform.yml/badge.svg)](https://github.com/kilroybot/kilroy-face-client-py-sdk/actions/workflows/test-multiplatform.yml)\n[![Docs](https://github.com/kilroybot/kilroy-face-client-py-sdk/actions/workflows/docs.yml/badge.svg)](https://github.com/kilroybot/kilroy-face-client-py-sdk/actions/workflows/docs.yml)\n\n</div>\n\n---\n\n## Installing\n\nUsing `pip`:\n\n```sh\npip install kilroy-face-client-py-sdk\n```\n',
    'author': 'kilroy',
    'author_email': 'kilroymail@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kilroybot/kilroy-face-client-py-sdk',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
