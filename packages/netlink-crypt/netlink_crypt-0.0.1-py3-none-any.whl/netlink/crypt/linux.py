import hashlib
import os
import uuid


def __get_key():
    with open("/etc/machine-id") as f:
        a = f.read().strip()
    return uuid.UUID(a).bytes


def __get_user_id():
    uid = os.getuid()
    if not uid:
        uid = 4711
    while uid > 100000:
        uid = uid // 10
    md5 = hashlib.md5()
    md5.update((os.getlogin() * uid).encode())
    return md5.digest()


key = __get_key()
salt = __get_user_id()
