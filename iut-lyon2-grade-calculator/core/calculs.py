def calcul_average(UE_grades):
    total_grade = 0
    total_coefficient = 0
    
    for info in UE_grades['Subjects'].values():
        grade = info['Grade']
        coefficient = info['Coefficient']

        total_grade += grade*coefficient
        total_coefficient += coefficient
    
    if total_coefficient == 0:
        return None
    
    average = round(total_grade/total_coefficient, 2)
    return average

def calcul_bonus(grade):
    match grade :
        case _ if grade > 17:
            return 0.5
        case _ if grade > 14:
            return 0.45
        case _ if grade > 10:
            return round((grade - 10)*0.1,2)
        case _ :
            return 0
        
def add_bonus(bonus, UE_grades):
    for UE in UE_grades:
        UE_grades[UE]["Average"] += bonus