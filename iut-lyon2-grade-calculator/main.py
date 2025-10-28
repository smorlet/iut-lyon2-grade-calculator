from gui import App, init_theme


def main():
    init_theme()
    app = App()
    app.mainloop()  # boucle principale Tkinter


if __name__ == "__main__":
    main()