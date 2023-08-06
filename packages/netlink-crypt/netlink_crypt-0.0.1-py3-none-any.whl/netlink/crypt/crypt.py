import base64
import sys

from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad

if sys.platform == "linux":
    from .linux import key as __key, salt as __salt
elif sys.platform == "win32":
    from .win32 import key as __key, salt as __salt


def __get_cipher():
    return AES.new(key=__key, mode=AES.MODE_CBC, iv=__salt)


def enigma(value):
    return __get_cipher().encrypt(pad(value.encode(), AES.block_size))


def denigma(value):
    if isinstance(value, bytes):
        return unpad(__get_cipher().decrypt(value), AES.block_size).decode()
    if isinstance(value, str):
        return unpad(__get_cipher().decrypt(base64.b64decode(value)), AES.block_size).decode()
    return denigma(b"".join([i.to_bytes(1, "big") for i in value]))
