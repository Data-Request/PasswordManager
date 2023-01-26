import tkinter
import customtkinter
import sqlite3
from PIL import Image
from colors import *


class History:
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
        self.main_textbox_height = 110


        # Copy / Generate Password Buttons
        self.copy_image = customtkinter.CTkImage(Image.open(r"C:\Users\xjord\Desktop\PasswordManager\images\copy-icon.png"), size=(20, 20))

        # Create History Textbox Frames
        self.history_textbox_frame = customtkinter.CTkFrame(master=self.landing_tabview.tab('History'), fg_color="transparent")
        self.history_textbox_0 = customtkinter.CTkTextbox(master=self.history_textbox_frame, state='disabled',
                                                         width=self.main_textbox_width, font=('Arial', 16),
                                                         height=self.main_textbox_height, corner_radius=15)
        self.copy_button_0 = customtkinter.CTkButton(master=self.history_textbox_frame, text='', image=self.copy_image, fg_color=BLUE,
                                                    command=None, width=self.button_width, height=self.button_height)
        self.history_textbox_1 = customtkinter.CTkTextbox(master=self.history_textbox_frame, state='disabled',
                                                         width=self.main_textbox_width, font=('Arial', 16),
                                                         height=self.main_textbox_height, corner_radius=15)
        self.copy_button_1 = customtkinter.CTkButton(master=self.history_textbox_frame, text='', image=self.copy_image, fg_color=BLUE,
                                                    command=None, width=self.button_width, height=self.button_height)
        self.history_textbox_2 = customtkinter.CTkTextbox(master=self.history_textbox_frame, state='disabled',
                                                         width=self.main_textbox_width, font=('Arial', 16),
                                                         height=self.main_textbox_height, corner_radius=15)
        self.copy_button_2 = customtkinter.CTkButton(master=self.history_textbox_frame, text='', image=self.copy_image, fg_color=BLUE,
                                                    command=None, width=self.button_width, height=self.button_height)
        self.history_textbox_3 = customtkinter.CTkTextbox(master=self.history_textbox_frame, state='disabled',
                                                         width=self.main_textbox_width, font=('Arial', 16),
                                                         height=self.main_textbox_height, corner_radius=15)
        self.copy_button_3 = customtkinter.CTkButton(master=self.history_textbox_frame, text='', image=self.copy_image, fg_color=BLUE,
                                                    command=None, width=self.button_width, height=self.button_height)
        self.history_textbox_4 = customtkinter.CTkTextbox(master=self.history_textbox_frame, state='disabled',
                                                         width=self.main_textbox_width, font=('Arial', 16),
                                                         height=self.main_textbox_height, corner_radius=15)
        self.copy_button_4 = customtkinter.CTkButton(master=self.history_textbox_frame, text='', image=self.copy_image, fg_color=BLUE,
                                                    command=None, width=self.button_width, height=self.button_height)
        # Password Strength Placement
        self.history_textbox_frame.place(relx=0.5, rely=0.02, anchor=tkinter.N)
        self.history_textbox_frame.grid_columnconfigure(0, weight=1)
        self.history_textbox_frame.grid_rowconfigure(5, weight=1)
        self.history_textbox_0.grid(row=0, column=0, sticky="w")
        self.copy_button_0.grid(row=0, column=1, sticky="e")
        self.history_textbox_1.grid(row=1, column=0, pady=(10, 0),  sticky="w")
        self.copy_button_1.grid(row=1, column=1, sticky="e")
        self.history_textbox_2.grid(row=2, column=0, pady=(10, 0),  sticky="w")
        self.copy_button_2.grid(row=2, column=1, sticky="e")
        self.history_textbox_3.grid(row=3, column=0, pady=(10, 0),  sticky="w")
        self.copy_button_3.grid(row=3, column=1, sticky="e")
        self.history_textbox_4.grid(row=4, column=0, pady=(10, 0),  sticky="w")
        self.copy_button_4.grid(row=4, column=1, sticky="e")

        # Initialize Text
        with sqlite3.connect('data.db') as db:
            cursor = db.execute('SELECT * FROM History WHERE account_id = ?', [self.account_id])
            history_row = cursor.fetchall()
            for row in history_row:
                print(row)