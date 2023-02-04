import tkinter
import customtkinter
from PIL import Image
from support import generate_password_key
from sql import update_last_login, get_user_account
from colors import *


class AccountLogin:
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.key_image = customtkinter.CTkImage(
            Image.open(r"C:\Users\xjord\Desktop\PasswordManager\images\key-solid.png"), size=(20, 20))
        self.create_login_frame()

    def create_login_frame(self):
        # Create and place Login Button Frame
        self.login_frame = customtkinter.CTkFrame(master=self.parent.landing_page_tabview.tab('Vault'), fg_color="transparent")
        self.warning_label = customtkinter.CTkLabel(master=self.login_frame, text='', text_color=RED)
        self.username_label = customtkinter.CTkLabel(master=self.login_frame, text="Username:", anchor="w")
        self.username = customtkinter.CTkEntry(master=self.login_frame, placeholder_text="Username or Email")
        self.password_label = customtkinter.CTkLabel(master=self.login_frame, text="Master Password:", anchor="w")
        self.password = customtkinter.CTkEntry(master=self.login_frame, placeholder_text="Master Password")
        self.login_button = customtkinter.CTkButton(master=self.login_frame, text_color=BLACK,
                                                    text='                             Log in', image=self.key_image,
                                                    compound='left', command=self.validate_log_info, anchor='w')
        self.verify_label = customtkinter.CTkLabel(master=self.login_frame, text_color=WHITE, width=300,
                                                   text='Your vault is locked. Verify your identity to continue.')
        self.login_frame.place(relx=0.5, rely=0.36, anchor=tkinter.N)
        self.login_frame.grid_columnconfigure(1, weight=1)
        self.login_frame.grid_rowconfigure(6, weight=1)
        self.warning_label.grid(row=0, column=0, sticky="ew")
        self.username_label.grid(row=2, column=0, sticky="ew")
        self.username.grid(row=3, column=0, pady=(0, 20), sticky="ew")
        self.password_label.grid(row=4, column=0, sticky="ew")
        self.password.grid(row=5, column=0, pady=(0, 20), sticky="ew")
        self.login_button.grid(row=6, column=0, pady=(0, 20), sticky="ew")
        self.verify_label.grid(row=7, column=0, pady=(0, 20), sticky="ew")

    def validate_log_info(self):
        username = self.username.get()
        password = self.password.get()
        user_account = get_user_account(username)
        if user_account is None:    # No user with entered username in db
            self.warning_label.configure(text='Incorrect username or password.')
            return

        current_key = generate_password_key(user_account[2], password)
        if current_key != user_account[3]:   # Password key doesnt match key in db
            self.warning_label.configure(text='Incorrect username or password.')
            return

        update_last_login(user_account[0])
        self.parent.account_id = user_account[0]
        self.parent.enabled_tabview()
        self.login_frame.destroy()
