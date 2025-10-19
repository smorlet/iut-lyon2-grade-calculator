# iut-lyon2-grade-calculator
Program designed to simplify the calculation of UE averages for students of IUT Lumière Lyon 2. The program connects to the IUT extranet using the student's credentials to automatically retrieve the grades required for the calculation.

# 📦 moyenne_ue/

## main.py  
Point d’entrée de l’application.

---

## gui/
- `__init__.py`
- **app.py** — fenêtre principale (root) + gestion de la navigation  
- **frames_login.py** — page de connexion  
- **frames_result.py** — page des résultats  
- **styles.py** — polices, couleurs, thèmes  

---

## selenium_part/
- `__init__.py`
- **driver_setup.py** — configuration de Selenium  
- **login_flow.py** — fonction `connexion()`  
- **scraper.py** — fonction `collect_grades()`  
- **utils_selenium.py** — fonctions utilitaires (`switch_sem()`, etc.)  

---

## core/
- `__init__.py`
- **calculs.py** — bonus sport, moyenne pondérée  
- **config.py** — URL, timeouts, options Selenium  

---

## utils/
- `__init__.py`
- **helpers.py** — fonctions utilitaires (`toggle_visibility`, `clear_frame`, etc.)
