import tkinter
import customtkinter

MAX_HISTORY_ENTRIES = 5


class SettingsTab:
    def __init__(self, landing_tabview, account_id):
        super().__init__()
        self.landing_tabview = landing_tabview

        self.settings_frame = customtkinter.CTkFrame(master=self.landing_tabview.tab('Settings'), fg_color="transparent")
        self.appearance_mode_label = customtkinter.CTkLabel(master=self.settings_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_option_menu = customtkinter.CTkOptionMenu(self.settings_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.scaling_label = customtkinter.CTkLabel(self.settings_frame, text="UI Scaling:", anchor="w")
        self.scaling_option_menu = customtkinter.CTkOptionMenu(self.settings_frame,
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.settings_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.appearance_mode_label.grid(row=0, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_option_menu.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.scaling_label.grid(row=2, column=0, padx=20, pady=(10, 0))
        self.scaling_option_menu.grid(row=3, column=0, padx=20, pady=(10, 20))

        # Set Defaults
        self.appearance_mode_option_menu.set('Dark')
        self.scaling_option_menu.set('100%')

    @staticmethod
    def change_appearance_mode_event(new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    @staticmethod
    def change_scaling_event(new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
