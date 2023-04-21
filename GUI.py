from appointments_methods import *
from customers_methods import *


class Appointment_manager(Appointment_methods, Customers_methods):
    def __init__(self):
        #     MAIN WINDOW    #
        ######################
        self.main_window = tk.Tk()
        self.main_window.geometry("1000x560")
        self.main_window.title("Appointment Manager")
        icon = tk.PhotoImage(file="pics/appointment_manager.png")
        self.main_window.iconphoto(True, icon)
        
        window_width = 1000
        window_height = 560
        screen_width = self.main_window.winfo_screenwidth()
        screen_height = self.main_window.winfo_screenheight()
        x_coordinate = int((screen_width/2) - (window_width/2))
        y_coordinate = int((screen_height/2) - (window_height/2))
        self.main_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Set minimum and maximum window size
        self.main_window.minsize(window_width, window_height)
        self.main_window.maxsize(window_width, window_height)


        # TAB HANDLER ATTACHED TO THE MAIN WINDOW #
        ###########################################
        self.notebook = ttk.Notebook(self.main_window)
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("TNotebook.Tab", font=("Segoe UI", 12, "bold"), foreground="blue", width=16, height=10)
        self.notebook.place(x=0, y=0, relwidth=1, relheight=1)

        #     FRAMES FOR THE TAB HANDLER    #
        #####################################
        self.appointments_tab = tk.Frame(self.notebook)
        self.customers_tab = tk.Frame(self.notebook)
        self.search_tab = tk.Frame(self.notebook)
        self.print_apt = tk.Frame(self.notebook)
        #   ICONS FOR TABS   #
        ######################

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
        
        # ICONS FOR THINGS IN APPOINTMENTS TAB #
        ########################################

        #searching customer img
        searching_customer_img = Image.open("pics/searching.png")
        searching_customer_img = searching_customer_img.resize((24,24), Image.ANTIALIAS)
        searching_customer_img = ImageTk.PhotoImage(searching_customer_img)



        # ICONS FOR THINGS IN CUSTOMERS TAB #
        #####################################
        #TEMP EMPTY

        # ADDING THE TABS TO THE TAB MANAGER #
        ######################################
        self.notebook.add(self.appointments_tab, text="Appointments", image=appointments_icon, compound='left')
        self.notebook.add(self.customers_tab, text="Customers", image=customers_icon, compound='left')
        self.notebook.add(self.search_tab, text="Search", image=search_icon, compound='left')   
        self.notebook.add(self.print_apt, text="Print appointments", image=print_apt_icon, compound='left')


        # STRINGVARS AND ALL GLOBAL VARIABLES NEEDED FOR THE WIDGETS IN APPOINTMENTS TAB #
        ##################################################################################
        self.selected_customer_full_name = tk.StringVar()
        self.selected_customer_full_name.set("None")
        self.selected_customer_phone_number = None
        self.selected_appointment_date = None

