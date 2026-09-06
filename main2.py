from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time
from dotenv import load_dotenv
import random
from functions import sendMessage, calculating, clearing_env, login, searching_for_subject, making_right_array, getting_to_subjects

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
    return 0

load_dotenv()
TOKEN = os.getenv("API_KEY")
chat_id = os.getenv("CHAT_ID")

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

subjectcode = input("Please enter the code of the Subject: ")
course_number = int(input("Please enter the coursenumber: "))
clearing_env(subjectcode, course_number)

good = False
tries = 0
current_url = ""
driver = webdriver.Chrome()
login(username, password, driver)
current_url = getting_to_subjects(driver, (tries==0), current_url)
classes = searching_for_subject(driver, subjectcode)
change_course(driver, course_number)