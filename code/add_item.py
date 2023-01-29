import tkinter
import customtkinter
import sqlite3
from PIL import Image
from colors import *


class AddItem:
    def __init__(self, landing_tabview, parent, account_id):
        super().__init__()

        # General Setup
        self.account_id = account_id
        self.landing_tabview = landing_tabview
        self.parent = parent
        self.button_width = 25
        self.button_height = 25
        self.textbox_width = 300
        self.textbox_height = 10

        # Images
        self.close_image = customtkinter.CTkImage(
            Image.open(r"C:\Users\xjord\Desktop\PasswordManager\images\close.png"), size=(15, 15))
        self.save_image = customtkinter.CTkImage(
            Image.open(r"C:\Users\xjord\Desktop\PasswordManager\images\save.png"), size=(20, 20))

        # Initialize
        self.create_main_frame()
        if self.parent.name == 'Generator':
            self.create_generator_option_frame()
        else:
            self.create_vault_option_frame()

    def create_main_frame(self):
        # Create Main Frame
        if self.parent.name == 'Generator':
            self.main_frame = customtkinter.CTkFrame(master=self.landing_tabview.tab('Generator'),
                                                     fg_color="transparent", height=600, width=400,
                                                     border_width=3, border_color=WHITE, corner_radius=15)
        else:
            self.main_frame = customtkinter.CTkFrame(master=self.landing_tabview.tab('Vault'), fg_color="transparent",
                                                     height=600, width=400, border_width=3, border_color=WHITE,
                                                     corner_radius=15)
        # History Textbox Frame Placement
        self.main_frame.place(relx=0.5, rely=0.01, anchor=tkinter.N)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(10, weight=1)

    def create_generator_option_frame(self):
        self.options_frame = customtkinter.CTkFrame(master=self.main_frame, fg_color="transparent")
        self.folder_label = customtkinter.CTkLabel(master=self.options_frame, text="Folder")
        self.folder_menu = customtkinter.CTkOptionMenu(master=self.options_frame, width=300,
                                                       values=["Unsorted", "Accounting", 'Tech'])
        self.item_name_label = customtkinter.CTkLabel(master=self.options_frame, text="Website Name")
        self.item_name_textbox = customtkinter.CTkTextbox(master=self.options_frame,
                                                          width=self.textbox_width, font=('Arial', 16),
                                                          height=self.textbox_height, corner_radius=15)
        self.username_label = customtkinter.CTkLabel(master=self.options_frame, text="Username")
        self.username_textbox = customtkinter.CTkTextbox(master=self.options_frame,
                                                         width=self.textbox_width, font=('Arial', 16),
                                                         height=self.textbox_height, corner_radius=15)
        self.password_label = customtkinter.CTkLabel(master=self.options_frame, text="Password")
        self.password_textbox = customtkinter.CTkTextbox(master=self.options_frame, state='normal',
                                                         width=self.textbox_width, font=('Arial', 16),
                                                         height=self.textbox_height, corner_radius=15)
        self.website_label = customtkinter.CTkLabel(master=self.options_frame, text="URL")
        self.website_textbox = customtkinter.CTkTextbox(master=self.options_frame,
                                                        width=self.textbox_width, font=('Arial', 16),
                                                        height=self.textbox_height, corner_radius=15)
        self.warning_label = customtkinter.CTkLabel(master=self.options_frame, text='', text_color=RED)
        self.cancel_save_button = customtkinter.CTkSegmentedButton(master=self.options_frame, width=300,
                                                                   text_color=BLACK, values=["Cancel", "Save"],
                                                                   unselected_color=GREEN,
                                                                   unselected_hover_color=DARK_GREEN,
                                                                   command=self.cancel_or_save_event)
        self.options_frame.place(relx=0.5, rely=0.05, anchor=tkinter.N)
        self.options_frame.grid_columnconfigure(1, weight=1)
        self.options_frame.grid_rowconfigure(12, weight=1)
        self.folder_label.grid(row=0, column=0, pady=(0, 10), sticky="w")
        self.folder_menu.grid(row=1, column=0, pady=(0, 20), sticky="w")
        self.item_name_label.grid(row=2, column=0, padx=(10, 0), pady=(0, 10), sticky="w")
        self.item_name_textbox.grid(row=3, column=0, pady=(0, 10), sticky="n")
        self.username_label.grid(row=4, column=0, padx=(10, 0), pady=(0, 10), sticky="w")
        self.username_textbox.grid(row=5, column=0, pady=(0, 10), sticky="n")
        self.password_label.grid(row=6, column=0, padx=(10, 0), pady=(0, 10), sticky="w")
        self.password_textbox.grid(row=7, column=0, pady=(0, 10), sticky="n")
        self.website_label.grid(row=8, column=0, padx=(10, 0), pady=(0, 10), sticky="w")
        self.website_textbox.grid(row=9, column=0, pady=(0, 10), sticky="n")
        self.warning_label.grid(row=10, column=0, pady=(0, 5), sticky="n")
        self.cancel_save_button.grid(row=11, column=0, sticky="n")

        # Set Defaults
        self.password_textbox.insert('end', self.parent.main_textbox.get('0.0', 'end'))
        self.password_textbox.configure(state='disabled')

    def create_vault_option_frame(self):
        print('Create Vault options now')

    def cancel_or_save_event(self, *args):
        if args[0] == 'Cancel':
            self.destroy_main_frame()
        else:
            self.save_item()

    def save_item(self):
        self.warning_label.configure(text='')
        item_name = self.item_name_textbox.get('0.0', 'end').strip()
        username = self.username_textbox.get('0.0', 'end').strip()
        key = self.password_textbox.get('0.0', 'end').strip()
        url = self.website_textbox.get('0.0', 'end').strip()

        if item_name == '':
            self.warning_label.configure(text='Website Name is blank.')
            return
        elif username == '':
            self.warning_label.configure(text='Username is blank.')
            return
        elif url == '':
            self.warning_label.configure(text='URL is blank.')
            return

        if self.folder_menu.get() == 'Unsorted':
            with sqlite3.connect('data.db') as db:
                db.execute('INSERT INTO Unsorted (account_id, item_name, username, key, url) VALUES (?,?,?,?,?)',
                           (self.account_id, item_name, username, key, url))
        else:
            print('Goes to folder')

        if self.parent.name == 'Generator':
            self.parent.update_history()

        self.destroy_main_frame()

    def destroy_main_frame(self):
        self.main_frame.destroy()

