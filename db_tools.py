
import mysql.connector as MYSQL
import smtplib

#open conn with the db func
def open_connection():
    try:
        return MYSQL.connect(
            host = "localhost",
            user = "amdb_user",
            password = "amdb_eap_project",
            database = "amdb"
        )
    #printing error if any occurs
    except MYSQL.Error as e:
        print(e)

#closing the conn with the connector obj as the arg
def close_connection(connector):
    try:
        connector.close()      
    except MYSQL.Error as e:
        print(e)


#returns a list of dicts after the execution of a specified query passed as an argument together with the conn object
def fetch_all_dict_list(connector, query):
    try:
        #init cursor to be able to interact with the object, and each entry will be returned as a dict
        cursor = connector.cursor(dictionary = True)
        #executing the query
        cursor.execute(query)
        #result set is now a list of dicts
        result_set = cursor.fetchall()

        return result_set
    except MYSQL.Error as e:
        print(e)

#returns a list of tuples after the execution of a specified query passed as an argument together with the conn object
def fetch_all_tuple_list(connector, query):
    try:
        #init cursor to be able to interact with the object, and each entry will be returned as a tuple
        cursor = connector.cursor()
        #executing the query
        cursor.execute(query)
        #result set is now a list of tuples
        result_set = cursor.fetchall()

        return result_set
    except MYSQL.Error as e:
        print(e)


####MAYBE NEEDS REFACTORING BECAUSE OF DIFFERENT DATABASE
####IGNORE ALL COMMENTS TO THIS
#func to insert entries to the db
def insert_query(connector, query):
    cursor = connector.cursor()
    cursor.execute(query)
    #close the cursor
    cursor.close()


#abstract name to basic operation of cursor execution
def update_query(connector, query):
    cursor = connector.cursor()
    cursor.execute(query)
    cursor.close()

#abstract name to basic operation of cursor execution
def delete_query(connector, query):
    cursor = connector.cursor()
    cursor.execute(query)
    cursor.close()