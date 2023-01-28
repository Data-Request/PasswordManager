import os
import tkinter
import customtkinter
import sqlite3
from colors import *
from PIL import Image
from add import AddItem
from add_copy_create import AddCopyCreate


class VaultTab:
    def __init__(self, landing_tabview, width, height, account_id):
        super().__init__()

        # General Setup
        self.account_id = account_id
        self.landing_tabview = landing_tabview
        self.name = 'Vault'
        self.vault_tabview_width = width - 72
        self.vault_tabview_height = height - 270
        self.button_width = 25
        self.button_height = 25
        self.main_textbox_width = width - 115
        self.main_textbox_height = 107

        # Tabview Variables
        self.num_of_folders = 15
        self.num_of_unsorted = 0
        self.num_of_secure_notes = 0

        #Images
        self.folder_image = customtkinter.CTkImage(Image.open(r"C:\Users\xjord\Desktop\PasswordManager\images\folder-open-solid.png"), size=(20, 20))
        self.menu_image = customtkinter.CTkImage(Image.open(r"C:\Users\xjord\Desktop\PasswordManager\images\menu.png"), size=(20, 20))

        # Create and Place Bottom Label Frame
        self.bottom_label_frame = customtkinter.CTkFrame(master=self.landing_tabview.tab('Vault'),
                                                            fg_color="transparent")
        self.bottom_label = customtkinter.CTkLabel(master=self.bottom_label_frame, text=f'Number of Folders: {self.num_of_folders}')
        self.bottom_label_frame.grid_columnconfigure(1, weight=1)
        self.bottom_label_frame.grid_rowconfigure(1, weight=1)
        self.bottom_label_frame.place(relx=0.5, rely=1, anchor=tkinter.S)
        self.bottom_label.grid(row=0, column=0, pady=(0, 10), sticky="n")

        # Create Password Textbox
        self.main_textbox = customtkinter.CTkTextbox(master=self.landing_tabview.tab('Vault'), state='disabled',
                                                     width=self.main_textbox_width, font=('Arial', 16),
                                                     height=self.main_textbox_height, corner_radius=15)
        self.main_textbox.place(relx=0.45, rely=0.01, anchor=tkinter.N)


        # Create Add / Copy / Create
        self.add_copy_create = AddCopyCreate(self.landing_tabview, self, self.account_id)


        """=======================       Tabview Section       ======================="""

        self.password_tabview = customtkinter.CTkTabview(master=self.landing_tabview.tab('Vault'),
                                                         width=self.vault_tabview_width,
                                                         height=self.vault_tabview_height,
                                                         segmented_button_selected_color=GREEN, corner_radius=15,
                                                         border_width=3, border_color=WHITE)
        self.password_tabview.place(relx=0.5, rely=0.2, anchor=tkinter.N)
        self.password_tabview.add('Folders')
        self.password_tabview.add('Unsorted')
        self.password_tabview.add('Secure Notes')

        """=======================       Folders Section       ======================="""

        container = tkinter.Frame(self.password_tabview.tab('Folders'), bg=MID_DARK_GRAY2)
        canvas = tkinter.Canvas(container, bg=MID_DARK_GRAY2, highlightbackground=MID_DARK_GRAY2, height=380, width=355)
        scrollbar = customtkinter.CTkScrollbar(container, command=canvas.yview)
        scrollable_frame = tkinter.Frame(canvas, bg=MID_DARK_GRAY2)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for i in range(15):
            customtkinter.CTkButton(master=scrollable_frame, text="                                     Tech", image=self.folder_image, compound='left',
                                    bg_color='transparent',  text_color=BLACK, anchor='w', width=350, corner_radius=15).pack(pady=(20, 0))

        container.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        """=======================       Unsorted Section       ======================="""

        unsorted_container = tkinter.Frame(self.password_tabview.tab('Unsorted'), bg=MID_DARK_GRAY2)
        unsorted_canvas = tkinter.Canvas(unsorted_container, bg=MID_DARK_GRAY2, highlightbackground=MID_DARK_GRAY2, height=380, width=355)
        unsorted_scrollbar = customtkinter.CTkScrollbar(unsorted_container, command=unsorted_canvas.yview)
        unsorted_scrollable_frame = tkinter.Frame(unsorted_canvas, bg=MID_DARK_GRAY2)
        unsorted_scrollable_frame.bind("<Configure>", lambda e: unsorted_canvas.configure(scrollregion=unsorted_canvas.bbox("all")))
        unsorted_canvas.create_window((0, 0), window=unsorted_scrollable_frame, anchor="nw")
        unsorted_canvas.configure(yscrollcommand=unsorted_scrollbar.set)

        with sqlite3.connect('data.db') as db:
            cursor = db.execute('SELECT * FROM Unsorted WHERE account_id = ?', [self.account_id])
            unsorted_row = cursor.fetchall()

        for index in range(len(unsorted_row)):
            customtkinter.CTkButton(master=unsorted_scrollable_frame, text=unsorted_row[index][1], image=self.menu_image, compound='left',
                                    bg_color='transparent',  text_color=BLACK, anchor='w', width=350, corner_radius=15).pack(pady=(20, 0))

        unsorted_container.pack()
        unsorted_canvas.pack(side="left", fill="both", expand=True)
        unsorted_scrollbar.pack(side="right", fill="y")


        """=======================       Secure Notes Section       ======================="""

        note_container = tkinter.Frame(self.password_tabview.tab('Secure Notes'), bg=MID_DARK_GRAY2)
        note_canvas = tkinter.Canvas(note_container, bg=MID_DARK_GRAY2, highlightbackground=MID_DARK_GRAY2, height=380, width=355)
        note_scrollbar = customtkinter.CTkScrollbar(note_container, command=note_canvas.yview)
        note_scrollable_frame = tkinter.Frame(note_canvas, bg=MID_DARK_GRAY2)
        note_scrollable_frame.bind("<Configure>", lambda e: note_canvas.configure(scrollregion=note_canvas.bbox("all")))
        note_canvas.create_window((0, 0), window=note_scrollable_frame, anchor="nw")
        note_canvas.configure(yscrollcommand=note_scrollbar.set)

        with sqlite3.connect('data.db') as db:
            cursor = db.execute('SELECT * FROM Secure_Notes WHERE account_id = ?', [self.account_id])
            note_row = cursor.fetchall()

        for index in range(len(note_row)):
            customtkinter.CTkButton(master=note_scrollable_frame, text=note_row[index][1], image=self.menu_image, compound='left',
                                    bg_color='transparent',  text_color=BLACK, anchor='w', width=350, corner_radius=15).pack(pady=(20, 0))

        note_container.pack()
        note_canvas.pack(side="left", fill="both", expand=True)
        note_scrollbar.pack(side="right", fill="y")






