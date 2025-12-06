import customtkinter as ctk
from selenium_part import collect_grades
from gui.styles import font_text

class Result(ctk.CTkScrollableFrame):

    def __init__(self, root):
        super().__init__(root)

        self.semesters = 1
        self.show_grades()

    def show_grades(self):
        UE_info = collect_grades()

        for UE in UE_info["UE"]:
            title = ctk.CTkLabel(self, text = UE_info["UE"][UE]["Title"], font=font_text) 
            title.pack(anchor="w", padx=25, pady=(30, 20))

            if UE_info["UE"][UE]["Average"]:
                for subject in UE_info["UE"][UE]["Subjects"] :
                    subject = ctk.CTkLabel(self, text = f"{subject} : {UE_info["UE"][UE]["Subjects"][subject]["Grade"]}", font=font_text)
                    subject.pack(anchor="w", padx=30)

                average = ctk.CTkLabel(self, text = f"Moyenne : {UE_info["UE"][UE]["Average"]}", font=font_text)
            else:
                average = ctk.CTkLabel(self, text = "Moyenne : Aucune note disponible", font=font_text)

            average.pack(anchor="w", padx=30, pady=(15, 0))
