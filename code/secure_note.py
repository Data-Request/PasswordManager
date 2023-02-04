import tkinter
import customtkinter
from colors import *
from sql import *
from support import get_encrypted_text, get_decrypted_note_and_name

# todo add warning label for empty field
# todo add limit to length on note names


class SecureNote:
    def __init__(self, parent_frame, parent, account_id, note_id):
        super().__init__()

        # General Setup
        self.account_id = account_id
        self.parent_frame = parent_frame
        self.parent = parent
        self.note_id = note_id
        self.textbox_width = 300
        self.note_textbox_height = 250

        # Initialize
        self.create_secure_note_frame()

    def create_secure_note_frame(self):
        # Create and place Secure Note Frame, change configs based on if we are creating or editing a note
        self.secure_note_frame = customtkinter.CTkFrame(master=self.parent_frame, fg_color="transparent")
        self.title_label = customtkinter.CTkLabel(master=self.secure_note_frame, text="")
        self.name_label = customtkinter.CTkLabel(master=self.secure_note_frame, text="Name:")
        self.name_entry = customtkinter.CTkEntry(master=self.secure_note_frame, width=self.textbox_width,
                                                 placeholder_text='Name')
        self.note_label = customtkinter.CTkLabel(master=self.secure_note_frame, text="Secure Note:")
        self.note_textbox = customtkinter.CTkTextbox(master=self.secure_note_frame,
                                                     width=self.textbox_width, font=('Arial', 14),
                                                     height=self.note_textbox_height)
        self.cancel_save_button = customtkinter.CTkSegmentedButton(master=self.secure_note_frame, text_color=BLACK,
                                                                   width=300, unselected_color=GREEN,
                                                                   unselected_hover_color=DARK_GREEN,
                                                                   command=self.cancel_save_delete_event)
        self.secure_note_frame.grid(row=3, column=0, sticky="n")
        self.secure_note_frame.grid_columnconfigure(1, weight=1)
        self.secure_note_frame.grid_rowconfigure(6, weight=1)
        self.name_entry.grid(row=2, column=0, pady=(0, 20), sticky="n")
        self.note_textbox.grid(row=4, column=0, pady=(0, 25), sticky="n")

        if self.note_id:    # Editing a note, so we need to reshape the frame to fill the screen
            self.secure_note_frame.configure(border_width=3, border_color=WHITE, corner_radius=15)
            self.title_label.grid(row=0, column=0, pady=(15, 5), padx=155, sticky="N")
            self.title_label.configure(text='Edit Secure Note')
            self.name_label.grid(row=1, column=0, pady=(15, 5), padx=(55, 0), sticky="w")
            self.note_label.grid(row=3, column=0, padx=(55, 0), sticky="w")
            self.note_textbox.configure(height=self.note_textbox_height + 80)
            self.cancel_save_button.configure(values=['Cancel', 'Save', 'Delete'])
            self.cancel_save_button.grid(row=5, column=0, pady=(0, 30), sticky="n")
            # Get note from db then decrypt and display
            note_row = get_single_secure_note(self.note_id)
            master_key = get_master_key_with_account_id(self.account_id)[0]
            decrypted_note_name, decrypted_note = get_decrypted_note_and_name(master_key, note_row[0][2], note_row[0][3])
            self.name_entry.insert(0, decrypted_note_name)
            self.note_textbox.insert('end', decrypted_note)
        else:      # We are adding an item so we set default placements
            self.name_label.grid(row=1, column=0, pady=(15, 5), sticky="w")
            self.note_label.grid(row=3, column=0, sticky="w")
            self.cancel_save_button.configure(values=['Cancel', 'Save'])
            self.cancel_save_button.grid(row=5, column=0, sticky="n")

    def destroy_secure_note_frame(self):
        # This is called from parent to kill child
        self.secure_note_frame.destroy()

    def cancel_save_delete_event(self, *args):
        # Handles the segmented button event, they always send a value with command
        if args[0] == 'Save':
            if not self.note_id:
                self.save_note()
                self.parent.main_frame.destroy()
                self.parent.parent.update_secure_note_frame()
            else:
                self.edit_note()
                self.destroy_secure_note_frame()
                self.parent.update_secure_note_frame()
        elif args[0] == 'Cancel':
            if self.note_id:
                self.destroy_secure_note_frame()
            else:
                self.parent.main_frame.destroy()
        else:
            self.create_delete_note_frame()

    def save_note(self):
        # Grabs note and encrypts then stores in db
        note_name_input = self.name_entry.get().strip()
        note_body_input = self.note_textbox.get('0.0', 'end').strip()
        master_key = get_master_key_with_account_id(self.account_id)[0]
        encrypted_note_name, encrypted_note = get_encrypted_text(master_key, note_name_input, note_body_input)
        create_new_secure_note(self.account_id, encrypted_note_name, encrypted_note)

    def edit_note(self):
        # Grab note inputs and the master_key from db, then encrypt both and update note in db
        note_name_input = self.name_entry.get().strip()
        note_Body_input = self.note_textbox.get('0.0', 'end').strip()
        master_key = get_master_key_with_account_id(self.account_id)[0]
        encrypted_note_name, encrypted_note = get_encrypted_text(master_key, note_name_input, note_Body_input)
        update_secure_note(encrypted_note_name, encrypted_note, self.note_id)

    def create_delete_note_frame(self):
        # Create and place delete note frame
        self.delete_note_frame = customtkinter.CTkFrame(master=self.secure_note_frame, fg_color=GREEN)
        delete_label = customtkinter.CTkLabel(master=self.delete_note_frame, text_color=BLACK,
                                              text='Confirm Deletion of Secure Note:',
                                              font=('Arial', 18))
        delete_button = customtkinter.CTkSegmentedButton(master=self.delete_note_frame, values=['Yes', 'No'],
                                                         command=self.delete_event)
        self.delete_note_frame.place(relx=0.5, rely=0.5, anchor=tkinter.N)
        self.delete_note_frame.grid_columnconfigure(1, weight=1)
        self.delete_note_frame.grid_rowconfigure(2, weight=1)
        delete_label.grid(row=0, column=0, padx=50, pady=(20, 20), sticky="n")
        delete_button.grid(row=1, column=0, pady=(0, 20), sticky="n")

    def delete_event(self, *args):
        # Handles the segmented button event, they always send a value with command
        # Deletes the secure note from database, and resets screen
        if args[0] == 'Yes':
            delete_secure_note(self.note_id)
        self.destroy_secure_note_frame()
        self.parent.update_secure_note_frame()

