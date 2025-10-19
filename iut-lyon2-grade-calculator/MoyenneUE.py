from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import customtkinter as ctk
import sys

'''INITIALISATION'''

#selenium

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")  
chrome_options.add_argument("--no-sandbox")  
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get("https://iut-extranet.univ-lyon2.fr")


#custom tkinter

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

font_text = ("Arial",16)
font_UE = ("Arial",18,"bold","underline")
font_moy = ("Arial",16,"bold")

root = ctk.CTk()
root.geometry("900x600")

login = ctk.CTkFrame(root)
result = ctk.CTkScrollableFrame(root)  #scrollable car bcp de notes 


'''FONCTION'''

#FONCTION GENERALE UTILE

#liste mdp déjà utilisé ou usrn bloqué
psw_alr_used = {}
blocked_usrn = []
current_connexion = {}

#fenetre fermé
def root_closing() :
    root.destroy()
    sys.exit()
root.protocol("WM_DELETE_WINDOW", root_closing)

#afficher mdp
def toggle_visibility(field, button):
    if field.cget("show") == "*" :
        field.configure(show="") 
        button.configure(text="Masquer")
    else:
        field.configure(show="*")  # masque le mpasse
        button.configure(text="Afficher")  # change le texte du bouton    

#obtenir la frame actuelle
def get_current_frame():
    return root.winfo_children()[-1]

#switch de frame
def switch_frame(fg_frame,frame):
        
    fg_frame.pack_forget()
    frame.pack(pady=30, padx=50, fill="both", expand=True)
    root.focus_set()

    if frame==login :
        #remasque le mdp
        if password_field.cget("show") != '*' :
            toggle_visibility(password_field, toggle_psw)
        root.bind('<Return>', lambda event : connect.invoke())  #bind du raccourci en fonction de la frame pour eviter d'eventuelle bug
        reset_scroll(fg_frame)  
        
    elif frame == result :
        root.unbind('<Return>') #unbind du raccourci 

#switch semestre
def switch_sem(option) :
    
    #est ce que c'est le semestre deja affiché ou pas
    if option != f"Semestre {semestre.first_selected_option.get_attribute('value')}":
        ls_sem.set("Chargement...")
        root.update_idletasks() 
        semestre.select_by_value(option.replace("Semestre ",""))
        clear_frame(result)
        reset_scroll(result)
        configure_result()

    
#bouton present ou nan 
def button_found(button_ID) :
    try:
        driver.find_element(By.ID, button_ID)
        return True  # Si trouvé, retourne True
    except NoSuchElementException:
        return False

#virer le contenu d'une frame
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def reset_scroll(frame):
    frame._parent_canvas.yview_moveto(0)
    
def rename_matiere(matiere, UE):
    return UE + " " + matiere.split(" - ", 1)[1]

#CONFIGURATION FRAME 
  
#taille, frame, texte et champs
def configure_login() :
    
    global connect, toggle_psw, password_field
    
    text1 = ctk.CTkLabel(login, text = "Bienvenue", font=("Arial",34,"bold"))
    text1.pack(pady=(70,0),padx=(0,256))    
        
    text2 = ctk.CTkLabel(login, text = "Veuillez saisir vos informations pour accéder à vos moyennes", font=font_text)
    text2.pack()  
        
    username_field = ctk.CTkEntry(login, placeholder_text= "Nom d'utilisateur", width=400, height = 40)
    username_field.pack(pady=(50,30))
        
    password_field = ctk.CTkEntry(login, placeholder_text= "Mot de passe", width=400, height = 40, show="*")
    password_field.pack(padx=0)
    
    toggle_psw = ctk.CTkButton(login, text="Afficher", font=font_text,  width=100, height=30, border_width = 0)
    toggle_psw.configure(command=lambda:toggle_visibility(password_field, toggle_psw))
    toggle_psw.pack(pady=10)
    
    #message apres id rentré
    feedback = ctk.CTkLabel(login, text="", font=font_text)
    feedback.pack()
    
    connect = ctk.CTkButton(login, text = "Connexion", font=("Arial",18), width=180, height = 40, command=lambda:connexion(username_field, password_field, feedback))
    connect.pack(pady=10)
    root.bind('<Return>', lambda event : connect.invoke())
    
    textinfo = ctk.CTkLabel(login, text = "Les moyennes affichées prennent en compte les coefficients, et le bonus sport s'il y'en a un.", font=("Arial",16,"italic"))
    textinfo.pack(pady=(35,0))    
    
