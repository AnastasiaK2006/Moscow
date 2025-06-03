from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup as soup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
url = 'https://tcshops.ru/gorod/moskva/'
driver.get(url)
time.sleep(5)

dictionary_ultra_districts = {1 :"СЗАО", 4 : "ЦАО",  5 : "CAO", 6 : "СВАО", 7 : "ВАО", 8 : "ЮВАО", 9 : "ЮАО", 10 : "ЮЗАО",11 : "ЗАО"}
url = 'https://www.cian.ru/cat.php?conditioner=1&currency=2&deal_type=rent&demolished_in_moscow_programm=0&district[0]=23&engine_version=2&house_material[0]=1&include_new_moscow=0&maxprice=100000&offer_type=flat&only_flat=1&room2=1&room3=1&sort=total_price_desc&type=4'
for key in dictionary_ultra_districts:
    current_url = "https://www.cian.ru/cat.php?conditioner=1&currency=2&deal_type=rent&demolished_in_moscow_programm=0&district[0]=" + str(key) + "&engine_version=2&house_material[0]=1&include_new_moscow=0&maxprice=100000&offer_type=flat&only_flat=1&room2=1&room3=1&sort=total_price_desc&type=4"
    print(current_url)
    driver.get(current_url)
    time.sleep(5)


    button = driver.find_element(By.XPATH, "//span[contains(text(), 'Сохранить файл Excel')]")
    button.click()
    time.sleep(5)  
    button = driver.find_element(By.XPATH, "//span[@class='_93444fe79c--text--V2xLI' and text()='Сохранить файл в Excel']")
    button.click()
    button = driver.find_element(By.XPATH, "//span[@class='_25d45facb5--text--V2xLI' and text()='Другой способ']")
    button.click()
    input_elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'username')))
    email = 'tech-diamond-08@icloud.com'
    email = '18offer.hoists@icloud.com'
    email = 'dancing-vitals.05@icloud.com'
    input_elem.send_keys(email)
    button = driver.find_element(By.XPATH, "//span[@class='_25d45facb5--text--V2xLI' and text()='Продолжить']")
    button.click()
    input_elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'password')))
    password = 'UA^U8=&Ks5vf-R2'
    password = '%JS^N6:wrx>jGHW'
    password = '9BCFbUsjnCwt.]x'
    input_elem.send_keys(password)
    button = driver.find_element(By.XPATH, "//span[@class='_25d45facb5--text--V2xLI' and text()='Продолжить']")
    button.click()
    time.sleep(10)