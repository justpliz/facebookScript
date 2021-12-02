import mysql.connector
from mysql.connector import Error

CONNECTION = {'host': 'localhost', 'database': 'facebookScript', 'user': 'root', 'password': 'MYSQL'}
connection = mysql.connector.connect(**CONNECTION)


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

def insert_resource(cursor, insert_content):
    try:
        mySql_insert_resources = """INSERT INTO resource (source_url, number_of_subscribers, full_name, 
        user_id, type, update_date)
                               VALUES (%s, %s, %s, %s, %s, %s) """
        cursor.execute(mySql_insert_resources, insert_content)
        connection.commit()
        print("Record inserted successfully into resource table")

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

def update_resource(cursor, update_content):
    try:
        mySql_update_resources = """Update resource set source_id = %s, source_url = %s, number_of_subscribers = %s, 
        full_name = %s, user_id = %s, type = %s, update_date = %s where 
        source_id = 1"""

        source_id = update_content[0]
        source_url = update_content[1]
        number_of_subscribers = update_content[2]
        full_name = update_content[3]
        user_id = update_content[4]
        type = update_content [5]
        update_date = update_content [6]

        cursor.execute(mySql_update_resources, update_content)
        connection.commit()
        print("Record updated successfully into resource table")
        #record = cursor.fetchone()
        #print(record)

    except mysql.connector.Error as error:
        print("Failed to update table record: {}".format(error))

def get_source_url(cursor, source_url):
    cursor.execute("SELECT source_url FROM resource")
    url = cursor.fetchall()[source_url - 1]
    resource_url = ''.join(map(str, url))
    return resource_url