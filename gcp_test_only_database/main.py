import mysql.connector
#kanoume import tis 2 methodous gia sindesi kai aposindesi ston sql server
from db_tools import open_connection, close_connection,fetch_all_dict_list
MYSQL=mysql.connector



#"anoigei" i sindesi kai to antikeimeno apothieuetai
#stin mtavliti conn
conn=open_connection()

try:
    #dimiourgoume to antikeimeno MySQLCursor kai to
    #apothikeuoumai sti metavliti cursor
    cursor=conn.cursor()

    #sti metavliti query sintassoumai kai apothikeuoumai me morfi str
    #to erotima pros tin vasi dedomenon. En sinexeia ti metavliti query
    #tin thetoume os orisma sthn methodo execute.
    query=f"SELECT first_name,last_name,email\
                FROM amdb.clients\
                JOIN appointments ON clients.client_id = appointments.client_id\
                WHERE DATE(appointments.appointment_date)='2023-05-12'"
    cursor.execute(query)


    #Pairnoume tin apantisi meso tou fetch. kai afou tin apothikeusoume
    #sti metavliti rows ,tin ektiponoume.
    rows=cursor.fetchall()
    print(rows)
    print(type(rows))
    print(type(rows[0]))
    set_rows={values for values in rows}
    print(type(set_rows))
    set_list1=list(set_rows)
    print(set_list1[0][2])
    print(type(set_list1))
    
    #Telos kelinoume ton cursor
    cursor.close()
except MYSQL.Error as e:
    print(e)

#Termatismos tou connection
close_connection(conn)