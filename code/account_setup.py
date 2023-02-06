import os
import tkinter
import customtkinter
from validate_email_address import validate_email
from support import generate_master_key, generate_master_password_hash
from sql import create_new_user_account, get_email_with_email
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
        self.new_email_label = customtkinter.CTkLabel(master=self.new_account_frame, text="Email:", anchor="w")
        self.new_email_input = customtkinter.CTkEntry(master=self.new_account_frame, placeholder_text="Email",
                                                      width=300)
        self.new_master_password_label = customtkinter.CTkLabel(master=self.new_account_frame, text="Master Password:",
                                                                anchor="w")
        self.new_master_password_input = customtkinter.CTkEntry(master=self.new_account_frame,
                                                                placeholder_text="Master Password")
        self.new_master_password_verify_label = customtkinter.CTkLabel(master=self.new_account_frame,
                                                                       text="Retype Master Password:", anchor="w")
        self.new_master_password_verify_input = customtkinter.CTkEntry(master=self.new_account_frame,
                                                                       placeholder_text="Renter Master Password")
        self.back_forward_button = customtkinter.CTkSegmentedButton(master=self.new_account_frame, width=300,
                                                                    text_color=BLACK, values=["Back", "Create"],
                                                                    unselected_color=GREEN,
                                                                    unselected_hover_color=DARK_GREEN,
                                                                    command=self.back_forward_button_event)
        self.new_account_frame.place(relx=0.5, rely=0.38, anchor=tkinter.N)
        self.new_account_frame.grid_columnconfigure(1, weight=1)
        self.new_account_frame.grid_rowconfigure(9, weight=1)
        self.new_email_label.grid(row=0, column=0, sticky="ew")
        self.new_email_input.grid(row=1, column=0, pady=(0, 20), sticky="ew")
        self.new_master_password_label.grid(row=2, column=0, sticky="ew")
        self.new_master_password_input.grid(row=3, column=0, pady=(0, 20), sticky="ew")
        self.new_master_password_verify_label.grid(row=4, column=0, sticky="ew")
        self.new_master_password_verify_input.grid(row=5, column=0, pady=(0, 20), sticky="ew")
        self.back_forward_button.grid(row=6, column=0, pady=(42, 20), sticky="ew")

    def create_warning_label(self):
        # Create and place warning label
        self.warning_label = customtkinter.CTkLabel(master=self.parent.landing_page_tabview.tab('Vault'),
                                                    text='', text_color=RED)
        self.warning_label.place(relx=0.5, rely=0.01, anchor=tkinter.N)

    def back_forward_button_event(self, *args):
        # Handles the segmented button event, they always send a value with command
        if args[0] == 'Create':
            self.create_new_account()
        else:  # Back button
            self.destroy_all_widgets()
            self.parent.initialize_account_login()

    def create_new_account(self):
        # Gets user input and then creates an account in the db
        email_input = self.new_email_input.get().strip()
        email_input.lower()
        master_password_input = self.new_master_password_input.get().strip()
        master_password_verify_input = self.new_master_password_verify_input.get().strip()

        if self.check_for_invalid_entries(email_input, master_password_input, master_password_verify_input):
            self.refresh_and_insert_fields(email_input, master_password_input, master_password_verify_input)
            return

        email_row = get_email_with_email(email_input)
        if email_row is not None:
            self.refresh_and_insert_fields(email_input, master_password_input, master_password_verify_input)
            self.warning_label.configure(text='Email already in use.')
            return

        salt = os.urandom(32)
        master_key = generate_master_key(salt, master_password_input)
        master_password_hash = generate_master_password_hash(master_password_input, master_key)
        create_new_user_account(email_input, salt, master_key, master_password_hash)
        self.destroy_all_widgets()
        self.parent.initialize_account_login()

    def destroy_all_widgets(self):
        # Destroys all widgets created in this class
        self.new_account_frame.destroy()
        self.warning_label.destroy()

    def check_for_invalid_entries(self, email, master_password, master_password_verify):
        # Checks for blank fields and mismatched passwords
        if email == '':
            self.warning_label.configure(text='Email is blank.')
            return True
        elif master_password == '':
            self.warning_label.configure(text='Password is blank.')
            return True
        elif master_password_verify == '':
            self.warning_label.configure(text='Please verify password.')
            return True
        elif not validate_email(email):
            self.warning_label.configure(text='Not a valid email.')
            return True
        elif master_password != master_password_verify:
            self.warning_label.configure(text='Passwords do not match.')
            return True
        else:
            return False

    def refresh_and_insert_fields(self, email, master_password, master_password_verify):
        # Refresh the page and inserts the entered text back into each field
        self.new_account_frame.destroy()
        self.create_new_account_frame()
        self.new_email_input.insert(0, email)
        self.new_master_password_input.insert(0, master_password)
        self.new_master_password_verify_input.insert(0, master_password_verify)
