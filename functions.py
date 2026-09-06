from selenium.webdriver.common.by import By
import os
import time
import pyotp
import requests


def sendMessage(message, TOKEN, chat_id):
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}")

def clearing_env(subjectcode, course_number):
    with open(".env", "r") as file:
        lines = file.readlines()
    os.remove(".env")

    with open(".env", "w") as file:
        for line in lines:
            if not "SUBJECT" in line:
                if not "COURSE_NUMBER" in line:
                    file.write(line)
        file.write(f"SUBJECT = \"{subjectcode}\"\n")
        file.write(f"COURSE_NUMBER = \"{course_number}\"")


def login(username, password, driver):
    driver.get("https://neptun.elte.hu/Account/Login")
    username_box= driver.find_element(By.ID, "LoginName") 
    username_box.send_keys(username)
    password_box = driver.find_element(By.ID, "Password") 
    password_box.send_keys(password)
    next_button = driver.find_element(By.CLASS_NAME, "btn-primary")
    next_button.click()
    driver.implicitly_wait(2)
    totp_box = driver.find_element(By.ID, "TOTPCode") 
    totp_box.send_keys(pyotp.TOTP(os.getenv("TOTP_SECRET")).now())
    next_button = driver.find_element(By.CLASS_NAME, "btn-primary")
    next_button.click()
    driver.implicitly_wait(2)

def getting_to_subjects(driver, first, current_url):
    tries = 0
    driver.get("https://neptun.elte.hu/" + "ToNeptunWeb/ToNeptunHWeb")
    if first:
        while not "dashboard" in driver.current_url  and not tries > 3:
            tries += 1
            driver.get("https://neptun.elte.hu/" + "ToNeptunWeb/ToNeptunHWeb")
            time.sleep(5)
    else:
        driver.get(f"{current_url}.neptun.elte.hu/dashboard")
    while not "dashboard" in driver.current_url and not tries > 3:
        tries += 1
        time.sleep(3)
    if "dashboard" in driver.current_url and current_url == "":
        current_url = driver.current_url.split(".")[0]
    if not driver.current_url == f"{current_url}.neptun.elte.hu/dashboard":
        print("NEm a dashboard volt")
        raise Exception("Wrong path")
    driver.get(f"{current_url}.neptun.elte.hu/subjects/registration")
    if not driver.current_url == f"{current_url}.neptun.elte.hu/subjects/registration":
        time.sleep(2)
    return current_url

def searching_for_subject(driver, subjectcode):
    try:
        accept_cookies = driver.find_element(By.ID, "notification-bar-0-notification-button-accept")
        accept_cookies.click()
    except Exception as e:
       tries = 0 
    
    try:
        skip_tasks = driver.find_element(By.ID, "important-tasks-close-button")
        skip_tasks.click()
        print("Clicked")
    except Exception as e:
        tries = 0
    search_box_input = driver.find_element(By.ID, "title-form-input")
    if not search_box_input.get_attribute("value") == subjectcode:
        search_box_input.send_keys(subjectcode)
    search_box_button = driver.find_element(By.ID, "filter-table")
    search_box_button.click()
    time.sleep(2)
    expand_box = driver.find_element(By.CLASS_NAME, "mat-expansion-indicator")
    expand_box.click()
    time.sleep(3)
    classes = driver.find_element(By.ID, "subject-registration-subject-list-0-course-list-0")

    return classes.find_elements(By.XPATH, "./div/neptun-course-list-item")


def making_right_array():
    array = []
    with open(".adatok", "r") as file:
        for line in file:
            line = line.strip("\n")
            if " limit" in line:
                array2 = line.split(" ")
                corrected_line = str(array2[0]) + " " +  str(array2[3])
                array.append(corrected_line)
    return array


def calculating(array, course_number):
    index = (course_number-1)
    attedence_number = int(array[index].split(" ")[0])
    max_number = int(array[index].split(" ")[1])
    print(f"attandence: {attedence_number} max_number: {max_number}")
    return (attedence_number < max_number)


def change_course(driver, course_number, current_url, subjectcode):
    getting_to_subjects(driver, False, current_url)
    searching_for_subject(driver, subjectcode)
    course_change_button = driver.find_element(By.CSS_SELECTOR, "[id*='course-change-btn']")
    course_change_button.click()
    time.sleep(1)
    course_number_field = driver.find_element(By.CSS_SELECTOR, f"[id*='course-{course_number - 1}-cb-input']")
    course_number_field.click()
    time.sleep(1)
    course_finish_button = driver.find_element(By.CSS_SELECTOR, f"[id*='finish-course-change-btn']")
    course_finish_button.click()
    time.sleep(1)
    course_finalize_button = driver.find_element(By.CSS_SELECTOR, f"[id*='confirm-dialog-btn1']")
    course_finalize_button.click()