import tkinter as tk
from tkinter import ttk
from tkcalendar import *
from db_tools import *
from datetime import datetime

class Appointment_manager:
    def __init__(self):
        #main app window
        self.main_window = tk.Tk()
        self.main_window.geometry("1000x600")
        self.main_window.title("Appointment Manager")
        icon = tk.PhotoImage(file="time-management.png")
        self.main_window.iconphoto(True, icon)


        #making the notebook object to hold the tabs of the app
        self.notebook = ttk.Notebook(self.main_window)
        notebook_style = ttk.Style()
        notebook_style.configure('TNotebook.Tab', font=('Segoe UI', 12), padding=[2, 1])
        self.notebook.grid()

        #making the frames that will go to the notebook as tabs
        self.new_apt = tk.Frame(self.notebook)
        self.apt_changes = tk.Frame(self.notebook)
        self.del_apt = tk.Frame(self.notebook)
        self.print_apt = tk.Frame(self.notebook)

        self.temp = tk.Frame(self.notebook)
    def start(self):
        #loading the pictures of the GUI
        new_apt_icon = tk.PhotoImage(file="calendar.png").subsample(30)
        apt_changes_icon = tk.PhotoImage(file="recurrent.png").subsample(30)
        del_apt_icon = tk.PhotoImage(file="del.png").subsample(30)
        print_apt_icon = tk.PhotoImage(file="printing.png").subsample(30)

        #adding the tabs
        self.notebook.add(self.new_apt, text="Schedule appointment", image=new_apt_icon, compound='left')
        self.notebook.add(self.apt_changes, text="Reschedule appointment", image=apt_changes_icon, compound='left')
        self.notebook.add(self.del_apt, text="Delete appointment", image=del_apt_icon, compound='left')
        self.notebook.add(self.print_apt, text="Print appointments", image=print_apt_icon, compound='left')

        #adding the labels and entry boxes to the new_apt tab of the notebook 
        self.first_name_label = tk.Label(self.new_apt, text = "First name: ", font=("Segoe UI", 12))
        self.first_name_entry = tk.Entry(self.new_apt, width=50)
        self.first_name_label.grid(row = 0, column = 0, sticky= tk.W, padx=12, pady=12)
        self.first_name_entry.grid(row = 0,padx=100,sticky= tk.W)

        self.surname_label = tk.Label(self.new_apt, text = "Surname: ", font=("Segoe UI", 12))
        self.surname_entry = tk.Entry(self.new_apt, width=50)
        self.surname_label.grid(row = 1, column = 0, sticky= tk.W, padx=12, pady=12)
        self.surname_entry.grid(row = 1,padx=100,sticky= tk.W)

        self.email_label = tk.Label(self.new_apt, text = "Email: ", font=("Segoe UI", 12))
        self.email_entry = tk.Entry(self.new_apt, width=50)
        self.email_label.grid(row = 2, column = 0, sticky= tk.W, padx=12, pady=12)
        self.email_entry.grid(row = 2,padx=100,sticky= tk.W)

        self.phone_number_label = tk.Label(self.new_apt, text = "Phone Number: ", font=("Segoe UI", 12))
        self.phone_number_entry = tk.Entry(self.new_apt, width=15)
        self.phone_number_label.grid(row = 3, column = 0, padx=12, pady=12, sticky= tk.W)
        self.phone_number_entry.grid(row = 3,padx=130, sticky= tk.W)

        self.cal = Calendar(self.new_apt, selectmode='day', showweeknumbers=False, showothermonth=False, font=("Segoe UI", 10))
        self.cal.grid(row=4, column=0, pady = 30, padx=12, sticky=tk.W)
        self.cal.config(background='Steel Blue', foreground='black')


        self.time_label = tk.Label(self.new_apt, text="Select Time:")
        self.time_label.grid(row=4,column=0,padx=150)
        self.time_entry = tk.Entry(self.new_apt)
        self.time_entry.insert(0, "12:00")
        self.time_entry.grid()


        #buttons to set dates etc
        self.date_button = tk.Button(self.new_apt,width=28,bg='Steel Blue', font=("Segoe UI", 11), text = "Set Date", command = self.get_date)
        self.date_button.grid(row = 5,column=0, padx=11, sticky=tk.W, columnspan=1)

        self.contact_info_button = tk.Button(self.new_apt,height = 1,width =20, bg='Steel Blue', font = ("Segoe UI",10), text = "Set Contact Info", command = self.get_contact_info)
        self.contact_info_button.grid(row=3, padx=254,column=0, sticky=tk.W)
        #opening the database connection
        self.connection = open_connection()
        
        #mainloop
        self.main_window.mainloop()

    ##NEEDS REFACTORING
    def get_date(self):
        date = self.cal.selection_get()
        print("Selected Date:", date)

    def get_contact_info(self):
        name = self.first_name_entry.get()
        surname = self.surname_entry.get()
        email = self.email_entry.get()
        phone_number = self.phone_number_entry.get()
        print(f"Contact info: {name} {surname} {email} {phone_number}")


    #IGNORE FOR NOW  
    def schedule(self):
        pass
    
    def reschedule(self):
        pass

    def delete(self):
        pass

    def print_one_day_apt(self):
        pass