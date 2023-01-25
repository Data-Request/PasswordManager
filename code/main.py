import tkinter
import customtkinter
import sqlite3
from generator import GeneratorTab
from settings import Settings
from colors import *

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
connection = sqlite3.connect('data.db')
cursor = connection.cursor()


class LandingPage(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configure Window
        self.width = 480
        self.height = 720
        self.geometry(f"{self.width}x{self.height}")
        # app.resizable(width=False, height=False)
        self.title('Password Manager')
        self.tabview_width = self.width - 50
        self.tabview_height = self.height - 30
        # self.attributes('-fullscreen', True)
        #self.tabview_width = self.winfo_screenwidth() - 50
        #self.tabview_height = self.winfo_screenheight() - 50

        # Create Tabview
        self.landing_page_tabview = customtkinter.CTkTabview(self, height=self.tabview_height, width=self.tabview_width,
                                                             corner_radius=15, segmented_button_selected_color=BLUE,
                                                             border_width=3, border_color=WHITE, state='disabled')
        self.landing_page_tabview.place(relx=0.5, rely=0.015, anchor=tkinter.N)
        self.landing_page_tabview.add('Vault')
        self.landing_page_tabview.add("Generator")
        self.landing_page_tabview.add("History")
        self.landing_page_tabview.add("Settings")
        self.landing_page_tabview.tab('Vault').grid_columnconfigure(0, weight=1)

        self.warning_label = customtkinter.CTkLabel(master=self.landing_page_tabview.tab('Vault'),
                                                    text='', text_color=RED)
        self.warning_label.place(relx=0.5, rely=1, anchor=tkinter.S)

        # Initialize
        self.create_log_in_widgets()
        self.generator = GeneratorTab(self.landing_page_tabview, self.width, self.height)
        self.settings = Settings(self.landing_page_tabview)

    def create_log_in_widgets(self):
        # Create Login Button Frame
        self.login_frame = customtkinter.CTkFrame(master=self.landing_page_tabview.tab('Vault'), fg_color="transparent")
        self.verify_text = tkinter.StringVar(value="Your vault is locked. Verify your identity to continue.")
        self.username = customtkinter.CTkEntry(master=self.login_frame, placeholder_text="Username or Email")
        self.password = customtkinter.CTkEntry(master=self.login_frame, placeholder_text="Master Password")
        self.login_button = customtkinter.CTkButton(master=self.login_frame, text='Log in',
                                                    command=lambda: self.login_button_event(self.warning_label))
        self.verify_label = customtkinter.CTkLabel(master=self.login_frame, text_color=WHITE,
                                                   text='Your vault is locked. Verify your identity to continue.')
        self.new_account_button = customtkinter.CTkButton(master=self.login_frame, text="Don't have an account?",
                                                          command=self.account_setup)
        # Placement of all items
        self.login_frame.place(relx=0.5, rely=0.3, anchor=tkinter.N)
        self.login_frame.grid_columnconfigure(0, weight=1)
        self.login_frame.grid_rowconfigure(5, weight=1)
        self.username.grid(row=0, column=0, pady=(0, 20), sticky="ew")
        self.password.grid(row=1, column=0, pady=(0, 20), sticky="ew")
        self.login_button.grid(row=2, column=0, pady=(0, 20), sticky="ew")
        self.verify_label.grid(row=3, column=0, pady=(0, 20), sticky="ew")
        self.new_account_button.grid(row=4, column=0, pady=(200, 0), sticky="ew")

    def account_setup(self):
        self.login_frame.destroy()
        # Create New Account Frame
        self.new_account_frame = customtkinter.CTkFrame(master=self.landing_page_tabview.tab('Vault'), fg_color="transparent")
        self.new_username = customtkinter.CTkEntry(master=self.new_account_frame, placeholder_text="Username")
        self.new_email = customtkinter.CTkEntry(master=self.new_account_frame, placeholder_text="Email")
        self.new_master_password = customtkinter.CTkEntry(master=self.new_account_frame, placeholder_text="Master Password")
        self.new_master_password_verify = customtkinter.CTkEntry(master=self.new_account_frame, placeholder_text="Renter Master Password")
        self.continue_button = customtkinter.CTkButton(master=self.new_account_frame, text="Continue",
                                                       command=self.check_valid_new_account)
        # New Account Placement
        self.new_account_frame.place(relx=0.5, rely=0.3, anchor=tkinter.N)
        self.new_account_frame.grid_columnconfigure(0, weight=1)
        self.new_account_frame.grid_rowconfigure(5, weight=1)
        self.new_username.grid(row=0, column=0, pady=(0, 20), sticky="ew")
        self.new_email.grid(row=1, column=0, pady=(0, 20), sticky="ew")
        self.new_master_password.grid(row=2, column=0, pady=(0, 20), sticky="ew")
        self.new_master_password_verify.grid(row=3, column=0, pady=(0, 20), sticky="ew")
        self.continue_button.grid(row=4, column=0, pady=(40, 20), sticky="ew")

    def check_valid_new_account(self):
        username = self.new_username.get()
        email = self.new_email.get()
        master_password = self.new_master_password.get()
        master_password_verify = self.new_master_password_verify.get()

        # todo remove once finish testing
        self.create_person_table()

        # Reset in case method is called twice in a row for different reasons
        self.reset_new_account_text_color()

        if self.check_for_blank_field(username, email, master_password, master_password_verify):
            return
        if master_password != master_password_verify:
            self.new_master_password.configure(text_color=RED)
            self.new_master_password_verify.configure(text_color=RED)
            self.warning_label.configure(text='Passwords do not match.')
            return

        cursor.execute('SELECT username FROM Person WHERE username = ?', username)
        username_row = cursor.fetchone()
        cursor.execute('SELECT email FROM Person WHERE email = ?', email)
        email_row = cursor.fetchone()
        connection.commit()

        if username_row is None:
            if email_row is None:
                command = 'INSERT INTO Person VALUES (?,?,?)'
                cursor.execute(command, (username, email, master_password))
                connection.commit()
                self.new_account_frame.destroy()
                self.create_log_in_widgets()
                self.warning_label.configure(text='')
            else:
                self.new_email.configure(text_color=RED)
                self.warning_label.configure(text='Email already in use.')
        else:
            self.new_username.configure(text_color=RED)
            self.warning_label.configure(text='Username taken.')

    def reset_new_account_text_color(self):
        self.new_username.configure(text_color=WHITE)
        self.new_master_password.configure(text_color=WHITE)
        self.new_master_password_verify.configure(text_color=WHITE)

    def check_for_blank_field(self, username, email, master_password, master_password_verify):
        if username == '':
            self.warning_label.configure(text='Username is blank.')
            return True
        elif email == '':
            self.warning_label.configure(text='Email is blank.')
            return True
        elif master_password == '':
            self.warning_label.configure(text='Password is blank.')
            return True
        elif master_password_verify == '':
            self.warning_label.configure(text='Please verify password.')
            return True
        else:
            return False

    @staticmethod
    def create_person_table():
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Person (
            username TEXT,
            email TEXT,
            master_password TEXT
        )
        """)
        connection.commit()

    def login_button_event(self, warning_label):
        username = self.username.get()
        password = self.password.get()
        if username == '':
            pass
        elif username == 'a' and password == 'a':
            self.landing_page_tabview.configure(state='normal')
            self.landing_page_tabview.set("Generator")
            self.login_frame.destroy()


if __name__ == '__main__':
    app = LandingPage()
    app.mainloop()
