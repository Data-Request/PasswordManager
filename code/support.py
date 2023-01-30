import hashlib
from datetime import datetime


def generate_key(salt, password):
    key = hashlib.pbkdf2_hmac(
        'sha256',  # The hash digest algorithm for HMAC
        password.encode('utf-8'),  # Convert the password to bytes
        salt,  # Provide the salt
        100000  # It is recommended to use at least 100,000 iterations of SHA-256
    )
    return key


def get_timestamp():
    now = datetime.now()
    return now.strftime("%c")
