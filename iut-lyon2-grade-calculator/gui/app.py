import customtkinter as ctk
from .frames import Login, Result

class App(ctk.CTk) :
    
    def __init__(self) :
        #main setup
        super().__init__()
        self.title("Calcul moyenne IUT Lumière Lyon 2")
        self.geometry("900x600")
        self.minsize(900,600)
        
        #frame
        self.menu = Login(self)