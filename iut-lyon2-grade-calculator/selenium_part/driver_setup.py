from selenium import webdriver

def create_driver():
    global driver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://iut-extranet.univ-lyon2.fr")

    return driver

def quit_driver():
    global driver
    driver.quit()
    driver = None

def reset_driver():
    quit_driver()
    create_driver()