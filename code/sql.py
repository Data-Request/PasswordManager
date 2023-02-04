import sqlite3
from support import get_timestamp
from settings import MAX_HISTORY_ENTRIES

DATABASE = '../database/data.db'

"""=======================                 Database - Table Section                           ======================="""


def create_database():
    connection = None
    try:
        connection = sqlite3.connect(DATABASE)
    except:
        print('Could not create database.')
    finally:
        if connection:
            connection.close()


def create_database_tables():
    with sqlite3.connect(DATABASE) as db:
        db.execute(""" CREATE TABLE IF NOT EXISTS Person 
        (account_id INTEGER PRIMARY KEY, email TEXT, 
        salt TEXT, master_key TEXT, master_password_hash TEXT,
        account_creation_timestamp TEXT, last_login_timestamp TEXT, folder_list Text)""")

        db.execute(""" CREATE TABLE IF NOT EXISTS Logins 
        (login_id INTEGER PRIMARY KEY, account_id INTEGER, login_name TEXT, url TEXT,
        username TEXT, password TEXT,  folder TEXT, creation_timestamp TEXT, edition_timestamp TEXT,
        FOREIGN KEY(account_id) REFERENCES Person (account_id) )""")

        db.execute(""" CREATE TABLE IF NOT EXISTS History
        (account_id INTEGER, password TEXT, creation_timestamp TEXT,
        FOREIGN KEY(account_id) REFERENCES Person (account_id) )""")

        db.execute(""" CREATE TABLE IF NOT EXISTS Secure_Notes 
        (note_id INTEGER PRIMARY KEY, account_id INTEGER, note_name TEXT, note_body TEXT, 
        creation_timestamp TEXT, edition_timestamp TEXT,
        FOREIGN KEY(account_id) REFERENCES Person (account_id) )""")


"""=======================                       Person Section                               ======================="""


def get_user_account_with_email(email):
    with sqlite3.connect(DATABASE) as db:
        cursor = db.execute('SELECT * FROM Person WHERE email = ?', [email])
        return cursor.fetchone()


def get_email_with_account_id(account_id):
    with sqlite3.connect(DATABASE) as db:
        cursor = db.execute('SELECT email FROM Person WHERE account_id = ?', [account_id])
        return cursor.fetchone()[0]


def get_email_with_email(email):
    # Seem redundant, but it is used to see if an email is already in use
    with sqlite3.connect(DATABASE) as db:
        cursor = db.execute('SELECT email FROM Person WHERE email = ?', [email])
        return cursor.fetchone()


def get_master_key_with_account_id(account_id):
    with sqlite3.connect(DATABASE) as db:
        cursor = db.execute('SELECT master_key FROM Person WHERE account_id = ?', [account_id])
        return cursor.fetchone()


def get_folder_list(account_id):
    with sqlite3.connect(DATABASE) as db:
        cursor = db.execute('SELECT folder_list FROM Person WHERE account_id = ?', [account_id])
        folder_string = cursor.fetchone()[0]
        folder_list = folder_string.split(',')
    return folder_list


def create_new_user_account(email, salt, master_key, master_password_hash):
    with sqlite3.connect(DATABASE) as db:
        db.execute(
            'INSERT INTO Person (email, salt, master_key, master_password_hash, account_creation_timestamp, folder_list) VALUES (?,?,?,?,?,?)',
            (email, salt, master_key, master_password_hash, get_timestamp(), 'Unsorted'))


def update_last_login(account_id):
    with sqlite3.connect(DATABASE) as db:
        db.execute('UPDATE Person '
                   'SET last_login_timestamp = ?'
                   'WHERE account_id = ?', (get_timestamp(), account_id))


def update_folder_list(folder_string, account_id):
    with sqlite3.connect(DATABASE) as db:
        db.execute('UPDATE Person '
                   'SET folder_list = ?'
                   'WHERE account_id = ?', (folder_string, account_id))


"""=======================                       Login Section                                ======================="""


