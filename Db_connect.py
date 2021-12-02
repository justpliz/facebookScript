import mysql.connector
from main import item_content
from mysql.connector import Error

CONNECTION = {'host': 'localhost', 'database': 'facebookScript', 'user': 'root', 'password': 'MYSQL'}
connection = mysql.connector.connect(**CONNECTION)
cursor = connection.cursor()

def create_resource_table(cursor):
    try:
        mySql_create_table_query = """CREATE TABLE resource (
                                     source_id bigint(20) NOT NULL AUTO_INCREMENT,
                                     source_url varchar(255) NOT NULL,
                                     number_of_subscribers int(10) NOT NULL,
                                     full_name varchar(255) NOT NULL,
                                     user_id varchar(255) NOT NULL,
                                     type varchar(255) NOT NULL,
                                     update_date date NOT NULL,
                                     PRIMARY KEY (source_id)) """
        result = cursor.execute(mySql_create_table_query) #delete
        print("resource Table created successfully")

    except mysql.connector.Error as error:
        print("Failed to create table in MySQL: {}".format(error))

# def insert_resource(CONTENT):
#     try:
#         connection = mysql.connector.connect(**CONNECTION)
#         mySql_insert_resources_query = """INSERT INTO resource (source_url, number_of_subscribers, full_name)
#                                VALUES (%s, %s, %s) """
#         record = CONTENT
#         cursor = connection.cursor()
#         cursor.execute(mySql_insert_resources_query, record)
#         connection.commit()
#         print("Record inserted successfully into resource table")
#
#     except mysql.connector.Error as error:
#         print("Failed to insert into MySQL table {}".format(error))

def update_resource(cursor, item_content):
    try:
        print("Before updating a record ")
        sql_select_query = ""f"select * from resource where id = {item_content[0]}"""
        cursor.execute(sql_select_query)
        record = cursor.fetchone()
        print(record)

    except mysql.connector.Error as error:
        print("Failed to update table record: {}".format(error))

def get_source_url(source_url):
    cursor.execute("SELECT source_url FROM resource")
    url = cursor.fetchall()[source_url]
    resource_url = ''.join(map(str, url))
    return resource_url

create_resource_table(cursor)

if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")