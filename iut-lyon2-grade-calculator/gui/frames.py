import customtkinter as ctk
from .styles import font_text
from selenium_part import connection_works, path_connection

class Login(ctk.CTkFrame):

    def __init__(self, root):
        super().__init__(root)
        
        #widget reused later
        self.feedback = ctk.CTkLabel(self, text="", font=font_text)
        self.username_field = ctk.CTkEntry(self, placeholder_text= "Nom d'utilisateur", width=400, height = 40)
        self.password_field = ctk.CTkEntry(self, placeholder_text= "Mot de passe", width=400, height = 40, show="*")
        self.display_button = ctk.CTkButton(self, text="Afficher", font=font_text,  width=100, height=30, corner_radius=10,command=lambda:self.toggle_visibility())
        #static widget
        headline = ctk.CTkLabel(self, text = "Bienvenue", font=("Arial",34,"bold"))
        subhead = ctk.CTkLabel(self, text = "Veuillez saisir vos informations pour accéder à vos moyennes", font=font_text)
        notabene = ctk.CTkLabel(self, text = "Les moyennes affichées prennent en compte les coefficients, et le bonus sport s'il y'en a un.", font=("Arial",16,"italic"))
        connect_button = ctk.CTkButton(self, text = "Connexion", font=("Arial",18), width=180, height = 40, command=lambda:self.try_connexion(root))

        #pack widget
        headline.pack(pady=(70,0),padx=(0,274))
        subhead.pack() 
        self.username_field.pack(pady=(30,30))
        self.password_field.pack(padx=0)
        self.display_button.pack(pady=10)
        self.feedback.pack()
        connect_button.pack(pady=10)
        notabene.pack(pady=(35,0))

        #key bind
        root.bind('<Return>', lambda event: connect_button.invoke())

        self.pack(pady=30, padx=50, fill="both", expand=True)

    def toggle_visibility(self):
        if self.password_field.cget("show") == "*" :
            self.password_field.configure(show="") 
            self.display_button.configure(text="Masquer")
        else:
            self.password_field.configure(show="*")  
            self.display_button.configure(text="Afficher")
    
    def try_connexion(self, root) :
        self.feedback.configure(text="Chargement...", text_color="white")
        root.update_idletasks()
        status = connection_works(self.username_field, self.password_field)
        match status :
            case "invalid psw":
                self.feedback.configure(text="Nom d'utilisateur et mot de passe non valide. Entrez de nouveau vos informations d'utilisateur.", text_color="red")
                self.password_field.delete(0,"end")
            case "locked acc":
                self.feedback.configure(text="Trop de tentative échoué, compte vérouillé. Veuillez réessayer ultérieurement.", text_color="grey")
                self.username_field.delete(0,"end")
                self.password_field.delete(0,"end")
            case "too many users":
                self.feedback.configure(text="Nombre d'utilisateurs ayant simultanément ouvert une session dans le système trop élevé. Veuillez réessayer ultérieurement.", text_color="grey")
                self.username_field.delete(0,"end")
                self.password_field.delete(0,"end")
            case "valid psw" | "valid psw but other sess":
                self.feedback.configure(text="Nom d'utilisateur et mot de passe valide. Veuillez patienter...", text_color="white")
                self.show_averages(status)
            case "error":
                self.feedback.configure(text="Une erreur est survenue. Veuillez réessayer ultérieurement.", text_color="grey")

    def show_averages(self, status):
        if path_connection(status):
            pass
        else :
            self.feedback.configure(text="Désolé, nous n'avons pas pu accéder à vos notes. Veuillez relancer réessayer ultérieurement.", text_color="grey")

    def frame_switch(self):
        pass

class Result(ctk.CTkFrame):

    def __init__(self, root):
        super().__init__(root)