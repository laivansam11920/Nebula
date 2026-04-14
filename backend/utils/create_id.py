import secrets
from utils.hash256 import get_sha256_hash


def generate_secure_id(length=20) -> int:
    digits = "".join([str(secrets.randbelow(10)) for _ in range(length)])
    return digits


def create_id() -> int:
    my_id = generate_secure_id(20)
    hashed_id = get_sha256_hash(my_id)
    return hashed_id
