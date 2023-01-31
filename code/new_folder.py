import customtkinter
from colors import *
from sql import get_folder_list, update_folder_list

# todo add warning label so we can tell them the file name is blank.


class NewFolder:
    def __init__(self, parent, parent_frame, account_id):
        super().__init__()

        # General Setup
        self.parent = parent
        self.parent_frame = parent_frame
        self.account_id = account_id
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
        self.cancel_save_button = customtkinter.CTkSegmentedButton(master=self.new_folder_frame, text_color=BLACK,
                                                                   width=300, unselected_color=GREEN,
                                                                   unselected_hover_color=DARK_GREEN,
                                                                   command=self.cancel_save_delete_event)
        # Secure Note Frame Placement
        self.new_folder_frame.grid(row=3, column=0, sticky="n")
        self.new_folder_frame.grid_columnconfigure(1, weight=1)
        self.new_folder_frame.grid_rowconfigure(3, weight=1)
        self.name_label.grid(row=0, column=0, pady=(15, 5), sticky="w")
        self.name_textbox.grid(row=1, column=0, pady=(0, 20), sticky="w")
        self.cancel_save_button.configure(values=['Cancel', 'Save'])
        self.cancel_save_button.grid(row=2, column=0, sticky="n")

    def destroy_new_folder_frame(self):
        # This is called from parent to kill child
        self.new_folder_frame.destroy()

    def cancel_save_delete_event(self, *args):
        # Handles the segmented button event, they always send a value with command
        if args[0] == 'Save':
            self.save_note()

        self.parent.main_frame.destroy()

    def save_note(self):
        new_folder = self.name_textbox.get('0.0', 'end').strip()
        folder_list = get_folder_list(self.account_id)
        folder_string = ''

        if new_folder == '':
            print('empty folder name')
            return
        if new_folder in folder_list:
            print('Already a folder')
        else:
            folder_list.append(new_folder)
            folder_list.sort()
            for index, word in enumerate(folder_list):
                if index == 0:
                    folder_string += f'{word}'
                else:
                    folder_string += f',{word}'

            update_folder_list(folder_string, self.account_id)
            self.destroy_new_folder_frame()
            self.create_new_folder_frame()





