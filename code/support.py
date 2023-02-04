import hashlib
from cryptography.fernet import Fernet
import secrets
from datetime import datetime


def generate_password_key(salt, password):
    key = hashlib.pbkdf2_hmac(
        'sha256',  # The hash digest algorithm for HMAC
        password.encode('utf-8'),  # Convert the password to bytes
        salt,  # Provide the salt
        100000  # It is recommended to use at least 100,000 iterations of SHA-256
    )
    return key


def generate_encryption_key():
    return Fernet.generate_key()


def encrypt_text(key, text):
    encrypter = Fernet(key)
    return encrypter.encrypt(text.encode('utf-8'))


def decrypt_text(key, text):
    decrypter = Fernet(key)
    return decrypter.decrypt(text)


def get_encrypted_note_and_name(key, note_name, note):
    encrypted_note_name = encrypt_text(key, note_name)
    encrypted_note = encrypt_text(key, note)
    return encrypted_note_name, encrypted_note


def get_decrypted_note_and_name(key, note_name, note):
    decrypted_note_name = decrypt_text(key, note_name)
    decrypted_note = decrypt_text(key, note)
    return decrypted_note_name, decrypted_note


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
