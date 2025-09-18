import hashlib
import os

salt = os.environ.get("SALT")
if not salt:
    salt = "test_salt"


def hash_password(password: str) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
    ).hex()
