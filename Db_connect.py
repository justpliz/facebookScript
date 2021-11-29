import mysql.connector
from mysql.connector import Error

CONNECTION = {'host': 'localhost', 'database': 'facebookScript', 'user': 'root', 'password': 'MYSQL'}

try:
    connection = mysql.connector.connect(**CONNECTION)

    mySql_create_table_query = """CREATE TABLE resource (
                                 source_id bigint(20) NOT NULL AUTO_INCREMENT,
                                 source_url varchar(255) NOT NULL,
                                 number_of_subscribers int(10) NULL,
                                 first_name varchar(255) NULL,
                                 second_name varchar(255) NULL,
                                 PRIMARY KEY (source_id)) """
    cursor = connection.cursor()
    result = cursor.execute(mySql_create_table_query)
    print("resource Table created successfully")


except mysql.connector.Error as error:
    print("Failed to create table in MySQL: {}".format(error))

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


def insert_resource(source_url, number_of_subscribers, first_name, second_name):
    try:
        connection = mysql.connector.connect(**CONNECTION)
        mySql_insert_resources_query = """INSERT INTO resource (source_url, number_of_subscribers, 
        first_name, second_name)
                               VALUES
                               (%s, %s, %s, %s) """
        record = (source_url, number_of_subscribers, first_name, second_name)
        cursor = connection.cursor()
        cursor.execute(mySql_insert_resources_query, record)
        connection.commit()
        print("Record inserted successfully into resource table")

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")