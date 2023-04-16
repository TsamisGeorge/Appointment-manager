#this is where the database tools and connection objects will be
import mysql.connector as MYSQL


#defining open connection to connect to the db
def open_connection():
    try:
        return MYSQL.connect(
            host = "localhost",
            user = "amdb_user",
            password = "amdb_eap_project",
            #database will be the name of the mysql database
            database = "amdb"
        )
    except MYSQL.Error as e:
        #if there is any error while trying to connect to the database it will print the exact error
        print(e)

def close_connection(connection):
    try:
        connection.close()
    except MYSQL.Error as e:
        print(e)


