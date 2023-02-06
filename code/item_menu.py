import tkinter
import customtkinter
from sql import *
from colors import *
from new_folder import NewFolder
from secure_note import SecureNote
from support import encrypt_text, decrypt_text

# todo add limit to fields like note name


class ItemMenu:
    def __init__(self, landing_tabview, parent, account_id, login_id):
        super().__init__()

        # General Setup
        self.account_id = account_id
        self.login_id = login_id
        self.landing_tabview = landing_tabview
        self.parent = parent
        self.website_name_character_limit = 30
        self.textbox_width = 300
        self.textbox_height = 150

        # Initialize
        self.create_main_frame()
        if self.login_id == '':
            if self.parent.name == 'Vault':
                self.create_vault_option_frame()
            else:
                self.create_basic_option_frame()
        else:
            self.create_basic_option_frame()

    def create_main_frame(self):
        if self.parent.name == 'Generator':
            self.main_frame = customtkinter.CTkFrame(master=self.landing_tabview.tab('Generator'),
                                                     fg_color="transparent", height=600, width=403,
                                                     border_width=3, border_color=WHITE, corner_radius=15)
        else:
            self.main_frame = customtkinter.CTkFrame(master=self.landing_tabview.tab('Vault'), fg_color="transparent",
                                                     height=600, width=403, border_width=3, border_color=WHITE,
                                                     corner_radius=15)
        self.main_frame.place(relx=0.5, rely=0.01, anchor=tkinter.N)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(10, weight=1)

    def create_basic_option_frame(self):
        folder_list = get_folder_list(self.account_id)
        self.options_frame = customtkinter.CTkFrame(master=self.main_frame, fg_color="transparent")
        self.main_label = customtkinter.CTkLabel(master=self.options_frame)
        self.folder_label = customtkinter.CTkLabel(master=self.options_frame, text="Folder:")
        self.folder_menu = customtkinter.CTkOptionMenu(master=self.options_frame, values=folder_list, width=300)
        self.website_name_label = customtkinter.CTkLabel(master=self.options_frame, text="Website Name:")
        self.website_name_entry = customtkinter.CTkEntry(master=self.options_frame, width=self.textbox_width,
                                                         placeholder_text='Website Name')
        self.url_label = customtkinter.CTkLabel(master=self.options_frame, text="URL:")
        self.url_entry = customtkinter.CTkEntry(master=self.options_frame, width=self.textbox_width,
                                                placeholder_text='URL')
        self.username_label = customtkinter.CTkLabel(master=self.options_frame, text="Username:")
        self.username_entry = customtkinter.CTkEntry(master=self.options_frame, width=self.textbox_width,
                                                     placeholder_text='Username')
        self.password_label = customtkinter.CTkLabel(master=self.options_frame, text="Password:")
        self.password_textbox = customtkinter.CTkTextbox(master=self.options_frame, state='normal',
                                                         width=self.textbox_width, font=('Arial', 16),
                                                         height=self.textbox_height, corner_radius=5)
        self.cancel_save_button = customtkinter.CTkSegmentedButton(master=self.options_frame, width=300,
                                                                   text_color=BLACK, values=["Cancel", "Save"],
                                                                   unselected_color=GREEN,
                                                                   unselected_hover_color=DARK_GREEN,
                                                                   command=self.cancel_or_save_event)
        self.options_frame.place(relx=0.5, rely=0.01, anchor=tkinter.N)
        self.options_frame.grid_columnconfigure(1, weight=1)
        self.options_frame.grid_rowconfigure(13, weight=1)
        self.main_label.grid(row=0, column=0, sticky="n")
        self.folder_label.grid(row=1, column=0, pady=(15, 5), sticky="w")
        self.folder_menu.grid(row=2, column=0, pady=(0, 20), sticky="w")
        self.website_name_label.grid(row=3, column=0, sticky="w")
        self.website_name_entry.grid(row=4, column=0, pady=(0, 10), sticky="n")
        self.url_label.grid(row=5, column=0, sticky="w")
        self.url_entry.grid(row=6, column=0, pady=(0, 10), sticky="n")
        self.username_label.grid(row=7, column=0, sticky="w")
        self.username_entry.grid(row=8, column=0, pady=(0, 10), sticky="n")
        self.password_label.grid(row=9, column=0, sticky="w")
        self.password_textbox.grid(row=10, column=0, pady=(0, 10), sticky="n")
        self.cancel_save_button.grid(row=11, column=0, pady=(30, 0), sticky="n")

        # Set Defaults
        if self.parent.name == 'Generator':  # Coming from generator tab - password, or passphrase
            self.main_label.configure(text='Add Login')
            if self.parent.generator_tabview.get() == 'Username':  # Coming from generator tab, username
                if self.parent.username_checkbox.get() == 1:
                    self.username_entry.insert(0, self.parent.main_textbox.get('0.0', 'end').strip())
                    self.username_entry.configure(state='disabled')
            else:
                self.password_textbox.insert('end', self.parent.main_textbox.get('0.0', 'end').strip())
                self.password_textbox.configure(state='disabled')
        else:
            if self.login_id:  # Coming from vault tab - edit item
                self.main_label.configure(text='Edit Login')
                login = get_all_from_logins(self.login_id)
                # Decrypt and insert all fields
                master_key = get_master_key_with_account_id(self.account_id)[0]
                decrypted_login_name = decrypt_text(master_key, login[0][2])
                decrypted_url = decrypt_text(master_key, login[0][3])
                decrypted_username = decrypt_text(master_key, login[0][4])
                decrypted_password = decrypt_text(master_key, login[0][5])
                self.website_name_entry.insert(0, decrypted_login_name)
                self.url_entry.insert(0, decrypted_url)
                self.username_entry.insert(0, decrypted_username)
                self.password_textbox.insert('end', decrypted_password)
                self.cancel_save_button.configure(values=["Cancel", "Save", 'Delete'])
            else:  # Coming from vault tab - right menu - new login
                self.main_label.configure(text='Add Login')

    def create_vault_option_frame(self):
        self.options_frame = customtkinter.CTkFrame(master=self.main_frame, fg_color="transparent")
        self.main_label = customtkinter.CTkLabel(master=self.options_frame, text='Add Item')
        self.folder_label = customtkinter.CTkLabel(master=self.options_frame, text="Type:")
        self.folder_menu = customtkinter.CTkOptionMenu(master=self.options_frame, command=self.type_chosen_event,
                                                       values=['Folder', 'Secure Note', 'Login'], width=300)
        self.options_frame.place(relx=0.5, rely=0.01, anchor=tkinter.N)
        self.options_frame.grid_columnconfigure(1, weight=1)
        self.options_frame.grid_rowconfigure(4, weight=1)
        self.main_label.grid(row=0, column=0, sticky="n")
        self.folder_label.grid(row=1, column=0, pady=(15, 5), sticky="w")
        self.folder_menu.grid(row=2, column=0, pady=(0, 10), sticky="w")

        self.new_folder = NewFolder(self, self.options_frame, self.account_id)

    def type_chosen_event(self, *button_clicked_name):
        if button_clicked_name[0] == 'Folder':
            if self.secure_note:
                self.secure_note.destroy_secure_note_frame()
            self.new_folder = NewFolder(self, self.options_frame, self.account_id)
        elif button_clicked_name[0] == 'Secure Note':
            if self.new_folder:
                self.new_folder.destroy_new_folder_frame()
            self.secure_note = SecureNote(self.options_frame, self, self.account_id, None)
        elif button_clicked_name[0] == 'Login':
            if self.new_folder:
                self.new_folder.destroy_new_folder_frame()
            elif self.secure_note:
                self.secure_note.destroy_secure_note_frame()
            self.login = self.create_basic_option_frame()

    def cancel_or_save_event(self, *button_clicked_name):
        if button_clicked_name[0] == 'Cancel':
            self.main_frame.destroy()
        elif button_clicked_name[0] == 'Delete':
            self.create_delete_login_frame()
        elif self.login_id == '':
            self.save_login()
        else:
            self.edit_login()
            self.main_frame.destroy()

    def get_all_login_fields(self):
        website_name = self.website_name_entry.get().strip()
        url = self.url_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_textbox.get('0.0', 'end').strip()
        folder = self.folder_menu.get()
        return website_name,  url, username, password, folder

    def edit_login(self):
        website_name, url, username, password, folder = self.get_all_login_fields()

        self.reset_all_labels()
        if self.check_invalid_input(website_name, url, username, password):
            return

        master_key = get_master_key_with_account_id(self.account_id)[0]
        encrypted_login_name = encrypt_text(master_key, website_name)
        encrypted_url = encrypt_text(master_key, url)
        encrypted_username = encrypt_text(master_key, username)
        encrypted_password = encrypt_text(master_key, password)
        update_login(encrypted_login_name, encrypted_url, encrypted_username, encrypted_password, folder, self.login_id)
        self.parent.update_folder_frame()

    def save_login(self):
        website_name, url, username, password, folder = self.get_all_login_fields()

        self.reset_all_labels()
        if self.check_invalid_input(website_name, url, username, password):
            return

        master_key = get_master_key_with_account_id(self.account_id)[0]
        encrypted_login_name = encrypt_text(master_key, website_name)
        encrypted_url = encrypt_text(master_key, url)
        encrypted_username = encrypt_text(master_key, username)
        encrypted_password = encrypt_text(master_key, password)
        create_new_login(self.account_id, encrypted_login_name, encrypted_url, encrypted_username, encrypted_password,
                         folder)

        if self.parent.name == 'Generator':
            self.parent.update_history()
            self.main_frame.destroy()
        else:
            self.main_frame.destroy()
            self.parent.update_folder_frame()

    def reset_all_labels(self):
        self.website_name_label.configure(text='Website Name:')
        self.url_label.configure(text='URL:')
        self.username_label.configure(text='Username:')
        self.password_label.configure(text='Password:')

    def check_invalid_input(self, website_name, url, username, password):
        if website_name == '':
            self.refresh_frames()
            self.website_name_label.configure(text='Website Name:            Website Name is blank.')
            self.insert_all_fields(website_name, url, username, password)
            return True
        elif len(website_name) > self.website_name_character_limit:
            self.refresh_frames()
            self.website_name_label.configure(text='Website Name:            Website Name too long.')
            self.insert_all_fields(website_name, url, username, password)
            return True
        elif url == '':
            self.refresh_frames()
            self.url_label.configure(text='URL:                     URL is blank.')
            self.insert_all_fields(website_name, url, username, password)
            return True
        elif username == '':
            self.refresh_frames()
            self.username_label.configure(text='Username:                Username is blank.')
            self.insert_all_fields(website_name, url, username, password)
            return True
        elif password == '':
            self.refresh_frames()
            self.password_label.configure(text='Password:                Password is blank.')
            self.insert_all_fields(website_name, url, username, password)
            return True
        else:
            return False

    def insert_all_fields(self, website_name, url, username, password):
        self.website_name_entry.insert(0, website_name)
        self.url_entry.insert(0, url)
        self.username_entry.insert(0, username)
        self.password_textbox.insert('end', password)

    def refresh_frames(self):
        self.main_frame.destroy()
        self.create_main_frame()
        self.create_basic_option_frame()

    def create_delete_login_frame(self):
        self.delete_login_frame = customtkinter.CTkFrame(master=self.options_frame, fg_color=GREEN)
        delete_label = customtkinter.CTkLabel(master=self.delete_login_frame, text_color=BLACK,
                                              text='Confirm Deletion of Login:',
                                              font=('Arial', 18))
        delete_button = customtkinter.CTkSegmentedButton(master=self.delete_login_frame, values=['Yes', 'No'],
                                                         command=self.delete_event)
        self.delete_login_frame.place(relx=0.5, rely=0.5, anchor=tkinter.N)
        self.delete_login_frame.grid_columnconfigure(1, weight=1)
        self.delete_login_frame.grid_rowconfigure(2, weight=1)
        delete_label.grid(row=0, column=0, padx=50, pady=(20, 20), sticky="n")
        delete_button.grid(row=1, column=0, pady=(0, 20), sticky="n")

    def delete_event(self, *button_clicked_name):
        # Handles the segmented button event, they always send a value with command
        # Deletes the secure note from database, and resets screen
        if button_clicked_name[0] == 'Yes':
            delete_login(self.login_id)
        self.main_frame.destroy()
        self.parent.update_folder_frame()
