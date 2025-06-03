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
url = 'https://www.cian.ru/cat.php?conditioner=1&currency=2&deal_type=rent&demolished_in_moscow_programm=0&district[0]=23&engine_version=2&house_material[0]=1&include_new_moscow=0&maxprice=100000&offer_type=flat&only_flat=1&room2=1&room3=1&sort=total_price_desc&type=4'
driver.get(url)
time.sleep(5)

pattern = r"в районе\s+\b([^\s]+)\b\s+на"
district_element = driver.find_element(By.XPATH, "//h1[@class='_93444fe79c--color_text-primary-default--vSRPB _93444fe79c--lineHeight_36px--K6dvk _93444fe79c--fontWeight_bold--BbhnX _93444fe79c--fontSize_28px--P1gR4 _93444fe79c--display_block--KYb25 _93444fe79c--text--b2YS3 _93444fe79c--text_letterSpacing__normal--yhcXb']")
district_name = district_element.text
extracted_district_name = str(re.search(pattern, district_name).group(1)) # Corrected to extract the captured group
print(extracted_district_name)

'''button = driver.find_element(By.XPATH, "//span[contains(text(), 'Сохранить файл Excel')]")
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
button.click()'''
time.sleep(10)
driver.quit()