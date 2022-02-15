#!/root/facebook_script/venv/bin/python3
import time
import requests

from Db_connect import close_connect
from Db_connect import create_resource_table
from Db_connect import get_content_from_db
from Db_connect import sorted_table_TWI
from Db_connect import update_resource

start_time = time.time()
# создание таблицы resource
create_resource_table()
# сортировка таблицы по дате и типу(Twitter)
sorted_source_id = sorted_table_TWI()
# bearer token генерируемый Twitter API
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAGMqZAEAAAAAmr0DBSJDr%2F8p22MFU8%2FkSafrG8A%3DQJe3Dgcjpz98zExwm51MhynAMT0OF8HJiHkDGtrvCfn42gWXT4'
headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}


# отправка запросов Twitter
def twitter_api(user_id):
    search_url = f"https://api.twitter.com/2/users/{user_id}?user.fields=public_metrics"
    time.sleep(2)
    search_url_req = requests.get(search_url, headers=headers).json()
    user_id = search_url_req['data']['id']
    full_name = search_url_req['data']['name']
    number_of_subscribers = search_url_req['data']['public_metrics']['following_count']
    source_url = 'https://twitter.com/' + search_url_req['data']['username']
    usefull_content = (source_url, number_of_subscribers, full_name, user_id)
    return usefull_content


x = 0
for i in range(0, len(sorted_source_id)):
    content_from_db = get_content_from_db(sorted_source_id[x])
    usefull_content = twitter_api(content_from_db[2])
    source_url = usefull_content[0]
    number_of_subscribers = usefull_content[1]
    full_name = usefull_content[2]
    user_id = usefull_content[3]
    source_id = content_from_db[0]
    # обновление полей таблицы resource
    update_content = (source_url, number_of_subscribers, full_name, user_id, source_id)
    update_resource(update_content)
    x += 1

# # добавление страницы в табицу resource
# insert_content = ('source_url', 'number_of_subscribers', 'full_name', 'user_id', 'type')
# #insert_resource(insert_content)
#
close_connect()
print("--- %s seconds ---" % (time.time() - start_time))