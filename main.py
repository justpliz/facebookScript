import mysql.connector
from mysql.connector import Error

CONNECTION = {'host': 'localhost', 'database': 'facebookScript','user': 'root', 'password': 'MYSQL'}

try:
    connection = mysql.connector.connect(**CONNECTION)

    mySql_create_table_query = """CREATE TABLE facebookScript (
                                 source_id bigint(20) NOT NULL AUTO_INCREMENT,
                                 followers int(10) NULL,
                                 followers_url varchar(255) NOT NULL,
                                 name varchar(255) NULL,
                                 PRIMARY KEY (source_id)) """
    cursor = connection.cursor()
    result = cursor.execute(mySql_create_table_query)
    print("facebookScript Table created successfully")


except mysql.connector.Error as error:
    print("Failed to create table in MySQL: {}".format(error))

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")