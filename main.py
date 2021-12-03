from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time

from Db_connect import sorted_table
from Db_connect import create_resource_table
from Db_connect import get_content_from_db
from Db_connect import insert_resource
from Db_connect import update_resource
from Db_connect import close_connect


start_time = time.time()
# This example requires Selenium WebDriver 3.13 or newer
create_resource_table() # создание таблицы resource
count = sorted_table()

def group_parse(number_of_subscribers):
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

def parse_facebook(source_url):
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

        if source_url.find("id=") != -1:
            user_id = source_url.split("id=", 1)[1]
        elif source_url.find("groups") != -1:
            user_id = source_url.partition('groups/')[-1].rpartition('/')[0]
            number_of_subscribers = group_parse(number_of_subscribers)
        elif source_url.find(".com/") != -1:
            user_id = source_url.split(".com/", 1)[1]
        else:
            user_id = "incorrect url"

        useful_content = (full_name, number_of_subscribers, user_id)
        return useful_content
        # if source_url.find("/group") != -1:
        #     number_of_subscribers = group_parse(number_of_subscribers)

x = 1
for i in range(1, count):
    source_url = get_content_from_db(x)
    useful_content = parse_facebook(source_url[1])
    number_of_subscribers = useful_content[1]
    full_name = useful_content[0]
    user_id = useful_content[2]
    source_id = useful_content[0]
    update_content = (source_url, number_of_subscribers, full_name, user_id, source_id)
    update_resource(update_content)
    x += 1


insert_content = ('https://www.facebook.com/brigittelindholm.me', '1', 'Абай Молдабеков2', '', 'Facebook')
#insert_resource(insert_content)

close_connect()
print("--- %s seconds ---" % (time.time() - start_time))