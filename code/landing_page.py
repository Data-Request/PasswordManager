import tkinter
import customtkinter
from PIL import Image
from vault import VaultTab
from generator import GeneratorTab
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
        self.create_vault_image()
        self.create_log_in_widgets()

    def create_tabview(self):
        self.landing_page_tabview = customtkinter.CTkTabview(self, height=self.tabview_height, width=self.tabview_width,
                                                             corner_radius=15, segmented_button_selected_color=GREEN,
                                                             border_width=3, border_color=GREEN, state='disabled',
                                                             text_color=WHITE, command=self.tabview_clicked_event)
        self.landing_page_tabview.place(relx=0.5, rely=0.015, anchor=tkinter.N)
        self.landing_page_tabview.add('Vault')
        self.landing_page_tabview.add("Generator")
        self.landing_page_tabview.add("History")
        self.landing_page_tabview.add("Settings")
        self.landing_page_tabview.tab('Vault').grid_columnconfigure(0, weight=1)

    def create_vault_image(self):
        # Create Vault Image Frame
        self.vault_image_frame = customtkinter.CTkFrame(master=self.landing_page_tabview.tab('Vault'),
                                                        fg_color="transparent")
        self.vault_image_button = customtkinter.CTkButton(master=self.vault_image_frame, text='',
                                                          image=self.vault_image,
                                                          fg_color="transparent", state='disabled')
        # Vault Image Frame Placement
        self.vault_image_frame.place(relx=0.5, rely=0.06, anchor=tkinter.N)
        self.vault_image_frame.grid_columnconfigure(1, weight=1)
        self.vault_image_frame.grid_rowconfigure(1, weight=1)
        self.vault_image_button.grid(row=0, column=0, pady=(0, 20), sticky="n")

    def create_log_in_widgets(self):
        self.account_login = AccountLogin(self)
        self.new_account_button = customtkinter.CTkButton(master=self.landing_page_tabview.tab('Vault'), width=300,
                                                          text="                Don't have an account?",
                                                          text_color=BLACK, image=self.account_image, compound='left',
                                                          command=self.create_account_setup, anchor='w')
        self.new_account_button.place(relx=0.5, rely=0.98, anchor=tkinter.S)

    def create_account_setup(self):
        self.account_login.login_frame.destroy()
        self.account_login.warning_label.destroy()
        self.new_account_button.destroy()
        self.account_setup = AccountSetup(self)

    def tabview_clicked_event(self):
        if self.landing_page_tabview.get() == 'History':
            self.history.refresh_history_tab()

    def initialize_all_tabs(self):
        self.landing_page_tabview.configure(state='normal')
        self.landing_page_tabview.set("Vault")
        VaultTab(self.landing_page_tabview, self.width, self.height, self.account_id)
        GeneratorTab(self.landing_page_tabview, self.width, self.height, self.account_id)
        self.history = HistoryTab(self.landing_page_tabview, self.width, self.height, self.account_id)
        SettingsTab(self.landing_page_tabview, self.account_id)
