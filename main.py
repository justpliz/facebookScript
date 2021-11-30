from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from Db_connect import insert_resource
from selenium.webdriver.support.expected_conditions import presence_of_element_located

# This example requires Selenium WebDriver 3.13 or newer
source_url = "https://www.facebook.com/profile.php?id=100011366594475"
with webdriver.Chrome() as driver:
    wait = WebDriverWait(driver, 10)
    driver.get(source_url)
    #first_result = driver.find_element(By.TAG_NAME, "h1")
    #print(first_result.get_attribute("textContent")) # Абай Молдабеков
    content = []
    sub_result = driver.find_elements(By.CLASS_NAME, "d2edcug0")
    for sub in sub_result:
        content.append(sub.get_attribute("textContent"))

    full_name = content[11]
    print(full_name)
    number_of_subscribers = content[20]
    print(number_of_subscribers)

insert_resource(source_url, number_of_subscribers, full_name)