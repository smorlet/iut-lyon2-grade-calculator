import customtkinter as ctk
from selenium_part import collect_grades

class Result(ctk.CTkScrollableFrame):

    def __init__(self, root):
        super().__init__(root)

        self.semesters = 1
        self.show_grades()

    def show_grades(self):
        content = collect_grades()