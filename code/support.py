import hashlib
import secrets
from datetime import datetime


def generate_key(salt, password):
    key = hashlib.pbkdf2_hmac(
        'sha256',  # The hash digest algorithm for HMAC
        password.encode('utf-8'),  # Convert the password to bytes
        salt,  # Provide the salt
        100000  # It is recommended to use at least 100,000 iterations of SHA-256
    )
    return key


def create_username():
    random_word = ''
    random_numbers = ''
    for i in range(0, secrets.randbelow(5)):
        random_numbers += str(secrets.randbelow(10))

    random_index = secrets.randbelow(58110)
    with open(r'C:\Users\xjord\Desktop\PasswordManager\word_files\mielie_stronk_list_58110', 'r') as file:
        lines = file.readlines()
        current_word = lines[random_index].strip()
        random_word += f'{current_word}{random_numbers}'

    return random_word


def get_timestamp():
    now = datetime.now()
    return now.strftime("%c")
