import string
import tkinter
import customtkinter
from colors import *
from support import create_valid_chars_dict

class PasswordStrength:
    def __init__(self, landing_tabview, parent):
        super().__init__()

        # General Setup
        self.parent = parent
        self.landing_tabview = landing_tabview

        # Initialize
        self.reset_scoring_variables()
        self.create_generator_password_strength_frame()

    def create_generator_password_strength_frame(self):
        # Create and place Password strength frame
        if self.parent.name == 'Generator':
            self.password_strength_frame = customtkinter.CTkFrame(master=self.landing_tabview.tab('Generator'),
                                                                  fg_color="transparent")
        else:
            self.password_strength_frame = customtkinter.CTkFrame(master=self.landing_tabview.tab('Checker'),
                                                                  fg_color="transparent")
        self.strength_label = customtkinter.CTkLabel(master=self.password_strength_frame, text="Password Strength:")
        self.strength_bar = customtkinter.CTkProgressBar(self.password_strength_frame, width=350, height=20)
        self.password_strength_frame.place(relx=0.5, rely=1, anchor=tkinter.S)
        self.password_strength_frame.grid_columnconfigure(0, weight=1)
        self.password_strength_frame.grid_rowconfigure(2, weight=1)
        self.strength_label.grid(row=0, column=0, sticky="ew")
        self.strength_bar.grid(row=1, column=0, pady=(0, 20), sticky="ew")

    def reset_scoring_variables(self):
        self.num_of_uppercase_chars = 0
        self.num_of_lowercase_chars = 0
        self.num_of_num_chars = 0
        self.num_of_symbol_chars = 0
        self.num_or_symbol_used_in_middle = 0
        self.consecutive_uppercase = 0
        self.consecutive_lowercase = 0
        self.consecutive_numbers = 0
        self.repeated_characters = 0
        self.sequential_letters = 0
        self.sequential_numbers = 0
        self.sequential_symbols = 0
        self.all_scores = {'num_of_char_score': 0, 'num_of_uppercase_chars': 0, 'num_of_lowercase_chars': 0,
                           'num_of_num_chars': 0, 'num_of_symbol_chars': 0, 'num_or_symbol_used_in_middle': 0,
                           'requirements_score': 0, 'only_letter_score': 0, 'only_numbers_score': 0,
                           'only_symbol_score': 0, 'repeat_char_score': 0, 'consec_uppercase_score': 0,
                           'consec_lowercase_score': 0, 'consec_numbers_score': 0, 'sequen_letter_score': 0,
                           'sequen_numbers_score': 0, 'sequen_symbols_score': 0}

    def update_scoring_variables(self, valid_symbols, password):
        current_string = ''
        valid_chars = create_valid_chars_dict(valid_symbols)

        for char in range(len(password)):
            # Count usage of each character type
            if password[char] in string.ascii_lowercase:
                self.num_of_lowercase_chars += 1
            elif password[char] in string.ascii_uppercase:
                self.num_of_uppercase_chars += 1
            elif password[char] in string.digits:
                self.num_of_num_chars += 1
            elif password[char] in valid_symbols:
                self.num_of_symbol_chars += 1

            # Count usage of numbers and symbols not at the start or end of the password
            if char != 0 and char != (len(password) - 1):
                if password[char] in string.digits or password[char] in valid_symbols:
                    self.num_or_symbol_used_in_middle += 1

            # Consecutive Uppercase/Lowercase/Numbers
            if char < len(password) - 1:
                if password[char] in string.ascii_uppercase:
                    if password[char + 1] in string.ascii_uppercase:
                        self.consecutive_uppercase += 1
                elif password[char] in string.ascii_lowercase:
                    if password[char + 1] in string.ascii_lowercase:
                        self.consecutive_lowercase += 1
                elif password[char] in string.digits:
                    if password[char + 1] in string.digits:
                        self.consecutive_numbers += 1

            # Counts repeated chars
            count = valid_chars[password[char]]
            valid_chars[password[char]] = count + 1

            # Sequential Numbers Letters
            current_string += password[char]
            if len(current_string) < 3:
                continue
            if current_string in string.ascii_lowercase or current_string in string.ascii_uppercase:
                self.sequential_letters += len(current_string) - 2
                if len(current_string) > 3:
                    self.sequential_letters -= len(current_string) - 3
            elif current_string in string.digits:
                self.sequential_numbers += len(current_string) - 2
                if len(current_string) > 3:
                    self.sequential_numbers -= len(current_string) - 3
            elif current_string in valid_symbols:
                self.sequential_symbols += len(current_string) - 2
                if len(current_string) > 3:
                    self.sequential_symbols -= len(current_string) - 3
            else:
                current_string = current_string[len(current_string) - 3:]

        # Loop through all valid chars getting the num of time used
        for index in valid_chars:
            if valid_chars[index] > 5:
                self.repeated_characters += int(valid_chars[index] * 0.5)


    def calc_password_strength_score(self, password_length):
        # Positive Scores
        # Password Length
        self.all_scores.update({'num_of_char_score': (password_length * 4)})

        # Password requirements
        requirements_meet = 0
        if self.num_of_uppercase_chars > 0:
            requirements_meet += 1
            self.all_scores.update({'num_of_uppercase_chars': (password_length - self.num_of_uppercase_chars) * 2})
        if self.num_of_lowercase_chars > 0:
            requirements_meet += 1
            self.all_scores.update({'num_of_lowercase_chars': (password_length - self.num_of_lowercase_chars) * 2})
        if self.num_of_num_chars > 0:
            requirements_meet += 1
            self.all_scores.update({'num_of_num_chars': (self.num_of_num_chars * 4)})
        if self.num_of_symbol_chars > 0:
            requirements_meet += 1
            self.all_scores.update({'num_of_symbol_chars': (self.num_of_symbol_chars * 6)})
        if password_length > 12:
            requirements_meet += 1
        self.all_scores.update({'requirements_score': (requirements_meet * 2)})

        # Numbers and symbols not at the start or end of the password
        if self.num_or_symbol_used_in_middle > 0:
            self.all_scores.update({'num_or_symbol_used_in_middle': (self.num_or_symbol_used_in_middle * 2)})

        # Negative Scores
        # Repeated Characters
        self.all_scores.update({'repeat_char_score': self.repeated_characters * -1})

        # Mono-typed password
        if (self.num_of_uppercase_chars > 0 or self.num_of_lowercase_chars > 0) and self.num_of_num_chars == 0 and self.num_of_symbol_chars == 0:
            self.all_scores.update(
                {'only_letter_score': (self.num_of_uppercase_chars + self.num_of_lowercase_chars) * -1})
        elif self.num_of_uppercase_chars == 0 and self.num_of_lowercase_chars == 0 and self.num_of_num_chars > 0 and self.num_of_symbol_chars == 0:
            self.all_scores.update({'only_numbers_score': self.num_of_num_chars * -1})
        elif self.num_of_uppercase_chars == 0 and self.num_of_lowercase_chars == 0 and self.num_of_num_chars == 0 and self.num_of_symbol_chars > 0:
            self.all_scores.update({'only_symbol_score': self.num_of_symbol_chars * -1})

        # Consecutive typing
        if self.consecutive_uppercase != 0:
            self.all_scores.update({'consec_uppercase_score': (self.consecutive_uppercase * -2)})
        if self.consecutive_lowercase != 0:
            self.all_scores.update({'consec_lowercase_score': (self.consecutive_lowercase * -2)})
        if self.consecutive_numbers != 0:
            self.all_scores.update({'consec_numbers_score': (self.consecutive_numbers * -2)})

        # Sequential typing
        if self.sequential_letters != 0:
            self.all_scores.update({'sequen_letter_score': (self.sequential_letters * -3)})
        elif self.sequential_numbers != 0:
            self.all_scores.update({'sequen_numbers_score': (self.sequential_numbers * -3)})
        elif self.sequential_symbols != 0:
            self.all_scores.update({'sequen_symbols_score': (self.sequential_symbols * -3)})

        total_score = 0
        for score in self.all_scores.values():
            total_score += score
        self.update_strength_bar(total_score)

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

    def return_all_scores(self):
        return self.all_scores
