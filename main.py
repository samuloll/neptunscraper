
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time
from dotenv import load_dotenv
import random
from functions import sendMessage, calculating, clearing_env, login, searching_for_subject, making_right_array, getting_to_subjects, change_course
from selenium.webdriver.chrome.options import Options




if __name__ == "__main__":

    load_dotenv()
    TOKEN = os.getenv("API_KEY")
    chat_id = os.getenv("CHAT_ID")

    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    subjectcode = os.getenv("SUBJECT") 
    course_number = int(os.getenv("COURSE_NUMBER")) # int(input("Please enter the coursenumber: ")) 
     
    clearing_env(subjectcode, course_number)

    options = Options()
    options.add_argument("--headless=new")  # A modern headless motor
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")  # Érdemes fix felbontást adni, hogy a gombok ne essenek szét

    good = False
    tries = 0
    current_url = ""

    driver = webdriver.Chrome(options=options)
    login(username, password, driver)
    while not good:
        try:
            sleep = random.randrange(50, 70)
            print(sleep)
            current_url = getting_to_subjects(driver, (tries==0), current_url)
            if not "registration" in driver.current_url:
                raise Exception("Something went wrong")
            classes = searching_for_subject(driver, subjectcode)
            with open(".adatok", "w") as file:
                for item in classes:
                    file.write(item.text)
            array = making_right_array()
            if calculating(array, course_number):
                good = True
            tries += 1
            if not good:
                time.sleep(sleep)
        except Exception as e:
            print("Exception")
            time.sleep(30)
            driver.quit()
            tries = 0
            driver = webdriver.Chrome()
            login(username, password, driver)
            current_url = ""

    if good:
        try:
            change_course(driver=driver, course_number=course_number, current_url=current_url, subjectcode=subjectcode)
            sendMessage("Sikeresen felvéve", TOKEN, chat_id)
        except Exception as e:
            sendMessage(f"Vegyed fel\n{e}", TOKEN, chat_id)
    driver.quit()
