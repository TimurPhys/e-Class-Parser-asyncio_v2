from selenium import webdriver
from selenium.webdriver.firefox.service import Service


def create_driver():
    options = webdriver.ChromeOptions()

    # !!! ГЛАВНАЯ ОПЦИЯ: запуск без графического интерфейса !!!
    options.add_argument("--headless=new")
    options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.headless = True

    driver = webdriver.Chrome(
        options=options,
    )

    return driver