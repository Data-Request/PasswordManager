import tkinter
import customtkinter
import sqlite3
import functools
from PIL import Image
from colors import *
from settings import MAX_HISTORY_ENTRIES

# todo find a way to reset scrollbar.
"""problem: full history, scroll to bottom,  delete history, then generate new history 
and click back on history tab, you cant see all history"""


class HistoryTab:
    def __init__(self, landing_tabview, width, height, account_id):
        super().__init__()

        # General Setup
        self.account_id = account_id
        self.landing_tabview = landing_tabview
        self.password_tabview_width = width - 72
        self.password_tabview_height = height - 300
        self.textbox_width = width - 135
        self.textbox_height = 70
        self.clear_history_width = 100
        self.clear_history_height = 30
        self.copy_button_width = 25
        self.copy_button_height = 50

        # Images
        self.delete_image = customtkinter.CTkImage(Image.open(r"C:\Users\xjord\Desktop\PasswordManager\images\trash"
                                                              r"-solid.png"), size=(20, 20))

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
        # Create Max Entries Label
        self.max_entries_label = customtkinter.CTkLabel(master=self.landing_tabview.tab('History'),
                                                        text=f'Max History: {MAX_HISTORY_ENTRIES}')
        self.max_entries_label.place(relx=0.25, rely=1, anchor=tkinter.S)
        # Clear History Button
        self.clear_history_button = customtkinter.CTkButton(master=self.landing_tabview.tab('History'),
                                                            text='Clear History', command=self.clear_history_entries,
                                                            fg_color=GREEN, text_color=BLACK, image=self.delete_image,
                                                            width=self.clear_history_width,
                                                            height=self.clear_history_height)
        self.clear_history_button.place(relx=0.7, rely=1, anchor=tkinter.S)

        # Initialize
        self.create_history_frame()

    def create_history_frame(self):
        history_frame = tkinter.Frame(self.landing_tabview.tab('History'), bg=LIGHT_GRAY)
        canvas = tkinter.Canvas(history_frame, bg=LIGHT_GRAY, highlightbackground=LIGHT_GRAY, height=550, width=385)
        scrollbar = customtkinter.CTkScrollbar(history_frame, command=canvas.yview)
        self.scrollable_frame = tkinter.Frame(canvas, bg=LIGHT_GRAY)
        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        history_frame.place(relx=0.5, rely=0.03, anchor=tkinter.N)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_buttons(self):
        with sqlite3.connect('data.db') as db:
            cursor = db.execute('SELECT * FROM History WHERE account_id = ?', [self.account_id])
            history_row = cursor.fetchall()

        for index in range(len(history_row)):
            self.history_textbox[index] = customtkinter.CTkTextbox(master=self.scrollable_frame,
                                                                   width=self.textbox_width, font=('Arial', 16),
                                                                   height=self.textbox_height, corner_radius=15)
            self.date_times[index] = customtkinter.CTkLabel(master=self.scrollable_frame, fg_color=DARK_GRAY,
                                                            corner_radius=15)
            self.copy_buttons[index] = customtkinter.CTkButton(master=self.scrollable_frame, text='',
                                                               image=self.copy_image, fg_color=BLUE,
                                                               command=functools.partial(self.copy_text, index),
                                                               width=self.copy_button_width,
                                                               height=self.copy_button_height)
            self.history_textbox[index].grid(row=(index + index), column=0, sticky="w")
            self.date_times[index].grid(row=(index + index + 1), column=0, padx=(30, 0), pady=(0, 15), sticky="w")
            self.copy_buttons[index].grid(row=(index + index), rowspan=1, column=1, sticky="e")

            self.history_textbox[index].insert('end', history_row[index][1])
            self.history_textbox[index].configure(state='disabled')
            self.date_times[index].configure(text=history_row[index][2])

    def destroy_history_tab(self):
        for index in range(len(self.history_textbox)):
            if not self.history_textbox[index] is None:
                self.history_textbox[index].destroy()
                self.history_textbox[index] = None
                self.date_times[index].destroy()
                self.date_times[index] = None
                self.copy_buttons[index].destroy()
                self.copy_buttons[index] = None

    def clear_history_entries(self):
        with sqlite3.connect('data.db') as db:
            db.execute('DELETE FROM History WHERE account_id = ?', [self.account_id])
        self.destroy_history_tab()

    def copy_text(self, index):
        self.history_textbox[index].clipboard_clear()
        self.history_textbox[index].clipboard_append(self.history_textbox[index].get('0.0', 'end').strip())
