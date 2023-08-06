#!/usr/local/opt/python@3.9/bin/python3.9
# -*- coding: utf-8 -*-

import datetime
import subprocess
import time
import keyboard
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def auto_strongbox_fixity():
    print(datetime.datetime.now())
    print("Strongbox Opening......")
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920x1080')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--ignore-certificate-errors')
    # options.add_experimental_option('download.default_directory', ['~/Downloads'])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        driver.get('https://192.168.255.11')
        print("\t->Strongbox/Home opened.")
    except Exception as e:
        print(e)
        print("\t->Strongbox Open Failed")
    time.sleep(2)
    print("Logining in......")
    try:
        userId = driver.find_element(By.ID, "login")
        userId.clear()
        userId.send_keys("admin")
        print("\t->Username Has Input")
        keyboard.press_and_release('tab')
        driver.find_element(By.ID, "password").send_keys("?I?2022")
        print("\t->Password Has Input")
        driver.find_element(By.ID, "do_login").click()
        print("\t->SUBMIT")
    except Exception as e:
        print(e)
        print("Login Failed")
    time.sleep(2)
    print("Getting CSV file......")
    try:
        driver.find_element(By.ID, "reporting").click()
        print("\t->Going to Reporting menu")
        time.sleep(2)
        # driver.find_element(By.XPATH, "//a[contains(., 'Generate CSV Reports')]").click()
        # error: element not interactable
        # Directly relocate by URL
        driver.get('https://192.168.255.11/download_reports')
        print("\t->Going to Generate CSV Reports page")
        time.sleep(2)
        driver.find_element(By.XPATH, "//input[@value='Generate File Report now']").click()
        print("\t->Generating CSV......\n\tPending for 2 minutes")
        time.sleep(90)
        # driver.get('https://192.168.255.11/download_reports/download?type=file_report')
        driver.find_element(By.XPATH, "//a[contains(., '_report.csv.zip')]").click()
        print('\t->CSV Downloading......')
        time.sleep(10)
    except Exception as e:
        print(e)
        print("CSV Ingest Failed")
    subprocess.run('open', 'Downloads')


auto_strongbox_fixity()