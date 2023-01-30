import sqlite3


def create_database_tables():
    with sqlite3.connect('data.db') as db:
        db.execute(""" CREATE TABLE IF NOT EXISTS Person 
        (account_id INTEGER PRIMARY KEY, username TEXT, email TEXT, salt TEXT, key TEXT )""")

        db.execute(""" CREATE TABLE IF NOT EXISTS History
        (account_id INTEGER, key TEXT, timestamp TEXT,
        FOREIGN KEY(account_id) REFERENCES Person (account_id) )""")

        db.execute(""" CREATE TABLE IF NOT EXISTS Item 
        (item_id INTEGER PRIMARY KEY, account_id INTEGER, item_name TEXT, username TEXT, key TEXT, url TEXT, folder TEXT,
        FOREIGN KEY(account_id) REFERENCES Person (account_id) )""")

        db.execute(""" CREATE TABLE IF NOT EXISTS Secure_Notes 
        (account_id INTEGER, item_name TEXT, note TEXT,
        FOREIGN KEY(account_id) REFERENCES Person (account_id) )""")


def get_folder_list(account_id):
    # Grab a unique set of all folders names used for the account, then sort in a list A-Z
    folder_set = set()
    with sqlite3.connect('data.db') as db:
        cursor = db.execute('SELECT * FROM Item WHERE account_id = ?', (account_id,))
        folder_row = cursor.fetchall()
        for item in folder_row:
            folder_set.add(item[6])
    folder_list = list(folder_set)
    folder_list.sort()
    # If folder list is empty(new account) or no folder created, then default to unsorted
    if not folder_list:
        folder_list = ['Unsorted']
    return folder_list

