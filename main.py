#!/root/facebook_script/venv/bin/python3
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from Db_connect import close_connect
from Db_connect import create_resource_table
from Db_connect import get_content_from_db
from Db_connect import sorted_table_FB
from Db_connect import update_resource

start_time = time.time()
# создание таблицы resource
create_resource_table()
# сортировка таблицы по дате и типу(Facebook)
sorted_source_id = sorted_table_FB()

# обработка количества участников группы
def group_parse(number_of_subscribers):
    number_of_subscribers = number_of_subscribers.replace('Участники: ', '')
    number_of_subscribers = number_of_subscribers.replace('K members', '')
    if number_of_subscribers.find("тыс.") != -1:
        number_of_subscribers = number_of_subscribers.replace('\xa0тыс.', '')
        number_of_subscribers = number_of_subscribers.replace(',', '.')
        number_of_subscribers = float(number_of_subscribers)
        number_of_subscribers *= 1000
    elif number_of_subscribers.find("млн") != -1:
        number_of_subscribers = number_of_subscribers.replace('\xa0млн', '')
        number_of_subscribers = number_of_subscribers.replace(',', '.')
        number_of_subscribers = float(number_of_subscribers)
        number_of_subscribers *= 1000000
    else:
        number_of_subscribers = float(number_of_subscribers)
    return number_of_subscribers


# парсинг страницы Facebook
def parse_facebook(source_url):
    # This example requires Selenium WebDriver 3.13 or newer
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--no-sandbox')
    options.headless = True
    # options.add_argument('--headless')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('window-size=1920x935')
    # driver = webdriver.Chrome(executable_path=r'/root/facebook_script/chromedriver', options=options)
    driver = webdriver.Chrome(options=options)
    WebDriverWait(driver, 10)
    driver.get(source_url)
    content = []
    time.sleep(10)
    sub_result = driver.find_elements(By.CLASS_NAME, "d2edcug0")
    for sub in sub_result:
        content.append(sub.get_attribute("textContent"))
    full_name = content[13]
    print(full_name)
    number_of_subscribers = content[20]

    if source_url.find("id=") != -1:
        user_id = source_url.split("id=", 1)[1]
        number_of_subscribers = content[18]
    elif source_url.find("groups") != -1:
        user_id = source_url.partition('groups/')[-1].rpartition('/')[0]
        number_of_subscribers = group_parse(number_of_subscribers)
    elif source_url.find(".com/") != -1:
        user_id = source_url.split(".com/", 1)[1]
    else:
        user_id = "incorrect url"

    useful_content = (number_of_subscribers, full_name, user_id)
    return useful_content

x = 0
for i in range(0, len(sorted_source_id)):
    content_from_db = get_content_from_db(sorted_source_id[x])
    useful_content = parse_facebook(content_from_db[1])
    number_of_subscribers = useful_content[0]
    full_name = useful_content[1]
    user_id = useful_content[2]
    source_id = content_from_db[0]
    source_url = content_from_db[1]
    # обновление полей таблицы resource
    update_content = (source_url, number_of_subscribers, full_name, user_id, source_id)
    update_resource(update_content)
    x += 1

# добавление страницы в табицу resource
insert_content = ('source_url', 'number_of_subscribers', 'full_name', 'user_id', 'type')
#insert_resource(insert_content)

close_connect()
print("--- %s seconds ---" % (time.time() - start_time))