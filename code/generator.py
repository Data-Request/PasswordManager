import tkinter
import customtkinter
import secrets
import string
from colors import *
from right_button_sidebar import RightButtonSidebar
from sql import *
from support import create_username, encrypt_text, decrypt_text
from settings import TEXTBOX_FONT
from password_strength import PasswordStrength

# todo password generate per requirements - min numbers and min specials
# todo remove password strength is on passphrase or username tabs
# todo change numbers shown next to sliders to be entries


class GeneratorTab:
    def __init__(self, landing_tabview, width, height, account_id):
        super().__init__()

        # General Setup
        self.account_id = account_id
        self.landing_tabview = landing_tabview
        self.name = 'Generator'
        self.password_tabview_width = width - 72
        self.password_tabview_height = height - 300
        self.button_width = 25
        self.button_height = 25
        self.main_textbox_width = width - 115
        self.main_textbox_height = 107

        # Password Variables
        self.min_password_length = 8
        self.max_password_length = 128
        self.password_length = 32
        self.valid_symbols = "!@#$%^&*"
        self.default_min_number = 1
        self.default_min_symbol = 1
        self.min_min_num = 0
        self.max_min_num = self.password_length // 10
        self.min_symbols_num = 0
        self.max_symbols_num = self.password_length // 10

        # Passphrase
        self.min_words = 3
        self.max_words = 20
        self.default_word_separator = '-'

        # Initialize all frames
        self.main_textbox = customtkinter.CTkTextbox(master=self.landing_tabview.tab('Generator'), state='disabled',
                                                     width=self.main_textbox_width, font=TEXTBOX_FONT,
                                                     height=self.main_textbox_height, corner_radius=15)
        self.main_textbox.place(relx=0.45, rely=0.01, anchor=tkinter.N)
        self.right_side_button_bar = RightButtonSidebar(self.landing_tabview, self, self.account_id)
        self.create_generator_tabview()
        # Password strength needs created before password_frame as it updates based on each password created
        self.password_strength_frame = PasswordStrength(self.landing_tabview, self)
        self.create_password_frame()
        self.create_passphrase_frame()
        self.create_username_frame()

    def create_generator_tabview(self):
        self.generator_tabview = customtkinter.CTkTabview(master=self.landing_tabview.tab('Generator'),
                                                          width=self.password_tabview_width,
                                                          height=self.password_tabview_height,
                                                          segmented_button_selected_color=GREEN, corner_radius=15,
                                                          border_width=3, border_color=WHITE,
                                                          command=self.generator_tabview_event)
        self.generator_tabview.place(relx=0.5, rely=0.2, anchor=tkinter.N)
        self.generator_tabview.add('Password')
        self.generator_tabview.add('Passphrase')
        self.generator_tabview.add("Username")

    def create_password_frame(self):
        # Create Length Slider and Ambiguous Checkbox Frame
        self.length_slider_frame = customtkinter.CTkFrame(master=self.generator_tabview.tab('Password'),
                                                          fg_color='transparent')
        self.length_label = customtkinter.CTkLabel(master=self.length_slider_frame)
        self.length_slider = customtkinter.CTkSlider(master=self.length_slider_frame,
                                                     command=self.update_length,
                                                     from_=self.min_password_length, to=self.max_password_length,
                                                     number_of_steps=self.max_password_length - self.min_password_length)
        # Removes l (ell), 1 (one), I (capital i), o O (oh), and 0 (zero)
        self.ambiguous_checkbox = customtkinter.CTkCheckBox(master=self.length_slider_frame,
                                                            text="Avoid Ambiguous Characters",
                                                            command=self.create_password)
        # Length Slider and Ambiguous Checkbox Placement
        self.length_slider_frame.grid(row=0, column=0, padx=(50, 0), pady=(30, 0), sticky="n")
        self.length_slider_frame.grid_columnconfigure(2, weight=1)
        self.length_slider_frame.grid_rowconfigure(2, weight=1)
        self.length_label.grid(row=0, column=0, padx=(0, 20), sticky="w")
        self.length_slider.grid(row=0, column=1, padx=10, sticky="e")
        self.ambiguous_checkbox.grid(row=1, column=0, padx=(50, 0), pady=(20, 0), columnspan=2, sticky="ew")

        # Create Password Checkbox Frame
        self.checkbox_slider_frame = customtkinter.CTkFrame(master=self.generator_tabview.tab('Password'))
        self.lowercase_checkbox = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text='a-z',
                                                            command=self.check_valid_checkbox)
        self.uppercase_checkbox = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text='A-Z',
                                                            command=self.check_valid_checkbox)
        self.numbers_checkbox = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text='0-9',
                                                          command=self.check_valid_checkbox)
        self.symbols_checkbox = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text='!@#$%^&*',
                                                          command=self.check_valid_checkbox)
        # Password Checkbox Frame Placement
        self.checkbox_slider_frame.grid(row=1, column=0, padx=(50, 0), pady=(20, 0), sticky='n')
        self.lowercase_checkbox.grid(row=0, column=0, padx=(40, 0), pady=10, sticky="w")
        self.uppercase_checkbox.grid(row=0, column=1, padx=(0, 40), pady=10, sticky="e")
        self.numbers_checkbox.grid(row=1, column=0, padx=(40, 10), pady=10, sticky="w")
        self.symbols_checkbox.grid(row=1, column=1, padx=(0, 40), pady=10, sticky="e")

        # Create Extras Slider Frame
        self.extras_slider_frame = customtkinter.CTkFrame(master=self.generator_tabview.tab('Password'),
                                                          fg_color='transparent')
        self.extras_slider_frame.grid(row=2, column=0, padx=(40, 0), pady=(25, 0), sticky="n")
        self.extras_slider_frame.grid_columnconfigure(0, weight=1)
        self.extras_slider_frame.grid_rowconfigure(0, weight=1)
        self.min_numbers_label = customtkinter.CTkLabel(master=self.extras_slider_frame)
        self.min_numbers_label.grid(row=0, column=0, sticky="w")
        self.min_numbers_slider = customtkinter.CTkSlider(master=self.extras_slider_frame, state='disabled',
                                                          command=self.update_min_number,
                                                          from_=self.min_min_num, to=self.max_min_num,
                                                          number_of_steps=self.max_min_num - self.min_min_num)
        self.min_numbers_slider.grid(row=0, column=1, sticky="e")
        self.min_symbol_label = customtkinter.CTkLabel(master=self.extras_slider_frame)
        self.min_symbol_label.grid(row=1, column=0, pady=(15, 0), columnspan=1, sticky="w")
        self.min_symbol_slider = customtkinter.CTkSlider(master=self.extras_slider_frame, state='disabled',
                                                         command=self.update_min_special,
                                                         from_=self.min_symbols_num, to=self.max_symbols_num,
                                                         number_of_steps=self.max_symbols_num - self.min_symbols_num)
        self.min_symbol_slider.grid(row=1, column=1, pady=(15, 0), sticky="e")

        # Set Defaults
        self.lowercase_checkbox.select()
        self.length_slider.set(self.password_length)
        self.create_password()
        self.length_label.configure(text=f'Length: {self.password_length}')
        self.min_numbers_slider.set(self.default_min_number)
        self.min_numbers_label.configure(text=f'Minimum Numbers: {self.default_min_number}')
        self.min_symbol_slider.set(self.default_min_symbol)
        self.min_symbol_label.configure(text=f'Minimum Symbols: {self.default_min_symbol}')

    def create_passphrase_frame(self):
        # Create Passphrase Length Slider Frame
        self.passphrase_length_slider_frame = customtkinter.CTkFrame(master=self.generator_tabview.tab('Passphrase'),
                                                                     fg_color='transparent')
        self.passphrase_length_label = customtkinter.CTkLabel(master=self.passphrase_length_slider_frame, text='Words:')
        self.passphrase_length_slider = customtkinter.CTkSlider(master=self.passphrase_length_slider_frame,
                                                                from_=self.min_words, to=self.max_words,
                                                                command=self.update_words,
                                                                number_of_steps=self.max_words - self.min_words)
        # Passphrase Length Slider Placement
        self.passphrase_length_slider_frame.grid(row=0, column=0, padx=(50, 0), pady=(30, 0), sticky="n")
        self.passphrase_length_slider_frame.grid_columnconfigure(2, weight=1)
        self.passphrase_length_slider_frame.grid_rowconfigure(1, weight=1)
        self.passphrase_length_label.grid(row=0, column=0, padx=(0, 20), sticky="w")
        self.passphrase_length_slider.grid(row=0, column=1, padx=10, sticky="e")

        # Create Word Separator Frame
        self.word_separator_frame = customtkinter.CTkFrame(master=self.generator_tabview.tab('Passphrase'),
                                                           fg_color='transparent')
        self.word_separator_label = customtkinter.CTkLabel(master=self.word_separator_frame, text='Word Separator:')
        self.word_separator_entry = customtkinter.CTkEntry(master=self.word_separator_frame, width=100,)
        # Word Separator Frame Placement
        self.word_separator_frame.grid(row=1, column=0, padx=(50, 0), pady=(30, 0), sticky="n")
        self.word_separator_frame.grid_columnconfigure(2, weight=1)
        self.word_separator_frame.grid_rowconfigure(1, weight=1)
        self.word_separator_label.grid(row=0, column=0, padx=(0, 20), sticky="w")
        self.word_separator_entry.grid(row=0, column=1, padx=(0, 20), sticky="e")

        # Create Capitalize - Number Checkbox Frame
        self.capitalize_checkbox_frame = customtkinter.CTkFrame(master=self.generator_tabview.tab('Passphrase'))
        self.capitalize_checkbox = customtkinter.CTkCheckBox(master=self.capitalize_checkbox_frame, text='Capitalize',
                                                             command=self.create_passphrase)
        self.use_number_checkbox = customtkinter.CTkCheckBox(master=self.capitalize_checkbox_frame,
                                                             text='Include number',
                                                             command=self.create_passphrase)
        # Password Checkbox Frame Placement
        self.capitalize_checkbox_frame.grid(row=2, column=0, padx=(50, 0), pady=(20, 0), sticky='n')
        self.capitalize_checkbox_frame.grid_columnconfigure(2, weight=1)
        self.capitalize_checkbox_frame.grid_rowconfigure(1, weight=1)
        self.capitalize_checkbox.grid(row=0, column=0, padx=(40, 0), pady=10, sticky="w")
        self.use_number_checkbox.grid(row=0, column=1, padx=(0, 40), pady=10, sticky="e")

        # Set Defaults
        self.passphrase_length_label.configure(text=f'Words {self.min_words}')
        self.passphrase_length_slider.set(self.min_words)
        self.word_separator_entry.bind('<KeyRelease>', self.create_passphrase)
        self.word_separator_entry.insert(0, self.default_word_separator)

    def create_username_frame(self):
        # Create Username Checkbox Frame
        self.username_checkbox_frame = customtkinter.CTkFrame(master=self.generator_tabview.tab('Username'))
        self.username_checkbox = customtkinter.CTkCheckBox(master=self.username_checkbox_frame, text='Username',
                                                           command=self.random_word_clicked, width=150,
                                                           state='disabled')
        self.sub_address_checkbox = customtkinter.CTkCheckBox(master=self.username_checkbox_frame,
                                                              text='Email sub-address',
                                                              command=self.sub_address_clicked, width=150)
        # Username Checkbox Frame Placement
        self.username_checkbox_frame.grid(row=0, column=0, padx=(90, 0), pady=(40, 0), sticky='n')
        self.username_checkbox_frame.grid_columnconfigure(1, weight=1)
        self.username_checkbox_frame.grid_rowconfigure(2, weight=1)
        self.username_checkbox.grid(row=0, column=0, padx=(40, 0), pady=20, sticky="n")
        self.sub_address_checkbox.grid(row=1, column=0, padx=(40, 0), pady=20, sticky="n")

        # Set Defaults
        self.username_checkbox.select()

    def check_valid_checkbox(self):
        if self.numbers_checkbox.get() == 1:
            self.min_numbers_slider.configure(state='normal')
        else:
            self.min_numbers_slider.configure(state='disabled')
        if self.symbols_checkbox.get() == 1:
            self.min_symbol_slider.configure(state='normal')
        else:
            self.min_symbol_slider.configure(state='disabled')

        if self.uppercase_checkbox.get() == 0 and self.lowercase_checkbox.get() == 0 and self.numbers_checkbox.get() == 0 and self.symbols_checkbox.get() == 0:
            self.lowercase_checkbox.select()

        self.create_password()

    def sub_address_clicked(self):
        self.username_checkbox.deselect()
        self.create_sub_address()
        self.username_checkbox.configure(state='normal')
        self.sub_address_checkbox.configure(state='disabled')

    def random_word_clicked(self):
        self.sub_address_checkbox.deselect()
        self.create_random_word()
        self.sub_address_checkbox.configure(state='normal')
        self.username_checkbox.configure(state='disabled')

    def update_length(self, *args):
        text = 'Length:'
        length = int(self.length_slider.get())
        self.length_label.configure(text=f'{text:7} {length:3d}')
        self.update_min_number_and_special()
        self.create_password()

    def update_words(self, *args):
        text = 'Words:'
        length = int(self.passphrase_length_slider.get())
        self.passphrase_length_label.configure(text=f'{text:7} {length:2d}')
        self.create_passphrase()

    def update_min_number(self, *args):
        self.min_numbers_label.configure(text=f'Minimum Numbers: {int(self.min_numbers_slider.get())}')
        self.create_password()

    def update_min_special(self, *args):
        self.min_symbol_label.configure(text=f'Minimum Symbols: {int(self.min_symbol_slider.get())}')
        self.create_password()

    def update_min_number_and_special(self):
        self.max_min_num = self.password_length // 10
        self.max_symbols_num = self.password_length // 10
        # Next parts stops from division of zero errors when updating the bar
        if self.max_min_num < 1:
            self.max_min_num = 1
        if self.max_symbols_num < 1:
            self.max_symbols_num = 1
        current_min_num = int(self.min_numbers_slider.get())
        current_symbol_num = int(self.min_symbol_slider.get())
        if current_min_num > self.max_min_num:
            current_min_num = self.max_min_num
        if current_symbol_num > self.max_symbols_num:
            current_symbol_num = self.max_symbols_num
        self.min_numbers_slider.configure(to=self.max_min_num, number_of_steps=self.max_min_num - self.min_min_num)
        self.min_numbers_slider.set(current_min_num)
        self.min_numbers_label.configure(text=f'Minimum Numbers: {int(self.min_numbers_slider.get())}')
        self.min_symbol_slider.configure(to=self.max_symbols_num,
                                         number_of_steps=self.max_symbols_num - self.min_symbols_num)
        self.min_symbol_label.configure(text=f'Minimum Symbols: {int(self.min_symbol_slider.get())}')
        self.min_symbol_slider.set(current_symbol_num)

    def copy_main_textbox(self):
        self.main_textbox.clipboard_clear()
        self.main_textbox.clipboard_append(self.main_textbox.get('0.0', 'end'))
        self.update_history()

    def generator_tabview_event(self):
        if self.generator_tabview.get() == 'Password':
            self.create_password()
        elif self.generator_tabview.get() == 'Passphrase':
            self.create_passphrase()
        else:
            if self.username_checkbox.get() == 1:
                self.create_random_word()
            else:
                self.create_sub_address()

    def update_main_textbox(self, text):
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

    def create_passphrase(self, *args):
        current_passphrase = ''
        num_of_words = int(self.passphrase_length_slider.get())
        current_seperator = self.word_separator_entry.get().strip()

        for i in range(0, num_of_words):
            random_index = secrets.randbelow(58110)
            with open(r'C:\Users\xjord\Desktop\PasswordManager\word_files\mielie_stronk_list_58110', 'r') as file:
                lines = file.readlines()
                current_word = lines[random_index].strip()
                if self.capitalize_checkbox.get() == 1:
                    current_word = current_word.capitalize()
                if self.use_number_checkbox.get() == 1:
                    random_number = secrets.randbelow(10)
                    if i == 0:
                        current_passphrase += f'{current_word}{random_number}'
                    else:
                        current_passphrase += f'{current_seperator}{current_word}{random_number}'
                else:
                    if i == 0:
                        current_passphrase += f'{current_word}'
                    else:
                        current_passphrase += f'{current_seperator}{current_word}'

        self.update_main_textbox(current_passphrase)

    def create_random_word(self):
        self.update_main_textbox(create_username())

    def create_sub_address(self):
        char_list = string.ascii_lowercase + string.digits
        extra_letters = ''
        email = get_email_with_account_id(self.account_id)
        email = email.split('@')
        for i in range(0, 8):
            character = secrets.choice(char_list)
            extra_letters += character
        sub_address = email[0] + '+' + extra_letters + '@' + email[1]
        self.update_main_textbox(sub_address)

    def create_required_char_list(self):
        char_list = ''
        if self.uppercase_checkbox.get() == 1:
            char_list += string.ascii_uppercase
        if self.lowercase_checkbox.get() == 1:
            char_list += string.ascii_lowercase
        if self.numbers_checkbox.get() == 1:
            char_list += string.digits
        if self.symbols_checkbox.get() == 1:
            char_list += self.valid_symbols
        if self.ambiguous_checkbox.get() == 1:
            char_list = char_list.replace('l', '').replace('1', '').replace('I', '').replace('o', '').replace('O', '').replace( '0', '')
        return char_list

    def create_password(self):
        self.password_length = int(self.length_slider.get())
        char_list = self.create_required_char_list()
        password = ''
        min_num = self.min_numbers_slider.get()
        min_special = self.min_symbol_slider.get()
        self.password_strength_frame.reset_scoring_variables()
        for index in range(0, self.password_length):
            char = secrets.choice(char_list)
            password += char
            self.password_strength_frame.update_basic_scoring_variables(index, char, self.valid_symbols, self.password_length)
        self.password_strength_frame.update_advanced_scoring_variables(self.valid_symbols, password)
        self.update_main_textbox(password)
        self.password_strength_frame.calc_password_strength_score(self.password_length)

    def update_history(self):
        password = self.main_textbox.get('0.0', 'end').strip()
        master_key = get_master_key_with_account_id(self.account_id)[0]
        encrypted_password = encrypt_text(master_key, password)

        if self.generator_tabview.get() == 'Username':
            return
        if self.check_if_already_entered(master_key, encrypted_password):
            return

        delete_oldest_history_if_at_limit(self.account_id)
        create_new_history(self.account_id, encrypted_password)

    def check_if_already_entered(self, master_key, encrypted_password):
        history = get_all_from_history(self.account_id)
        decrypted_input_password = decrypt_text(master_key, encrypted_password)
        for history_row in history:
            decrypted_db_password = decrypt_text(master_key, history_row[1])
            if decrypted_db_password == decrypted_input_password:
                return True
        return False
