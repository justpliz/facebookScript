import mysql.connector

CONNECTION = {'host': 'localhost', 'database': 'facebook_script', 'user': 'Abay', 'password': 'MYSQL'}
connection = mysql.connector.connect(**CONNECTION)
cursor = connection.cursor()

def create_resource_table():
    try:
        mySql_create_table_query = """CREATE TABLE resource (
                                     source_id bigint(20) NOT NULL AUTO_INCREMENT,
                                     source_url varchar(255) NOT NULL,
                                     number_of_subscribers int(10) NOT NULL,
                                     full_name varchar(255) NOT NULL,
                                     user_id varchar(255) NOT NULL,
                                     type varchar(255) NOT NULL,
                                     update_date datetime NOT NULL,
                                     PRIMARY KEY (source_id)) """
        cursor.execute(mySql_create_table_query)
        print("resource Table created successfully")

    except mysql.connector.Error as error:
        print("Failed to create table in MySQL: {}".format(error))

def sorted_table():
    try:
        mySql_sorted_table = "SELECT source_id FROM resource WHERE type = 'Facebook' ORDER BY update_date"
        cursor.execute(mySql_sorted_table)
        sorted_source_id = cursor.fetchall()
        sorted_source_id = list(sum(sorted_source_id, ()))
        connection.commit()

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    return sorted_source_id

def insert_resource(insert_content):
    try:
        mySql_insert_resources = """INSERT INTO resource (source_url, number_of_subscribers, full_name, 
        user_id, type, update_date)
                               VALUES (%s, %s, %s, %s, %s, NOW()) """
        record = insert_content
        connection.cursor()
        cursor.execute(mySql_insert_resources, record)
        connection.commit()
        print("Record inserted successfully into resource table")

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

def update_resource(update_content):
    try:
        mySql_update_resources = """Update resource set source_url = %s, number_of_subscribers = %s, 
        full_name = %s, user_id = %s, update_date = NOW() where source_id = %s"""

        source_url = update_content[0]
        number_of_subscribers = update_content[1]
        full_name = update_content[2]
        user_id = update_content[3]
        source_id = update_content[4]

        cursor.execute(mySql_update_resources, update_content)
        connection.commit()
        print("Record updated successfully into resource table")

    except mysql.connector.Error as error:
        print("Failed to update table record: {}".format(error))

def get_content_from_db(count):
    cursor.execute("SELECT source_id FROM resource")
    source_id = cursor.fetchall()[count - 1]
    source_id = ''.join(map(str, source_id))
    cursor.execute("SELECT source_url FROM resource")
    source_url = cursor.fetchall()[count - 1]
    source_url = ''.join(map(str, source_url))
    source_id_and_url = (source_id, source_url)
    return source_id_and_url

def close_connect():
    cursor.close()
    connection.close()
    print("MySQL connection is closed")