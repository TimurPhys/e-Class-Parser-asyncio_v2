from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import requests
import json

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from __init__ import headers

# period = 1 - 1-ый семестр
# period = 2 - 2-ый семестр
# period = 3 - весь год


driver = webdriver.Chrome()
def get_auth_token():
    token = driver.execute_script("return window.sessionStorage")
    token_raw = json.loads(token['oidc.secureTokens.currentToken'])
    auth_token = token_raw['token_type'] + " " + token_raw['id_token']
    return auth_token



def get_profiles(username, password):
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

    driver.get("https://family.e-klase.lv/profile-selection")

    session = requests.Session()
    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'])

    token = get_auth_token()
    headers["Authorization"] = token

    response = session.get("https://family.e-klase.lv/api/user/profiles", headers=headers)
    profiles = json.loads(response.content)['activeProfiles']
    return profiles


def get_stats(profile, period):
    profileId = profile['profileId']
    driver.get("https://family.e-klase.lv/overview")

    time.sleep(1)

    session = requests.Session()
    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'])

    headers["X-Profile-Id"] = profileId

    file_url = ""
    if (period == 1):
        file_url = "https://family.e-klase.lv/api/evaluation-reports?from=2025-09-01&to=2025-12-31"
    elif (period == 2):
        file_url = "https://family.e-klase.lv/api/evaluation-reports?from=2026-01-01&to=2026-08-31"
    elif (period == 3):
        file_url = "https://family.e-klase.lv/api/evaluation-reports?from=2025-09-01&to=2026-08-31"

    response = session.get(file_url, headers=headers)

    time.sleep(2)

    file_name = f"Izraksts_profile={profileId}_period={period}.pdf"
    file_path = os.path.join("../downloads", file_name)

    with open(file_path, "wb") as pdf_file:
        pdf_file.write(response.content)
    driver.close()
    driver.quit()



profiles = get_profiles("180108-24659", "v537nami")

get_stats(profiles[0], 1)