###          APPOINTMENT TAB WIDGETS
##################################################################################################################################################################################################
        # DECORATIONS #
        ###############
        
        #main window decor
        self.bottom_decoration = tk.Frame(self.main_window,background="#A6A8A8",width=1000,height=50,relief="raised")
        self.bottom_decoration.place(y=510)

        #appointments decor
        self.top_decoration = tk.Frame(self.appointments_tab,background="#C0C6C6",width=1000,height=54,relief="raised")
        self.top_decoration.place(y=0)
        

        #Label, Button and Entry to search a customer
        self.search_customer_label = tk.Label(self.appointments_tab, text = "Create Appointment", font=("Segoe UI", 14, "bold"), background="#C0C6C6", foreground="dark blue")
        self.search_customer_label.place(x=72,y=8)
        self.prompt_label = tk.Label(self.appointments_tab, text = "Enter customers phone number or email", font=("Segoe UI", 12))
        self.prompt_label.place(x=56,y=76)
        self.search_customer_entry = tk.Entry(self.appointments_tab, width= 50)
        self.search_customer_entry.place(x=50, y=106)
        self.search_customer_button = tk.Button(self.appointments_tab, compound=tk.LEFT, image=searching_customer_img, command=self.search_customer)
        self.search_customer_button.place(x=364, y=101)
        self.search_customer_entry.bind("<Return>", self.search_customer_enter)


        ##Labels to show which customer is selected
        self.selected_customer_static_text = tk.Label(self.appointments_tab, text = "Selected Customer: ", font=("Segoe UI", 11))
        self.selected_customer_static_text.place(x=56,y=126)
        self.picked_customer_label = tk.Label(self.appointments_tab, textvariable=self.selected_customer_full_name, font=("Segoe UI", 11, "bold"))
        self.picked_customer_label.place(x = 194, y = 126)

        ##Label and listbox for the selected customers appointments
        self.selected_customer_appointments_label = tk.Label(self.appointments_tab, text = "Selected Customer Appointments", font=("Segoe UI", 12))
        self.selected_customer_appointments_label.place(x=622,y=76)

        self.selected_customer_appointments_listbox = tk.Listbox(self.appointments_tab, font=("Segoe UI", 10), width=40,height=10)
        self.selected_customer_appointments_listbox.place(x=594,y=106)

        #scrollbar for the listbox
        self.scrollbar = tk.Scrollbar(self.appointments_tab, orient="vertical", background="red", troughcolor="blue")
        self.scrollbar.config(command=self.selected_customer_appointments_listbox.yview)
        self.scrollbar.place(x=882, y=106, height=182)
        self.selected_customer_appointments_listbox.config(yscrollcommand=self.scrollbar.set)


        #date picker and label for it
        self.date_picker_label = tk.Label(self.appointments_tab, text = "Appointment Date", font = ("Segoe UI", 12))
        self.date_picker_label.place(x=48,y=224)
        today = date.today()
        self.date_picker = Calendar(self.appointments_tab, selectmode='day', showweeknumbers=False, font=("Segoe UI", 10), mindate = today, background='Steel Blue',weekendbackground="white", showothermonthdays = False)
        self.date_picker.place(x=12, y=260)
        

        #appointment time picker and label for it
        self.time_picker_label = tk.Label(self.appointments_tab, text = "Appointment Time", font=("Segoe UI", 11))
        self.time_picker_label.place(x = 260, y =224)
        hour = 24 -(24-datetime.now().hour)
        time_var = tk.StringVar()
        self.time_picker = ttk.Combobox(self.appointments_tab, values=[f"{str(h).zfill(2)}:{str(m).zfill(2)}" for h in range(hour+1, 24) for m in range(0, 60, 10)])
        self.time_picker.place(x = 260, y =260)
        self.time_picker.configure(state="readonly")

        #updating the time of the time picker according to the calendar selection every time there is any new calendar selection
        self.date_picker.bind("<<CalendarSelected>>", self.update_time_picker)
        
        #appointment duration picker and label for it
        self.time_picker_label2 = tk.Label(self.appointments_tab, text = "Appointment Duration", font=("Segoe UI", 11))
        self.time_picker_label2.place(x = 252, y =296)
        self.time_picker2 = ttk.Combobox(self.appointments_tab, values=[f"{m}" for m in range(20, 60+1, 10)])
        self.time_picker2.place(x = 260, y =332)
        self.time_picker2.configure(state="readonly")

        #button to sumbit an appointment and start the logic testing
        self.create_apt_button = tk.Button(self.appointments_tab, bg='Steel Blue', font = ("Segoe UI",12), text = "Create", command = self.create_appointment, state="disabled",width=10, relief="sunken")
        self.create_apt_button.place(x = 280, y = 380)

        #label for manage appointments side
        self.search_customer_label = tk.Label(self.appointments_tab, text = "Manage Appointments", font=("Segoe UI", 14, "bold"), bg='Steel Blue', background="#C0C6C6", foreground="dark blue")
        self.search_customer_label.place(x=624,y=8)

        #buttons for rescheduling and deleting apts
        self.reschedule_apt_button = tk.Button(self.appointments_tab,text="Reschedule", font=("Segoe UI", 11), bg='Steel Blue', command=self.reschedule_apt_command)
        self.reschedule_apt_button.place(x=594, y=300)

        self.delete_apt_button = tk.Button(self.appointments_tab,text="Delete", font=("Segoe UI", 11), bg='Steel Blue', command=self.delete_apt_command, width=10)
        self.delete_apt_button.place(x=788, y=300)

###            CUSTOMERS TAB WIDGETS
##################################################################################################################################################################################################
        #adding the labels and entry boxes to the customers_tab

        self.create_new_customer_label = tk.Label(self.customers_tab, text = "Add Customer", font = ("Segoe UI", 12, "bold"))
        self.create_new_customer_label.place(x=146,y=10)


        self.first_name_label = tk.Label(self.customers_tab, text = "First name: ", font=("Segoe UI", 12))
        self.first_name_entry = tk.Entry(self.customers_tab, width=50)
        self.first_name_label.place(x=12, y=40)
        self.first_name_entry.place(x=100, y=45)

        self.surname_label = tk.Label(self.customers_tab, text = "Surname: ", font=("Segoe UI", 12))
        self.surname_entry = tk.Entry(self.customers_tab, width=50)
        self.surname_label.place(x=12, y=100)
        self.surname_entry.place(x=100, y=105)

        self.email_label = tk.Label(self.customers_tab, text = "Email: ", font=("Segoe UI", 12))
        self.email_entry = tk.Entry(self.customers_tab, width=50)
        self.email_label.place(x=12, y=160)
        self.email_entry.place(x=100, y=165)

        self.phone_number_label = tk.Label(self.customers_tab, text = "Phone Number: ", font=("Segoe UI", 12))
        self.phone_number_entry = tk.Entry(self.customers_tab, width=15)
        self.phone_number_label.place(x=12, y=220)
        self.phone_number_entry.place(x=135, y=225)

        #button to get client credentials
        self.contact_info_button = tk.Button(self.customers_tab,height = 1,width= 20, bg='Steel Blue', font = ("Segoe UI",10), text = "Set Contact Info", command = self.get_contact_info)
        self.contact_info_button.place(x=250, y=220)

        # TK MAINLOOP #
        ##############
        self.main_window.mainloop()