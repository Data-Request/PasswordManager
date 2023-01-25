import tkinter
import customtkinter
import secrets
import string
from colors import *
from PIL import Image


# todo add in consecutive lowercase letter, numbers, and sequential numbers/ symbols to generate password
# todo password strength fix
# todo password generate per requirements - min numbers and min specials
# todo look into generating passphrase on word separator input


class GeneratorTab:
    def __init__(self, landing_tabview, width, height):
        super().__init__()

        # General Setup
        self.landing_tabview = landing_tabview
        self.password_tabview_width = width - 72
        self.password_tabview_height = height - 300
        self.button_width = 25
        self.button_height = 25
        self.main_textbox_width = width - 115
        self.main_textbox_height = 110

        # Password Variables
        self.min_password_length = 8
        self.max_password_length = 128
        self.password_length = 32
        self.password = ''
        self.default_min_number = 3
        self.default_min_symbol = 3
        self.min_min_num = 1
        self.max_min_num = int(self.password_length / 10)
        self.min_symbols_num = 1
        self.max_symbols_num = int(self.password_length / 10)

        # Passphrase
        self.min_words = 3
        self.max_words = 20
        self.word_separator = '-'
        self.number_of_words = self.min_words

        # Password Strength
        self.uppercase_used_number = 0
        self.lowercase_used_number = 0
        self.number_used_number = 0
        self.symbol_used_number = 0
        self.only_uppercase = False
        self.only_lowercase = False
        self.only_numbers = False
        self.only_symbols = False
        self.num_or_symbol_used_in_middle = 0

        # Create Password Textbox
        self.password_textbox = customtkinter.CTkTextbox(master=self.landing_tabview.tab('Generator'),
                                                         width=self.main_textbox_width, font=('Arial', 16),
                                                         height=self.main_textbox_height, corner_radius=15)
        self.password_textbox.place(relx=0.45, rely=0.01, anchor=tkinter.N)
        self.password_textbox.configure(state='disabled')

        # Copy / Generate Password Buttons
        self.copy_image = customtkinter.CTkImage(Image.open(r"C:\Users\xjord\Desktop\PasswordManager\images\copy-icon.png"), size=(20, 20))
        self.regenerate_image = customtkinter.CTkImage(Image.open(r'C:\Users\xjord\Desktop\PasswordManager\images\recycle-transparent-25.png'), size=(20, 20))

        self.copy_gen_button_frame = customtkinter.CTkFrame(master=self.landing_tabview.tab('Generator'), fg_color="transparent")
        self.copy_buttons = customtkinter.CTkButton(master=self.copy_gen_button_frame, text='', image=self.copy_image, fg_color=BLUE,
                                                    command=self.copy_main_textbox, width=self.button_width, height=self.button_height)
        self.regenerate_buttons = customtkinter.CTkButton(master=self.copy_gen_button_frame, text='', image=self.regenerate_image, fg_color=BLUE,
                                                          command=self.update_main_textbox, width=self.button_width, height=self.button_height)
        # Copy / Generate Placement
        self.copy_gen_button_frame.place(relx=0.96, rely=0.05, anchor=tkinter.N)
        self.copy_gen_button_frame.grid_columnconfigure(0, weight=1)
        self.copy_gen_button_frame.grid_rowconfigure(2, weight=1)
        self.copy_buttons.grid(row=0, column=0, sticky="n")
        self.regenerate_buttons.grid(row=1, column=0, sticky="n")

        # Password Strength
        self.password_strength_frame = customtkinter.CTkFrame(master=self.landing_tabview.tab('Generator'), fg_color="transparent")
        self.strength_label = customtkinter.CTkLabel(master=self.password_strength_frame, text="Password Strength:")
        self.strength_bar = customtkinter.CTkProgressBar(self.password_strength_frame, width=350, height=20, progress_color=RED)
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
                                                            command=self.generate_password)
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
        self.min_numbers_slider = customtkinter.CTkSlider(master=self.extras_slider_frame,
                                                          command=self.update_min_number,
                                                          from_=self.min_min_num, to=self.max_min_num,
                                                          number_of_steps=self.max_min_num - self.min_min_num)
        self.min_numbers_slider.grid(row=0, column=1, sticky="e")
        self.min_symbol_label = customtkinter.CTkLabel(master=self.extras_slider_frame)
        self.min_symbol_label.grid(row=1, column=0, pady=(15, 0), columnspan=1, sticky="w")
        self.min_symbol_slider = customtkinter.CTkSlider(master=self.extras_slider_frame,
                                                         command=self.update_min_special,
                                                         from_=self.min_symbols_num, to=self.max_symbols_num,
                                                         number_of_steps=self.max_symbols_num - self.min_symbols_num)
        self.min_symbol_slider.grid(row=1, column=1, pady=(15, 0), sticky="e")

        # Set Defaults
        self.generate_password()
        self.password_textbox.insert('0.0', self.password)
        self.length_slider.set(self.password_length)
        self.length_label.configure(text=f'Length: {self.password_length}')
        self.min_numbers_slider.set(self.default_min_number)
        self.min_numbers_label.configure(text=f'Minimum Numbers: {self.default_min_number}')
        self.min_symbol_slider.set(self.default_min_symbol)
        self.min_symbol_label.configure(text=f'Minimum Symbols: {self.default_min_symbol}')
        self.strength_bar.set(0)

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
        self.word_separator_textbox.insert('0.0', self.word_separator)

        # Create Capitalize - Number Checkbox Frame
        self.capitalize_checkbox_frame = customtkinter.CTkFrame(master=self.password_tabview.tab('Passphrase'))
        self.capitalize_checkbox = customtkinter.CTkCheckBox(master=self.capitalize_checkbox_frame, text='Capitalize',
                                                             command=self.generate_passphrase)
        self.use_number_checkbox = customtkinter.CTkCheckBox(master=self.capitalize_checkbox_frame, text='Include number',
                                                             command=self.generate_passphrase)
        # Password Checkbox Frame Placement
        self.capitalize_checkbox_frame.grid(row=2, column=0, padx=(50, 0), pady=(20, 0), sticky='n')
        self.capitalize_checkbox_frame.grid_columnconfigure(2, weight=1)
        self.capitalize_checkbox_frame.grid_rowconfigure(1, weight=1)
        self.capitalize_checkbox.grid(row=0, column=0, padx=(40, 0), pady=10, sticky="w")
        self.use_number_checkbox.grid(row=0, column=1, padx=(0, 40), pady=10, sticky="e")

        # Set Defaults
        self.passphrase_length_label.configure(text=f'Words {self.number_of_words}')
        self.passphrase_length_slider.set(self.number_of_words)
        self.word_separator_textbox.bind('<KeyPress>', self.reset_word_separator_box)
        self.strength_bar.set(0)

        """=======================       Username Section       ======================="""

        # Create Username Checkbox Frame
        self.username_checkbox_frame = customtkinter.CTkFrame(master=self.password_tabview.tab('Username'))
        self.random_word_checkbox = customtkinter.CTkCheckBox(master=self.username_checkbox_frame, text='Random word',
                                                              command=self.generate_random_word, state='disabled')
        # Password Checkbox Frame Placement
        self.username_checkbox_frame.grid(row=0, column=0, padx=(50, 50), pady=(20, 0), sticky='n')
        self.username_checkbox_frame.grid_columnconfigure(1, weight=1)
        self.username_checkbox_frame.grid_rowconfigure(1, weight=1)
        self.random_word_checkbox.grid(row=0, column=0, padx=(40, 0), pady=10, sticky="n")

        # Set Defaults
        self.random_word_checkbox.select()

    def reset_password_box(self):
        self.password_textbox.configure(state='normal')
        self.password_textbox.delete('1.0', 'end')
        self.password_textbox.configure(state='disabled')

    def reset_word_separator_box(self, *args):
        self.word_separator_textbox.delete('1.0', 'end')

    def check_valid_checkbox(self):
        if self.uppercase.get() == 1:
            self.generate_password()
            return
        if self.lowercase.get == 1:
            self.generate_password()
            return
        if self.numbers.get() == 1:
            self.generate_password()
            return
        if self.special_characters.get() == 1:
            self.generate_password()
            return
        self.lowercase.select()
        self.generate_password()

    def update_length(self, *args):
        text = 'Length:'
        length = int(self.length_slider.get())
        self.length_label.configure(text=f'{text:7} {length:3d}')
        self.update_min_number_and_special()
        self.generate_password()

    def update_words(self, *args):
        text = 'Words:'
        length = int(self.passphrase_length_slider.get())
        self.passphrase_length_label.configure(text=f'{text:7} {length:2d}')
        self.generate_passphrase()

    def update_min_number(self, *args):
        self.min_numbers_label.configure(text=f'Minimum Numbers: {int(self.min_numbers_slider.get())}')
        self.generate_password()

    def update_min_special(self, *args):
        self.min_symbol_label.configure(text=f'Minimum Symbols: {int(self.min_symbol_slider.get())}')
        self.generate_password()

    def update_min_number_and_special(self):
        self.max_min_num = int(self.password_length / 10)
        self.max_symbols_num = int(self.password_length / 10)
        # Next parts stops from division of zero errors when updating the bar
        if self.max_min_num < 3:
            self.max_min_num = 3
        if self.max_symbols_num < 3:
            self.max_symbols_num = 3
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
        self.password_textbox.clipboard_clear()
        self.password_textbox.clipboard_append(self.password_textbox.get('0.0', 'end'))

    def update_main_textbox(self):
        if self.password_tabview.get() == 'Password':
            self.generate_password()
            self.update_password_strength()
        elif self.password_tabview.get() == 'Passphrase':
            self.generate_passphrase()
        else:
            self.generate_random_word()

    def change_main_text_box(self, text):
        self.password_textbox.configure(state='normal')
        self.password_textbox.delete('1.0', 'end')
        self.password_textbox.insert('end', text)
        self.password_textbox.configure(state='disabled')

    def generate_passphrase(self):
        current_passphrase = ''
        self.number_of_words = int(self.passphrase_length_slider.get())
        current_seperator = self.word_separator_textbox.get('0.0', 'end').strip()

        for i in range(0, self.number_of_words):
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
        self.update_history(current_passphrase)
        self.copy_main_textbox()

    def generate_random_word(self):
        random_word = ''
        random_numbers = ''

        for i in range(1, secrets.randbelow(5)):
            random_numbers += str(secrets.randbelow(10))

        random_index = secrets.randbelow(58110)
        with open(r'C:\Users\xjord\Desktop\PasswordManager\word_files\mielie_stronk_list_58110', 'r') as file:
            lines = file.readlines()
            current_word = lines[random_index].strip()
            random_word += f'{current_word}{random_numbers}'

        self.change_main_text_box(random_word)
        self.update_history(random_word)
        self.copy_main_textbox()

    def generate_password(self):
        self.password_length = int(self.length_slider.get())
        special = "!@#$%^&*"
        char_list = ''
        password = ''
        if self.uppercase.get() == 1:
            char_list += string.ascii_uppercase
        if self.lowercase.get() == 1:
            char_list += string.ascii_lowercase
        if self.numbers.get() == 1:
            char_list += string.digits
        if self.special_characters.get() == 1:
            char_list += special
        if self.ambiguous_checkbox.get() == 1:
            char_list = char_list.replace('l', '')
            char_list = char_list.replace('1', '')
            char_list = char_list.replace('I', '')
            char_list = char_list.replace('o', '')
            char_list = char_list.replace('O', '')
            char_list = char_list.replace('0', '')
        min_num = self.min_numbers_slider.get()
        min_special = self.min_symbol_slider.get()
        for i in range(0, self.password_length - 1):
            character = secrets.choice(char_list)
            password += character
            if character in string.ascii_lowercase:
                self.lowercase_used_number += 1
            elif character in string.ascii_uppercase:
                self.uppercase_used_number += 1
            elif character in string.digits:
                self.number_used_number += 1
                if i != 1 or i != self.password_length:
                    self.num_or_symbol_used_in_middle += 1
            elif character in special:
                self.symbol_used_number += 1
                if i != 1 or i != self.password_length:
                    self.num_or_symbol_used_in_middle += 1

        self.password = password
        self.change_main_text_box(password)
        self.update_history(password)
        self.copy_main_textbox()

    def update_password_strength(self):
        return
        # Positive Score
        total_score = 0
        total_score += (self.password_length * 4)
        print(f'Number of Characters: {total_score}')
        total_score += ((self.password_length - self.uppercase_used_number) * 2)
        print(f'Uppercase: {total_score}')
        total_score += ((self.password_length - self.lowercase_used_number) * 2)
        print(f'Lowercase: {total_score}')
        total_score += (self.number_used_number * 4)
        print(f'Numbers: {total_score}')
        total_score += (self.symbol_used_number * 2)
        print(f'Special: {total_score}')
        if self.num_or_symbol_used_in_middle > 0:
            total_score += (self.num_or_symbol_used_in_middle * 2)
        print(f'Special In middle: {total_score}')
        if self.password_length > self.min_password_length:
            total_score += 1
        print(f'Requirements: {total_score}')

        # Negative Score
        if self.only_uppercase:
            total_score -= self.uppercase_used_number
        elif self.only_lowercase:
            total_score -= self.lowercase_used_number
        elif self.only_numbers:
            total_score -= self.number_used_number
        elif self.only_symbols:
            total_score -= self.symbol_used_number

        print(f'Total Score: {total_score}')
        print(f'Strength Bar Set Value to: {total_score // 100}')
        self.strength_bar.set(total_score // 100)

    @staticmethod
    def update_history(text):
        print('update history')

