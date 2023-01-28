import os
import tkinter
import webbrowser
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

        # Copy / Generate Password Buttons
        self.copy_image = customtkinter.CTkImage( Image.open(r"C:\Users\xjord\Desktop\PasswordManager\images\copy-icon.png"), size=(20, 20))
        self.launch_image = customtkinter.CTkImage( Image.open(r"C:\Users\xjord\Desktop\PasswordManager\images\click.png"), size=(20, 20))
        self.copy_gen_button_frame = customtkinter.CTkFrame(master=self.landing_tabview.tab('Vault'),
                                                            fg_color="transparent")
        self.copy_buttons = customtkinter.CTkButton(master=self.copy_gen_button_frame, text='', image=self.copy_image,
                                                    fg_color=BLUE,  width=self.button_width,  height=self.button_height)
        self.launch_button = customtkinter.CTkButton(master=self.copy_gen_button_frame, text='',
                                                     image=self.launch_image, fg_color=BLUE,
                                                     command=self.launch_event, width=self.button_width,
                                                     height=self.button_height)
        # Copy / Generate Placement
        self.copy_gen_button_frame.place(relx=0.96, rely=0.04, anchor=tkinter.N)
        self.copy_gen_button_frame.grid_columnconfigure(1, weight=1)
        self.copy_gen_button_frame.grid_rowconfigure(2, weight=1)
        self.copy_buttons.grid(row=0, column=0, pady=(0, 10), sticky="n")
        self.launch_button.grid(row=1, column=0, sticky="n")

        """=======================       Tabview Section       ======================="""

        self.password_tabview = customtkinter.CTkTabview(master=self.landing_tabview.tab('Vault'),
                                                         width=self.vault_tabview_width,
                                                         height=self.vault_tabview_height,
                                                         segmented_button_selected_color=BLUE, corner_radius=15,
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

        for i in range(50):
            customtkinter.CTkButton(master=scrollable_frame, text="                                     Tech", image=self.folder_image, compound='left',
                                    bg_color='transparent',  text_color=BLACK, anchor='w', width=350, corner_radius=15).pack(pady=(20, 0))

        container.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def launch_event(self):
        browser = webbrowser.get()
        browser.open_new_tab('https://www.creditkarma.com/auth/logon')
        print(browser.name)






