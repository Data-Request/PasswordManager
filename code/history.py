import tkinter
import customtkinter
import sqlite3
import functools
from PIL import Image
from colors import *
from settings import MAX_HISTORY_ENTRIES


# todo fix delete button

class HistoryTab:
    def __init__(self, landing_tabview, width, height, account_id):
        super().__init__()

        # General Setup
        self.account_id = account_id
        self.landing_tabview = landing_tabview
        self.password_tabview_width = width - 72
        self.password_tabview_height = height - 300
        self.textbox_width = width - 115
        self.textbox_height = 70
        self.clear_history_width = 100
        self.clear_history_height = 30
        self.copy_button_width = 25
        self.copy_button_height = 50

        # History / Copy / Buttons
        self.history_textbox = [None] * MAX_HISTORY_ENTRIES
        self.date_times = [None] * MAX_HISTORY_ENTRIES
        self.copy_buttons = [None] * MAX_HISTORY_ENTRIES
        self.copy_image = customtkinter.CTkImage(Image.open(r"C:\Users\xjord\Desktop\PasswordManager\images\copy-icon.png"), size=(20, 20))
        # Create History Textbox Frame
        self.history_textbox_frame = customtkinter.CTkFrame(master=self.landing_tabview.tab('History'), fg_color="transparent")
        # History Textbox Frame Placement
        self.history_textbox_frame.place(relx=0.5, rely=0.05, anchor=tkinter.N)
        self.history_textbox_frame.grid_columnconfigure(1, weight=1)
        self.history_textbox_frame.grid_rowconfigure(10, weight=1)


        # Clear History Button Frame
        self.delete_image = customtkinter.CTkImage(Image.open(r"C:\Users\xjord\Desktop\PasswordManager\images\trash-solid.png"), size=(20, 20))
        self.clear_history_frame = customtkinter.CTkFrame(master=self.landing_tabview.tab('History'), fg_color="transparent")
        self.clear_history_button = customtkinter.CTkButton(master=self.clear_history_frame, text='Clear History',
                                                            fg_color=BLUE, text_color=BLACK,
                                                               command=self.clear_history_entries, width=self.clear_history_width,
                                                               height=self.clear_history_height, image=self.delete_image)
        # History Textbox Frame Placement
        self.clear_history_frame.place(relx=0.5, rely=1, anchor=tkinter.S)
        self.clear_history_frame.grid_columnconfigure(1, weight=1)
        self.clear_history_frame.grid_rowconfigure(1, weight=1)
        self.clear_history_button.grid(row=0, column=0, sticky="e")



        # Initialize Widgets
        self.create_buttons()

    def create_buttons(self):
        with sqlite3.connect('data.db') as db:
            cursor = db.execute('SELECT * FROM History WHERE account_id = ?', [self.account_id])
            history_row = cursor.fetchall()

        for index in range(len(history_row)):
            self.history_textbox[index] = customtkinter.CTkTextbox(master=self.history_textbox_frame,
                                                                   width=self.textbox_width, font=('Arial', 16),
                                                                   height=self.textbox_height, corner_radius=15)
            self.date_times[index] = customtkinter.CTkLabel(master=self.history_textbox_frame,
                                                          fg_color=DARK_GRAY, corner_radius=15)
            self.copy_buttons[index] = customtkinter.CTkButton(master=self.history_textbox_frame, text='',
                                                               image=self.copy_image, fg_color=BLUE,
                                                               command=functools.partial(self.copy_text, index), width=self.copy_button_width,
                                                               height=self.copy_button_height)
            self.history_textbox[index].grid(row=(index + index), column=0, sticky="w")
            self.date_times[index].grid(row=(index + index + 1), column=0, padx=(30,0), pady=(0, 10), sticky="w")
            self.copy_buttons[index].grid(row=(index + index), rowspan=1, column=1, sticky="e")

            self.history_textbox[index].insert('end', history_row[index][1])
            self.history_textbox[index].configure(state='disabled')
            self.date_times[index].configure(text=history_row[index][2])

    def destroy_history_tab(self):
        for index in range(len(self.history_textbox)):
            self.history_textbox[index].destroy()
            self.date_times[index].destroy()
            self.copy_buttons[index].destroy()

    def clear_history_entries(self):
        with sqlite3.connect('data.db') as db:
            db.execute('DELETE FROM History WHERE account_id = ?', [self.account_id])
        self.destroy_history_tab()

    def copy_text(self, index):
        self.history_textbox[index].clipboard_clear()
        self.history_textbox[index].clipboard_append(self.history_textbox[index].get('0.0', 'end').strip())
