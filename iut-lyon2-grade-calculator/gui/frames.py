import customtkinter as ctk
from .styles import font_text
from utils import toggle_visibility

class Login(ctk.CTkFrame):

    def __init__(self, root):
        super().__init__(root)
        
        #widget
        headline = ctk.CTkLabel(self, text = "Bienvenue", font=("Arial",34,"bold"))
        subhead = ctk.CTkLabel(self, text = "Veuillez saisir vos informations pour accéder à vos moyennes", font=font_text)
        feedback = ctk.CTkLabel(self, text="", font=font_text)
        notabene = ctk.CTkLabel(self, text = "Les moyennes affichées prennent en compte les coefficients, et le bonus sport s'il y'en a un.", font=("Arial",16,"italic"))
        username_field = ctk.CTkEntry(self, placeholder_text= "Nom d'utilisateur", width=400, height = 40)
        password_field = ctk.CTkEntry(self, placeholder_text= "Mot de passe", width=400, height = 40, show="*")
        display_button = ctk.CTkButton(self, text="Afficher", font=font_text,  width=100, height=30, corner_radius=10,command=lambda:toggle_visibility(password_field, display_button))
        connect_button = ctk.CTkButton(self, text = "Connexion", font=("Arial",18), width=180, height = 40)

        #pack widget
        headline.pack(pady=(70,0),padx=(0,256))
        subhead.pack() 
        username_field.pack(pady=(50,30))
        password_field.pack(padx=0)
        display_button.pack(pady=10)
        feedback.pack()
        connect_button.pack(pady=10)
        notabene.pack(pady=(35,0))

        #key bind
        root.bind('<Return>', lambda event: connect_button.invoke())

        self.pack(pady=30, padx=50, fill="both", expand=True)


class Result(ctk.CTkFrame):

    def __init__(self, root):
        super().__init__(root)