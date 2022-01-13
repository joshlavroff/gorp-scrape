import requests
import sys
from PyQt5.QtWidgets import QLineEdit,QComboBox,QGridLayout,QLabel,QApplication,QWidget, QPushButton, QProgressBar, \
    QTextBrowser
from PyQt5 import QtGui
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import time

url="https://www.grailed.com/shop"

chrome_options=webdriver.ChromeOptions()
ser=Service("D:\chromedriver_win32\chromedriver.exe")
driver=webdriver.Chrome(service=ser,options=chrome_options)
driver.get(url)

try:
    searchBox = driver.find_element(By.CLASS_NAME, "Search-module__input___NFsRw")
    searchButton = driver.find_element(By.XPATH, "//*[contains(text(),'Search')]")
    action = ActionChains(driver)
    action.click().perform()
    action.click().perform()
    searchBox.send_keys("arcteryx")
    action.move_to_element(searchButton).click().perform()
    driver.implicitly_wait(1)


except:
    driver.quit()

time.sleep(1)
pri=driver.find_elements(By.XPATH,"//*[contains(text(),'$')]")
total=0
for i in range(2,len(pri)-2):
    total+=float(pri[i].text[1:])
avg=round(total/(len(pri)-3),2)
print(avg)
time.sleep(10)

def checkSoldListings():
    try:
        showOnly = driver.find_element(By.XPATH, "//*[contains(text(),'Show Only')]")
        showOnly.click()
    except:
        driver.close()

    time.sleep(1)

    try:
        sold = driver.find_element(By.XPATH, "//*[contains(text(),'Sold')]")
        action.move_to_element(sold).click().perform()
        action.move_to_element(sold).click().perform()

    except:
        driver.close()