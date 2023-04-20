import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from tkcalendar import *
from db_tools import *
from datetime import *
from email_validator import validate_email
from PIL import Image, ImageTk


class Appointment_manager:
    def __init__(self):
        #main app window
        self.main_window = tk.Tk()
        self.main_window.geometry("1000x600")
        self.main_window.title("Appointment Manager")
        icon = tk.PhotoImage(file="pics/appointment_manager.png")
        self.main_window.iconphoto(True, icon)


        #making the notebook object to hold the tabs of the app
        self.notebook = ttk.Notebook(self.main_window)
        notebook_style = ttk.Style()
        notebook_style.configure('TNotebook.Tab', font=('Segoe UI', 12), padding=[18, 2])
        self.notebook.place(x=0, y=0, relwidth=1, relheight=1)

        #making the frames that will go to the notebook as tabs
        self.appointments_tab = tk.Frame(self.notebook)
        self.customers_tab = tk.Frame(self.notebook)
        self.search_tab = tk.Frame(self.notebook)
        self.print_apt = tk.Frame(self.notebook)

    def start(self):
        #ICONS FOR TABS

        #Appointments tab
        appointments_icon = Image.open("pics/appointment.png")
        appointments_icon = appointments_icon.resize((26,26), Image.ANTIALIAS)
        appointments_icon = ImageTk.PhotoImage(appointments_icon)
        #Customers tab
        customers_icon = Image.open("pics/customer.png")
        customers_icon = customers_icon.resize((26, 26), Image.ANTIALIAS)
        customers_icon = ImageTk.PhotoImage(customers_icon)
        #Search tab
        search_icon = Image.open("pics/search.png")
        search_icon = search_icon.resize((26,26), Image.ANTIALIAS)
        search_icon = ImageTk.PhotoImage(search_icon)
        #Print Appointments tab
        print_apt_icon = Image.open("pics/printing.png")
        print_apt_icon = print_apt_icon.resize((26,26), Image.ANTIALIAS)
        print_apt_icon = ImageTk.PhotoImage(print_apt_icon)
        
        #ICONS FOR THINGS IN APPOINTMENTS TAB

        #searching customer img
        searching_customer_img = Image.open("pics/searching.png")
        searching_customer_img = searching_customer_img.resize((26,26), Image.ANTIALIAS)
        searching_customer_img = ImageTk.PhotoImage(searching_customer_img)

        #ADDING THE TABS TO THE notebook
        self.notebook.add(self.appointments_tab, text="Appointments", image=appointments_icon, compound='left')
        self.notebook.add(self.customers_tab, text="Customers", image=customers_icon, compound='left')
        self.notebook.add(self.search_tab, text="Search", image=search_icon, compound='left')   
        self.notebook.add(self.print_apt, text="Print appointments", image=print_apt_icon, compound='left')

        #####WIDGETS INSIDE THE CUSTOMERS TAB

        #adding the labels and entry boxes to the customers_tab
        self.first_name_label = tk.Label(self.customers_tab, text = "First name: ", font=("Segoe UI", 12))
        self.first_name_entry = tk.Entry(self.customers_tab, width=50)
        self.first_name_label.place(x=12, y=20)
        self.first_name_entry.place(x=100, y=25)

        self.surname_label = tk.Label(self.customers_tab, text = "Surname: ", font=("Segoe UI", 12))
        self.surname_entry = tk.Entry(self.customers_tab, width=50)
        self.surname_label.place(x=12, y=80)
        self.surname_entry.place(x=100, y=85)

        self.email_label = tk.Label(self.customers_tab, text = "Email: ", font=("Segoe UI", 12))
        self.email_entry = tk.Entry(self.customers_tab, width=50)
        self.email_label.place(x=12, y=140)
        self.email_entry.place(x=100, y=145)

        self.phone_number_label = tk.Label(self.customers_tab, text = "Phone Number: ", font=("Segoe UI", 12))
        self.phone_number_entry = tk.Entry(self.customers_tab, width=15)
        self.phone_number_label.place(x=12, y=200)
        self.phone_number_entry.place(x=135, y=205)

        #button to get client credentials
        self.contact_info_button = tk.Button(self.customers_tab,height = 1,width= 20, bg='Steel Blue', font = ("Segoe UI",10), text = "Set Contact Info", command = self.get_contact_info)
        self.contact_info_button.place(x=250, y=200)

        ##### WIDGETS INSIDE THE APPOINTMENTS TAB

        #Label, Button and Entry to search a customer and also print the customers appointments below
        self.search_customer_label = tk.Label(self.appointments_tab, text = "Search Customer", font=("Segoe UI", 12))
        self.search_customer_label.place(x=92,y=10)
        self.prompt_label = tk.Label(self.appointments_tab, text = "Enter customers phone number or email", font=("Segoe UI", 12))
        self.prompt_label.place(x=24,y=30)
        self.search_customer_entry = tk.Entry(self.appointments_tab, width= 50)
        self.search_customer_entry.place(x=12, y=60)
        self.search_customer_button = tk.Button(self.appointments_tab, compound=tk.LEFT, image=searching_customer_img, command=self.search_customer)
        self.search_customer_button.place(x=320, y=55)
        self.search_customer_entry.bind("<Return>", self.search_customer_enter)

        #string vars that are used to update labels of chosen customers/appointments etc
        self.selected_customer_full_name = tk.StringVar()
        self.selected_customer_full_name.set("Selected Customer: None")
        self.selected_customer_phone_number = None
        ##Label to show which customer is picked
        self.picked_customer_label = tk.Label(self.appointments_tab, textvariable=self.selected_customer_full_name, font=("Segoe UI", 11))
        self.picked_customer_label.place(x = 12, y = 80)

        #date picker
        today = date.today()
        self.date_picker = Calendar(self.appointments_tab, selectmode='day', showweeknumbers=False, showothermonth=False, font=("Segoe UI", 10), mindate = today)
        self.date_picker.place(x=12, y=300)
        self.date_picker.config(background='Steel Blue', foreground='black')

        #appointment time picker
        self.time_picker_label = tk.Label(self.appointments_tab, text = "Pick Appointment Time ", font=("Segoe UI", 11))
        self.time_picker_label.place(x = 252, y =294)
        hour = 24 -(24-datetime.now().hour)
        time_var = tk.StringVar()
        self.time_picker = ttk.Combobox(self.appointments_tab, textvariable=time_var, values=[f"{str(h).zfill(2)}:{str(m).zfill(2)}" for h in range(hour+1, 24) for m in range(0, 60, 10)])
        self.time_picker.place(x = 260, y =330)
        
        #appointment duration picker
        self.time_picker_label2 = tk.Label(self.appointments_tab, text = "Pick Appointment Duration ", font=("Segoe UI", 11))
        self.time_picker_label2.place(x = 252, y =380)
        time_var2 = tk.StringVar()
        self.time_picker2 = ttk.Combobox(self.appointments_tab, textvariable=time_var2, values=[f"{m}" for m in range(20, 60+1, 10)])
        self.time_picker2.place(x = 260, y =416)

        #button to set date
        self.date_button = tk.Button(self.appointments_tab,width=28,bg='Steel Blue', font=("Segoe UI", 11), text = "Set Date", command = self.set_date)
        self.date_button.place(x= 11, y = 490)

        #button to sumbit an appointment and start the logic testing
        self.create_apt_button = tk.Button(self.appointments_tab,bg='Steel Blue', font = ("Segoe UI",12), text = "Create Appointment", command = self.create_appointment, state="disabled")
        self.create_apt_button.place(x = 255, y = 488)

        #mainloop
        self.main_window.mainloop()
    


    ######FUNCS TO WORK WITH THE WIDGETS ON THE TABS
    def search_customer(self):
        self.connection = open_connection()
        prompt = self.search_customer_entry.get().lstrip().rstrip()
        if prompt.isalpha() or (not prompt.isdigit() and ('@' not in prompt or '.' not in prompt)):
            messagebox.showwarning(title="Invalid Input", message=f"Invalid Input")
            self.selected_customer_full_name.set(f"Selected Customer: None")
            self.selected_customer_phone_number = 0
            self.create_apt_button.configure(state="disabled")
            close_connection(self.connection)
        else:
            search_customer_query = f"SELECT * FROM Clients WHERE phone_number = '{prompt}' OR email = '{prompt}'"
            search_customer_results = fetch_all_dict_list(self.connection, search_customer_query)
            if not search_customer_results:
                messagebox.showwarning(title="Customer not found", message=f"Customer with {'phone number' if prompt.isdigit() else 'email'} {prompt} doesn't exist.")
                self.selected_customer_full_name.set(f"Selected Customer: None")
                self.selected_customer_phone_number = 0
                self.create_apt_button.configure(state="disabled")
                close_connection(self.connection)
            else:
                print(f"{search_customer_results[0]['first_name']} {search_customer_results[0]['last_name']}")
                self.selected_customer_full_name.set(f"Selected Customer: {search_customer_results[0]['first_name']} {search_customer_results[0]['last_name']}")
                self.selected_customer_phone_number = f"{search_customer_results[0]['phone_number']}"
                self.create_apt_button.configure(state="normal")
                close_connection(self.connection)

    def search_customer_enter(self, event):
        self.connection = open_connection()
        prompt = self.search_customer_entry.get().lstrip().rstrip()
        if prompt.isalpha() or (not prompt.isdigit() and ('@' not in prompt or '.' not in prompt)):
            messagebox.showwarning(title="Invalid Input", message=f"Invalid Input")
            self.selected_customer_full_name.set(f"Selected Customer: None")
            self.selected_customer_phone_number = 0
            self.create_apt_button.configure(state="disabled")
            close_connection(self.connection)
        else:
            search_customer_query = f"SELECT * FROM Clients WHERE phone_number = '{prompt}' OR email = '{prompt}'"
            search_customer_results = fetch_all_dict_list(self.connection, search_customer_query)
            if not search_customer_results:
                messagebox.showwarning(title="Customer not found", message=f"Customer with {'phone number' if prompt.isdigit() else 'email'} {prompt} doesn't exist.")
                self.selected_customer_full_name.set(f"Selected Customer: None")
                self.selected_customer_phone_number = 0
                self.create_apt_button.configure(state="disabled")
                close_connection(self.connection)
            else:
                print(f"{search_customer_results[0]['first_name']} {search_customer_results[0]['last_name']}")
                self.selected_customer_full_name.set(f"Selected Customer: {search_customer_results[0]['first_name']} {search_customer_results[0]['last_name']}")
                self.selected_customer_phone_number = f"{search_customer_results[0]['phone_number']}"
                self.create_apt_button.configure(state="normal")
                close_connection(self.connection)


    def get_contact_info(self):
            try:
                name = self.first_name_entry.get().lstrip().rstrip()
                if not name.isalpha():
                    raise ValueError(f"'{name}' is not a valid name.")
                surname = self.surname_entry.get().lstrip().rstrip()
                if not surname.isalpha():
                    raise ValueError(f"'{surname}' is not a valid surname.")
                email = self.email_entry.get().rstrip().lstrip()
                #temp validation, could be done with regex and only smtp
                if not validate_email(email).email:
                    raise ValueError(f"'{email}' is not a valid email.")
                phone_number = self.phone_number_entry.get().lstrip().rstrip()
                if not phone_number.isalnum() or len(phone_number) != 10:
                    raise ValueError(f"'{phone_number}' is not a valid phone number.")
            except ValueError as e:
                messagebox.showwarning(title = "Invalid Input", message=f"{e}")
            self.connection = open_connection()
            fetch_query = f"SELECT * FROM Clients WHERE phone_number = '{phone_number}' OR email = '{email}'"
            fetch_results = fetch_all_dict_list(self.connection, fetch_query)
            print(fetch_results)
            if fetch_results:
                messagebox.showinfo(title="Customer exists",message=f"Customer {fetch_results[0]['first_name']} {fetch_results[0]['last_name']} already exists")
                close_connection(self.connection)
            else:
                last_customer_query = f"SELECT client_id FROM Clients ORDER BY client_id desc LIMIT 1"
                last_entry_id = fetch_all_dict_list(self.connection, last_customer_query)
                print()
                if not last_entry_id:
                    final_query = f"INSERT INTO Clients(client_id, first_name, last_name, phone_number, email) VALUES(1,'{name}','{surname}','{phone_number}','{email}')"
                else:
                    inserting_query1 = f"INSERT INTO Clients(client_id, first_name, last_name, phone_number, email)"
                    inserting_query2 = f" VALUES({int(last_entry_id[0]['client_id']) + 1},'{name}','{surname}','{phone_number}','{email}')"
                    final_query = inserting_query1 + inserting_query2
                insert_query(self.connection, final_query)
                self.connection.commit()
                messagebox.showinfo(title="Inserted successfully",message=f"Customer {name} {surname} has been inserted successfully")
                close_connection(self.connection)

    def create_appointment(self):
        #user_submit_input = messagebox.askyesno(title="Confirmation", message='Are you sure you want to submit this appointment?')
        selected_date = self.date_picker.selection_get()
        if not self.time_picker.get():
            messagebox.showwarning(title="Missing Parameters", message="You need to choose an appointment time")
        elif not self.time_picker2.get():
            messagebox.showwarning(title="Missing Parameters", message="You need to choose an appointment duration")
        else:
            selected_time = self.time_picker.get() + ':00'
            time_format = '%H:%M:%S'
            selected_time = datetime.strptime(selected_time, time_format).time()
            apt_date = datetime.combine(selected_date, selected_time)
            apt_min = timedelta(minutes=int(self.time_picker2.get()))
            apt_duration = apt_date + apt_min
            print(apt_date)
            print(apt_duration)
            self.connection = open_connection()
            appointments_query = f'''SELECT * FROM appointments WHERE appointment_date BETWEEN '{apt_date}' AND '{apt_duration}'
            OR appointment_interval BETWEEN '{apt_date}' AND '{apt_duration}' OR '{apt_date}' BETWEEN appointment_date AND appointment_interval 
            OR '{apt_duration}' BETWEEN appointment_date AND appointment_interval'''
            appointmnents_results = fetch_all_dict_list(self.connection, appointments_query)
            print(appointmnents_results)
            if not appointmnents_results:
                current_customer_query = f"SELECT * FROM clients WHERE phone_number = '{self.selected_customer_phone_number}'"
                current_customer_results = fetch_all_dict_list(self.connection, current_customer_query)
                last_appointment_query = f"SELECT appointment_id FROM appointments ORDER BY appointment_id desc LIMIT 1"
                last_appointment_id = fetch_all_dict_list(self.connection, last_appointment_query)
                apt_creation_query = f'''INSERT INTO appointments(appointment_id, appointment_date, appointment_interval, client_id) VALUES({last_appointment_id[0]['appointment_id'] + 1},'{apt_date}', '{apt_duration}', {current_customer_results[0]['client_id']})'''
                validation = messagebox.askyesno("Validation", message= "Are you sure you want to schedule this appointment?")
                if validation:
                    insert_query(self.connection, apt_creation_query)
                    self.connection.commit()
                    messagebox.showinfo(title="Appointment Scheduled", message = f'''An appointment has been scheduled for customer {current_customer_results[0]['first_name']} {current_customer_results[0]['last_name']} at {apt_date} with duration {int(self.time_picker2.get())} minutes''')
            else:
                messagebox.showwarning(title="Appointment Time Taken", message=f'''There's already an appointment set on {appointmnents_results[0]['appointment_date']} until {appointmnents_results[0]['appointment_interval']}''')
            close_connection(self.connection)
            
    def set_date(self):
        date_string = f'{self.date_picker.selection_get()}'
        date_format = '%Y-%m-%d'
        date_obj = datetime.strptime(date_string, date_format).date()
        if(date_obj.day == datetime.today().day):
            #destroy time widget, but make it the same as above, because the hour might have changed
            self.time_picker.destroy()
            hour = 24 -(24-datetime.now().hour)
            time_var = tk.StringVar()
            self.time_picker = ttk.Combobox(self.appointments_tab, textvariable=time_var, values=[f"{str(h).zfill(2)}:{str(m).zfill(2)}" for h in range(hour+1, 24) for m in range(0, 60, 10)])
            self.time_picker.place(x = 260, y =330)
        else:
            #make widget but make it whole
            self.time_picker.destroy()
            hour = 0
            time_var = tk.StringVar()
            self.time_picker = ttk.Combobox(self.appointments_tab, textvariable=time_var, values=[f"{str(h).zfill(2)}:{str(m).zfill(2)}" for h in range(hour, 24) for m in range(0, 60, 10)])
            self.time_picker.place(x = 260, y =330)