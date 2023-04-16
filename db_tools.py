
import mysql.connector as MYSQL


#open conn with the db fuct
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
    #setting the local variable last_row_id as None
    last_row_id = None
    #if there is a primary key, with autoincrement(whenever a new entry is made, it raises the value of the primary key by a set amount)
    #and then cursor.lastrowid has the value of the last entry that we just made
    #if cursor.lastrowid is not none then we assign its value to last_row_id
    if cursor.lastrowid:
        last_row_id = cursor.lastrowid
    #close the cursor
    cursor.close()
    #return last row id whether it's none or it has a value 
    return last_row_id



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
    