import tkinter
import customtkinter
import webbrowser
from colors import *
from item_menu import ItemMenu
from images import CREATE_IMAGE, LAUNCH_IMAGE, ADD_IMAGE, COPY_IMAGE


class RightButtonSidebar:
    def __init__(self, landing_tabview, parent, account_id):
        super().__init__()

        # General Setup
        self.account_id = account_id
        self.landing_tabview = landing_tabview
        self.parent = parent
        self.button_width = 25
        self.button_height = 25

        # Add / Copy / Create / Launch Buttons
        if self.parent.name == 'Generator':
            self.copy_button_frame = customtkinter.CTkFrame(master=self.landing_tabview.tab('Generator'),
                                                            fg_color="transparent")
            self.create_or_launch_button = customtkinter.CTkButton(master=self.copy_button_frame, text='',
                                                                   image=CREATE_IMAGE, fg_color=GREEN,
                                                                   command=self.parent.generator_tabview_event,
                                                                   width=self.button_width, height=self.button_height)

        else:
            self.copy_button_frame = customtkinter.CTkFrame(master=self.landing_tabview.tab('Vault'),
                                                            fg_color="transparent")
            self.create_or_launch_button = customtkinter.CTkButton(master=self.copy_button_frame, text='',
                                                                   image=LAUNCH_IMAGE, fg_color=GREEN,
                                                                   command=self.launch_event, width=self.button_width,
                                                                   height=self.button_height)

        self.add_button = customtkinter.CTkButton(master=self.copy_button_frame, text='', image=ADD_IMAGE,
                                                  fg_color=GREEN, command=self.create_add_frame,
                                                  width=self.button_width, height=self.button_height)
        self.copy_button = customtkinter.CTkButton(master=self.copy_button_frame, text='', image=COPY_IMAGE,
                                                   fg_color=GREEN, command=self.copy_main_textbox,
                                                   width=self.button_width, height=self.button_height)
        # Add / Copy Placement
        self.copy_button_frame.place(relx=0.96, rely=0.01, anchor=tkinter.N)
        self.copy_button_frame.grid_columnconfigure(0, weight=1)
        self.copy_button_frame.grid_rowconfigure(3, weight=1)
        self.add_button.grid(row=0, column=0, pady=(0, 10), sticky="n")
        self.copy_button.grid(row=1, column=0, pady=(0, 10), sticky="n")
        self.create_or_launch_button.grid(row=2, column=0, sticky="n")

    def copy_main_textbox(self):
        self.parent.main_textbox.clipboard_clear()
        self.parent.main_textbox.clipboard_append(self.parent.main_textbox.get('0.0', 'end').strip())
        self.parent.update_history()

    def create_add_frame(self):
        # Last parameter is blank as we only need it if calling from outside this class
        # such as calling item from within the vault tab by clicking an item name to edit the item
        self.item_menu = ItemMenu(self.landing_tabview, self.parent, self.account_id, '')

    def launch_event(self):
        if self.parent.website != '':
            browser = webbrowser.get()
            website = f"https://{self.parent.website}"
            browser.open_new_tab(website)
