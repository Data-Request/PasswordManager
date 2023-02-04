import customtkinter
from colors import *
from sql import get_folder_list, update_folder_list


class NewFolder:
    def __init__(self, parent, parent_frame, account_id):
        super().__init__()

        # General Setup
        self.parent = parent
        self.parent_frame = parent_frame
        self.account_id = account_id
        self.entry_width = 300

        # Initialize
        self.create_warning_label_frame()
        self.create_new_folder_frame()

    def create_warning_label_frame(self):
        # Create and place warning label frame
        self.warning_label_frame = customtkinter.CTkFrame(master=self.parent_frame, fg_color="transparent")
        self.warning_label = customtkinter.CTkLabel(master=self.warning_label_frame, text_color=RED, text='')
        self.warning_label_frame.grid(row=3, column=0, sticky="n")
        self.warning_label_frame.grid_columnconfigure(1, weight=1)
        self.warning_label_frame.grid_rowconfigure(1, weight=1)
        self.warning_label.grid(row=0, column=0, pady=(0, 0), sticky="n")

    def create_new_folder_frame(self):
        # Create and place new folder frame
        self.new_folder_frame = customtkinter.CTkFrame(master=self.parent_frame, fg_color="transparent")
        self.name_label = customtkinter.CTkLabel(master=self.new_folder_frame, text="Name:")
        self.name_entry = customtkinter.CTkEntry(master=self.new_folder_frame, width=self.entry_width)
        self.cancel_save_button = customtkinter.CTkSegmentedButton(master=self.new_folder_frame, text_color=BLACK,
                                                                   width=300, unselected_color=GREEN,
                                                                   unselected_hover_color=DARK_GREEN,
                                                                   values=['Cancel', 'Save'],
                                                                   command=self.cancel_save_delete_event)
        self.new_folder_frame.grid(row=4, column=0, sticky="n")
        self.new_folder_frame.grid_columnconfigure(1, weight=1)
        self.new_folder_frame.grid_rowconfigure(3, weight=1)
        self.name_label.grid(row=0, column=0, pady=(0, 5), sticky="w")
        self.name_entry.grid(row=1, column=0, pady=(0, 20), sticky="w")
        self.cancel_save_button.grid(row=2, column=0, sticky="n")

    def destroy_new_folder_frame(self):
        # This is called from parent to kill child
        self.new_folder_frame.destroy()

    def cancel_save_delete_event(self, *args):
        # Handles the segmented button event, they always send a value with command
        if args[0] == 'Save':
            self.save_folder()
        else:
            self.parent.main_frame.destroy()

    def check_for_valid_entry(self, new_folder_name, folder_list):
        if new_folder_name == '':
            self.warning_label.configure(text='Folder name is blank.')
            # Updates the save/cancel button by refreshing the frame
            self.new_folder_frame.destroy()
            self.create_new_folder_frame()
            return False
        elif new_folder_name in folder_list:
            self.warning_label.configure(text='Folder already exists.')
            # Updates the save/cancel button by refreshing the frame
            self.new_folder_frame.destroy()
            self.create_new_folder_frame()
            self.name_entry.insert(0, new_folder_name)
            return False
        else:
            return True

    def save_folder(self):
        new_folder_name = self.name_entry.get().strip()
        folder_list = get_folder_list(self.account_id)
        folder_string = ''

        # Create new folder_string and update in db
        if self.check_for_valid_entry(new_folder_name, folder_list):
            folder_list.append(new_folder_name)
            folder_list.sort()
            for index, word in enumerate(folder_list):
                if index == 0:
                    folder_string += f'{word}'
                else:
                    folder_string += f',{word}'
            update_folder_list(folder_string, self.account_id)

            # Reset and refresh all frames
            self.new_folder_frame.destroy()
            self.create_new_folder_frame()
            self.parent.main_frame.destroy()
            self.parent.parent.update_folder_frame()
