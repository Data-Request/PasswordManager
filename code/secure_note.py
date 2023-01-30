import customtkinter
import sqlite3
from colors import *
from datetime import datetime


class SecureNote:
    def __init__(self, parent_frame, parent, account_id):
        super().__init__()

        # General Setup
        self.account_id = account_id
        self.parent_frame = parent_frame
        self.parent = parent
        self.button_width = 25
        self.button_height = 25
        self.textbox_width = 300
        self.textbox_height = 10
        self.note_textbox_width = 300
        self.note_textbox_height = 250

        # Initialize
        self.create_secure_note_frame()

    def create_secure_note_frame(self):
        # Create Secure Note Frame
        self.secure_note_frame = customtkinter.CTkFrame(master=self.parent_frame, fg_color="transparent")
        self.name_label = customtkinter.CTkLabel(master=self.secure_note_frame, text="Name:")
        self.name_textbox = customtkinter.CTkTextbox(master=self.secure_note_frame,
                                                          width=self.textbox_width, font=('Arial', 16),
                                                          height=self.textbox_height, corner_radius=15)
        self.note_label = customtkinter.CTkLabel(master=self.secure_note_frame, text="Secure Note:")
        self.note_textbox = customtkinter.CTkTextbox(master=self.secure_note_frame,
                                                         width=self.note_textbox_width, font=('Arial', 16),
                                                         height=self.note_textbox_height, corner_radius=15)
        self.save_button = customtkinter.CTkButton(master=self.secure_note_frame, text_color=BLACK, width=300,
                                               text='Save', command=self.save_note)
        # Secure Note Frame Placement
        self.secure_note_frame.grid(row=3, column=0, sticky="n")
        self.secure_note_frame.grid_columnconfigure(1, weight=1)
        self.secure_note_frame.grid_rowconfigure(5, weight=1)
        self.name_label.grid(row=0, column=0, pady=(15, 5), sticky="w")
        self.name_textbox.grid(row=1, column=0, pady=(0, 20), sticky="w")
        self.note_label.grid(row=2, column=0, sticky="w")
        self.note_textbox.grid(row=3, column=0, pady=(0, 25), sticky="n")
        self.save_button.grid(row=4, column=0, sticky="n")

    def destroy_secure_note_frame(self):
        # This is called from parent to kill child
        self.secure_note_frame.destroy()

    def save_note(self):
        now = datetime.now()
        timestamp = now.strftime("%c")
        item_name = self.name_textbox.get('0.0', 'end').strip()
        note = self.note_textbox.get('0.0', 'end').strip()

        with sqlite3.connect('data.db') as db:
            db.execute('INSERT INTO Secure_Notes (account_id, item_name, note, timestamp) VALUES (?,?,?,?)', (self.account_id, item_name, note, timestamp))

        self.destroy_secure_note_frame()
        self.create_secure_note_frame()





