#############SEARCH METHODS for SEARCH TAB#######################

import xlsxwriter
import tkinter as tk
import sqlite3
import calendar
from datetime import date
from db_tools import open_connection, close_connection
from tkinter import filedialog
from tkinter.messagebox import showinfo,showerror,showwarning




class Search_methods():

    def update_days(self,year_combo,month_combo,day_combo):
        '''Μέθοδος για τον  υπολογισμο του πληθους ημερών στο combobox DAY του search tab ανάλογα με την επιλογή
          που έκανε ο χρήστης στο combobox MONTH.'''
        #Έλεγχος για το αν ο χρήστης εισήγαγε και έτος πριν συνεχίσει στην επιλογή του μήνα.
        if year_combo.get()=='':
            showerror(title="Error",message="Invalid date. Please select a valid Year first!")
        else:    
            self.selected_month=int(month_combo.get())
            self.selected_year=int(year_combo.get())
            self.num_days=calendar.monthrange(self.selected_year,self.selected_month)[1]
            self.day_cb=day_combo['values']=list(range(1,self.num_days+1))



    def appointment_date(self,rv_date):
        '''Μέθοδος για fetch των πληροφοριών των πελατών οι οποίοι έχουν ραντεβού σε συγκεκριμένη ημερομηνία.
            Ορίσματα: rv_date: Ημερομηνία για την οποία θα γίνει αναζήτηση των ραντεβού.'''
        self.connection=open_connection()
        try:
            cursor=self.connection.cursor()
            query=f"SELECT clients.first_name, clients.last_name, clients.email, strftime('%H:%M:%S', appointments.appointment_date) AS appointment_time, strftime('%Y-%m-%d', appointments.appointment_date) AS appointment_date FROM clients JOIN appointments ON clients.client_id = appointments.client_id WHERE strftime('%Y-%m-%d', appointments.appointment_date) = '{rv_date}'"
            cursor.execute(query)
            rows=cursor.fetchall()
            return(rows)                       

            cursor.close()
        except sqlite3.Error as e:
            print(e)
        close_connection(self.connection)

    
    
    def delete_info(self):
        '''Μέθοδος για την διαγραφή των πληροφοριών που βρίσκονται στο widget treeview.'''
        children=self.tree.get_children()
        for child in children:
            self.tree.delete(child)
    
    

    def add_info(self,tree_info):
        '''Μέθοδος για προσθήκη των πληροφοριών στο widget treeview.
            Ορίσματα: Λίστα με πληροφορίες πελατών'''
        #'Ελεγχος αν η λίστα είναι κενή και επιστροφή κατάλληλου μηνύματος
        if tree_info==[]:
            list_info=showinfo(title="Info",message="No Appointments at selected date!!")
        #Αν η λίστα περέχει πληροφορίες γίνεται χρήση της insert και εισαγωγή των πληροφοριών στο treeview
        else:
            for contact in tree_info:
                self.tree.insert('', tk.END, values=contact)

            
    def confirmation_button(self,year_combo,month_combo,day_combo):
        '''Μέθοδος η οποία καλείται όταν ο χρήστης επιλέξει το πλήκτρο (button) 'OK' αφού πρώτα έχει επιλέξει
            την επιθυμητή ημερομηνία μέσω των comboboxes YEAR,MONTH,DAY.
            Ορίσματα:
                 year_combo: Χρονολογία (έτος)
                 month_combo: Μήνας
                 day_combo: Ημέρα(του μήνα)'''
        # Έλεγχος για τον αν τα ορίσματα είναι εγκυρα(αν ο χρήστης έχει επιλέξει τιμές στα comboboxes YEAR,MONTH,DAY)
        # Αν κάποια τιμή έχει μείνει κενή εμφανίζεται ανάλογο μήνυμα.
        if year_combo=='': 
            show_error=showerror(title="Error",message="Invalid date. Please select a valid date (Year)!")
        elif month_combo=='':
            show_error=showerror(title="Error",message="Invalid date. Please select a valid date (Month)!")
        elif day_combo=='':
            show_error=showerror(title="Error",message="Invalid date. Please select a valid date (Day)!")
        else:
            # καλείται η function delete_info() για να καθαρίσει το widget treeview απο παλαιότερες αναζητήσεις
            self.delete_info()
            #Μετατροπή των τιμών απο str σε int και με τη date() μετατροπή σε ημερομηνία.            
            self.selected_date=date(int(year_combo),int(month_combo),int(day_combo))     
            self.add_info(self.appointment_date(self.selected_date))

    #function του πλήκτρου Print Appointments
    def print_appointment(self):
        '''Μέθοδος για εξαγωγή των στοιχείων απο το widget treeview και αποθήκευση σε αρχείο .xlsx'''
        # Εξαγωγή των στοιχείων απο το widget treeview και αποθήκευση ως list στη variable data
        data=self.extraction_data()
        # Χρήση του module filedialog.asksaveasfilename για την δημιουργία "παραθύρου" για επιλογή που θα
        # αποθηκευθεί το αρχείο με defaultxtension .xlsx και αρχικό όνομα.
        if data==[]:
            show_print_warn=showwarning(title="Warning",message="No appointments to print!")
        else:       
            file_path=filedialog.asksaveasfilename(defaultextension='.xlsx',initialfile=f'Appointment of {data[0][4]}')
            
            if file_path:
                self.workbook=xlsxwriter.Workbook(file_path)
                self.worksheet=self.workbook.add_worksheet()

                #bold format
                bold=self.workbook.add_format({'bold':True})

                #onomasia ton headers
                
                self.worksheet.write('A1','#',bold)
                self.worksheet.write('B1','First Name',bold)
                self.worksheet.write('C1','Last Name',bold)
                self.worksheet.write('D1','EMAIL',bold)
                self.worksheet.write('E1','Appointment Time',bold)
                    
                
                

                #adust the width
                self.worksheet.set_column('A:A',5)
                self.worksheet.set_column('B:B',15)
                self.worksheet.set_column('C:C',15)
                self.worksheet.set_column('D:D',23)
                self.worksheet.set_column('E:E',20)

                


                row=1
                col=0
                #insert data
                for i in range(len(data)):
                    self.worksheet.write(row,col,f'{i+1}')
                    self.worksheet.write(row,col+1,f'{data[i][0]}')
                    self.worksheet.write(row,col+2,f'{data[i][1]}')
                    self.worksheet.write(row,col+3,f'{data[i][2]}')
                    self.worksheet.write(row,col+4,f'{data[i][3]}')
                    row+=1

                show_info=showinfo(message=f'The file "Appointment of {data[0][4]}" was saved.')


                self.workbook.close()  