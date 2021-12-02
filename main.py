from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import time
import mysql.connector

# from Db_connect import insert_resource
from Db_connect import create_resource_table
from Db_connect import get_source_url
from Db_connect import insert_resource
from Db_connect import update_resource

start_time = time.time()
# This example requires Selenium WebDriver 3.13 or newer

CONNECTION = {'host': 'localhost', 'database': 'facebookScript', 'user': 'root', 'password': 'MYSQL'}
connection = mysql.connector.connect(**CONNECTION)
cursor = connection.cursor()
create_resource_table(cursor)
source_id = 1
source_url = get_source_url(cursor, source_id)

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
    update_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # print(content)

    if source_url.find("/group") != -1:
        number_of_subscribers = group_parse(number_of_subscribers)



update_content = (source_id, source_url, number_of_subscribers, full_name, "test_user_id", "Facebook", update_date)
update_resource(cursor, update_content)

insert_content = ('https://www.facebook.com/brigittelindholm.me', '1', 'Абай Молдабеков1', '', 'Facebook', update_date)
insert_resource(cursor, insert_content)


if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


print("--- %s seconds ---" % (time.time() - start_time))