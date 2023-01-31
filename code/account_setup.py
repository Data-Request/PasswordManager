import os
import tkinter
import customtkinter
import sqlite3
from validate_email_address import validate_email
from support import generate_key, get_timestamp
from colors import *


class AccountSetup:
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.create_new_account_frame()

    def create_new_account_frame(self):
        self.new_account_frame = customtkinter.CTkFrame(master=self.parent.landing_page_tabview.tab('Vault'),
                                                        fg_color="transparent")
        self.new_username_label = customtkinter.CTkLabel(master=self.new_account_frame, text="Username:", anchor="w")
        self.new_username = customtkinter.CTkEntry(master=self.new_account_frame, placeholder_text="Username", width=300)
        self.new_email_label = customtkinter.CTkLabel(master=self.new_account_frame, text="Email:", anchor="w")
        self.new_email = customtkinter.CTkEntry(master=self.new_account_frame, placeholder_text="Email")
        self.new_master_password_label = customtkinter.CTkLabel(master=self.new_account_frame, text="Master Password:", anchor="w")
        self.new_master_password = customtkinter.CTkEntry(master=self.new_account_frame,
                                                          placeholder_text="Master Password")
        self.new_master_password_verify_label = customtkinter.CTkLabel(master=self.new_account_frame, text="Retype Master Password:", anchor="w")
        self.new_master_password_verify = customtkinter.CTkEntry(master=self.new_account_frame,
                                                                 placeholder_text="Renter Master Password")
        self.back_forward_button = customtkinter.CTkSegmentedButton(master=self.new_account_frame, width=300,
                                                                    text_color=BLACK, values=["Back", "Create"],
                                                                    unselected_color=GREEN, unselected_hover_color=DARK_GREEN,
                                                                    command=self.back_forward_button)
        # New Account Placement
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
        # Create and Place Warning Label
        self.warning_label = customtkinter.CTkLabel(master=self.parent.landing_page_tabview.tab('Vault'),
                                                    text='', text_color=RED)
        self.warning_label.place(relx=0.5, rely=0.01, anchor=tkinter.N)

    def back_forward_button(self, *args):
        if args[0] == 'Create':
            print(args[0])
            self.create_new_account()
        else:
            self.new_account_frame.destroy()
            self.warning_label.destroy()
            self.parent.create_log_in_widgets()

    def create_new_account(self):
        username = self.new_username.get().strip()
        username.lower()
        email = self.new_email.get().strip()
        email.lower()
        master_password = self.new_master_password.get().strip()
        master_password_verify = self.new_master_password_verify.get().strip()

        # Reset in case method is called twice in a row for different reasons
        self.reset_new_account_text_color()

        if self.check_for_blank_field(username, email, master_password, master_password_verify):
            return
        if not validate_email(email):
            self.new_email.configure(text_color=RED)
            self.warning_label.configure(text='Not a valid email.')
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
                key = generate_key(salt, master_password)
                with sqlite3.connect('data.db') as db:
                    db.execute('INSERT INTO Person (username, email, salt, key, account_creation) VALUES (?,?,?,?,?)',
                               (username, email, salt, key, get_timestamp()))
                self.new_account_frame.destroy()
                self.warning_label.destroy()
                self.parent.create_log_in_widgets()
            else:
                self.new_email.configure(text_color=RED)
                self.warning_label.configure(text='Email already in use.')
        else:
            self.new_username.configure(text_color=RED)
            self.warning_label.configure(text='Username taken.')

    def reset_new_account_text_color(self):
        self.new_username.configure(text_color=WHITE)
        self.new_email.configure(text_color=WHITE)
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

