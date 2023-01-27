import tkinter
import customtkinter
import sqlite3
import secrets
import string
from colors import *
from PIL import Image
from datetime import datetime
from settings import MAX_HISTORY_ENTRIES

# todo password strength fix
# todo password generate per requirements - min numbers and min specials
# todo look into generating passphrase on word separator input


class GeneratorTab:
    def __init__(self, landing_tabview, width, height, account_id):
        super().__init__()

        # General Setup
        self.account_id = account_id
        self.landing_tabview = landing_tabview
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

        # Password Strength
        self.num_of_uppercase_chars = 0
        self.num_of_lowercase_chars = 0
        self.num_of_num_chars = 0
        self.num_of_symbol_chars = 0
        self.num_or_symbol_used_in_middle = 0
        self.repeat_char = 0
        self.consecutive_uppercase = 0
        self.consecutive_lowercase = 0
        self.consecutive_numbers = 0
        self.sequential_letters = 0
        self.sequential_numbers = 0
        self.sequential_symbols = 0

        # Create Password Textbox
        self.main_textbox = customtkinter.CTkTextbox(master=self.landing_tabview.tab('Generator'), state='disabled',
                                                     width=self.main_textbox_width, font=('Arial', 16),
                                                     height=self.main_textbox_height, corner_radius=15)
        self.main_textbox.place(relx=0.45, rely=0.01, anchor=tkinter.N)

        # Copy / Generate Password Buttons
        self.copy_image = customtkinter.CTkImage(Image.open(r"C:\Users\xjord\Desktop\PasswordManager\images\copy-icon.png"), size=(20, 20))
        self.regenerate_image = customtkinter.CTkImage(Image.open(r'C:\Users\xjord\Desktop\PasswordManager\images\arrows-spin-solid.png'), size=(20, 20))

        self.copy_gen_button_frame = customtkinter.CTkFrame(master=self.landing_tabview.tab('Generator'), fg_color="transparent")
        self.copy_buttons = customtkinter.CTkButton(master=self.copy_gen_button_frame, text='', image=self.copy_image, fg_color=BLUE,
                                                    command=self.copy_main_textbox, width=self.button_width, height=self.button_height)
        self.regenerate_buttons = customtkinter.CTkButton(master=self.copy_gen_button_frame, text='', image=self.regenerate_image, fg_color=BLUE,
                                                          command=self.update_main_textbox, width=self.button_width, height=self.button_height)
        # Copy / Generate Placement
        self.copy_gen_button_frame.place(relx=0.96, rely=0.04, anchor=tkinter.N)
        self.copy_gen_button_frame.grid_columnconfigure(0, weight=1)
        self.copy_gen_button_frame.grid_rowconfigure(2, weight=1)
        self.copy_buttons.grid(row=0, column=0, pady=(0, 10), sticky="n")
        self.regenerate_buttons.grid(row=1, column=0, sticky="n")

        # Password Strength
        self.password_strength_frame = customtkinter.CTkFrame(master=self.landing_tabview.tab('Generator'), fg_color="transparent")
        self.strength_label = customtkinter.CTkLabel(master=self.password_strength_frame, text="Password Strength:")
        self.strength_bar = customtkinter.CTkProgressBar(self.password_strength_frame, width=350, height=20)
        # Password Strength Placement
        self.password_strength_frame.place(relx=0.5, rely=1, anchor=tkinter.S)
        self.password_strength_frame.grid_columnconfigure(0, weight=1)
        self.password_strength_frame.grid_rowconfigure(2, weight=1)
        self.strength_label.grid(row=0, column=0, sticky="ew")
        self.strength_bar.grid(row=1, column=0, pady=(0, 20), sticky="ew")

        # Create Password/UserName Tabview
        self.password_tabview = customtkinter.CTkTabview(master=self.landing_tabview.tab('Generator'),
                                                         width=self.password_tabview_width, height=self.password_tabview_height,
                                                         segmented_button_selected_color=BLUE, corner_radius=15,
                                                         border_width=3, border_color=WHITE, command=self.update_main_textbox)
        self.password_tabview.place(relx=0.5, rely=0.2, anchor=tkinter.N)
        self.password_tabview.add('Password')
        self.password_tabview.add('Passphrase')
            # Separator
            # capitalize
            # include number
        self.password_tabview.add("Username")

        """=======================       Password Section       ======================="""
        # Create Length Slider and Ambiguous Checkbox Frame
        self.length_slider_frame = customtkinter.CTkFrame(master=self.password_tabview.tab('Password'), fg_color='transparent')
        self.length_label = customtkinter.CTkLabel(master=self.length_slider_frame)
        self.length_slider = customtkinter.CTkSlider(master=self.length_slider_frame,
                                                     command=self.update_length,
                                                     from_=self.min_password_length, to=self.max_password_length,
                                                     number_of_steps=self.max_password_length - self.min_password_length)
        # Removes l (ell), 1 (one), I (capital i), o O (oh), and 0 (zero)
        self.ambiguous_checkbox = customtkinter.CTkCheckBox(master=self.length_slider_frame, text="Avoid Ambiguous Characters",
                                                            command=self.create_password)
        # Length Slider and Ambiguous Checkbox Placement
        self.length_slider_frame.grid(row=0, column=0, padx=(50, 0), pady=(30, 0), sticky="n")
        self.length_slider_frame.grid_columnconfigure(2, weight=1)
        self.length_slider_frame.grid_rowconfigure(2, weight=1)
        self.length_label.grid(row=0, column=0, padx=(0, 20), sticky="w")
        self.length_slider.grid(row=0, column=1, padx=10, sticky="e")
        self.ambiguous_checkbox.grid(row=1, column=0, padx=(50, 0), pady=(20, 0), columnspan=2, sticky="ew")

        # Create Password Checkbox Frame
        self.checkbox_slider_frame = customtkinter.CTkFrame(master=self.password_tabview.tab('Password'))
        self.lowercase = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text='a-z',
                                                   command=self.check_valid_checkbox)
        self.uppercase = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text='A-Z',
                                                   command=self.check_valid_checkbox)
        self.numbers = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text='0-9',
                                                 command=self.check_valid_checkbox)
        self.special_characters = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text='!@#$%^&*',
                                                            command=self.check_valid_checkbox)
        # Password Checkbox Frame Placement
        self.checkbox_slider_frame.grid(row=1, column=0, padx=(50, 0), pady=(20, 0), sticky='n')
        self.lowercase.grid(row=0, column=0, padx=(40, 0), pady=10, sticky="w")
        self.uppercase.grid(row=0, column=1,  padx=(0, 40), pady=10, sticky="e")
        self.numbers.grid(row=1, column=0, padx=(40, 10), pady=10,  sticky="w")
        self.special_characters.grid(row=1, column=1,  padx=(0, 40), pady=10, sticky="e")
        # Default
        self.lowercase.select()

        # Create Extras Slider Frame
        self.extras_slider_frame = customtkinter.CTkFrame(master=self.password_tabview.tab('Password'),
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
        self.length_slider.set(self.password_length)
        self.create_password()
        self.length_label.configure(text=f'Length: {self.password_length}')
        self.min_numbers_slider.set(self.default_min_number)
        self.min_numbers_label.configure(text=f'Minimum Numbers: {self.default_min_number}')
        self.min_symbol_slider.set(self.default_min_symbol)
        self.min_symbol_label.configure(text=f'Minimum Symbols: {self.default_min_symbol}')

        """=======================       Passphrase Section       ======================="""

        # Create Passphrase Length Slider Frame
        self.passphrase_length_slider_frame = customtkinter.CTkFrame(master=self.password_tabview.tab('Passphrase'), fg_color='transparent')
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
        self.word_separator_frame = customtkinter.CTkFrame(master=self.password_tabview.tab('Passphrase'), fg_color='transparent')
        self.word_separator_label = customtkinter.CTkLabel(master=self.word_separator_frame, text='Word Separator:')
        self.word_separator_textbox = customtkinter.CTkTextbox(master=self.word_separator_frame,
                                                               width=70, height=40, corner_radius=15)
        # Word Separator Frame Placement
        self.word_separator_frame.grid(row=1, column=0, padx=(50, 0), pady=(30, 0), sticky="n")
        self.word_separator_frame.grid_columnconfigure(2, weight=1)
        self.word_separator_frame.grid_rowconfigure(1, weight=1)
        self.word_separator_label.grid(row=0, column=0, padx=(0, 20), sticky="w")
        self.word_separator_textbox.grid(row=0, column=1, padx=(0, 20), sticky="e")

        # Create Capitalize - Number Checkbox Frame
        self.capitalize_checkbox_frame = customtkinter.CTkFrame(master=self.password_tabview.tab('Passphrase'))
        self.capitalize_checkbox = customtkinter.CTkCheckBox(master=self.capitalize_checkbox_frame, text='Capitalize',
                                                             command=self.create_passphrase)
        self.use_number_checkbox = customtkinter.CTkCheckBox(master=self.capitalize_checkbox_frame, text='Include number',
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
        self.word_separator_textbox.bind('<KeyPress>', self.reset_word_separator_box)
        self.word_separator_textbox.insert('0.0', self.default_word_separator)

        """=======================       Username Section       ======================="""

        # Create Username Checkbox Frame
        self.username_checkbox_frame = customtkinter.CTkFrame(master=self.password_tabview.tab('Username'))
        self.random_word_checkbox = customtkinter.CTkCheckBox(master=self.username_checkbox_frame, text='Random word',
                                                              command=self.random_word_clicked, width=150,
                                                              state='disabled')
        self.sub_address_checkbox = customtkinter.CTkCheckBox(master=self.username_checkbox_frame, text='Email sub-address',
                                                              command=self.sub_address_clicked, width=150)
        # Password Checkbox Frame Placement
        self.username_checkbox_frame.grid(row=0, column=0, padx=(90, 0), pady=(40, 0), sticky='n')
        self.username_checkbox_frame.grid_columnconfigure(1, weight=1)
        self.username_checkbox_frame.grid_rowconfigure(2, weight=1)
        self.random_word_checkbox.grid(row=0, column=0, padx=(40, 0), pady=20, sticky="n")
        self.sub_address_checkbox.grid(row=1, column=0, padx=(40, 0), pady=20, sticky="n")

        # Set Defaults
        self.random_word_checkbox.select()

    def reset_password_box(self):
        self.main_textbox.configure(state='normal')
        self.main_textbox.delete('1.0', 'end')
        self.main_textbox.configure(state='disabled')

    def reset_word_separator_box(self, *args):
        # Only allows one character to be input into textbox
        self.word_separator_textbox.delete('1.0', 'end')

    def check_valid_checkbox(self):
        if self.numbers.get() == 1:
            self.min_numbers_slider.configure(state='normal')
        else:
            self.min_numbers_slider.configure(state='disabled')
        if self.special_characters.get() == 1:
            self.min_symbol_slider.configure(state='normal')
        else:
            self.min_symbol_slider.configure(state='disabled')

        if self.uppercase.get() == 0 and self.lowercase.get() == 0 and self.numbers.get() == 0 and self.special_characters.get() == 0:
            self.lowercase.select()

        self.create_password()

    def sub_address_clicked(self):
        self.random_word_checkbox.deselect()
        self.create_sub_address()
        self.random_word_checkbox.configure(state='normal')
        self.sub_address_checkbox.configure(state='disabled')

    def random_word_clicked(self):
        self.sub_address_checkbox.deselect()
        self.create_random_word()
        self.sub_address_checkbox.configure(state='normal')
        self.random_word_checkbox.configure(state='disabled')

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
        self.min_symbol_slider.configure(to=self.max_symbols_num, number_of_steps=self.max_symbols_num - self.min_symbols_num)
        self.min_symbol_label.configure(text=f'Minimum Symbols: {int(self.min_symbol_slider.get())}')
        self.min_symbol_slider.set(current_symbol_num)

    def copy_main_textbox(self):
        self.main_textbox.clipboard_clear()
        self.main_textbox.clipboard_append(self.main_textbox.get('0.0', 'end'))
        self.update_history()

    def update_main_textbox(self):
        if self.password_tabview.get() == 'Password':
            self.create_password()
        elif self.password_tabview.get() == 'Passphrase':
            self.create_passphrase()
        else:
            if self.random_word_checkbox.get() == 1:
                self.create_random_word()
            else:
                self.create_sub_address()

    def change_main_text_box(self, text):
        self.main_textbox.configure(state='normal')
        self.main_textbox.delete('1.0', 'end')
        self.main_textbox.insert('end', text)
        self.main_textbox.configure(state='disabled')

    def create_passphrase(self):
        current_passphrase = ''
        num_of_words = int(self.passphrase_length_slider.get())
        current_seperator = self.word_separator_textbox.get('0.0', 'end').strip()

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

        self.change_main_text_box(current_passphrase)

    def create_random_word(self):
        random_word = ''
        random_numbers = ''
        for i in range(0, secrets.randbelow(5)):
            random_numbers += str(secrets.randbelow(10))

        random_index = secrets.randbelow(58110)
        with open(r'C:\Users\xjord\Desktop\PasswordManager\word_files\mielie_stronk_list_58110', 'r') as file:
            lines = file.readlines()
            current_word = lines[random_index].strip()
            random_word += f'{current_word}{random_numbers}'

        self.change_main_text_box(random_word)

    def create_sub_address(self):
        char_list = string.ascii_lowercase + string.digits
        extra_letters = ''
        with sqlite3.connect('data.db') as db:
            cursor = db.execute('SELECT email FROM Person WHERE account_id = ?', [self.account_id])
            email = cursor.fetchone()[0]
            email = email.split('@')
            for i in range(0, 8):
                character = secrets.choice(char_list)
                extra_letters += character
        sub_address = email[0] + '+' + extra_letters + '@' + email[1]
        self.change_main_text_box(sub_address)

    def create_required_char_list(self):
        char_list = ''
        if self.uppercase.get() == 1:
            char_list += string.ascii_uppercase
        if self.lowercase.get() == 1:
            char_list += string.ascii_lowercase
        if self.numbers.get() == 1:
            char_list += string.digits
        if self.special_characters.get() == 1:
            char_list += self.valid_symbols
        if self.ambiguous_checkbox.get() == 1:
            char_list = char_list.replace('l', '').replace('1', '').replace('I', '').replace('o', '').replace('O', '').replace('0', '')
        return char_list

    def reset_scoring_variables(self):
        self.num_of_uppercase_chars = 0
        self.num_of_lowercase_chars = 0
        self.num_of_num_chars = 0
        self.num_of_symbol_chars = 0
        self.num_or_symbol_used_in_middle = 0
        self.consecutive_uppercase = 0
        self.consecutive_lowercase = 0
        self.consecutive_numbers = 0
        self.repeat_char = 0
        self.sequential_letters = 0
        self.sequential_numbers = 0
        self.sequential_symbols = 0

    def update_basic_scoring_variables(self, index, char):
        if char in string.ascii_lowercase:
            self.num_of_lowercase_chars += 1
        elif char in string.ascii_uppercase:
            self.num_of_uppercase_chars += 1
        elif char in string.digits:
            self.num_of_num_chars += 1
        elif char in self.valid_symbols:
            self.num_of_symbol_chars += 1

        if index != 0 or index != self.password_length - 1:
            if char in string.digits or char in self.valid_symbols:
                self.num_or_symbol_used_in_middle += 1

    def update_advanced_scoring_variables(self, password):
        for char in range(len(password)):
            if char < len(password) - 1:
                if password[char] in string.ascii_uppercase:
                    if password[char+1] in string.ascii_uppercase:
                        self.consecutive_uppercase += 1
                elif password[char] in string.ascii_lowercase:
                    if password[char+1] in string.ascii_lowercase:
                        self.consecutive_lowercase += 1
                elif password[char] in string.digits:
                    if password[char+1] in string.digits:
                        self.consecutive_numbers += 1

            # todo figure out sequential numbers/letters

            #Looks for repeated chars
            for char_b in range(len(password)):
                if password[char] == password[char_b] and char != char_b:
                    self.repeat_char += 1

    def create_password(self):
        self.password_length = int(self.length_slider.get())
        char_list = self.create_required_char_list()
        password = ''
        min_num = self.min_numbers_slider.get()
        min_special = self.min_symbol_slider.get()
        self.reset_scoring_variables()
        for index in range(0, self.password_length):
            char = secrets.choice(char_list)
            password += char
            self.update_basic_scoring_variables(index, char)
        self.update_advanced_scoring_variables(password)
        self.change_main_text_box(password)
        self.update_password_strength()

    def update_history(self):
        now = datetime.now()
        date = now.strftime("%c")
        key = self.main_textbox.get('0.0', 'end').strip()

        if self.password_tabview.get() != 'Password' and self.password_tabview.get() != 'Passphrase':
            return

        if self.check_if_already_entered(key):
            return

        self.check_if_max_history_entries()
        with sqlite3.connect('data.db') as db:
            db.execute('INSERT INTO History (account_id, key, timestamp) VALUES (?, ?,?)', (self.account_id, key, date))

    def check_if_already_entered(self, key):
        with sqlite3.connect('data.db') as db:
            cursor = db.execute('SELECT * FROM History WHERE account_id = ?', [self.account_id])
            history = cursor.fetchall()
            for row in history:
                if row[1] == key:
                    return True
            return False

    def check_if_max_history_entries(self):
        with sqlite3.connect('data.db') as db:
            cursor = db.execute('SELECT * FROM History WHERE account_id = ?', [self.account_id])
            history = cursor.fetchall()
            if len(history) == MAX_HISTORY_ENTRIES:
                db.execute('Delete FROM History WHERE timestamp = ?', [history[0][2]])

    def update_password_strength(self):
        # Positive Scores
        requirements_meet = 0
        score = (self.password_length * 4)
        if self.uppercase.get() == 1:
            requirements_meet += 1
            score += ((self.password_length - self.num_of_uppercase_chars) * 2)
        if self.lowercase.get() == 1:
            requirements_meet += 1
            score += ((self.password_length - self.num_of_lowercase_chars) * 2)
        if self.numbers.get() == 1:
            requirements_meet += 1
            score += (self.num_of_num_chars * 4)
        if self.special_characters.get() == 1:
            requirements_meet += 1
            score += (self.num_of_symbol_chars * 6)
        if self.password_length > 12:
            requirements_meet += 1
        score += (requirements_meet * 2)
        print(f'\nRequirements: {(requirements_meet * 2)}')

        # todo look into this part
        if self.num_or_symbol_used_in_middle > 0:
            score += (self.num_or_symbol_used_in_middle * 2)
        print(f'Special In middle: {(self.num_or_symbol_used_in_middle * 2)}')

        # Negative Scores
        if self.num_of_uppercase_chars > 0 or self.num_of_lowercase_chars > 0 and self.num_of_num_chars == 0 and self.num_of_symbol_chars == 0:
            score -= self.num_of_uppercase_chars + self.num_of_lowercase_chars
        elif self.num_of_uppercase_chars == 0 and self.num_of_lowercase_chars == 0 and self.num_of_num_chars > 0 and self.num_of_symbol_chars == 0:
            score -= self.num_of_num_chars
        elif self.num_of_uppercase_chars == 0 and self.num_of_lowercase_chars == 0 and self.num_of_num_chars == 0 and self.num_of_symbol_chars > 0:
            score -= self.num_of_symbol_chars

        if self.consecutive_uppercase != 0:
            score -= (self.consecutive_uppercase * 2)
        if self.consecutive_lowercase != 0:
            score -= (self.consecutive_lowercase * 2)
        if self.consecutive_numbers != 0:
            score -= (self.consecutive_numbers * 2)

        if self.sequential_letters != 0:
            score -= (self.sequential_letters * 3)
        elif self.sequential_numbers != 0:
            score -= (self.sequential_numbers * 3)
        elif self.sequential_symbols != 0:
            score -= (self.sequential_symbols * 3)


        print(f'Total Score: {score}')
        self.update_strength_bar(score)

    def update_strength_bar(self, score):
        if score > 100:
            strength = 1
        else:
            strength = score / 100
        self.strength_bar.set(strength)

        if score <= 40:
            self.strength_bar.configure(progress_color=RED)
        elif score < 75:
            self.strength_bar.configure(progress_color=DARK_GREEN)
        else:
            self.strength_bar.configure(progress_color=GREEN)

