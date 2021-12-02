from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time

from Db_connect import insert_resource
from Db_connect import resource_url

start_time = time.time()
# This example requires Selenium WebDriver 3.13 or newer
source_url = resource_url(8)

def test_parse(number_of_subscribers):
    subscribers = number_of_subscribers.replace('Участники: ', '')
    print(subscribers)
    number_of_subscribers = subscribers.replace('Участники: ', '')
    print(number_of_subscribers)
    if number_of_subscribers.find("тыс.") != -1:
        number_of_subscribers = number_of_subscribers.replace('\xa0тыс.', '')
        number_of_subscribers = number_of_subscribers.replace(',', '.')
        number_of_subscribers = float(number_of_subscribers)
        number_of_subscribers *= 1000
        print(number_of_subscribers)
    elif number_of_subscribers.find(" млн") != -1:
        number_of_subscribers = number_of_subscribers.replace('\xa0млн', '')
        number_of_subscribers = number_of_subscribers.replace(',', '.')
        number_of_subscribers = float(number_of_subscribers)
        number_of_subscribers *= 1000000
        print(number_of_subscribers)
    else:
        number_of_subscribers = float(number_of_subscribers)
        print(number_of_subscribers)
    return number_of_subscribers

with webdriver.Chrome() as driver:
    wait = WebDriverWait(driver, 10)
    driver.get(source_url)
    content = []
    time.sleep(1)
    sub_result = driver.find_elements(By.CLASS_NAME, "d2edcug0")
    for sub in sub_result:
        content.append(sub.get_attribute("textContent"))
    full_name = content[13]
    print(full_name)
    number_of_subscribers = content[20]
    print(number_of_subscribers)
    # print(content)

    if source_url.find("/group") != -1:
        number_of_subscribers = test_parse(number_of_subscribers)

insert_resource(source_url, number_of_subscribers, full_name)

print("--- %s seconds ---" % (time.time() - start_time))