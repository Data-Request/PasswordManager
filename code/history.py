import tkinter
import customtkinter
import sqlite3
import functools
from PIL import Image
from colors import *
from settings import MAX_HISTORY_ENTRIES


class HistoryTab:
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

        # History / Copy / Buttons
        self.history_buttons = [None] * MAX_HISTORY_ENTRIES
        self.copy_buttons = [None] * MAX_HISTORY_ENTRIES
        self.copy_image = customtkinter.CTkImage(Image.open(r"C:\Users\xjord\Desktop\PasswordManager\images\copy-icon.png"), size=(20, 20))
        # Create History Textbox Frame
        self.history_textbox_frame = customtkinter.CTkFrame(master=self.landing_tabview.tab('History'), fg_color="transparent")
        # History Textbox Frame Placement
        self.history_textbox_frame.place(relx=0.5, rely=0.02, anchor=tkinter.N)
        self.history_textbox_frame.grid_columnconfigure(0, weight=1)
        self.history_textbox_frame.grid_rowconfigure(5, weight=1)
        # Initialize Widgets
        self.create_buttons()

    def create_buttons(self):
        with sqlite3.connect('data.db') as db:
            cursor = db.execute('SELECT * FROM History WHERE account_id = ?', [self.account_id])
            history_row = cursor.fetchall()

        for index in range(len(history_row)):
            self.history_buttons[index] = customtkinter.CTkTextbox(master=self.history_textbox_frame,
                                                              width=self.main_textbox_width, font=('Arial', 16),
                                                              height=self.main_textbox_height, corner_radius=15)
            self.copy_buttons[index] = customtkinter.CTkButton(master=self.history_textbox_frame, text='',
                                                         image=self.copy_image, fg_color=BLUE,
                                                         command=functools.partial(self.copy_text, index), width=self.button_width,
                                                         height=self.button_height)
            self.history_buttons[index].grid(row=index, column=0, pady=(0, 10), sticky="w")
            self.copy_buttons[index].grid(row=index, column=1, sticky="e")

            self.history_buttons[index].insert('end', history_row[index][1])
            self.history_buttons[index].configure(state='disabled')

    def copy_text(self, index):
        self.history_buttons[index].clipboard_clear()
        self.history_buttons[index].clipboard_append(self.history_buttons[index].get('0.0', 'end').strip())
