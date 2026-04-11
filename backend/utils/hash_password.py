import hashlib
import os
from configs.argon2 import ph

def make_salt():
    return os.urandom(16).hex()


def hash_password(password, salt):
    newpass = password + salt
    return hashlib.sha256(newpass.encode()).hexdigest()

def hash_password_v2(passworld):
    newpass = passworld
    hash = ph.hash(str(newpass))
    return hash