#taille et frame
def configure_result() :
    
    #bouton semestre
    global semestre, ls_sem
    semestre = Select(driver.find_element(By.ID, "MainContent_MainContent_ddlSemestre"))
    
    #est ce que plusieurs semestre sont dispo
    if len(semestre.options)>1 :
        options = []
        for num_sem in semestre.options : #liste avec les differents semestres
            options.append(f"Semestre {num_sem.get_attribute('value')}")
        ls_sem = ctk.CTkComboBox(result, values=options, state = "readonly", command=switch_sem, 
                                 button_color="#1F538D", width=150, height=35, corner_radius=6, font=font_text)
        ls_sem.set(f"Semestre {semestre.first_selected_option.get_attribute('value')}")
        ls_sem.pack(anchor="w", padx=25, pady=(30, 10))
   
    #essaye de voir s'il y'a une note en sport
    try :
        titre_UE, moyenne_UE, matiere_info, bonus = collect_grades()
        show_grades(titre_UE, moyenne_UE, matiere_info, bonus)
    except :
        titre_UE, moyenne_UE, matiere_info = collect_grades()
        show_grades(titre_UE, moyenne_UE, matiere_info)
    
    back = ctk.CTkButton(result, text = "Retour page connexion", font=font_text, width=150, height = 40, command=lambda:switch_frame(result, login))
    back.pack(padx=25, pady=20)
    


#FONCTION

#connexion à l'intranet
def connexion(u_field, p_field, fb) :
    
    fb.configure(text="Chargement...", text_color = "white")
    root.update_idletasks() 
    
    username = u_field.get()
    password = p_field.get()
    
    #evite de tester plusieurs fois le mdp et "bloquer" le compte, ou de reessayer avec un id qu'on sait "bloqué"
    if username in blocked_usrn :
        p_field.delete(0,"end")
        fb.configure(text="Trop de tentative échoué, compte vérouillé. Veuillez réessayer ultérieurement.", text_color="grey")
        return
    if (username in psw_alr_used and psw_alr_used[username] == password) :  
        p_field.delete(0,"end")
        fb.configure(text="Nom d'utilisateur et mot de passe non valide. Entrez de nouveau vos informations d'utilisateur.", text_color="red")
        return
    
    #si c'est un cas de connexion apres une autre
    if driver.current_url == "https://iut-intranet2.univ-lyon2.fr/Etudiants/Notes" :
        
        #evite de recalculer deux fois de suite les meme notes
        if username in current_connexion and current_connexion[username]==password :
            switch_frame(login, result)
            fb.configure(text="")
            p_field.delete(0,"end")
            u_field.delete(0,"end")
            return
        
        #sinon, se deconnecter de l'ancien compte sur selenium
        driver.find_element(By.ID, "dslMain").click()
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "signindiv"))).click()
        
    username_field_html = driver.find_element(By.ID,"username")
    username_field_html.send_keys(username)
    
    password_field_html = driver.find_element(By.ID,"password")
    password_field_html.send_keys(password)
    
    driver.find_element(By.ID, "btnSubmit_6").click()
    
    
    try :
        
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "table_LoginPage_4")))        
        message = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, "brcd-snackbar__message"))).text
        
        if message == "Nom d'utilisateur ou mot de passe non valide. Entrez de nouveau vos informations d'utilisateur." :  
            psw_alr_used[username] = password
            p_field.delete(0,"end")
            fb.configure(text="Nom d'utilisateur et mot de passe non valide. Entrez de nouveau vos informations d'utilisateur.", text_color="red")
            return
        
        elif message == "Votre compte est verrouillé." :
            blocked_usrn.append(username)
            p_field.delete(0,"end")
            fb.configure(text="Trop de tentative échoué, compte vérouillé. Veuillez réessayer ultérieurement.", text_color="grey")
            return
        raise TimeoutException
        
    except (TimeoutException,NoSuchElementException):
        fb.configure(text="Nom d'utilisateur et mot de passe valide. Veuillez patienter...", text_color="white")
        root.update_idletasks() 
        nb_try=0
        #while pour tester si l'acces au note réussit (des bugs de chargement ou un compte bloqué peuvent renvoyé une erreur)
        pdw = True #path doesnt works
        while pdw and nb_try <= 3 : 
            pdw = path_connexion()
            nb_try+=1
        if pdw:
            fb.configure(text="Désolé, nous n'avons pas pu accéder à vos notes. Veuillez relancer le programme et réessayer ultérieurement.", text_color="grey")
        else : 
            #remettre au propre la frame login + result avant de changer
            clear_frame(result)
            switch_frame(login, result)
            configure_result()
            
            fb.configure(text="")
            p_field.delete(0,"end")
            u_field.delete(0,"end")
            
            current_connexion.clear()
            current_connexion[username] = password

                
