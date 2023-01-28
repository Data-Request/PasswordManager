import customtkinter
import sqlite3
from landing_page import LandingPage

# todo add cancel button to create account page
# todo add email verification via email for master password resets
# todo add remember username feature, add settings to remove it
# todo sign out button
# todo add back button to account creation

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green


def create_database_tables():
    with sqlite3.connect('data.db') as db:
        db.execute(""" CREATE TABLE IF NOT EXISTS Person 
        (account_id INTEGER PRIMARY KEY, username TEXT, email TEXT, salt TEXT, key TEXT )""")

        db.execute(""" CREATE TABLE IF NOT EXISTS History
        (account_id INTEGER, key TEXT, timestamp TEXT,
        FOREIGN KEY(account_id) REFERENCES Person (account_id) )""")

        db.execute(""" CREATE TABLE IF NOT EXISTS Unsorted 
        (account_id INTEGER, item_name TEXT, username TEXT, key TEXT, url TEXT,
        FOREIGN KEY(account_id) REFERENCES Person (account_id) )""")

        db.execute(""" CREATE TABLE IF NOT EXISTS Secure_Notes 
        (account_id INTEGER, item_name TEXT, note TEXT,
        FOREIGN KEY(account_id) REFERENCES Person (account_id) )""")


if __name__ == '__main__':
    create_database_tables()
    app = LandingPage()
    app.resizable(width=False, height=False)
    app.mainloop()
