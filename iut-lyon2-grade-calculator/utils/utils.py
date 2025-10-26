def toggle_visibility(field, button):
    if field.cget("show") == "*" :
        field.configure(show="") 
        button.configure(text="Masquer")
    else:
        field.configure(show="*")  # masque le mpasse
        button.configure(text="Afficher")  # change le texte du bouton    