def get_all_from_logins(login_id):
    with sqlite3.connect(DATABASE) as db:
        cursor = db.execute('SELECT * FROM Logins WHERE login_id = ?', [login_id])
        return cursor.fetchall()


def get_each_login_within_folder(account_id, current_folder):
    with sqlite3.connect(DATABASE) as db:
        cursor = db.execute('SELECT * FROM Logins WHERE account_id = ? and folder = ?', (account_id, current_folder))
        return cursor.fetchall()


def create_new_login(account_id, login_name, url, username, password, folder):
    with sqlite3.connect(DATABASE) as db:
        db.execute(
            'INSERT INTO Logins (account_id, login_name, url, username, password, folder, creation_timestamp) VALUES (?,?,?,?,?,?,?)',
            (account_id, login_name, url, username, password, folder, get_timestamp()))


def update_login(login_name, url, username, password, folder, login_id):
    with sqlite3.connect(DATABASE) as db:
        db.execute('UPDATE Logins '
                   'SET login_name = ?,  url = ?, username = ?, password = ?, folder = ?, edition_timestamp = ?'
                   'WHERE login_id = ?', (login_name, url, username, password, folder, get_timestamp(), login_id))


def update_login_with_unsorted(login_id):
    with sqlite3.connect(DATABASE) as db:
        db.execute('UPDATE Logins '
                   'SET folder = ?'
                   'WHERE login_id = ?', ('Unsorted', login_id))


def delete_login(login_id):
    with sqlite3.connect(DATABASE) as db:
        db.execute('DELETE FROM Logins WHERE login_id = ?', [login_id])


def get_num_of_login(account_id):
    with sqlite3.connect(DATABASE) as db:
        cursor = db.execute('SELECT * FROM Logins WHERE account_id = ?', [account_id])
        logins = cursor.fetchall()
    return len(logins)


"""=======================                     Secure Note Section                            ======================="""


def get_all_from_secure_notes(account_id):
    with sqlite3.connect(DATABASE) as db:
        cursor = db.execute('SELECT * FROM Secure_Notes WHERE account_id = ?', [account_id])
        return cursor.fetchall()


def get_single_secure_note(note_id):
    with sqlite3.connect(DATABASE) as db:
        cursor = db.execute('SELECT * FROM Secure_Notes WHERE note_id = ?', [note_id])
        return cursor.fetchall()


def create_new_secure_note(account_id, note_name, note_body):
    with sqlite3.connect(DATABASE) as db:
        db.execute('INSERT INTO Secure_Notes '
                   '(account_id, note_name, note_body, creation_timestamp) VALUES (?,?,?,?)',
                   (account_id, note_name, note_body, get_timestamp()))


def update_secure_note(note_name, note_body, note_id):
    with sqlite3.connect(DATABASE) as db:
        db.execute('UPDATE Secure_Notes '
                   'SET note_name = ?, note_body = ?, edition_timestamp = ?'
                   'WHERE note_id = ?', (note_name, note_body, get_timestamp(), note_id))


def delete_secure_note(note_id):
    with sqlite3.connect(DATABASE) as db:
        db.execute('DELETE FROM Secure_Notes WHERE note_id = ?', [note_id])


"""=======================                        History Section                             ======================="""


def get_all_from_history(account_id):
    with sqlite3.connect(DATABASE) as db:
        cursor = db.execute('SELECT * FROM History WHERE account_id = ?', [account_id])
        history = cursor.fetchall()
    return history


def create_new_history(account_id, password):
    with sqlite3.connect(DATABASE) as db:
        db.execute('INSERT INTO History (account_id, password, creation_timestamp) VALUES (?,?,?)',
                   (account_id, password, get_timestamp()))


def delete_oldest_history_if_at_limit(account_id):
    history = get_all_from_history(account_id)
    if len(history) == MAX_HISTORY_ENTRIES:
        with sqlite3.connect(DATABASE) as db:
            db.execute('Delete FROM History WHERE creation_timestamp = ?', [history[0][2]])


def delete_all_from_history(account_id):
    with sqlite3.connect(DATABASE) as db:
        db.execute('DELETE FROM History WHERE account_id = ?', [account_id])
