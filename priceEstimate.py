from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import trim
def getAvgPrice(keyword):
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
        searchBox.send_keys(keyword)
        action.move_to_element(searchButton).click().perform()
        driver.implicitly_wait(1)


    except:
        driver.quit()

    time.sleep(1)
    pri=driver.find_elements(By.XPATH,"//*[contains(text(),'$')]")
    total=0
    for i in range(2,len(pri)-2):
        if " " not in pri[i].text:
            total+=float(trim.trimStr(pri[i].text[1:]))
    avg=round(total/(len(pri)-3),2)
    return avg

def checkSoldListings(driver,action):
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

#getAvgPrice("arcteryx")