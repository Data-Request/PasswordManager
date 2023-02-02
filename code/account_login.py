import tkinter
import customtkinter
from PIL import Image
from support import generate_key
from sql import update_last_login, get_user_account
from colors import *


class AccountLogin:
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.key_image = customtkinter.CTkImage(
            Image.open(r"C:\Users\xjord\Desktop\PasswordManager\images\key-solid.png"), size=(20, 20))
        self.create_log_in_widgets()

    def create_log_in_widgets(self):
        # Create Login Button Frame
        self.login_frame = customtkinter.CTkFrame(master=self.parent.landing_page_tabview.tab('Vault'), fg_color="transparent")
        self.username_label = customtkinter.CTkLabel(master=self.login_frame, text="Username:", anchor="w")
        self.username = customtkinter.CTkEntry(master=self.login_frame, placeholder_text="Username or Email")
        self.password_label = customtkinter.CTkLabel(master=self.login_frame, text="Master Password:", anchor="w")
        self.password = customtkinter.CTkEntry(master=self.login_frame, placeholder_text="Master Password")
        self.login_button = customtkinter.CTkButton(master=self.login_frame, text_color=BLACK,
                                                    text='                             Log in', image=self.key_image,
                                                    compound='left', command=self.validate_log_info, anchor='w')
        self.verify_label = customtkinter.CTkLabel(master=self.login_frame, text_color=WHITE, width=300,
                                                   text='Your vault is locked. Verify your identity to continue.')
        # Login Button Frame Placement
        self.login_frame.place(relx=0.5, rely=0.38, anchor=tkinter.N)
        self.login_frame.grid_columnconfigure(1, weight=1)
        self.login_frame.grid_rowconfigure(6, weight=1)
        self.username_label.grid(row=0, column=0, sticky="ew")
        self.username.grid(row=1, column=0, pady=(0, 20), sticky="ew")
        self.password_label.grid(row=2, column=0, sticky="ew")
        self.password.grid(row=3, column=0, pady=(0, 20), sticky="ew")
        self.login_button.grid(row=4, column=0, pady=(0, 20), sticky="ew")
        self.verify_label.grid(row=5, column=0, pady=(0, 20), sticky="ew")
        # Create and Place Warning Label
        self.warning_label = customtkinter.CTkLabel(master=self.parent.landing_page_tabview.tab('Vault'),
                                                    text='', text_color=RED)
        self.warning_label.place(relx=0.5, rely=0.01, anchor=tkinter.N)

    def validate_log_info(self):
        username = self.username.get()
        username.lower()
        password = self.password.get()

        user_account = get_user_account(username)

        if user_account is None:
            self.warning_label.configure(text='Incorrect username or password.')
        else:
            current_key = generate_key(user_account[2], password)
            if current_key == user_account[3]:
                self.parent.account_id = user_account[0]
                self.parent.initialize_vault_tab()
                self.parent.vault_image_frame.destroy()
                self.parent.new_account_button.destroy()
                self.login_frame.destroy()
                self.warning_label.destroy()
                update_last_login(self.parent.account_id)
            else:
                self.warning_label.configure(text='Incorrect username or password.')
