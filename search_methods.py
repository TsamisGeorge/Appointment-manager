#############SEARCH METHODS for SEARCH TAB#######################

import xlsxwriter
import tkinter as tk
import sqlite3
import calendar
from datetime import date
from db_tools import open_connection, close_connection
from tkinter import filedialog
from tkinter.messagebox import showinfo,showerror




class Search_methods():
    #function για υπολογισμο του πληθους ημερών ανά μήνα στο search tab
    def update_days(self,current_year,month_combo,day_combo):
        self.selected_month=int(month_combo.get())
        self.num_days=calendar.monthrange(current_year,self.selected_month)[1]
        self.day_cb=day_combo['values']=list(range(1,self.num_days+1))



    #function για fetch των στοιχειων απο την database
    def appointment_date(self,rv_date):
        self.connection=open_connection()
        try:
            cursor=self.connection.cursor()
            query=f"SELECT clients.first_name, clients.last_name, clients.email, strftime('%H:%M:%S', appointments.appointment_date) AS appointment_time, strftime('%Y-%m-%d', appointments.appointment_date) AS appointment_date FROM clients JOIN appointments ON clients.client_id = appointments.client_id WHERE strftime('%Y-%m-%d', appointments.appointment_date) = '{rv_date}'"
            cursor.execute(query)
            rows=cursor.fetchall()
            set_rows=[values for values in rows]
            list_rows=list(set_rows)
            return(list_rows)                       

            cursor.close()
        except sqlite3.Error as e:
            print(e)
        close_connection(self.connection)

    
    #function gia erase to stoixeion apo to treeview
    def delete_info(self):
        children=self.tree.get_children()
        for child in children:
            self.tree.delete(child)
    
    
    
    
    #function ta stoixeia na mpoun sto treeview

    def add_info(self,tree_info):
        for contact in tree_info:
            self.tree.insert('', tk.END, values=contact)

            



    #function του πλήκτρου OK στην επιλογή ημερομηνίας στο Search Tab
    def confirmation_button(self,year_combo,month_combo,day_combo):
        self.delete_info()
        if year_combo=='' or month_combo=='' or day_combo=='':
            show_error=showerror(message="Invalid date. Please select a valid date (Year,Month,Date)")
        else:
            self.selected_date=date(int(year_combo),int(month_combo),int(day_combo))     
            self.add_info(self.appointment_date(self.selected_date))

    #function του πλήκτρου Print Appointments
    def print_appointment(self):
        data=self.extraction_data()
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