# appointment_manager
App that manages appointments

(!)In order to run the program, download pip packages needed, change db_1.db filename to db_2.db, and run it through main.py, email being sent is as of now a WIP as to other users using it, thus it will produce bugs if you try to use it. 

Python project of an application that manages appointments and customers, and can perform CRUD operations on them.

The database used is a .db sqlite file, that gets accessed through the python code using its name and the sqlite3 connector

Appointments tab is used to handle appointments of a specific existing customer, searching him with phone or email and then performing the operations.
(rescheduling of an appointment draws values from the appointment time and appointment duration fields).

Customers tab is used to handle customers, searching a specific existing customer with phone or email to change or delete him, or creating a new one.
