from .driver_setup import driver
from selenium.webdriver.common.by import By
from collections import defaultdict
from core import calcul_average, calcul_bonus, add_bonus

def collect_grades():

    UE_info = {
        "UE": defaultdict(lambda: {
            "Title": "",
            "Subjects": defaultdict(dict),
            "Average": None
        }),
        "_meta": defaultdict(lambda: None)
    }

    bonus = None

    titles = driver.find_elements(By.XPATH, "//div[@class='libelle-ue']/span")
    for no, title in enumerate(titles, start=1) :
        UE_info["UE"][no]["Title"] = title.text

    for UE in UE_info["UE"]:

        grades = driver.find_elements(By.XPATH, f'//span[contains(text(), "{UE_info["UE"][UE]["Title"]}")]/ancestor::div[@class="libelle-ue"]/following-sibling::div[@class="pt-2"][1]//span[contains(text(), "Moyenne matière")]')
        subjects = driver.find_elements(By.XPATH, f'//span[contains(text(), "{UE_info["UE"][UE]["Title"]}")]/ancestor::div[@class="libelle-ue"]/following-sibling::div[@class="pt-2"]//div[@class="row p-1 bg-dark text-white ms-0 me-0"]//div[contains(@class, "col-md")]/span')
        coefficients = driver.find_elements(By.XPATH, f'//span[contains(text(), "{UE_info["UE"][UE]["Title"]}")]/ancestor::div[@class="libelle-ue"]/following-sibling::div[@class="pt-2"]//div[@class="row p-1 bg-dark text-white ms-0 me-0"]//div[contains(@class, "col-md-2")]//small[contains(text(), "coefficient")]')

        for i in range(len(grades)):
            
            grade = extract_grade(grades[i].text)
            if grade is not None:
                subject = rename_subject(subjects[i].text)
                coefficient = extract_coefficient(coefficients[i].text)

                if "sport" in subject.lower():
                    bonus = calcul_bonus(grade)

                UE_info["UE"][UE]["Subjects"][subject]["Grade"] = grade
                UE_info["UE"][UE]["Subjects"][subject]["Coefficient"] = coefficient

        average = calcul_average(UE_info["UE"][UE])
        UE_info["UE"][UE]["Average"] = average

    if bonus :
        add_bonus(bonus, UE_info["UE"])
        UE_info["_meta"]["Bonus"] = bonus
    
    return UE_info
         
def rename_subject(text):
    subject = text.split(" - ", 1)[1]
    return subject

def extract_grade(text):
    grade = text.replace("Moyenne matière :", "").replace(",",".").strip()
    if grade:
        return float(grade)
    else:
        return None

def extract_coefficient(text):
    coefficient = text.replace("coefficient :", "").replace(",",".").strip()
    return float(coefficient)