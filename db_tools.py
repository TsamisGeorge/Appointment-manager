# ------------------------------------------ #
# TOOLS FOR THE CONNECTION WITH THE DATABASE #
# ------------------------------------------ #


# sqlite import that has all the tools in order to connect to the .db database file
import sqlite3


def open_connection():
    '''Μέθοδος που επιστρέφει ενα αντικειμενο τυπου connection που είναι η σύνδεσ με την ΒΔ'''
    try:
        conn = sqlite3.connect("db_2.db")
        return conn
    except sqlite3.Error as e:
        print(f"Error: {e}")


def close_connection(connector):
    '''Μεθοδος που κλεινει την συνδεση με την βαση δεδομενων
    
    Ορίσματα:
    
    connector: Ένα αντικείμενο τυπου connection που εχει ήδη ανοιχθει'''
    try:
        connector.close()      
    except sqlite3.Error as e:
        print(e)



def fetch_all_dict_list(connector, query):
    '''Μέθοδος που επιστρέφει λίστα με λεξικά απο entries της ΒΔ
    
    Ορίσματα:
    
    connector: Αντικείμενο τυπου connection που έχει ήδη ανοιχθεί σε μία ΒΔ
    
    query: (str) Το query που θα εκτελεστεί στο σώμα της συνάρτησης'''
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
    '''Συναρτηση που εκτελει το query που δινεται σαν ορισμα
    
    Ορίσματα:
    
    connector: Αντικείμενο τυπου connection που έχει ήδη ανοιχθεί σε μία ΒΔ
    
    query :(str) Το query που θα εκτελεστεί στο σώμα της συνάρτησης'''
    try:
        cursor = connector.cursor()
        cursor.execute(query)
        cursor.close()
    except sqlite3.Error as e:
        print(e)