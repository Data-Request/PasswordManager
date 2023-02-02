import tkinter
import customtkinter
from settings import TEXTBOX_FONT
from password_strength import PasswordStrength
from colors import *


class PasswordCheckerTab:
    def __init__(self, landing_tabview, width):
        super().__init__()

        # General Setup
        self.landing_tabview = landing_tabview
        self.name = 'PasswordChecker'
        self.main_textbox_width = width - 90
        self.main_textbox_height = 107
        self.entry_width = 45
        self.valid_symbols = "!@#$%^&*"

        # Initialize all frames
        self.create_main_frame()
        self.create_additions_frame()
        self.create_subtractions_frame()
        self.password_strength_frame = PasswordStrength(self.landing_tabview, self)

    def create_main_frame(self):
        self.main_frame = customtkinter.CTkFrame(master=self.landing_tabview.tab('Checker'), fg_color='transparent')
        self.main_textbox = customtkinter.CTkTextbox(master=self.main_frame,
                                                     width=self.main_textbox_width, font=TEXTBOX_FONT,
                                                     height=self.main_textbox_height, corner_radius=15)
        self.check_button = customtkinter.CTkButton(master=self.main_frame, text='Check Password',
                                                    command=self.check_password, text_color=BLACK, width=300)
        self.main_frame.place(relx=0.5, rely=0.01, anchor=tkinter.N)
        self.main_textbox.grid(row=0, column=0, pady=(0, 15), sticky="n")
        self.check_button.grid(row=1, column=0, pady=(0, 30), sticky="n")

    def create_additions_frame(self):
        self.additions_frame = customtkinter.CTkFrame(master=self.main_frame, fg_color='transparent')
        self.additions_label = customtkinter.CTkLabel(master=self.additions_frame, text='Additions:')
        self.num_of_char_label = customtkinter.CTkLabel(master=self.additions_frame, text='Characters Used:')
        self.num_of_char_entry = customtkinter.CTkEntry(master=self.additions_frame, width=self.entry_width, state='disabled')
        self.middle_char_label = customtkinter.CTkLabel(master=self.additions_frame, text='Middle Non-Letter:')
        self.middle_char_entry = customtkinter.CTkEntry(master=self.additions_frame, width=self.entry_width, state='disabled')
        self.uppercase_label = customtkinter.CTkLabel(master=self.additions_frame, text='Uppercase Letters:')
        self.uppercase_entry = customtkinter.CTkEntry(master=self.additions_frame, width=self.entry_width, state='disabled')
        self.lowercase_label = customtkinter.CTkLabel(master=self.additions_frame, text='Lowercase Letters:')
        self.lowcercase_entry = customtkinter.CTkEntry(master=self.additions_frame, width=self.entry_width, state='disabled')
        self.numbers_label = customtkinter.CTkLabel(master=self.additions_frame, text='Numbers:')
        self.numbers_entry = customtkinter.CTkEntry(master=self.additions_frame, width=self.entry_width, state='disabled')
        self.symbols_label = customtkinter.CTkLabel(master=self.additions_frame, text='Symbols:')
        self.symbols_entry = customtkinter.CTkEntry(master=self.additions_frame, width=self.entry_width, state='disabled')
        self.requirements_label = customtkinter.CTkLabel(master=self.additions_frame, text='Requirements:')
        self.requirements_entry = customtkinter.CTkEntry(master=self.additions_frame, width=self.entry_width, state='disabled')
        self.additions_frame.grid(row=2, column=0, sticky="n")
        self.additions_frame.grid_columnconfigure(4, weight=1)
        self.additions_frame.grid_rowconfigure(5, weight=1)
        self.additions_label.grid(row=0, column=0, sticky="w")
        self.num_of_char_label.grid(row=1, column=0, padx=(0, 10), sticky="w")
        self.num_of_char_entry.grid(row=1, column=1, padx=(0, 10), sticky="w")
        self.middle_char_label.grid(row=1, column=2, padx=(0, 10), sticky="w")
        self.middle_char_entry.grid(row=1, column=3, sticky="w")
        self.uppercase_label.grid(row=2, column=0, padx=(0, 10), sticky="w")
        self.uppercase_entry.grid(row=2, column=1, sticky="w")
        self.lowercase_label.grid(row=2, column=2, padx=(0, 10), sticky="w")
        self.lowcercase_entry.grid(row=2, column=3, sticky="w")
        self.numbers_label.grid(row=3, column=0, padx=(0, 10), sticky="w")
        self.numbers_entry.grid(row=3, column=1, sticky="w")
        self.symbols_label.grid(row=3, column=2, padx=(0, 10), sticky="w")
        self.symbols_entry.grid(row=3, column=3, sticky="w")
        self.requirements_label.grid(row=4, column=0, padx=(0, 10), sticky="w")
        self.requirements_entry.grid(row=4, column=1, sticky="w")

    def create_subtractions_frame(self):
        self.subtractions_frame = customtkinter.CTkFrame(master=self.main_frame, fg_color='transparent')
        self.subtractions_label = customtkinter.CTkLabel(master=self.subtractions_frame, text='Subtractions:')
        self.only_letters_label = customtkinter.CTkLabel(master=self.subtractions_frame, text='Letters Only:')
        self.only_letters_entry = customtkinter.CTkEntry(master=self.subtractions_frame, width=self.entry_width, state='disabled')
        self.only_numbers_label = customtkinter.CTkLabel(master=self.subtractions_frame, text='Numbers Only:')
        self.only_numbers_entry = customtkinter.CTkEntry(master=self.subtractions_frame, width=self.entry_width, state='disabled')
        self.consec_uppercase_label = customtkinter.CTkLabel(master=self.subtractions_frame, text='Consec Uppercase:')
        self.consec_uppercase_entry = customtkinter.CTkEntry(master=self.subtractions_frame, width=self.entry_width, state='disabled')
        self.consec_lowercase_label = customtkinter.CTkLabel(master=self.subtractions_frame, text='Consec Lowercase:')
        self.consec_lowercase_entry = customtkinter.CTkEntry(master=self.subtractions_frame, width=self.entry_width, state='disabled')
        self.consec_numbers_label = customtkinter.CTkLabel(master=self.subtractions_frame, text='Consec Numbers:')
        self.consec_numbers_entry = customtkinter.CTkEntry(master=self.subtractions_frame, width=self.entry_width, state='disabled')
        self.sequen_numbers_label = customtkinter.CTkLabel(master=self.subtractions_frame, text='Sequential Numbers:')
        self.sequen_numbers_entry = customtkinter.CTkEntry(master=self.subtractions_frame, width=self.entry_width, state='disabled')
        self.sequen_symbols_label = customtkinter.CTkLabel(master=self.subtractions_frame, text='Sequential Symbols:')
        self.sequen_symbols_entry = customtkinter.CTkEntry(master=self.subtractions_frame, width=self.entry_width, state='disabled')
        self.sequen_letters_label = customtkinter.CTkLabel(master=self.subtractions_frame, text='Sequential Letters:')
        self.sequen_letters_entry = customtkinter.CTkEntry(master=self.subtractions_frame, width=self.entry_width, state='disabled')
        self.repeat_char_label = customtkinter.CTkLabel(master=self.subtractions_frame, text='Repeat Characters:')
        self.repeat_char_entry = customtkinter.CTkEntry(master=self.subtractions_frame, width=self.entry_width, state='disabled')
        self.subtractions_frame.grid(row=3, column=0, pady=(25, 0), sticky="n")
        self.subtractions_frame.grid_columnconfigure(4, weight=1)
        self.subtractions_frame.grid_rowconfigure(5, weight=1)
        self.subtractions_label.grid(row=0, column=0, sticky="w")
        self.only_letters_label.grid(row=1, column=0, padx=(0, 10), sticky="w")
        self.only_letters_entry.grid(row=1, column=1, padx=(0, 10), sticky="w")
        self.only_numbers_label.grid(row=1, column=2, padx=(0, 10), sticky="w")
        self.only_numbers_entry.grid(row=1, column=3, sticky="w")
        self.consec_uppercase_label.grid(row=2, column=0, padx=(0, 10), sticky="w")
        self.consec_uppercase_entry.grid(row=2, column=1, sticky="w")
        self.consec_lowercase_label.grid(row=2, column=2, padx=(0, 10), sticky="w")
        self.consec_lowercase_entry.grid(row=2, column=3, sticky="w")
        self.consec_numbers_label.grid(row=3, column=0, padx=(0, 10), sticky="w")
        self.consec_numbers_entry.grid(row=3, column=1, sticky="w")
        self.sequen_numbers_label.grid(row=3, column=2, padx=(0, 10), sticky="w")
        self.sequen_numbers_entry.grid(row=3, column=3, sticky="w")
        self.sequen_symbols_label.grid(row=4, column=0, padx=(0, 10), sticky="w")
        self.sequen_symbols_entry.grid(row=4, column=1, sticky="w")
        self.sequen_letters_label.grid(row=4, column=2, padx=(0, 10), sticky="w")
        self.sequen_letters_entry.grid(row=4, column=3, sticky="w")
        self.repeat_char_label.grid(row=5, column=0, padx=(0, 10), sticky="w")
        self.repeat_char_entry.grid(row=5, column=1, sticky="w")

    def enable_all_entries(self):
        self.num_of_char_entry.configure(state='normal')
        self.middle_char_entry.configure(state='normal')
        self.uppercase_entry.configure(state='normal')
        self.lowcercase_entry.configure(state='normal')
        self.numbers_entry.configure(state='normal')
        self.symbols_entry.configure(state='normal')
        self.requirements_entry.configure(state='normal')
        self.only_letters_entry.configure(state='normal')
        self.only_numbers_entry.configure(state='normal')
        self.consec_uppercase_entry.configure(state='normal')
        self.consec_lowercase_entry.configure(state='normal')
        self.consec_numbers_entry.configure(state='normal')
        self.sequen_numbers_entry.configure(state='normal')
        self.sequen_symbols_entry.configure(state='normal')
        self.sequen_letters_entry.configure(state='normal')
        self.repeat_char_entry.configure(state='normal')

    def clear_all_entries(self):
        self.num_of_char_entry.delete(0, 'end')
        self.middle_char_entry.delete(0, 'end')
        self.uppercase_entry.delete(0, 'end')
        self.lowcercase_entry.delete(0, 'end')
        self.numbers_entry.delete(0, 'end')
        self.symbols_entry.delete(0, 'end')
        self.requirements_entry.delete(0, 'end')
        self.only_letters_entry.delete(0, 'end')
        self.only_numbers_entry.delete(0, 'end')
        self.consec_uppercase_entry.delete(0, 'end')
        self.consec_lowercase_entry.delete(0, 'end')
        self.consec_numbers_entry.delete(0, 'end')
        self.sequen_numbers_entry.delete(0, 'end')
        self.sequen_symbols_entry.delete(0, 'end')
        self.sequen_letters_entry.delete(0, 'end')
        self.repeat_char_entry.delete(0, 'end')

    def disable_all_entries(self):
        self.num_of_char_entry.configure(state='disabled')
        self.middle_char_entry.configure(state='disabled')
        self.uppercase_entry.configure(state='disabled')
        self.lowcercase_entry.configure(state='disabled')
        self.numbers_entry.configure(state='disabled')
        self.symbols_entry.configure(state='disabled')
        self.requirements_entry.configure(state='disabled')
        self.only_letters_entry.configure(state='disabled')
        self.only_numbers_entry.configure(state='disabled')
        self.consec_uppercase_entry.configure(state='disabled')
        self.consec_lowercase_entry.configure(state='disabled')
        self.consec_numbers_entry.configure(state='disabled')
        self.sequen_numbers_entry.configure(state='disabled')
        self.sequen_symbols_entry.configure(state='disabled')
        self.sequen_letters_entry.configure(state='disabled')
        self.repeat_char_entry.configure(state='disabled')

    def update_all_fields(self):
        self.all_score = self.password_strength_frame.return_all_scores()
        self.enable_all_entries()
        self.clear_all_entries()

        self.num_of_char_entry.insert(0, self.all_score['num_of_char_score'])
        if self.all_score['num_of_char_score'] > 0:
            self.num_of_char_entry.configure(fg_color=GREEN, text_color=BLACK)
        self.middle_char_entry.insert(0, self.all_score['num_or_symbol_used_in_middle'])
        if self.all_score['num_or_symbol_used_in_middle'] > 0:
            self.middle_char_entry.configure(fg_color=GREEN, text_color=BLACK)
        self.uppercase_entry.insert(0, self.all_score['num_of_uppercase_chars'])
        if self.all_score['num_of_uppercase_chars'] > 0:
            self.uppercase_entry.configure(fg_color=GREEN, text_color=BLACK)
        self.lowcercase_entry.insert(0, self.all_score['num_of_lowercase_chars'])
        if self.all_score['num_of_lowercase_chars'] > 0:
            self.lowcercase_entry.configure(fg_color=GREEN, text_color=BLACK)
        self.numbers_entry.insert(0, self.all_score['num_of_num_chars'])
        if self.all_score['num_of_num_chars'] > 0:
            self.numbers_entry.configure(fg_color=GREEN, text_color=BLACK)
        self.symbols_entry.insert(0, self.all_score['num_of_symbol_chars'])
        if self.all_score['num_of_symbol_chars'] > 0:
            self.symbols_entry.configure(fg_color=GREEN, text_color=BLACK)
        self.requirements_entry.insert(0, self.all_score['requirements_score'])
        if self.all_score['requirements_score'] > 0:
            self.requirements_entry.configure(fg_color=GREEN, text_color=BLACK)

        self.only_letters_entry.insert(0, self.all_score['only_letter_score'])
        if self.all_score['only_letter_score'] < 0:
            self.only_letters_entry.configure(fg_color=RED, text_color=BLACK)
        self.only_numbers_entry.insert(0, self.all_score['only_numbers_score'])
        if self.all_score['only_numbers_score'] < 0:
            self.only_numbers_entry.configure(fg_color=RED, text_color=BLACK)
        self.consec_uppercase_entry.insert(0, self.all_score['consec_uppercase_score'])
        if self.all_score['consec_uppercase_score'] < 0:
            self.consec_uppercase_entry.configure(fg_color=RED, text_color=BLACK)
        self.consec_lowercase_entry.insert(0, self.all_score['consec_lowercase_score'])
        if self.all_score['consec_lowercase_score'] < 0:
            self.consec_lowercase_entry.configure(fg_color=RED, text_color=BLACK)
        self.consec_numbers_entry.insert(0, self.all_score['consec_number_score'])
        if self.all_score['consec_number_score'] < 0:
            self.consec_numbers_entry.configure(fg_color=RED, text_color=BLACK)
        self.sequen_numbers_entry.insert(0, self.all_score['sequen_number_score'])
        if self.all_score['sequen_number_score'] < 0:
            self.sequen_numbers_entry.configure(fg_color=RED, text_color=BLACK)
        self.sequen_symbols_entry.insert(0, self.all_score['sequen_symbols_score'])
        if self.all_score['sequen_symbols_score'] < 0:
            self.sequen_symbols_entry.configure(fg_color=RED, text_color=BLACK)
        self.sequen_letters_entry.insert(0, self.all_score['sequen_letter_score'])
        if self.all_score['sequen_letter_score'] < 0:
            self.sequen_letters_entry.configure(fg_color=RED, text_color=BLACK)
        self.repeat_char_entry.insert(0, self.all_score['repeat_char_score'])
        if self.all_score['repeat_char_score'] < 0:
            self.repeat_char_entry.configure(fg_color=RED, text_color=BLACK)

        self.disable_all_entries()

    def refresh_addition_subtraction_frames(self):
        # Refresh fields by destroy/creating
        self.additions_frame.destroy()
        self.subtractions_frame.destroy()
        self.create_additions_frame()
        self.create_subtractions_frame()

    def check_password(self):
        password = self.main_textbox.get('0.0', 'end').strip()
        password_length = len(password)
        self.password_strength_frame.reset_scoring_variables()
        for index, char in enumerate(password):
            self.password_strength_frame.update_basic_scoring_variables(index, char, self.valid_symbols, password_length)
        self.password_strength_frame.update_advanced_scoring_variables(self.valid_symbols, password)
        self.password_strength_frame.calc_password_strength_score(password_length)
        self.refresh_addition_subtraction_frames()
        self.update_all_fields()
