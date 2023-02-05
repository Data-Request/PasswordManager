import base64
import secrets
import string
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def generate_master_key(salt, master_password):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=480000)
    master_key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return master_key


def generate_master_password_hash(master_password, master_key):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=master_password.encode(), iterations=1)
    master_password_hash = base64.urlsafe_b64encode(kdf.derive(master_key))
    return master_password_hash


def encrypt_text(master_key, text):
    encrypter = Fernet(master_key)
    return encrypter.encrypt(text.encode('utf-8'))


def decrypt_text(master_key, text):
    decrypter = Fernet(master_key)
    return decrypter.decrypt(text)


def get_encrypted_text(key, note_name, note):
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


def create_valid_chars_dict(valid_symbols):
    all_valid_chars = f'{string.ascii_letters}{string.digits}{valid_symbols}'
    valid_chars_dict = {}
    for char in range(len(all_valid_chars)):
        valid_chars_dict[all_valid_chars[char]] = 0
    return valid_chars_dict
