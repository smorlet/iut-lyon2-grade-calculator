import customtkinter as ctk
from .frames.login import Login
from .frames.result import Result

class App(ctk.CTk) :
    
    def __init__(self):
        super().__init__()

        self.title("Calcul moyenne IUT Lumière Lyon 2")
        self.geometry("1000x600")
        self.minsize(1000,600)
        
        self.current_frame = Login(self)
        self.current_frame.pack(pady=30, padx=40, fill="both", expand=True)
        
    def show_frame(self, frame):
        self.current_frame.pack_forget()
        self.current_frame = frame
        self.current_frame.pack(pady=30, padx=40, fill="both", expand=True)