# netlink-crypt

Tools to encrypt passwords used for automation.

The keys used depend on the current user and the actual machine.

## Installation

Use your preferred python package manager (I use [Poetry](https://python-poetry.org/)).

### Dependencies

- [click](https://click.palletsprojects.com/en/8.1.x/)
- [pycryptodomex](https://pypi.org/project/pycryptodomex/)
- [pywin32](https://github.com/mhammond/pywin32) on Windows

## Contents

- `netlink.crypt.enigma`
- `netlink.crypt.denigma`
- `encrypt_secret`

### netlink.crypt.enigma

```python
from netlink.crypt import enigma

encrypted = enigma('secret sauce')
```

### netlink.crypt.denigma

Using **bytes**:
```python
from netlink.crypt import denigma

s = denigma(b'\xa2\x1c-\x8d\x19\xaa5"o\xfc&\x1e\xbc\xe5\xfe\x9e')
```
or using **base64** encoded string:

```python
from netlink.crypt import denigma

s = denigma('ohwtjRmqNSJv/CYevOX+ng==')
```

or using a list of integers (**toml**):

```python
from netlink.crypt import denigma

s = denigma([162, 28, 45, 141, 25, 170, 53, 34, 111, 252, 38, 30, 188, 229, 254, 158])
```

### encrypt_secret

Utility script to encrypt. Output can be

- bytes
- toml
- b64

```shell
Usage: encrypt_secret [OPTIONS] VALUE

  Encrypt VALUE using current user and machine to determine keys.

Options:
  -o, --output-format [toml|b64]  Bytes by default.
  --help                          Show this message and exit.
```

Binaries created with [PyIstaller](https://pyinstaller.org/en/stable/) available at [netlink-crypt/dist](https://gitlab.com/netlink-consulting/netlink-crypt/-/blob/main/dist/)

## License

MIT License

## Changes

### 0.0.1

Limit numerical uid in linux to prevent memory overflow.
