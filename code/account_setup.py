import os
import tkinter
import customtkinter
from validate_email_address import validate_email
from support import generate_password_key
from sql import create_new_user_account, get_username_with_username, get_email_with_email
from colors import *


class AccountSetup:
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.create_new_account_frame()
        self.create_warning_label()

    def create_new_account_frame(self):
        # Create and place new account frame
        self.new_account_frame = customtkinter.CTkFrame(master=self.parent.landing_page_tabview.tab('Vault'),
                                                        fg_color="transparent")
        self.new_username_label = customtkinter.CTkLabel(master=self.new_account_frame, text="Username:", anchor="w")
        self.new_username = customtkinter.CTkEntry(master=self.new_account_frame, placeholder_text="Username",
                                                   width=300)
        self.new_email_label = customtkinter.CTkLabel(master=self.new_account_frame, text="Email:", anchor="w")
        self.new_email = customtkinter.CTkEntry(master=self.new_account_frame, placeholder_text="Email")
        self.new_master_password_label = customtkinter.CTkLabel(master=self.new_account_frame, text="Master Password:",
                                                                anchor="w")
        self.new_master_password = customtkinter.CTkEntry(master=self.new_account_frame,
                                                          placeholder_text="Master Password")
        self.new_master_password_verify_label = customtkinter.CTkLabel(master=self.new_account_frame,
                                                                       text="Retype Master Password:", anchor="w")
        self.new_master_password_verify = customtkinter.CTkEntry(master=self.new_account_frame,
                                                                 placeholder_text="Renter Master Password")
        self.back_forward_button = customtkinter.CTkSegmentedButton(master=self.new_account_frame, width=300,
                                                                    text_color=BLACK, values=["Back", "Create"],
                                                                    unselected_color=GREEN,
                                                                    unselected_hover_color=DARK_GREEN,
                                                                    command=self.back_forward_button_event)
        self.new_account_frame.place(relx=0.5, rely=0.38, anchor=tkinter.N)
        self.new_account_frame.grid_columnconfigure(1, weight=1)
        self.new_account_frame.grid_rowconfigure(9, weight=1)
        self.new_username_label.grid(row=0, column=0, sticky="ew")
        self.new_username.grid(row=1, column=0, pady=(0, 20), sticky="ew")
        self.new_email_label.grid(row=2, column=0, sticky="ew")
        self.new_email.grid(row=3, column=0, pady=(0, 20), sticky="ew")
        self.new_master_password_label.grid(row=4, column=0, sticky="ew")
        self.new_master_password.grid(row=5, column=0, pady=(0, 20), sticky="ew")
        self.new_master_password_verify_label.grid(row=6, column=0, sticky="ew")
        self.new_master_password_verify.grid(row=7, column=0, pady=(0, 20), sticky="ew")
        self.back_forward_button.grid(row=8, column=0, pady=(42, 20), sticky="ew")

    def create_warning_label(self):
        self.warning_label = customtkinter.CTkLabel(master=self.parent.landing_page_tabview.tab('Vault'),
                                                    text='', text_color=RED)
        self.warning_label.place(relx=0.5, rely=0.01, anchor=tkinter.N)

    def back_forward_button_event(self, *args):
        if args[0] == 'Create':
            self.create_new_account()
        else:
            self.new_account_frame.destroy()
            self.warning_label.destroy()
            self.parent.initialize_account_login()

    def create_new_account(self):
        username = self.new_username.get().strip()
        username.lower()
        email = self.new_email.get().strip()
        email.lower()
        master_password = self.new_master_password.get().strip()
        master_password_verify = self.new_master_password_verify.get().strip()

        if self.check_for_invalid_entries(username, email, master_password, master_password_verify):
            self.refresh_and_insert_fields(username, email, master_password, master_password_verify)
            return

        username_row = get_username_with_username(username)
        email_row = get_email_with_email(email)
        if username_row is not None:
            self.refresh_and_insert_fields(username, email, master_password, master_password_verify)
            self.warning_label.configure(text='Username taken.')
            return
        elif email_row is not None:
            self.refresh_and_insert_fields(username, email, master_password, master_password_verify)
            self.warning_label.configure(text='Email already in use.')
            return

        salt = os.urandom(32)
        key = generate_password_key(salt, master_password)
        create_new_user_account(username, email, salt, key)
        self.new_account_frame.destroy()
        self.warning_label.destroy()
        self.parent.create_login_frame()

    def check_for_invalid_entries(self, username, email, master_password, master_password_verify):
        # Checks for blank fields and mismatched passwords
        invalid_entries = False
        if username == '':
            self.warning_label.configure(text='Username is blank.')
            invalid_entries = True
        elif email == '':
            self.warning_label.configure(text='Email is blank.')
            invalid_entries = True
        elif master_password == '':
            self.warning_label.configure(text='Password is blank.')
            invalid_entries = True
        elif master_password_verify == '':
            self.warning_label.configure(text='Please verify password.')
            invalid_entries = True
        elif not validate_email(email):
            self.warning_label.configure(text='Not a valid email.')
            invalid_entries = True
        elif master_password != master_password_verify:
            self.warning_label.configure(text='Passwords do not match.')
            invalid_entries = True
        return invalid_entries

    def refresh_and_insert_fields(self, username, email, master_password, master_password_verify):
        # Refresh the page and inserts the entered text back into each field
        self.new_account_frame.destroy()
        self.create_new_account_frame()
        self.new_username.insert(0, username)
        self.new_email.insert(0, email)
        self.new_master_password.insert(0, master_password)
        self.new_master_password_verify.insert(0, master_password_verify)
