import os
import hashlib
import tkinter
import customtkinter
import sqlite3
from vault import VaultTab
from generator import GeneratorTab
from history import HistoryTab
from settings import SettingsTab
from colors import *
from PIL import Image

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


# todo add email verification
# todo add remember username feature, add settings to remove it

class LandingPage(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configure Window
        self.width = 480
        self.height = 720
        self.geometry(f"{self.width}x{self.height}")
        self.title('Password Manager')
        self.tabview_width = self.width - 50
        self.tabview_height = self.height - 30

        # Create Tabview
        self.landing_page_tabview = customtkinter.CTkTabview(self, height=self.tabview_height, width=self.tabview_width,
                                                             corner_radius=15, segmented_button_selected_color=BLUE,
                                                             border_width=3, border_color=WHITE, state='disabled',
                                                             text_color=WHITE, command=self.tabview_clicked_event)
        self.landing_page_tabview.place(relx=0.5, rely=0.015, anchor=tkinter.N)
        self.landing_page_tabview.add('Vault')
        self.landing_page_tabview.add("Generator")
        self.landing_page_tabview.add("History")
        self.landing_page_tabview.add("Settings")
        self.landing_page_tabview.tab('Vault').grid_columnconfigure(0, weight=1)

        self.warning_label = customtkinter.CTkLabel(master=self.landing_page_tabview.tab('Vault'),
                                                    text='', text_color=RED)
        self.warning_label.place(relx=0.5, rely=1, anchor=tkinter.S)

        # Initialize
        self.account_id = None
        self.create_log_in_widgets()
        self.create_person_table()
        self.create_history_table()

    def create_log_in_widgets(self):
        # Create Vault Image Frame
        self.vault_image_frame = customtkinter.CTkFrame(master=self.landing_page_tabview.tab('Vault'), fg_color="transparent")
        self.vault_image = customtkinter.CTkImage(Image.open(r"C:\Users\xjord\Desktop\PasswordManager\images\vault.png"), size=(150, 150))
        self.vault_image_button = customtkinter.CTkButton(master=self.vault_image_frame,text='', image=self.vault_image,
                                                          fg_color="transparent", state='disabled')
        # Vault Image Frame Placement
        self.vault_image_frame.place(relx=0.5, rely=0.06, anchor=tkinter.N)
        self.vault_image_frame.grid_columnconfigure(1, weight=1)
        self.vault_image_frame.grid_rowconfigure(1, weight=1)
        self.vault_image_button.grid(row=0, column=0, pady=(0, 20), sticky="n")
        # Create Login Button Frame
        self.login_frame = customtkinter.CTkFrame(master=self.landing_page_tabview.tab('Vault'), fg_color="transparent")
        self.username_label = customtkinter.CTkLabel(master=self.login_frame, text="Username:", anchor="w")
        self.username = customtkinter.CTkEntry(master=self.login_frame, placeholder_text="Username or Email")
        self.password_label = customtkinter.CTkLabel(master=self.login_frame, text="Master Password:", anchor="w")
        self.password = customtkinter.CTkEntry(master=self.login_frame, placeholder_text="Master Password")
        self.key_image = customtkinter.CTkImage(Image.open(r"C:\Users\xjord\Desktop\PasswordManager\images\key-solid.png"), size=(20, 20))
        self.login_button = customtkinter.CTkButton(master=self.login_frame, text_color=BLACK,
                                                    text='                             Log in', image=self.key_image,
                                                    compound='left', command=self.validate_log_info, anchor='w')
        self.verify_label = customtkinter.CTkLabel(master=self.login_frame, text_color=WHITE, width=300,
                                                   text='Your vault is locked. Verify your identity to continue.')
        self.new_account_button = customtkinter.CTkButton(master=self.login_frame, text="Don't have an account?",
                                                          text_color=BLACK, command=self.account_setup)
        # Login Button Frame Placement
        self.login_frame.place(relx=0.5, rely=0.4, anchor=tkinter.N)
        self.login_frame.grid_columnconfigure(1, weight=1)
        self.login_frame.grid_rowconfigure(6, weight=1)
        self.username_label.grid(row=0, column=0, sticky="ew")
        self.username.grid(row=1, column=0, pady=(0, 20), sticky="ew")
        self.password_label.grid(row=2, column=0, sticky="ew")
        self.password.grid(row=3, column=0, pady=(0, 20), sticky="ew")
        self.login_button.grid(row=4, column=0, pady=(0, 20), sticky="ew")
        self.verify_label.grid(row=5, column=0, pady=(0, 20), sticky="ew")
        self.new_account_button.grid(row=6, column=0, pady=(60, 0), sticky="ew")

    def account_setup(self):
        self.login_frame.destroy()
        # Create New Account Frame
        self.new_account_frame = customtkinter.CTkFrame(master=self.landing_page_tabview.tab('Vault'), fg_color="transparent")
        self.new_username = customtkinter.CTkEntry(master=self.new_account_frame, placeholder_text="Username")
        self.new_email = customtkinter.CTkEntry(master=self.new_account_frame, placeholder_text="Email")
        self.new_master_password = customtkinter.CTkEntry(master=self.new_account_frame, placeholder_text="Master Password")
        self.new_master_password_verify = customtkinter.CTkEntry(master=self.new_account_frame, placeholder_text="Renter Master Password")
        self.continue_button = customtkinter.CTkButton(master=self.new_account_frame, text="Continue", width=300,
                                                       command=self.create_new_account)
        # New Account Placement
        self.new_account_frame.place(relx=0.5, rely=0.4, anchor=tkinter.N)
        self.new_account_frame.grid_columnconfigure(0, weight=1)
        self.new_account_frame.grid_rowconfigure(5, weight=1)
        self.new_username.grid(row=0, column=0, pady=(0, 20), sticky="ew")
        self.new_email.grid(row=1, column=0, pady=(0, 20), sticky="ew")
        self.new_master_password.grid(row=2, column=0, pady=(0, 20), sticky="ew")
        self.new_master_password_verify.grid(row=3, column=0, pady=(0, 20), sticky="ew")
        self.continue_button.grid(row=4, column=0, pady=(40, 20), sticky="ew")

    def tabview_clicked_event(self):
        if self.landing_page_tabview.get() == 'History':
            self.history.create_buttons()

    def initialize_all_tabs(self):
        self.landing_page_tabview.configure(state='normal')
        self.landing_page_tabview.set("Generator")
        self.vault_image_frame.destroy()
        self.login_frame.destroy()
        self.warning_label.destroy()
        VaultTab(self.landing_page_tabview, self.width, self.height, self.account_id)
        GeneratorTab(self.landing_page_tabview, self.width, self.height, self.account_id)
        self.history = HistoryTab(self.landing_page_tabview, self.width, self.height, self.account_id)
        SettingsTab(self.landing_page_tabview, self.account_id)

    def validate_log_info(self):
        username = self.username.get().lower()
        password = self.password.get()

        with sqlite3.connect('data.db') as db:
            cursor = db.execute('SELECT account_id, username, salt, key FROM Person WHERE username = ?', [username])
            user_account = cursor.fetchone()

        if user_account is None:
            self.warning_label.configure(text='Incorrect username or password.')
        else:
            current_key = self.generate_key(user_account[2], password)
            if current_key == user_account[3]:
                self.account_id = user_account[0]
                self.initialize_all_tabs()
            else:
                self.warning_label.configure(text='Incorrect username or password.')

    def create_new_account(self):
        username = self.new_username.get().lower()
        email = self.new_email.get().lower()
        master_password = self.new_master_password.get()
        master_password_verify = self.new_master_password_verify.get()

        # Reset in case method is called twice in a row for different reasons
        self.reset_new_account_text_color()

        if self.check_for_blank_field(username, email, master_password, master_password_verify):
            return
        if master_password != master_password_verify:
            self.new_master_password.configure(text_color=RED)
            self.new_master_password_verify.configure(text_color=RED)
            self.warning_label.configure(text='Passwords do not match.')
            return

        with sqlite3.connect('data.db') as db:
            cursor = db.execute('SELECT username FROM Person WHERE username = ?', [username])
            username_row = cursor.fetchone()
            cursor = db.execute('SELECT email FROM Person WHERE email = ?', [email])
            email_row = cursor.fetchone()

        if username_row is None:
            if email_row is None:
                salt = os.urandom(32)
                key = self.generate_key(salt, master_password)
                with sqlite3.connect('data.db') as db:
                    db.execute('INSERT INTO Person (username, email, salt, key) VALUES (?,?,?,?)', (username, email, salt, key))
                self.new_account_frame.destroy()
                self.warning_label.configure(text='')
                self.create_log_in_widgets()
            else:
                self.new_email.configure(text_color=RED)
                self.warning_label.configure(text='Email already in use.')
        else:
            self.new_username.configure(text_color=RED)
            self.warning_label.configure(text='Username taken.')

    def reset_new_account_text_color(self):
        self.new_username.configure(text_color=WHITE)
        self.new_master_password.configure(text_color=WHITE)
        self.new_master_password_verify.configure(text_color=WHITE)

    def check_for_blank_field(self, username, email, master_password, master_password_verify):
        if username == '':
            self.warning_label.configure(text='Username is blank.')
            return True
        elif email == '':
            self.warning_label.configure(text='Email is blank.')
            return True
        elif master_password == '':
            self.warning_label.configure(text='Password is blank.')
            return True
        elif master_password_verify == '':
            self.warning_label.configure(text='Please verify password.')
            return True
        else:
            return False

    @staticmethod
    def create_person_table():
        with sqlite3.connect('data.db') as db:
            db.execute("""
            CREATE TABLE IF NOT EXISTS Person (
                account_id INTEGER PRIMARY KEY,
                username TEXT,
                email TEXT,
                salt TEXT,
                key TEXT
            )
            """)

    @staticmethod
    def create_history_table():
        with sqlite3.connect('data.db') as db:
            db.execute("""
            CREATE TABLE IF NOT EXISTS History (
                account_id INTEGER,
                key TEXT,
                timestamp TEXT,
                FOREIGN KEY(account_id) REFERENCES Person (account_id)
            )
            """)

    @staticmethod
    def generate_key(salt, password):
        key = hashlib.pbkdf2_hmac(
            'sha256',  # The hash digest algorithm for HMAC
            password.encode('utf-8'),  # Convert the password to bytes
            salt,  # Provide the salt
            100000  # It is recommended to use at least 100,000 iterations of SHA-256
        )
        return key


if __name__ == '__main__':
    app = LandingPage()
    app.resizable(width=False, height=False)
    app.mainloop()
