from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time
from bs4 import BeautifulSoup as soup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
url = 'https://www.cian.ru/cat.php?conditioner=1&currency=2&deal_type=rent&demolished_in_moscow_programm=0&engine_version=2&house_material%5B0%5D=1&maxprice=100000&offer_type=flat&only_flat=1&region=1&room2=1&room3=1&sort=total_price_desc&type=4'
driver.get(url)
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
input_elem.send_keys(email)
button = driver.find_element(By.XPATH, "//span[@class='_25d45facb5--text--V2xLI' and text()='Продолжить']")
button.click()
input_elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'password')))
password = 'UA^U8=&Ks5vf-R2'
input_elem.send_keys(password)
button = driver.find_element(By.XPATH, "//span[@class='_25d45facb5--text--V2xLI' and text()='Продолжить']")
button.click()
time.sleep(10)
driver.quit()