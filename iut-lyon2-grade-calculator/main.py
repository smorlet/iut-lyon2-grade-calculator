from gui import App, init_theme
from selenium_part import create_driver, quit_driver


def main():
    create_driver()
    init_theme()
    app = App()
    app.mainloop()  # boucle principale Tkinter
    quit_driver()


if __name__ == "__main__":
    main()