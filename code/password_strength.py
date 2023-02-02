import tkinter
import customtkinter
import string
from colors import *

# todo fix repeated characters scoring need a better way to calculate
# todo fix consecutive numbers calc


class PasswordStrength:
    def __init__(self, landing_tabview, parent):
        super().__init__()

        # General Setup
        self.parent = parent
        self.landing_tabview = landing_tabview

        # Password Variables
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
        self.all_scores = {'num_of_char_score': 0, 'num_of_uppercase_chars': 0, 'num_of_lowercase_chars': 0,
                           'num_of_num_chars': 0, 'num_of_symbol_chars': 0, 'num_or_symbol_used_in_middle': 0,
                           'requirements_score': 0, 'only_letter_score': 0, 'only_numbers_score': 0,
                           'only_symbol_score': 0, 'repeat_char_score': 0, 'consec_uppercase_score': 0,
                           'consec_lowercase_score': 0, 'consec_number_score': 0, 'sequen_letter_score': 0,
                           'sequen_number_score': 0, 'sequen_symbols_score': 0}

        # Initialize
        self.create_generator_password_strength_frame()

    def create_generator_password_strength_frame(self):
        if self.parent.name == 'Generator':
            self.password_strength_frame = customtkinter.CTkFrame(master=self.landing_tabview.tab('Generator'),
                                                                  fg_color="transparent")
        else:
            self.password_strength_frame = customtkinter.CTkFrame(master=self.landing_tabview.tab('Checker'),
                                                                  fg_color="transparent")
        self.strength_label = customtkinter.CTkLabel(master=self.password_strength_frame, text="Password Strength:")
        self.strength_bar = customtkinter.CTkProgressBar(self.password_strength_frame, width=350, height=20)
        # Password Strength Placement
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
        self.repeat_char = 0
        self.sequential_letters = 0
        self.sequential_numbers = 0
        self.sequential_symbols = 0
        self.all_scores = {'num_of_char_score': 0, 'num_of_uppercase_chars': 0, 'num_of_lowercase_chars': 0,
                           'num_of_num_chars': 0, 'num_of_symbol_chars': 0, 'num_or_symbol_used_in_middle': 0,
                           'requirements_score': 0, 'only_letter_score': 0, 'only_numbers_score': 0,
                           'only_symbol_score': 0, 'repeat_char_score': 0, 'consec_uppercase_score': 0,
                           'consec_lowercase_score': 0, 'consec_number_score': 0, 'sequen_letter_score': 0,
                           'sequen_number_score': 0, 'sequen_symbols_score': 0}

    def update_basic_scoring_variables(self, index, char, valid_symbols, password_length):
        if char in string.ascii_lowercase:
            self.num_of_lowercase_chars += 1
        elif char in string.ascii_uppercase:
            self.num_of_uppercase_chars += 1
        elif char in string.digits:
            self.num_of_num_chars += 1
        elif char in valid_symbols:
            self.num_of_symbol_chars += 1

        if index != 0 and index != (password_length - 1):
            if char in string.digits or char in valid_symbols:
                self.num_or_symbol_used_in_middle += 1

    def update_advanced_scoring_variables(self, valid_symbols, password):
        current_string = ''
        for char in range(len(password)):
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

            # Looks for repeated chars
            for char_b in range(len(password)):
                if password[char] == password[char_b] and char != char_b:
                    self.repeat_char += 1

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

    def calc_password_strength_score(self, password_length):
        # Positive Scores
        requirements_meet = 0
        self.all_scores.update({'num_of_char_score': (password_length * 4)})
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

        if self.num_or_symbol_used_in_middle > 0:
            self.all_scores.update({'num_or_symbol_used_in_middle': (self.num_or_symbol_used_in_middle * 2)})

        # Negative Scores
        #self.all_scores.update({'repeat_char_score': self.repeat_char * -1})
        if (self.num_of_uppercase_chars > 0 or self.num_of_lowercase_chars > 0) and self.num_of_num_chars == 0 and self.num_of_symbol_chars == 0:
            self.all_scores.update({'only_letter_score': (self.num_of_uppercase_chars + self.num_of_lowercase_chars) * -1})
        elif self.num_of_uppercase_chars == 0 and self.num_of_lowercase_chars == 0 and self.num_of_num_chars > 0 and self.num_of_symbol_chars == 0:
            self.all_scores.update({'only_numbers_score': self.num_of_num_chars * -1})
        elif self.num_of_uppercase_chars == 0 and self.num_of_lowercase_chars == 0 and self.num_of_num_chars == 0 and self.num_of_symbol_chars > 0:
            self.all_scores.update({'only_symbol_score': self.num_of_symbol_chars * -1})

        if self.consecutive_uppercase != 0:
            self.all_scores.update({'consec_uppercase_score': (self.consecutive_uppercase * -2)})
        if self.consecutive_lowercase != 0:
            self.all_scores.update({'consec_lowercase_score': (self.consecutive_lowercase * -2)})
        if self.consecutive_numbers != 0:
            self.all_scores.update({'consec_numbers_score': (self.consecutive_numbers * -2)})

        if self.sequential_letters != 0:
            self.all_scores.update({'sequen_letter_score': (self.sequential_letters * -3)})
        elif self.sequential_numbers != 0:
            self.all_scores.update({'sequen_number_score': (self.sequential_numbers * -3)})
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
