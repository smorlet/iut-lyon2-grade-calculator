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

    return connection_links[key]

#rajouter la logique des mdp et user déjà testé

def path_connection(status):

    if status == "valid psw but other sess":
        try :
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "btnContinue"))).click()
        except TimeoutException:
            driver.get("https://iut-extranet.univ-lyon2.fr")
            return False
    
    try:
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "web_bookmark_card_0"))).click()
    except TimeoutException:
        try:
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "0-header"))).click()
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "web_bookmark_card_0"))).click()
        except TimeoutException:
            driver.get("https://iut-extranet.univ-lyon2.fr")
            return False 

    try :
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "MainContent_accesrapidesAccueil_rptAccesRapides_HyperLink1_1"))).click()
    except TimeoutException:
        driver.get("https://iut-extranet.univ-lyon2.fr")
        return False    
     
    return True