# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crypt']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'pycryptodomex>=3.14.1,<4.0.0']

extras_require = \
{':sys_platform == "win32"': ['pywin32>=304,<305']}

entry_points = \
{'console_scripts': ['encrypt_secret = netlink.crypt.cli:encrypt_secret']}

setup_kwargs = {
    'name': 'netlink-crypt',
    'version': '0.0.1',
    'description': 'Password Storage for Automation',
    'long_description': '# netlink-crypt\n\nTools to encrypt passwords used for automation.\n\nThe keys used depend on the current user and the actual machine.\n\n## Installation\n\nUse your preferred python package manager (I use [Poetry](https://python-poetry.org/)).\n\n### Dependencies\n\n- [click](https://click.palletsprojects.com/en/8.1.x/)\n- [pycryptodomex](https://pypi.org/project/pycryptodomex/)\n- [pywin32](https://github.com/mhammond/pywin32) on Windows\n\n## Contents\n\n- `netlink.crypt.enigma`\n- `netlink.crypt.denigma`\n- `encrypt_secret`\n\n### netlink.crypt.enigma\n\n```python\nfrom netlink.crypt import enigma\n\nencrypted = enigma(\'secret sauce\')\n```\n\n### netlink.crypt.denigma\n\nUsing **bytes**:\n```python\nfrom netlink.crypt import denigma\n\ns = denigma(b\'\\xa2\\x1c-\\x8d\\x19\\xaa5"o\\xfc&\\x1e\\xbc\\xe5\\xfe\\x9e\')\n```\nor using **base64** encoded string:\n\n```python\nfrom netlink.crypt import denigma\n\ns = denigma(\'ohwtjRmqNSJv/CYevOX+ng==\')\n```\n\nor using a list of integers (**toml**):\n\n```python\nfrom netlink.crypt import denigma\n\ns = denigma([162, 28, 45, 141, 25, 170, 53, 34, 111, 252, 38, 30, 188, 229, 254, 158])\n```\n\n### encrypt_secret\n\nUtility script to encrypt. Output can be\n\n- bytes\n- toml\n- b64\n\n```shell\nUsage: encrypt_secret [OPTIONS] VALUE\n\n  Encrypt VALUE using current user and machine to determine keys.\n\nOptions:\n  -o, --output-format [toml|b64]  Bytes by default.\n  --help                          Show this message and exit.\n```\n\nBinaries created with [PyIstaller](https://pyinstaller.org/en/stable/) available at [netlink-crypt/dist](https://gitlab.com/netlink-consulting/netlink-crypt/-/blob/main/dist/)\n\n## License\n\nMIT License\n\n## Changes\n\n### 0.0.1\n\nLimit numerical uid in linux to prevent memory overflow.\n',
    'author': 'Bernhard Radermacher',
    'author_email': 'bernhard.radermacher@netlink-consulting.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/netlink_python/netlink-crypt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