#navigation vers les differentes fenetre pour arriver au note, renvoie faux si un probleme intervient
def path_connexion():
    #PAGE AVERTISSEMENT (OPTIONNEL)
    
    if driver.current_url == "https://iut-extranet.univ-lyon2.fr/dana-na/auth/url_MJ55eorq301ZSVoH/welcome.cgi?p=user%2Dconfirm" :
        try :
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "btnContinue"))).click()
        except TimeoutException:
            return True
        
    #PAGE 2 BIENVENUE
    
    #appuie sur "signet web" avant si besoin
    for i in range(2):
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "0-header"))).click()
   
    #verif que ce soit pas "fichier" d'ouvert 
    try:
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "web_bookmark_card_0"))).click()
    except TimeoutException:
        try:
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "0-header"))).click()
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "web_bookmark_card_0"))).click()
        except TimeoutException:
            return True 
    
    
    #PAGE 3 ACCUEIL
    try :
        button = driver.find_element(By.ID, "MainContent_accesrapidesAccueil_rptAccesRapides_HyperLink1_1")
        driver.execute_script("arguments[0].scrollIntoView();", button)
        time.sleep(1)
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "MainContent_accesrapidesAccueil_rptAccesRapides_HyperLink1_1"))).click()
    except TimeoutException:
         return True    
     
    return False

#récupération et calcul des notes
def collect_grades() :
    
    titre_UE = {}
    moyenne_UE = {}
    matiere_info = {}
    
    #recup les titre UE dans un dico pour pouvoir trier les notes plus facilement
    class_UE = driver.find_elements(By.XPATH, "(//div[@class='container-fluid'][2])//div[@class='libelle-ue']")
    for no, UE in enumerate(class_UE, start=1) :
        key = "UE" + str(no)
        titre_UE[key] = UE.text
        
    for UE in titre_UE:
        
        #si il y'a l'UE contenant la note de sport, on l'a traite différement
        if "sport" in titre_UE[UE].lower() :
            class_notes = driver.find_elements(By.XPATH, f'//span[contains(text(), "{titre_UE[UE]}")]/ancestor::div[@class="libelle-ue"]/following-sibling::div[@class="pt-2"][1]//span[contains(text(), "Moyenne matière")]')
            class_matiere = driver.find_elements(By.XPATH, f'//span[contains(text(), "{titre_UE[UE]}")]/ancestor::div[@class="libelle-ue"]/following-sibling::div[@class="pt-2"]//div[@class="row p-1 bg-dark text-white ms-0 me-0"]//div[contains(@class, "col-md")]/span')
            
            if class_notes[0].text != "Moyenne matière :" :
                note = class_notes[0].text
                note = float(note.replace("Moyenne matière : ", "").replace(",","."))
                matiere = class_matiere[0].text
                matiere = UE + " " + matiere[8:]
                
                matiere_info[matiere] = {"UE" : UE, "note" : note, "coeff" : 0}
                
                #application points bonus
                bonus = sport_bonus(note)
                for UE in moyenne_UE :
                    moyenne_UE[UE] = round(moyenne_UE[UE]+bonus,2)
                
        else : 
            #liste des notes, des matières, et des coeff de l'UE en question
            class_notes = driver.find_elements(By.XPATH, f'//span[contains(text(), "{titre_UE[UE]}")]/ancestor::div[@class="libelle-ue"]/following-sibling::div[@class="pt-2"][1]//span[contains(text(), "Moyenne matière")]')
            class_matiere = driver.find_elements(By.XPATH, f'//span[contains(text(), "{titre_UE[UE]}")]/ancestor::div[@class="libelle-ue"]/following-sibling::div[@class="pt-2"]//div[@class="row p-1 bg-dark text-white ms-0 me-0"]//div[contains(@class, "col-md")]/span')
            class_coeff = driver.find_elements(By.XPATH, f'//span[contains(text(), "{titre_UE[UE]}")]/ancestor::div[@class="libelle-ue"]/following-sibling::div[@class="pt-2"]//div[@class="row p-1 bg-dark text-white ms-0 me-0"]//div[contains(@class, "col-md-2")]//small[contains(text(), "coefficient")]')
            
            note_tot = 0
            coeff_tot = 0
            
                
            for i in range(len(class_notes)):
                
                if class_notes[i].text != "Moyenne matière :" :    #évite de prendre en compte les notes inexistantes du à des absences
                    note = class_notes[i].text
                    note = float(note.replace("Moyenne matière : ", "").replace(",",".")) #extrait la note en elle même
                    
                    matiere = rename_matiere(class_matiere[i].text,UE)
                    
                    """
                    if matiere.startswith("R") :            #rename "propre" de la matière
                        matiere = UE + " " + matiere[8:]    #"UE + {matière}" pour différencier les matières venant affecter les moyennes de chaque UE
                    elif matiere.startswith("SAÉ") :
                        matiere = UE + " " + matiere[:3] + matiere[8:]
                    """

                    coeff = class_coeff[i].text
                    coeff = float(coeff.replace("coefficient : ", "").replace(",","."))  #extrait la note en elle même
                    
                    note_tot += note * coeff
                    coeff_tot += coeff
                    
                    matiere_info[matiere] = {"UE" : UE, "note" : note, "coeff" : coeff}
            
            if coeff_tot > 0 :      #verif que l'UE à au moins une note (au cas ou ya des absences)
                moy = round(note_tot / coeff_tot,2)
                moyenne_UE[titre_UE[UE]] = moy
    
    try :
        bonus
        return titre_UE, moyenne_UE, matiere_info, bonus
    except :
        return titre_UE, moyenne_UE, matiere_info
            
