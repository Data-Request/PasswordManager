import customtkinter
from colors import *


class NewFolder:
    def __init__(self, parent_frame):
        super().__init__()

        # General Setup
        self.parent_frame = parent_frame
        self.button_width = 25
        self.button_height = 25
        self.textbox_width = 300
        self.textbox_height = 10
        self.note_textbox_width = 300
        self.note_textbox_height = 250

        # Initialize
        self.create_new_folder_frame()

    def create_new_folder_frame(self):
        # Create Secure Note Frame
        self.new_folder_frame = customtkinter.CTkFrame(master=self.parent_frame, fg_color="transparent")
        self.name_label = customtkinter.CTkLabel(master=self.new_folder_frame, text="Name:")
        self.name_textbox = customtkinter.CTkTextbox(master=self.new_folder_frame,
                                                          width=self.textbox_width, font=('Arial', 16),
                                                          height=self.textbox_height, corner_radius=15)
        self.save_button = customtkinter.CTkButton(master=self.new_folder_frame, text_color=BLACK, width=300,
                                               text='Save', command=self.save_note)
        # Secure Note Frame Placement
        self.new_folder_frame.grid(row=3, column=0, sticky="n")
        self.new_folder_frame.grid_columnconfigure(1, weight=1)
        self.new_folder_frame.grid_rowconfigure(3, weight=1)
        self.name_label.grid(row=0, column=0, pady=(15, 5), sticky="w")
        self.name_textbox.grid(row=1, column=0, pady=(0, 20), sticky="w")
        self.save_button.grid(row=2, column=0, sticky="n")

    def destroy_new_folder_frame(self):
        # This is called from parent to kill child
        self.new_folder_frame.destroy()

    def save_note(self):
        print('Save HERE???')
        self.destroy_new_folder_frame()
        self.create_new_folder_frame()





