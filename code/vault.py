import tkinter
import customtkinter
import string
from colors import *
from PIL import Image
from right_button_sidebar import RightButtonSidebar
import functools
from item_menu import ItemMenu
from sql import *
from secure_note import SecureNote
from settings import TEXTBOX_FONT


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
        self.website = ''   # Child uses to launch website
        # Images
        self.folder_image = customtkinter.CTkImage(Image.open(r"C:\Users\xjord\Desktop\PasswordManager\images\folder-open-solid.png"), size=(20, 20))
        self.menu_image = customtkinter.CTkImage(Image.open(r"C:\Users\xjord\Desktop\PasswordManager\images\menu.png"), size=(20, 20))
        self.user_image = customtkinter.CTkImage(Image.open(r"C:\Users\xjord\Desktop\PasswordManager\images\user.png"), size=(20, 20))
        self.key_image = customtkinter.CTkImage(Image.open(r"C:\Users\xjord\Desktop\PasswordManager\images\key-solid.png"), size=(20, 20))
        self.note_image = customtkinter.CTkImage(Image.open(r"C:\Users\xjord\Desktop\PasswordManager\images\note.png"), size=(20, 20))

        # Create and Place Bottom Label Frame
        self.bottom_label_frame = customtkinter.CTkFrame(master=self.landing_tabview.tab('Vault'), fg_color="transparent")
        self.bottom_label = customtkinter.CTkLabel(master=self.bottom_label_frame,
                                                   text=f'Number of Logins: {get_num_of_login(self.account_id)}')
        self.bottom_label_frame.grid_columnconfigure(1, weight=1)
        self.bottom_label_frame.grid_rowconfigure(1, weight=1)
        self.bottom_label_frame.place(relx=0.5, rely=1, anchor=tkinter.S)
        self.bottom_label.grid(row=0, column=0, pady=(0, 10), sticky="n")

        # Create Password Textbox
        self.main_textbox = customtkinter.CTkTextbox(master=self.landing_tabview.tab('Vault'), state='disabled',
                                                     width=self.main_textbox_width, font=TEXTBOX_FONT,
                                                     height=self.main_textbox_height, corner_radius=15)
        self.main_textbox.place(relx=0.45, rely=0.01, anchor=tkinter.N)

        # Create Add / Copy / Launch
        self.right_side_button_bar = RightButtonSidebar(self.landing_tabview, self, self.account_id)

        # Initialize
        self.create_vault_tabview()
        self.create_folder_frame()
        self.create_secure_notes_frame()

    def create_vault_tabview(self):
        self.password_tabview = customtkinter.CTkTabview(master=self.landing_tabview.tab('Vault'),
                                                         width=self.vault_tabview_width,
                                                         height=self.vault_tabview_height,
                                                         segmented_button_selected_color=GREEN, corner_radius=15,
                                                         border_width=3, border_color=WHITE,
                                                         command=self.password_tabview_event)
        self.password_tabview.place(relx=0.5, rely=0.2, anchor=tkinter.N)
        self.password_tabview.add('Login')
        self.password_tabview.add('Secure Notes')

    def password_tabview_event(self):
        # When a tabview button is clicked it with refresh the tab by calling an update
        if self.password_tabview.get() == 'Secure Notes':
            notes = get_all_from_secure_notes(self.account_id)
            self.bottom_label.configure(text=f'Number of Secure Notes: {len(notes)}')
            self.update_secure_note_frame()
        else:
            self.bottom_label.configure(text=f'Number of Logins: {get_num_of_login(self.account_id)}')
            self.update_folder_item_frame()

    def create_folder_frame(self):
        folder_container = tkinter.Frame(self.password_tabview.tab('Login'), bg=MID_DARK_GRAY2)
        folder_canvas = tkinter.Canvas(folder_container, bg=MID_DARK_GRAY2, highlightbackground=MID_DARK_GRAY2, height=320, width=355)
        folder_scrollbar = customtkinter.CTkScrollbar(folder_container, command=folder_canvas.yview)
        self.folder_scrollable_frame = tkinter.Frame(folder_canvas, bg=MID_DARK_GRAY2)
        self.folder_scrollable_frame.bind("<Configure>", lambda e: folder_canvas.configure(scrollregion=folder_canvas.bbox("all")))
        folder_canvas.create_window((0, 0), window=self.folder_scrollable_frame, anchor="nw")
        folder_canvas.configure(yscrollcommand=folder_scrollbar.set)

        # Create folder Menu and place everything
        folder_list = get_folder_list(self.account_id)
        self.folder_menu = customtkinter.CTkOptionMenu(master=folder_container, values=folder_list, text_color=BLACK,
                                                       width=360, fg_color=DARK_GREEN, dropdown_text_color=BLACK,
                                                       dropdown_fg_color=GREEN, command=self.update_folder_item_frame)
        self.folder_menu.pack(pady=(10, 0))
        folder_container.pack()
        folder_canvas.pack(side="left", fill="both", expand=True, pady=(20, 0))
        folder_scrollbar.pack(side="right", fill="y", pady=(25, 0))

        # Create a row frame and each item row
        self.create_folder_row_frame()
        self.create_folder_rows()

    def update_folder_item_frame(self, *args):
        # Refreshes page by destroying and creating a new row_frame
        self.row_frame.destroy()
        self.create_folder_row_frame()
        self.create_folder_rows()

    def create_folder_row_frame(self):
        # This frame is used to hold each item_row, it is destroyed and created to refresh the page
        self.row_frame = customtkinter.CTkFrame(master=self.folder_scrollable_frame, fg_color="transparent")
        self.row_frame.pack()

    def create_folder_rows(self):
        current_folder = self.folder_menu.get()
        folder_row = get_each_login_within_folder(self.account_id, current_folder)

        for index in range(len(folder_row)):
            item_row = customtkinter.CTkFrame(master=self.row_frame, fg_color="transparent")
            item_name_button = customtkinter.CTkButton(master=item_row, text=folder_row[index][2],
                                                       image=self.menu_image, compound='left', bg_color='transparent',
                                                       text_color=BLACK, anchor='w', width=270,
                                                       command=functools.partial(self.edit_item, folder_row[index][0]))
            password_button = customtkinter.CTkButton(master=item_row, text='', image=self.key_image, compound='left',
                                                      bg_color='transparent', text_color=BLACK, anchor='w', width=25,
                                                      command=functools.partial(self.update_main_textbox, (folder_row[index][4]), folder_row[index][5]))
            user_button = customtkinter.CTkButton(master=item_row, text='', image=self.user_image, compound='left',
                                                  bg_color='transparent', text_color=BLACK, anchor='w', width=25,
                                                  command=functools.partial(self.update_main_textbox, (folder_row[index][3]), folder_row[index][5]))
            item_name_button.pack(side='left', pady=(10, 0))
            password_button.pack(side='right', pady=(10, 0))
            user_button.pack(side='right', pady=(10, 0))
            item_row.pack()

    def edit_item(self, item_id):
        ItemMenu(self.landing_tabview, self, self.account_id, item_id)

    def update_main_textbox(self, text, website):
        self.website = website
        self.main_textbox.configure(state='normal')
        self.main_textbox.delete('1.0', 'end')
        self.main_textbox.tag_config('letter', foreground=WHITE)
        self.main_textbox.tag_config('digit', foreground=GREEN)
        self.main_textbox.tag_config('symbol', foreground=BLUE)
        for char in text:
            if char in string.ascii_letters:
                self.main_textbox.insert('end', char, 'letter')
            elif char in string.digits:
                self.main_textbox.insert('end', char, 'digit')
            else:
                self.main_textbox.insert('end', char, 'symbol')
        self.main_textbox.configure(state='disabled')

    def create_secure_notes_frame(self):
        note_container = tkinter.Frame(self.password_tabview.tab('Secure Notes'), bg=MID_DARK_GRAY2)
        note_canvas = tkinter.Canvas(note_container, bg=MID_DARK_GRAY2, highlightbackground=MID_DARK_GRAY2, height=380, width=355)
        note_scrollbar = customtkinter.CTkScrollbar(note_container, command=note_canvas.yview)
        self.note_scrollable_frame = tkinter.Frame(note_canvas, bg=MID_DARK_GRAY2)
        self.note_scrollable_frame.bind("<Configure>", lambda e: note_canvas.configure(scrollregion=note_canvas.bbox("all")))
        note_canvas.create_window((0, 0), window=self.note_scrollable_frame, anchor="nw")
        note_canvas.configure(yscrollcommand=note_scrollbar.set)
        note_container.pack()
        note_canvas.pack(side="left", fill="both", expand=True)
        note_scrollbar.pack(side="right", fill="y")

        # Create a row frame and each item row
        self.create_secure_notes_row_frame()
        self.create_secure_notes_row()

    def update_secure_note_frame(self, *args):
        # Refreshes page by destroying and creating a new row_frame
        self.secure_notes_row_frame.destroy()
        self.create_secure_notes_row_frame()
        self.create_secure_notes_row()

    def create_secure_notes_row_frame(self):
        # This frame is used to hold each item_row, it is destroyed and created to refresh the page
        self.secure_notes_row_frame = customtkinter.CTkFrame(master=self.note_scrollable_frame, fg_color="transparent")
        self.secure_notes_row_frame.pack()

    def create_secure_notes_row(self):
        notes = get_all_from_secure_notes(self.account_id)
        for index in range(len(notes)):
            item_row = customtkinter.CTkFrame(master=self.secure_notes_row_frame, fg_color="transparent")
            note_button = customtkinter.CTkButton(master=item_row, text=notes[index][2],
                                                  image=self.note_image, compound='left',  bg_color='transparent',
                                                  text_color=BLACK, anchor='w', width=350, corner_radius=15,
                                                  command=functools.partial(self.edit_note, (notes[index][0])))
            note_button.pack(pady=(20, 0))
            item_row.pack()

    def edit_note(self, note_id):
        SecureNote(self.landing_tabview.tab('Vault'), self, self.account_id, note_id)



