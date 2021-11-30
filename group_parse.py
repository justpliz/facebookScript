from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

def group_parse(source_url):
    # This example requires Selenium WebDriver 3.13 or newer
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
        subscribers = content[20].replace('Участники: ', '')
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
    groups_content = []
    # groups_content.append()
    return groups_content