import tkinter
import customtkinter
from colors import *
from images import KEY_IMAGE
from sql import update_last_login, get_user_account_with_email
from support import generate_master_key, generate_master_password_hash


class AccountLogin:
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.create_login_frame()

    def create_login_frame(self):
        # Create and place Login Button Frame
        self.login_frame = customtkinter.CTkFrame(master=self.parent.landing_page_tabview.tab('Vault'),
                                                  fg_color="transparent")
        self.warning_label = customtkinter.CTkLabel(master=self.login_frame, text='', text_color=RED)
        self.email_label = customtkinter.CTkLabel(master=self.login_frame, text="Email:", anchor="w")
        self.email_entry = customtkinter.CTkEntry(master=self.login_frame, placeholder_text="Email")
        self.password_label = customtkinter.CTkLabel(master=self.login_frame, text="Master Password:", anchor="w")
        self.password_entry = customtkinter.CTkEntry(master=self.login_frame, placeholder_text="Master Password")
        self.login_button = customtkinter.CTkButton(master=self.login_frame, text_color=BLACK,
                                                    text='                             Log in', image=KEY_IMAGE,
                                                    compound='left', command=self.validate_log_info, anchor='w')
        self.verify_label = customtkinter.CTkLabel(master=self.login_frame, text_color=WHITE, width=300,
                                                   text='Your vault is locked. Verify your identity to continue.')
        self.login_frame.place(relx=0.5, rely=0.36, anchor=tkinter.N)
        self.login_frame.grid_columnconfigure(1, weight=1)
        self.login_frame.grid_rowconfigure(6, weight=1)
        self.warning_label.grid(row=0, column=0, sticky="ew")
        self.email_label.grid(row=1, column=0, sticky="ew")
        self.email_entry.grid(row=2, column=0, pady=(0, 20), sticky="ew")
        self.password_label.grid(row=3, column=0, sticky="ew")
        self.password_entry.grid(row=4, column=0, pady=(0, 20), sticky="ew")
        self.login_button.grid(row=5, column=0, pady=(0, 20), sticky="ew")
        self.verify_label.grid(row=6, column=0, pady=(0, 20), sticky="ew")

    def validate_log_info(self):
        # Checks db for an account with same email
        email_input = self.email_entry.get()
        email_input.lower()
        user_account = get_user_account_with_email(email_input)
        if user_account is None:  # No user with entered email in db
            self.warning_label.configure(text='Incorrect email or password.')
            return
        # Checks if password input matches hashed master password in db
        password_input = self.password_entry.get()
        current_password_key = generate_master_key(user_account[2], password_input)
        current_password_hash = generate_master_password_hash(password_input, current_password_key)
        if current_password_hash != user_account[4]:  # Password hash doesn't match hash in db
            self.warning_label.configure(text='Incorrect email or password.')
            return
        # Account is good to log in, update login timestamp in db and grab account id then destroy all widgets created
        update_last_login(user_account[0])
        self.parent.account_id = user_account[0]
        self.parent.enabled_tabview()
        self.login_frame.destroy()
