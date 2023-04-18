import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from tkcalendar import *
from db_tools import *
from datetime import *
from email_validator import validate_email, EmailNotValidError
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
        self.notebook.place(x=0, y=0, relwidth=1, relheight=1)

        #making the frames that will go to the notebook as tabs
        self.new_apt = tk.Frame(self.notebook)
        self.apt_changes = tk.Frame(self.notebook)
        self.del_apt = tk.Frame(self.notebook)
        self.print_apt = tk.Frame(self.notebook)

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
        self.first_name_label.place(x=12, y=20)
        self.first_name_entry.place(x=100, y=25)

        self.surname_label = tk.Label(self.new_apt, text = "Surname: ", font=("Segoe UI", 12))
        self.surname_entry = tk.Entry(self.new_apt, width=50)
        self.surname_label.place(x=12, y=80)
        self.surname_entry.place(x=100, y=85)

        self.email_label = tk.Label(self.new_apt, text = "Email: ", font=("Segoe UI", 12))
        self.email_entry = tk.Entry(self.new_apt, width=50)
        self.email_label.place(x=12, y=140)
        self.email_entry.place(x=100, y=145)

        self.phone_number_label = tk.Label(self.new_apt, text = "Phone Number: ", font=("Segoe UI", 12))
        self.phone_number_entry = tk.Entry(self.new_apt, width=15)
        self.phone_number_label.place(x=12, y=200)
        self.phone_number_entry.place(x=135, y=205)

        today = date.today()
        self.date_picker = Calendar(self.new_apt, selectmode='day', showweeknumbers=False, showothermonth=False, font=("Segoe UI", 10), mindate = today)
        self.date_picker.place(x=12, y=300)
        self.date_picker.config(background='Steel Blue', foreground='black')

        #appointment time picker
        self.time_picker_label = tk.Label(self.new_apt, text = "Pick Appointmen Time: ", font=("Segoe UI", 11))
        self.time_picker_label.place(x = 252, y =294)
        hour = 24 -(24-datetime.now().hour)
        time_var = tk.StringVar()
        self.time_picker = ttk.Combobox(self.new_apt, textvariable=time_var, values=[f"{str(h).zfill(2)}:{str(m).zfill(2)}" for h in range(hour+1, 24) for m in range(0, 60, 10)])
        self.time_picker.place(x = 260, y =330)
        
        #appointment duration picker
        self.time_picker_label2 = tk.Label(self.new_apt, text = "Pick Appointment Duration: ", font=("Segoe UI", 11))
        self.time_picker_label2.place(x = 252, y =380)
        time_var2 = tk.StringVar()
        self.time_picker2 = ttk.Combobox(self.new_apt, textvariable=time_var2, values=[f"{m}" for m in range(20, 60+1, 10)])
        self.time_picker2.place(x = 260, y =416)

        #button to set date
        self.date_button = tk.Button(self.new_apt,width=28,bg='Steel Blue', font=("Segoe UI", 11), text = "Set Date", command = self.get_date)
        self.date_button.place(x= 11, y = 490)

        #button to get client credentials
        self.contact_info_button = tk.Button(self.new_apt,height = 1,width= 20, bg='Steel Blue', font = ("Segoe UI",10), text = "Set Contact Info", command = self.get_contact_info)
        self.contact_info_button.place(x=250, y=200)

        #button to sumbit an appointment and start the logic testing
        self.sumbit_apt_button = tk.Button(self.new_apt,bg='Steel Blue', font = ("Segoe UI",12), text = "Submit", width=16, command = self.submit)
        self.sumbit_apt_button.place(x = 255, y = 460)


        #opening the database connection
        self.connection = open_connection()

        #mainloop
        self.main_window.mainloop()
    
    ##could need refactoring later
    def get_date(self):
        date_string = f'{self.date_picker.selection_get()}'
        date_format = '%Y-%m-%d'
        date_obj = datetime.strptime(date_string, date_format).date()
        if(date_obj.day == datetime.today().day):
            #destroy time widget, but make it the same as above, because the hour might have changed
            self.time_picker.destroy()
            hour = 24 -(24-datetime.now().hour)
            time_var = tk.StringVar()
            self.time_picker = ttk.Combobox(self.new_apt, textvariable=time_var, values=[f"{str(h).zfill(2)}:{str(m).zfill(2)}" for h in range(hour+1, 24) for m in range(0, 60, 10)])
            self.time_picker.place(x = 260, y =330)
        else:
            #make widget but make it whole
            self.time_picker.destroy()
            hour = 0
            time_var = tk.StringVar()
            self.time_picker = ttk.Combobox(self.new_apt, textvariable=time_var, values=[f"{str(h).zfill(2)}:{str(m).zfill(2)}" for h in range(hour, 24) for m in range(0, 60, 10)])
            self.time_picker.place(x = 260, y =330)

    #NEEDS REFACTORING
    def get_contact_info(self):
        name = self.first_name_entry.get()
        surname = self.surname_entry.get()
        email = self.email_entry.get()
        phone_number = self.phone_number_entry.get()
        print(f"Contact info: {name} {surname} {email} {phone_number} ")
    

    def submit(self):
        user_submit_input = messagebox.askyesno(title="Confirmation", message='Are you sure you want to submit this appointment?')
        if user_submit_input:
            try:
                name = self.first_name_entry.get().lstrip().rstrip()
                if not name.isalpha():
                    raise ValueError(f"'{name}' is not a valid name.")
                surname = self.surname_entry.get().lstrip().rstrip()
                if not surname.isalpha():
                    raise ValueError(f"'{surname}' is not a valid surname.")
                email = self.email_entry.get()
                if not validate_email(email).email:
                    raise ValueError(f"'{email}' is not a valid email.")
            except ValueError as e:
                messagebox.showwarning(title = "Invalid Input", message=f"{e}")
                
            #print(f'''{name} {surname} {self.email_entry.get()} {self.phone_number_entry.get()} {self.date_picker.selection_get()} {self.time_picker.get()} {self.time_picker2.get()}''')



    #IGNORE FOR NOW  
    def schedule(self):
        pass
    
    def reschedule(self):
        pass

    def delete(self):
        pass

    def print_one_day_apt(self):
        pass