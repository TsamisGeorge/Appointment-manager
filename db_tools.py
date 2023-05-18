###  TOOLS FOR THE CONNECTION WITH THE DATABASE  ###
####################################################


import sqlite3

#open conn with the db func
def open_connection():
    try:
        # Άνοιγμα του connection με χρήση της .connect() και όρισμα το .db αρχείο που θέλουμε να ανοίξουμε
        conn = sqlite3.connect("db_1.db")
        # επιστροφή του connection, εκτός αν κάτι πάει λάθος τότε τυπώνεται μύνημα του λάθους
        return conn
    except sqlite3.Error as e:
        print(f"Error: {e}")


def close_connection(connector):
    try:
        connector.close()      
    except sqlite3.Error as e:
        print(e)


#returns a list of dicts after the execution of a specified query passed as an argument together with the conn object
def fetch_all_dict_list(connector, query):
    try:
        cursor = connector.cursor()
        cursor.execute(query)

        # list comp to get the column names
        columns = [column[0] for column in cursor.description]

        # fetching all rows and converting them into a dict
        result_dict = [dict(zip(columns, row)) for row in cursor.fetchall()]

        #returning the resulting dict
        return result_dict
    except sqlite3.Error as e:
        print(e)


def execute_query(connector, query):
    try:

        cursor = connector.cursor()
        cursor.execute(query)
        cursor.close()
    except sqlite3.Error as e:
        print(e)