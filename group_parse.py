from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from Db_connect import insert_resource
from selenium.webdriver.support.expected_conditions import presence_of_element_located


# This example requires Selenium WebDriver 3.13 or newer
source_url = "https://www.facebook.com/groups/disco80.90"
# https://www.facebook.com/groups/290482172380193
with webdriver.Chrome() as driver:
    wait = WebDriverWait(driver, 10)
    driver.get(source_url)
    content = []
    sub_result = driver.find_elements(By.CLASS_NAME, "d2edcug0")
    for sub in sub_result:
        content.append(sub.get_attribute("textContent"))

    full_name = content[13]
    print(full_name)
    number_of_subscribers = content[20].replace('Участники: ', '')
    print(number_of_subscribers)

    number_of_subscribers = number_of_subscribers.replace('Участники: ', '')
    print(number_of_subscribers)
    if number_of_subscribers.find("тыс.") != -1:
        number_of_subscribers = number_of_subscribers.replace(' тыс.', '')
        number_of_subscribers = number_of_subscribers.replace(',', '.')
        number_of_subscribers = float(number_of_subscribers)
        number_of_subscribers *= 1000
        print(number_of_subscribers)
    elif number_of_subscribers.find(" млн") != -1:
        number_of_subscribers = number_of_subscribers.replace(' млн', '')
        number_of_subscribers = number_of_subscribers.replace(',', '.')
        number_of_subscribers = float(number_of_subscribers)
        number_of_subscribers *= 1000000
        print(number_of_subscribers)
    else:
        number_of_subscribers = float(number_of_subscribers)
        print(number_of_subscribers)

#insert_resource(source_url, number_of_subscribers, full_name)