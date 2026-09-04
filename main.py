
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time
import pyotp
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 
load_dotenv()
import requests

message = "Idk"



messages = {
    "Develop":"Develop this phase",
    "LoggedIn": "Ok works now",
    "YouCan" : "Most rátudsz jelentkezni",
    "YouCant" : "Most nem tudsz rájelentkezni"
}       
       
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

def getting_to_subjects(driver):
    tries = 0
    driver.get("https://neptun.elte.hu/" + "ToNeptunWeb/ToNeptunHWeb")
    while not driver.current_url== "https://neptun.elte.hu/ToNeptunWeb/ToNeptunHWeb" and not tries > 3:
        tries += 1
        time.sleep(3)
    tries = 0
    while not "dashboard" in driver.current_url and not tries > 3:
        tries += 1
        time.sleep(3)
    if not driver.current_url == "https://hallgato4.neptun.elte.hu/dashboard":
        return False
    driver.get("https://hallgato4.neptun.elte.hu/subjects/registration")
    if not driver.current_url == "https://hallgato4.neptun.elte.hu/subjects/registration":
        time.sleep(10)
    return True

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
    search_box_input.send_keys(subjectcode)
    search_box_button = driver.find_element(By.ID, "filter-table")
    search_box_button.click()
    time.sleep(2)
    expand_box = driver.find_element(By.CLASS_NAME, "mat-expansion-indicator")
    expand_box.click()
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


def calculating(array, course_number, urlYouCan, urlYouCant):
    index = (course_number-1)
    attedence_number = int(array[index].split(" ")[0])
    max_number = int(array[index].split(" ")[1])
    if (attedence_number < max_number):
        requests.get(urlYouCan)
    else:
        requests.get(urlYouCant)
    
    print(f"attandence: {attedence_number} max_number: {max_number}")


if __name__ == "__main__":

    TOKEN = os.getenv("API_KEY")
    chat_id = os.getenv("CHAT_ID")

    urlYouCan = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={messages["YouCan"]}"
    urlYouCant = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={messages["YouCant"]}"

    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    subjectcode = os.getenv("SUBJECT") #input("Please enter the code of the Subject: ")
    course_number = int(os.getenv("COURSE_NUMBER")) #int(input("Please enter the coursenumber: "))
    clearing_env(subjectcode, course_number)


    driver = webdriver.Chrome()
    driver.get("https://neptun.elte.hu/Account/Login")
    login(username, password, driver)
    getting_to_subjects(driver)
    classes = searching_for_subject(driver, subjectcode)
    with open(".adatok", "w") as file:
        for item in classes:
            file.write(item.text)
    array = making_right_array()
    calculating(array, course_number, urlYouCan, urlYouCant)
        
