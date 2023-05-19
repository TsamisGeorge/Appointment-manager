###  TOOLS FOR THE CONNECTION WITH THE DATABASE  ###
####################################################


import sqlite3


def open_connection():
    '''Μεθοδος που επιστρεφει ενα αντικειμενο τυπου connection
    που αντιπροσωπευει την συνδεση με την βαση δεδομενων που εχει δηλωθει'''
    try:
        conn = sqlite3.connect("db_1.db")
        return conn
    except sqlite3.Error as e:
        print(f"Error: {e}")


def close_connection(connector):
    '''Μεθοδος που κλεινει την συνδεση με την βαση δεδομενων,
    παιρνει σαν παραμετρο αντικειμενο τυπου sqlite3.connect()'''
    try:
        connector.close()      
    except sqlite3.Error as e:
        print(e)



def fetch_all_dict_list(connector, query):
    '''Μεθοδος που επιστρεφει λιστα με λεξικα, απο την βαση δεδομενων που
    δινεται σαν ορισμα, εκτελωντας το query που δινεται σαν ορισμα'''
    try:
        cursor = connector.cursor()
        cursor.execute(query)

        # Συνεπτυγμενη λιστα που περιεχει τα αναγνωριστικα των στηλων
        columns = [column[0] for column in cursor.description]

        # Συνεπτυγμενη λιστα που παιρνει τα δεδομενα μετα απο την εκτελεση
        # του query, και για καθε καταγραφη μεσα στο zip(columns, row) που ειναι
        # iterator που περιεχει αναγνωριστικο στηλης και την εκαστοτε καταγραφη,
        # δημιουργει ενα λεξικο με κλειδι το αναγνωριστικο και τιμη την καταγραφη       
        result_dict = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return result_dict
    except sqlite3.Error as e:
        print(e)


def execute_query(connector, query):
    '''Συναρτηση που εκτελει το query που δινεται σαν ορισμα'''
    try:
        cursor = connector.cursor()
        cursor.execute(query)
        cursor.close()
    except sqlite3.Error as e:
        print(e)