#point bonus note de sport
def sport_bonus(note):
    if note > 17 :
        bonus = 0.5
    elif note > 14 :
        bonus = 0.45
    elif note > 10 :
        bonus = round((note - 10)*0.1,2)
    else :
        bonus = 0
    return bonus

#affichage des moyennes
def show_grades(titre_UE, moyenne_UE, matiere_info, bonus=None) : 
        
    for UE in titre_UE:
        
        if "sport" in titre_UE[UE].lower() :
            text1 = ctk.CTkLabel(result, text = titre_UE[UE], font=font_UE)  #affichage titre UE
            text1.pack(anchor="w", padx=25, pady=(30, 20))
            
            for matiere in matiere_info :
                if matiere_info[matiere]["UE"] == UE:
                    matiere = ctk.CTkLabel(result, text = f"{matiere[4:]} : {matiere_info[matiere]['note']}", font=font_text)  #affichage matiere et note
                    matiere.pack(anchor="w", padx=30)
                    
            if bonus :
                textbonus = ctk.CTkLabel(result, text = f"Bonus sport : +{bonus}", font=font_moy)  #affichage moyenne
            else :
                textbonus = ctk.CTkLabel(result, text = f"Bonus sport : Aucun bonus disponible", font=font_moy)  #affichage moyenne

            textbonus.pack(anchor="w", padx=30, pady=(15, 0))
            
        else :
                text1 = ctk.CTkLabel(result, text = titre_UE[UE], font=font_UE)  #affichage titre UE
                text1.pack(anchor="w", padx=25, pady=(30, 20))
                
                if titre_UE[UE] in moyenne_UE :
                    for matiere in matiere_info :
                        if matiere_info[matiere]["UE"] == UE:
                            matiere = ctk.CTkLabel(result, text = f"{matiere[4:]} : {matiere_info[matiere]['note']}", font=font_text)  #affichage matiere et note
                            matiere.pack(anchor="w", padx=30)
                            
                    
                    moyenne = ctk.CTkLabel(result, text = f"Moyenne : {moyenne_UE[titre_UE[UE]]}", font=font_moy)  #affichage moyenne
                else :
                    moyenne = ctk.CTkLabel(result, text = "Moyenne : Aucune note disponible", font=font_moy)  #affichage moyenne
                
                moyenne.pack(anchor="w", padx=30, pady=(15, 0))

            
'''PROGRAMME'''

configure_login()
login.pack(pady=30, padx=50, fill="both", expand=True)


root.mainloop()