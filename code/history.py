import tkinter
import customtkinter
import functools
from colors import *
from settings import MAX_HISTORY_ENTRIES, TEXTBOX_FONT
from sql import get_all_from_history, delete_all_from_history, get_master_key_with_account_id
from support import decrypt_text
import string
from images import DELETE_IMAGE, COPY_IMAGE


class HistoryTab:
    def __init__(self, landing_tabview, width, account_id):
        super().__init__()

        # General Setup
        self.account_id = account_id
        self.landing_tabview = landing_tabview
        self.textbox_width = width - 135
        self.textbox_height = 70
        self.clear_history_width = 100
        self.clear_history_height = 30
        self.copy_button_width = 25
        self.copy_button_height = 50
        self.history_textbox = [None] * MAX_HISTORY_ENTRIES

        # Initialize
        self.create_main_frame()
        self.create_bottom_frame()
        self.create_history_frame()
        self.create_history_row()

    def create_main_frame(self):
        # Create and place main frame
        self.main_frame = tkinter.Frame(self.landing_tabview.tab('History'), bg=LIGHT_GRAY)
        canvas = tkinter.Canvas(self.main_frame, bg=LIGHT_GRAY, highlightbackground=LIGHT_GRAY, height=550, width=385)
        scrollbar = customtkinter.CTkScrollbar(self.main_frame, command=canvas.yview)
        self.scrollable_frame = tkinter.Frame(canvas, bg=LIGHT_GRAY)
        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        self.main_frame.place(relx=0.5, rely=0.03, anchor=tkinter.N)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_history_frame(self):
        # Create and place History textbox frame
        self.history_textbox_frame = customtkinter.CTkFrame(master=self.scrollable_frame, fg_color='transparent')
        self.history_textbox_frame.pack()

    def create_history_row(self):
        # Create and place each History row
        history = get_all_from_history(self.account_id)
        history.reverse()  # We want the history tab sorted from newest to oldest
        for index in (range(len(history))):
            history_row_frame = customtkinter.CTkFrame(master=self.history_textbox_frame, fg_color='transparent')
            history_row_frame.grid_columnconfigure(2, weight=1)
            history_row_frame.grid_rowconfigure(2, weight=1)
            self.history_textbox[index] = customtkinter.CTkTextbox(master=history_row_frame,
                                                                   width=self.textbox_width, font=TEXTBOX_FONT,
                                                                   height=self.textbox_height, corner_radius=15)
            date_times = customtkinter.CTkLabel(master=history_row_frame, fg_color=DARK_GRAY, corner_radius=15,
                                                text=history[index][2])
            copy_buttons = customtkinter.CTkButton(master=history_row_frame, text='', image=COPY_IMAGE,
                                                   fg_color=GREEN, command=functools.partial(self.copy_text, index),
                                                   width=self.copy_button_width, height=self.copy_button_height)
            # Decrypts password then applies color based on typing of each character
            master_key = get_master_key_with_account_id(self.account_id)[0]
            decrypted_input_password = decrypt_text(master_key, history[index][1]).decode()
            self.history_textbox[index].tag_config('letter', foreground=WHITE)
            self.history_textbox[index].tag_config('digit', foreground=GREEN)
            self.history_textbox[index].tag_config('symbol', foreground=BLUE)
            for char in decrypted_input_password:
                if char in string.ascii_letters:
                    self.history_textbox[index].insert('end', char, 'letter')
                elif char in string.digits:
                    self.history_textbox[index].insert('end', char, 'digit')
                else:
                    self.history_textbox[index].insert('end', char, 'symbol')
            self.history_textbox[index].configure(state='disabled')
            # Placement
            self.history_textbox[index].grid(row=(index + index), column=0, sticky="w")
            date_times.grid(row=(index + index + 1), column=0, padx=(30, 0), pady=(0, 15), sticky="w")
            copy_buttons.grid(row=(index + index), rowspan=1, column=1, sticky="e")
            history_row_frame.pack()

    def copy_text(self, index):
        self.history_textbox[index].clipboard_clear()
        self.history_textbox[index].clipboard_append(self.history_textbox[index].get('0.0', 'end').strip())

    def create_bottom_frame(self):
        self.max_entries_label = customtkinter.CTkLabel(master=self.landing_tabview.tab('History'),
                                                        text=f'Max History: {MAX_HISTORY_ENTRIES}')
        self.clear_history_button = customtkinter.CTkButton(master=self.landing_tabview.tab('History'),
                                                            text='Clear History', command=self.clear_history_event,
                                                            fg_color=GREEN, text_color=BLACK, image=DELETE_IMAGE,
                                                            width=self.clear_history_width,
                                                            height=self.clear_history_height)
        self.max_entries_label.place(relx=0.25, rely=1, anchor=tkinter.S)
        self.clear_history_button.place(relx=0.7, rely=1, anchor=tkinter.S)

    def refresh_history_tab(self):
        self.history_textbox_frame.destroy()
        self.create_history_frame()
        self.create_history_row()

    def clear_history_event(self):
        delete_all_from_history(self.account_id)
        self.main_frame.destroy()
        self.create_main_frame()
        self.max_entries_label.destroy()
        self.clear_history_button.destroy()
        self.create_bottom_frame()
        self.refresh_history_tab()
