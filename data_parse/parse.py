from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import requests

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# period = 1 - 1-ый семестр
# period = 2 - 2-ый семестр
# period = 3 - весь год
def get_stats(username, password, period):
    driver = webdriver.Chrome()
    driver.get("https://www.e-klase.lv")

    time.sleep(2)

    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='login-widget__login_button_wrapper']"))
    )

    student_button = button.find_elements(By.TAG_NAME, "a")[0]
    driver.execute_script("arguments[0].click()", student_button)

    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )

    username_input.clear()
    username_input.send_keys(username)

    time.sleep(1)

    password_input.clear()
    password_input.send_keys(password + Keys.ENTER)

    time.sleep(2)

    driver.get("https://family.e-klase.lv/overview")

    time.sleep(1)

    session = requests.Session()
    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'])


    file_url = ""
    if (period == 1):
        file_url = "https://family.e-klase.lv/api/evaluation-reports?from=2025-09-01&to=2025-12-31"
    elif (period == 2):
        file_url = "https://family.e-klase.lv/api/evaluation-reports?from=2026-01-01&to=2026-08-31"
    elif (period == 3):
        file_url = "https://family.e-klase.lv/api/evaluation-reports?from=2025-09-01&to=2026-08-31"

    response = session.get(file_url, stream=True)

    # download_dir = "B:\Python Projects and Tutorials\eClassParser2.0Aiogram"
    #
    # options = webdriver.ChromeOptions()
    # options.add_experimental_option("prefs", {
    #     "download.default_directory": download_dir,
    #     "download.prompt_for_download": False,
    #     "download.directory_upgrade": True,
    #     "plugins.always_open_pdf_externally": True
    # })
    # driver = webdriver.Chrome(options=options)

    time.sleep(2)

    file_name = f"Izraksts_username={username}_period={period}.pdf"
    file_path = os.path.join("../downloads", file_name)

    print(response.content)
    with open(file_path, "wb") as pdf_file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                pdf_file.write(chunk)

    driver.close()
    driver.quit()


get_stats("180108-24659", "v537nami", 1)