import tkinter
import customtkinter
import sqlite3
from colors import *
from PIL import Image

class VaultTab:
    def __init__(self, landing_tabview, width, height, account_id):
        super().__init__()

        # General Setup
        self.account_id = account_id
        self.landing_tabview = landing_tabview
        self.password_tabview_width = width - 72
        self.password_tabview_height = height - 300
        self.button_width = 25
        self.button_height = 25
        self.main_textbox_width = width - 115
        self.main_textbox_height = 107


        # Create Password Textbox
        self.password_textbox = customtkinter.CTkTextbox(master=self.landing_tabview.tab('Vault'), state='disabled',
                                                         width=self.main_textbox_width, font=('Arial', 16),
                                                         height=self.main_textbox_height, corner_radius=15)
        self.password_textbox.place(relx=0.45, rely=0.01, anchor=tkinter.N)

