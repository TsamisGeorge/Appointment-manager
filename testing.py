
import mysql.connector as MYSQL
from db_tools import *
def open_connection():
    try:
        return MYSQL.connect(
            host = "34.163.109.227",
            port = "3306",
            user = "amdb_user",
            password = "amdb_eap_project",
            database = "amdb"
        )
    except MYSQL.Error as e:
        print(e)

def close_connection(connector):
    try:
        connector.close()      
    except MYSQL.Error as e:
        print(e)

connection = open_connection()

x = fetch_all_dict_list(connection, "SELECT * FROM clients")
print(x)