import hashlib
import subprocess
import uuid

import win32api
import win32security


def __get_user_id():
    md5 = hashlib.md5()
    md5.update(
        win32security.ConvertSidToStringSid(win32security.LookupAccountName(None, win32api.GetUserName())[0]).encode()
    )
    return md5.digest()


key = uuid.UUID(f"{subprocess.check_output('wmic csproduct get uuid').decode().split()[1]}").bytes
salt = __get_user_id()
