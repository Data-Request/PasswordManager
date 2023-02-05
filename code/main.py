import customtkinter
from sql import create_database, create_database_tables
from landing_page import LandingPage

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

if __name__ == '__main__':
    create_database()
    create_database_tables()
    app = LandingPage()
    app.resizable(width=False, height=False)
    app.mainloop()
