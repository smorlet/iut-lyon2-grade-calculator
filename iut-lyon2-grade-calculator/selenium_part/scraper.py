from .driver_setup import driver
from selenium.webdriver.common.by import By
from collections import defaultdict
from core import calcul_average

def collect_grades():

    UE_info = defaultdict(lambda: {
        "Title": "",
        "Subjects": defaultdict(dict),
        "Average": None
    })

    titles = driver.find_elements(By.XPATH, "//div[@class='libelle-ue']/span")
    for no, title in enumerate(titles, start=1) :
        UE_info[f"UE {no}"]["Title"] = title.text

    for UE in UE_info:

        grades = driver.find_elements(By.XPATH, f'//span[contains(text(), "{UE_info[UE]["Title"]}")]/ancestor::div[@class="libelle-ue"]/following-sibling::div[@class="pt-2"][1]//span[contains(text(), "Moyenne matière")]')
        subjects = driver.find_elements(By.XPATH, f'//span[contains(text(), "{UE_info[UE]["Title"]}")]/ancestor::div[@class="libelle-ue"]/following-sibling::div[@class="pt-2"]//div[@class="row p-1 bg-dark text-white ms-0 me-0"]//div[contains(@class, "col-md")]/span')
        coefficients = driver.find_elements(By.XPATH, f'//span[contains(text(), "{UE_info[UE]["Title"]}")]/ancestor::div[@class="libelle-ue"]/following-sibling::div[@class="pt-2"]//div[@class="row p-1 bg-dark text-white ms-0 me-0"]//div[contains(@class, "col-md-2")]//small[contains(text(), "coefficient")]')

        for i in range(len(grades)):
            
            grade = extract_grade(grades[i].text)
            if grade :
                subject = rename_subject(subjects[i].text)
                coefficient = extract_coefficient(coefficients[i].text)

                UE_info[UE]["Subjects"][subject]["Grade"] = grade
                UE_info[UE]["Subjects"][subject]["Coefficient"] = coefficient

        average = calcul_average(UE_info[UE])
        UE_info[UE]["Average"] = average

#rajouter bonus sport (afficher UE + calculer bonus + ajouter bonus a chaque note)             
                
"""
            if class_notes[i].text != "Moyenne matière :" :    #évite de prendre en compte les notes inexistantes du à des absences
                note = class_notes[i].text
                note = float(note.replace("Moyenne matière : ", "").replace(",",".")) #extrait la note en elle même
                
                matiere = rename_matiere(class_matiere[i].text,UE)
                
            

                coeff = class_coeff[i].text
                coeff = float(coeff.replace("coefficient : ", "").replace(",","."))  #extrait la note en elle même
                
                note_tot += note * coeff
                coeff_tot += coeff
                
                matiere_info[matiere] = {"UE" : UE, "note" : note, "coeff" : coeff}
        
        if coeff_tot > 0 :      #verif que l'UE à au moins une note (au cas ou ya des absences)
            moy = round(note_tot / coeff_tot,2)
            moyenne_UE[titre_UE[UE]] = moy
    """

def extract_grade(text):
    grade = text.replace("Moyenne matière :", "").replace(",",".").strip()
    if grade:
        return float(grade)
    else:
        return None
    
def rename_subject(text):
    subject = text.split(" - ", 1)[1]
    return subject

def extract_coefficient(text):
    coefficient = text.replace("coefficient :", "").replace(",",".").strip()
    return float(coefficient)

def old_collect_grades() :
    
    UE_titles = {}
    UE_averages = {}
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