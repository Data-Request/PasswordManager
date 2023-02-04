import customtkinter
from sql import create_database_tables
from landing_page import LandingPage


# todo add email verification via email for master password resets
# todo add remember username feature, add settings to remove it
# todo sign out button
# todo fix issue with opening edit/add item then clicking change to change tabs

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

if __name__ == '__main__':
    create_database_tables()
    app = LandingPage()
    app.resizable(width=False, height=False)
    app.mainloop()
