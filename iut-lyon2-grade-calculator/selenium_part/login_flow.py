from .driver_setup import driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC

connection_links = {
    "https://iut-extranet.univ-lyon2.fr/dana-na/auth/url_MJ55eorq301ZSVoH/welcome.cgi": "base",
    "https://iut-extranet.univ-lyon2.fr/dana-na/auth/url_MJ55eorq301ZSVoH/welcome.cgi?p=failed": "invalid psw",
    "https://iut-extranet.univ-lyon2.fr/dana-na/auth/url_MJ55eorq301ZSVoH/welcome.cgi?p=account%2Dlocked%2Dout": "locked acc",
    "https://iut-extranet.univ-lyon2.fr/dana-na/auth/url_MJ55eorq301ZSVoH/welcome.cgi?p=too%2Dmany": "too many users",
    "https://iut-extranet.univ-lyon2.fr/dana/user/#": "valid psw",
    "https://iut-extranet.univ-lyon2.fr/dana-na/auth/url_MJ55eorq301ZSVoH/welcome.cgi?p=user%2Dconfirm": "valid psw but other sess",
    "error" : "error"
}

def connection_works(u_field, p_field) :

    username = u_field.get()
    password = p_field.get()

    username_field_html = driver.find_element(By.ID,"username")
    username_field_html.send_keys(username)
    password_field_html = driver.find_element(By.ID,"password")
    password_field_html.send_keys(password)

    driver.find_element(By.ID, "btnSubmit_6").click()
    
    try:
        WebDriverWait(driver, 5).until(lambda d: d.execute_script("return document.readyState") == "complete")
        key = driver.current_url

    except TimeoutException:
        key = "error"
    print(key)
    return connection_links[key]

#rajouter la logique des mdp et user déjà testé

def path_connection(status):
    if status == "valid psw but other sess":
        try :
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "btnContinue"))).click()
        except TimeoutException:
            return True
    
    
    pass


"""
def connexion(u_field, p_field, fb) :
    
    fb.configure(text="Chargement...")
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
     
    return False"""