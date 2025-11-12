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

def bonus_sport():
    pass