import customtkinter as ctk
from gui.login import Login
from gui.result import Result

class App(ctk.CTk) :
    
    def __init__(self):
        super().__init__()

        self.title("Calcul moyenne IUT Lumière Lyon 2")
        self.geometry("1000x600")
        self.minsize(1000,600)

        self.current_frame = None
        self.show_frame("login")
        
    def show_frame(self, frame):
        if self.current_frame is not None:
            self.current_frame.destroy()

        match frame:
            case "login":
                self.current_frame = Login(self)
            case "result":
                self.current_frame = Result(self)

        self.current_frame.pack(pady=30, padx=40, fill="both", expand=True)