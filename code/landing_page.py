import tkinter
import customtkinter
from PIL import Image
from vault import VaultTab
from generator import GeneratorTab
from password_checker import PasswordCheckerTab
from history import HistoryTab
from settings import SettingsTab
from account_setup import AccountSetup
from account_login import AccountLogin
from colors import *


class LandingPage(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configure Window
        self.width = 480
        self.height = 720
        self.geometry(f"{self.width}x{self.height}")
        self.title('Password Manager')
        self.tabview_width = self.width - 50
        self.tabview_height = self.height - 30
        self.account_id = None

        # Images
        self.vault_image = customtkinter.CTkImage(
            Image.open(r"C:\Users\xjord\Desktop\PasswordManager\images\vault-green.png"), size=(180, 180))
        self.account_image = customtkinter.CTkImage(
            Image.open(r"C:\Users\xjord\Desktop\PasswordManager\images\account.png"), size=(20, 20))

        # Initialize
        self.create_tabview()
        self.create_vault_image_frame()
        self.initialize_account_login()

    def create_tabview(self):
        # Creates the main tabview
        self.landing_page_tabview = customtkinter.CTkTabview(self, height=self.tabview_height, width=self.tabview_width,
                                                             corner_radius=15, segmented_button_selected_color=GREEN,
                                                             border_width=3, border_color=GREEN, state='disabled',
                                                             text_color=WHITE, command=self.load_current_tabview)
        self.landing_page_tabview.place(relx=0.5, rely=0.015, anchor=tkinter.N)
        self.landing_page_tabview.add('Vault')
        self.landing_page_tabview.add("Generator")
        self.landing_page_tabview.add("Checker")
        self.landing_page_tabview.add("History")
        self.landing_page_tabview.add("Settings")
        self.landing_page_tabview.tab('Vault').grid_columnconfigure(0, weight=1)

    def create_vault_image_frame(self):
        # Create and place vault image frame
        self.vault_image_frame = customtkinter.CTkFrame(master=self.landing_page_tabview.tab('Vault'),
                                                        fg_color="transparent")
        self.vault_image_button = customtkinter.CTkButton(master=self.vault_image_frame, text='',
                                                          image=self.vault_image,
                                                          fg_color="transparent", state='disabled')
        self.vault_image_frame.place(relx=0.5, rely=0.04, anchor=tkinter.N)
        self.vault_image_frame.grid_columnconfigure(1, weight=1)
        self.vault_image_frame.grid_rowconfigure(1, weight=1)
        self.vault_image_button.grid(row=0, column=0, pady=(0, 20), sticky="n")

    def initialize_account_login(self):
        # Initializes AccountLogin and creates new_account_button
        self.account_login = AccountLogin(self)
        self.new_account_button = customtkinter.CTkButton(master=self.landing_page_tabview.tab('Vault'), width=300,
                                                          text="                Don't have an account?",
                                                          text_color=BLACK, image=self.account_image, compound='left',
                                                          command=self.create_account_setup, anchor='w')
        self.new_account_button.place(relx=0.5, rely=0.98, anchor=tkinter.S)

    def create_account_setup(self):
        self.account_login.login_frame.destroy()
        self.new_account_button.destroy()
        self.account_setup = AccountSetup(self)

    def load_current_tabview(self):
        # Deletes old tab and initialized current tab
        self.delete_all_tabs()
        if self.landing_page_tabview.get() == 'Vault':
            self.vault = VaultTab(self.landing_page_tabview, self.width, self.height, self.account_id)
        elif self.landing_page_tabview.get() == 'Generator':
            self.generator = GeneratorTab(self.landing_page_tabview, self.width, self.height, self.account_id)
        elif self.landing_page_tabview.get() == 'Checker':
            self.checker = PasswordCheckerTab(self.landing_page_tabview, self.width)
        elif self.landing_page_tabview.get() == 'History':
            self.history = HistoryTab(self.landing_page_tabview, self.width, self.height, self.account_id)
        elif self.landing_page_tabview.get() == 'Settings':
            self.settings = SettingsTab(self.landing_page_tabview, self.account_id)

    def delete_all_tabs(self):
        # Try to delete an instance of each class if we are not on that classes tab
        if self.landing_page_tabview.get() != 'Vault':
            try:
                del self.vault
            except AttributeError:
                pass

        if self.landing_page_tabview.get() != 'Generator':
            try:
                del self.generator
            except AttributeError:
                pass

        if self.landing_page_tabview.get() != 'Checker':
            try:
                del self.checker
            except AttributeError:
                pass

        if self.landing_page_tabview.get() != 'History':
            try:
                del self.history
            except AttributeError:
                pass

        if self.landing_page_tabview.get() != 'Settings':
            try:
                del self.settings
            except AttributeError:
                pass

    def enabled_tabview(self):
        # Changes state to allow clicking of tabs after user is logged in called from account_login
        self.landing_page_tabview.configure(state='normal')
        self.landing_page_tabview.set("Vault")
        self.vault_image_frame.destroy()
        self.new_account_button.destroy()
        self.vault = VaultTab(self.landing_page_tabview, self.width, self.height, self.account_id)
