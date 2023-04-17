from db_tools import *

conn = open_connection()
#NEEDS REFACTORING
client_id = 3
clients_query = f"INSERT INTO clients(client_id, first_name, last_name, phone_number, email) VALUES ({client_id}, 'George', 'Tsamis', '6986530179', 'george.tsamis.cs@gmail.com')"
appointments_query = f"INSERT INTO appointments(appointment_id, appointment_date, appointment_interval, client_id) VALUES ({client_id}, '2023/5/13 10:00:00', '2023/5/13 10:30:00', 1)"
try:
    cursor = conn.cursor()
    cursor.execute(clients_query)
    cursor.execute(appointments_query)
    conn.commit()
except MYSQL.Error as e:
    print(e)

close_connection(conn)


#deletion query

