import time
import requests

from Db_connect import close_connect
from Db_connect import create_resource_table
from Db_connect import get_content_from_db
from Db_connect import sorted_table_VK
from Db_connect import update_resource

start_time = time.time()
# создание таблицы resource
create_resource_table()
# сортировка таблицы по дате и типу(Facebook)
sorted_source_id = sorted_table_VK()
#access token генерируемый VK API
token = "f5a848cc54bfd25e74c035280769ec7ee457670b7ddaeabfb4f2c3b8ad08116d5c40b58702f13cf3de81f"

# # парсинг страницы Facebook
def parse_facebook(source_url):
    URL = source_url.rpartition('/')[2]
    search_type = f"https://api.vk.com/method/utils.resolveScreenName?screen_name={URL}&access_token={token}&v=5.131"
    search_type_req = requests.get(search_type).json()
    if search_type_req["response"]["type"] == "user":
        url = f"https://api.vk.com/method/users.get?user_ids={URL}&fields=counters&access_token={token}&v=5.131"
        req = requests.get(url).json()
        number_of_subscribers = req["response"][0]["counters"]["friends"]
        print(number_of_subscribers)
        first_name = req["response"][0]["first_name"]
        last_name = req["response"][0]["last_name"]
        full_name = first_name + " " + last_name
        print(full_name)
        user_id = req["response"][0]["id"]
        print(user_id)
    elif search_type_req["response"]["type"] == "group":
        url = f"https://api.vk.com/method/groups.getById?group_id={URL}&fields=counters&access_token={token}&v=5.131"
        req = requests.get(url).json()
        number_of_subscribers = req["response"][0]["counters"]["clips_followers"]
        print(number_of_subscribers)
        full_name = req["response"][0]["name"]
        print(full_name)
        user_id = req["response"][0]["id"]
        print(user_id)

    usefull_content = (number_of_subscribers, full_name, user_id)
    return usefull_content


x = 0
for i in range(0, len(sorted_source_id)):
    source_id_and_url = get_content_from_db(sorted_source_id[x])
    usefull_content = parse_facebook(source_id_and_url[1])
    number_of_subscribers = usefull_content[0]
    full_name = usefull_content[1]
    user_id = usefull_content[2]
    source_id = source_id_and_url[0]
    source_url = source_id_and_url[1]
    # обновление полей таблицы resource
    update_content = (source_url, number_of_subscribers, full_name, user_id, source_id)
    update_resource(update_content)
    x += 1
#
# # добавление страницы в табицу resource
# insert_content = ('source_url', 'number_of_subscribers', 'full_name', 'user_id', 'type')
# #insert_resource(insert_content)
#
close_connect()
print("--- %s seconds ---" % (time.time() - start_time))