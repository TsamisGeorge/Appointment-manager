###  METHODS TO WORK WITH THE WIDGETS ON THE APPOINTMENT TAB  ###
#################################################################


import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from db_tools import open_connection,close_connection,fetch_all_dict_list,execute_query
from datetime import datetime, timedelta

class Appointment_methods():
    '''Parent Κλαση της κλασης Appointment_manager που δινει τις
    μεθοδους διαχειρισης ενος ραντεβου'''

    def check_if_apt_valid(self, apt_date, apt_duration):
        '''Μεθοδος ελεγχου αν ενα ραντεβου ειναι valid, δηλαδη αν δεν υπαρχει αλληλοεπικαλυψη μεταξυ του
           επιλεγμενου ραντεβου και των ραντεβου στη βαση, παιρνει σαν ορισμα την αρχη και την διαρκεια του ραντεβου'''
        
        # δημιουργει ενα ερωτημα το οποιο φαιρνει ολα τα δεδομενα απο το table appointments
        # με χρηση τετραπλου WHERE clause αν οποιοδηποτε απο τα στοιχεια ειτε του επιλεγμενου ραντεβου ειτε
        # των ηδη υπαρχον ραντεβου της βασης, ειναι αναμεσα το ενα στο αλλο, αν οποιαδηποτε απο τις OR συνθηκες ειναι true
        # το apt_results περιεχει ραντεβου, αν καμια τοτε το apt_results δεν περιεχει τιποτα, σε καθε περιπτωση επιστρεφεται
        # για μελλοντικη χρηση
        self.connection = open_connection()
        appointments_query = f'''SELECT * FROM appointments WHERE appointment_date BETWEEN '{apt_date}' AND '{apt_duration}'
        OR appointment_interval BETWEEN '{apt_date}' AND '{apt_duration}' OR '{apt_date}' BETWEEN appointment_date AND appointment_interval 
        OR '{apt_duration}' BETWEEN appointment_date AND appointment_interval'''
        apt_results = fetch_all_dict_list(self.connection, appointments_query)
        close_connection(self.connection)
        return apt_results


    def update_time_picker(self, event=None):
        '''Μεθοδος ανανεωσης του time_picker, αναλογα με το ποια ημερα ειναι
        επιλεγμενη στο Calendar, η κληση του μπορει να γινει και ως event'''


        # οταν επιλεγεται μια ημερομηνια απο το Calendar καλειται
        # η συγκεκριμενη μεθοδος, και ανανεωνει τις ωρες που μπορει να
        # κλεισει ενα ραντεβου ο χρηστης του προγραμματος αναλογα με
        # την επιλεγμενη ημερα, παιρνει σαν προαιρετικο ορισμα το event
        # για να μπορει να γινει και χρηση του ως συναρτηση


        # ανακτηση του Input της επιλεγμενης ημερας απο το Calendar
        # και δημιουργια ενος date αντικειμενου με format '%Y-%m-%d'
        # με χρηση της datetime.strptime().date()
        date_string = f'{self.date_picker.selection_get()}'
        date_format = '%Y-%m-%d'
        date_obj = datetime.strptime(date_string, date_format).date()
        
        # αν το date αντικειμενο που ανακτηθηκε ειναι η εκαστοτε σημερινή ημέρα
        if date_obj == datetime.today().date():
            # καταστροφη του προηγουμενου time picker combobox 
            self.time_picker.destroy()
            # ορισμα την μεταβλητη ωρα να ειναι 24-(24- {τωρινή ώρα})
            # ώστε να παρουμε το αποτελεσμα του ποια ωρα ειναι σε format
            # 24-ωρου ασχετως του timezone η αν ο χρηστης εχει 12 format στον
            # υπολογιστη του η οχι, #hour = datetime.now().hour
            hour = 24 -(24-datetime.now().hour)
            
            # η δημιουργια των επιλογων στο combobox γινεται με χρηση συνεπτιγμενης λιστας ως values στο combobox

            # αν η ωρα ειναι 7 και κατω, τοτε φτιαχνει τις επιλογες του timepicker να ειναι οι ωρες
            # 9 το πρωι με 9 το βραδυ
            if hour < 8: 
                self.time_picker = ttk.Combobox(self.appointments_tab, values=[f"{str(h).zfill(2)}:{str(m).zfill(2)}" for h in range(9, 21) for m in range(0, 60, 10)])
                self.time_picker['values'] +=("21:00",)

            # αν η ωρα ειναι μεγαλυτερη η ιση του 8 και μικροτερη του 19 φτιαχνει το timepicker με ωρες απο hour+2 μεχρι 21
            elif hour >= 8 and hour < 19:
                self.time_picker = ttk.Combobox(self.appointments_tab, values=[f"{str(h).zfill(2)}:{str(m).zfill(2)}" for h in range(hour+2, 21) for m in range(0, 60, 10)])
                self.time_picker['values'] +=("21:00",)
            
            # αν η ωρα ειναι μεγαλυτερη η ιση με το 19 τοτε δεν μπορει να φτιαξει επιλογες στην σημερινη ημερα
            else:
                self.time_picker = ttk.Combobox(self.appointments_tab)

        else: # αν εχει επιλεχθει καποια αλλη ημερα απο την σημερινη απλα δημιουργει το combobox με επιλογες απο 9 μεχρι 21
            self.time_picker.destroy()
            hour = 0
            self.time_picker = ttk.Combobox(self.appointments_tab, values=[f"{str(h).zfill(2)}:{str(m).zfill(2)}" for h in range(9, 21) for m in range(0, 60, 10)])
            self.time_picker['values'] +=("21:00",)

        # σε καθε περιπτωση γινεται place το combobox και configure το state
        # του σε readonly ωστε ο χρηστης να μην μπορει να εισαγει τιμες γραπτως
        self.time_picker.place(x = 260, y =260)
        self.time_picker.configure(state="readonly")


    def update_customer_appointments(self):
        '''Μεθοδος ενημερωσης του Listbox που περιεχει τα ραντεβου ενος επιλεγμενου πελατη'''
        
        # κληση της datetime.now() για ανακτηση της τωρινης ημερομηνιας και
        # χρηση του .strftime με ορισμα το format "%Y-%m-%d %H:%M:%S"
        # για την δημιουργια ενος datetime αντικειμενου
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        
        # ανοιγμα του connection, δημιουργια του ερωτηματος για τον επιλεγμενο πελατη και 
        # επιστροφη του αποτελεσματος στο curr_customer_results
        self.connection = open_connection()
        curr_customer_query = f"SELECT * FROM Clients WHERE phone_number = '{self.selected_customer_phone_number_apt_tab}'"
        curr_customer_results = fetch_all_dict_list(self.connection, curr_customer_query)

        # δημιουργια ερωτηματς που επιστρεφει ολα τα επικειμενα ραντεβου του επιλεγμενου πελατη
        # με χρηση διπλου WHERE clause με το id του πελατη και το formatted_datetime που ειναι
        # η τωρινη ημερομηνια ωστε να φερει μονο τα επικειμενα ραντεβου του
        curr_customer_appointments_query = f"SELECT * FROM appointments WHERE client_id = {curr_customer_results[0]['client_id']} AND appointment_interval > '{formatted_datetime}'"
        curr_customer_appointments_results = fetch_all_dict_list(self.connection, curr_customer_appointments_query)

        if curr_customer_appointments_results: # αν υπαρχουν επικειμενα ραντεβου

            # διαγραφη των επιλεγμενων ραντεβου του προηγουμενου πελατη
            self.selected_customer_appointments_listbox.delete(0, tk.END)

            for appointment in curr_customer_appointments_results: # για καθε ραντεβου μεσα στο curr_customer_appointments_results
                # ανακτηση της χρονικης διαρκειας του ραντεβου και μετατροπη της σε time αντικειμενο
                appointment_date = datetime.strptime(appointment['appointment_date'], "%Y-%m-%d %H:%M:%S")
                appointment_duration = datetime.strptime(appointment['appointment_interval'], "%Y-%m-%d %H:%M:%S").time()
                # .insert στο Listbox την συμβολοσειρα f"{appointment['appointment_date'].date()}   {appointment['appointment_date'].time()}  -  {appointment_duration}"
                # η οποια ειναι ενα ραντεβου του επιλεγμενου πελατη
                self.selected_customer_appointments_listbox.insert(tk.END, f"{appointment_date.date()}   {appointment_date.time()}  -  {appointment_duration}")
        
        else: # αν δεν υπαρχουν ραντεβου απλα διαγραφη των ραντεβου του προηγουμενου επιλεγμενου πελατη
            self.selected_customer_appointments_listbox.delete(0, tk.END)
        
        # σε καθε περιπτωση ενημερωση των κουμπιων στο appointments_tab και κλεισιμο του connection
        self.update_apt_manage_buttons()
        close_connection(self.connection)


    def update_apt_manage_buttons(self, event=None):
        '''Μεθοδος για ενημερωση των κουμπιων που διαχειριζονται τα reschedule
         delete κουμπια στο appointments_tab, μπορει να χρησιμοποιειθει και ως event'''

        # γινεται ανακτηση του επιλεγμενου ραντεβου με χρηση του
        # self.selected_customer_appointments_listbox.curselection()
        # αν επιστραφη τιμη στο apt_selected τοτε θετει τα κουμπια να 
        # ειναι normal, αλλιως τα θετει να ειναι disabled
        apt_selected = self.selected_customer_appointments_listbox.curselection()
        if apt_selected:
            self.reschedule_apt_button.configure(relief = "raised", state="normal")
            self.delete_apt_button.configure(relief = "raised", state="normal")
        else:
            self.reschedule_apt_button.configure(relief = "sunken", state="disabled")
            self.delete_apt_button.configure(relief = "sunken", state="disabled")


    def update_picked_customer_to_none(self):
        '''Μεθοδος ενημερωσης των widget ενος επιλεγμενου πελατη στο appointments_tab'''
        self.selected_customer_apt_tab.set(f"None")
        self.selected_customer_phone_number_apt_tab = 0
        self.create_apt_button.configure(state="disabled",relief="sunken")
        self.selected_customer_appointments_listbox.delete(0, tk.END)



    def search_customer_apt_tab(self, event=None):
        '''Μεθοδος για αναζητηση ενος πελατη στο appointments_tab, μπορει να χρησιμοποιηθει και σαν event'''
        # καλειται οταν ο χρηστης παταει enter εχοντας επιλεγμενο το self.search_customer_entry η οταν παταει
        # το κουμπι self.search_customer_button στο appointments_tab


        # ανοιγμα του connection, ανακτηση του prompt απο το self.search_customer_entry αφου γινει
        # lstrip και rstrip για να φυγουν τα περιττα κενα
        self.connection = open_connection()
        prompt = self.search_customer_entry.get().lstrip().rstrip()

        # ελεγχος αν το prompt που δοθηκε ειναι valid, αν δεν ειναι γινεται αλλαγη των μεταβλητων
        # ενος επιλεγμενου πελατη στο appointments_tab ωστε να μην υπαρχει επιλεγμενος πελατης, εμφανιση
        # μυνηματος invalid input μεσω messagebox και κλεισιμο του connection
        if prompt.isalpha() or "\\" in prompt or  (not prompt.isdigit() and ('@' not in prompt or '.' not in prompt)):
            messagebox.showwarning(title="Invalid Input", message=f"Invalid Input")
            self.update_picked_customer_to_none()
            close_connection(self.connection)
        
        else: # αν το input ειναι valid
            # δημιουργια ερωτηματος για αναζητηση ενος πελατη στην βαση με where clause το prompt σαν ονομα ή 
            # email, εκτελεση του ερωτηματος και επιστροφη των αποτελεσματων στο search_customer_results
            search_customer_query = f"SELECT * FROM Clients WHERE phone_number = '{prompt}' OR email = '{prompt}'"
            search_customer_results = fetch_all_dict_list(self.connection, search_customer_query)
            
            if not search_customer_results: # αν δεν ερθουν αποτελεσματα και δεν υπαρχει πελατης
                
                # αναδειξη messagebox που αναφερει πως δεν υπαρχουν πελατες, αλλαγη των μεταβλητων ενος επιλεγμενου πελατη
                # για να μην υπαρχει επιλεγμενος πελατης, αλλαγη της καταστασης του κουμπιου δημιουργιας ενος ραντεβου 
                # σε disabled και διαγραφη των ραντεβου του πρωην επιλεγμενου πελατη απο το listbox των ραντεβου
                messagebox.showwarning(title="Customer not found", message=f"Customer with {'phone number' if prompt.isdigit() else 'email'} {prompt} doesn't exist.")
                self.update_picked_customer_to_none()

            else: # αν ερθουν αποτελεσματα και υπαρχει πελατης

                # αλλαγη των μεταβλητων του επιλεγμενου πελατη του appointments_tab ωστε να φανει ο επιλγμενος πελατης
                # και να μπορει να γινει διαχειριση του μεσω του μοναδικου κινητου τηλεφωνου του, αλλαγη του state του κουμπιου δημιουργιας
                # ενος ραντεβου σε normal αφου επιλεχθει επιτυχως ο πελατης
                self.selected_customer_apt_tab.set(f"{search_customer_results[0]['first_name']} {search_customer_results[0]['last_name']}")
                self.selected_customer_phone_number_apt_tab = f"{search_customer_results[0]['phone_number']}"
                self.create_apt_button.configure(state="normal",relief="raised")
                # κληση της self.update_customer_appointments() για να ενημερωθει το listbox με επικειμενα ραντεβου ενος
                # επιλεγμενου πελατη
                self.update_customer_appointments()
            close_connection(self.connection)

        # κληση της self.update_apt_manage_buttons() σε καθε περιπτωση για να μπορουν η να μην μπορουν
        # να πατηθουν τα κουμπια αλλαγης η διαγραφης ενος ραντεβου
        self.update_apt_manage_buttons()




    def create_appointment(self):
        '''Mεθοδος για την δημιουργια ενος νεου ραντεβου για τον επιλεγμενο πελατη'''

        # ανακτηση τιμης απο το Calendar για ημερομηνια του ραντεβου
        selected_date = self.date_picker.selection_get()

        # ανακτηση τιμης απο το time_picker για την ωρα του ραντεβου, αν δεν
        # εχει επιλεχθει δειχνει messagebox με μυνημα λαθους
        if not self.time_picker.get():
            messagebox.showwarning(title="Missing Parameters", message="You need to choose an appointment time")
        
        # ανακτηση τιμης απο το time_picker2 για την διαρκεια του ραντεβου, αν δεν
        # εχει επιλεχθει δειχνει messagebox με μυνημα λαθους
        elif not self.time_picker2.get():
            messagebox.showwarning(title="Missing Parameters", message="You need to choose an appointment duration")

        else: # αν ολα εχουν επιλεχθει σωστα

            # ανακτηση τιμης απο το time_picker και προσθεση του ':00' ωστε να ειναι ιδιο με αντικειμενο
            # time, δημιουργια του format και χρηση της .strptime για την δημιουργια του time αντικειμενου
            selected_time = self.time_picker.get() + ':00'
            time_format = '%H:%M:%S'
            selected_time = datetime.strptime(selected_time, time_format).time()

            # χρηση της .combine με ορισμα τα date και time αντικειμενα ωστε να
            # εχουμε το datetime αντικειμενο το οποιο ειναι η ημερομηνια του ραντεβου
            apt_date = datetime.combine(selected_date, selected_time)

            # χρηση της timedelta με ορισμα σαν λεπτα τον ακεραιο αριθμο της επιλογης του χρηστη
            # απο το self.time_picker2 και προσθεση του apt_date με το apt_min για να παρουμε
            # την ημερομηνια και ωρα ληξης του ραντεβου
            apt_min = timedelta(minutes=int(self.time_picker2.get()))
            apt_duration = apt_date + apt_min

            # κληση της self.check_if_apt_valid με ορισμα τα 2 αντικειμενα για να δουμε
            # αν η ωρες του ραντεβου ειναι valid και ανοιγμα του connection
            appointmnents_results = self.check_if_apt_valid(apt_date, apt_duration)
            self.connection = open_connection()

            if not appointmnents_results: # αν δεν εχουν επιστραφει ραντεβου δηλαδη το επιλεγμενο ραντεβου ειναι valid
                
                # δημιουργια query για τα στοιχεια του επιλεγμενου πελατη με χρηση του self.selected_customer_phone_number_apt_tab
                # και εκτελεση του ερωτηματος και επιστροφη του αποτελεσματος στο current_customer_results
                current_customer_query = f"SELECT * FROM Clients WHERE phone_number = '{self.selected_customer_phone_number_apt_tab}'"
                current_customer_results = fetch_all_dict_list(self.connection, current_customer_query)
                
                # δημιουργια query για επιστροφη του τελευταιου appointment_id και εκτελεση του
                last_appointment_query = f"SELECT appointment_id FROM appointments ORDER BY appointment_id desc LIMIT 1"
                last_appointment_id = fetch_all_dict_list(self.connection, last_appointment_query)

                
                if last_appointment_id: # αν εχει βρεθει τελευταιο appointment_id(υπαρχουν καταγραφες απο ραντεβου στην βαση)

                    # δημιουργια ερωτηματος με τα στοιχεια της δημιουργιας του ραντεβου οπως και το τελευταιο appointment_id αυξημενο κατα 1
                    apt_creation_query = f'''INSERT INTO appointments(appointment_id, appointment_date, appointment_interval, client_id) VALUES({last_appointment_id[0]['appointment_id'] + 1},'{apt_date}', '{apt_duration}', {current_customer_results[0]['client_id']})'''

                else: # αν δεν βρεθει τελευταιο appointment_id(δεν υπαρχουν καταγραφες απο ραντεβου στην βαση)

                    # δημιουργια ερωτηματος με τα στοιχεια της δημιουργιας του ραντεβου και το appointment_id = 1
                    apt_creation_query = f'''INSERT INTO appointments(appointment_id, appointment_date, appointment_interval, client_id) VALUES(1,'{apt_date}', '{apt_duration}', {current_customer_results[0]['client_id']})'''
                
                # validation πριν την δημιουργια
                validation = messagebox.askyesno("Validation", message= "Are you sure you want to schedule this appointment?")

                if validation: # αν ο χρηστης δεχθει το validation
                    
                    # εκτελεση του ερωτηματος, commit στο connection τις αλλαγες, εμφανιση messagebox με ενημερωση πως εχει οριστει επιτυχως το ραντεβου και τα στοιχεια
                    # του ραντεβου, και ανανεωση των ραντεβου του επιλεγμενου πελατη με χρηση της self.update_customer_appointments()
                    execute_query(self.connection, apt_creation_query)
                    self.connection.commit()
                    messagebox.showinfo(title="Appointment Scheduled", message = f'''An appointment has been scheduled for customer {current_customer_results[0]['first_name']} {current_customer_results[0]['last_name']} at {apt_date} with duration {int(self.time_picker2.get())} minutes''')
                    self.update_customer_appointments()

            else: # αν το ραντεβου δεν ειναι valid γιατι εχουν επιστραφη αποτελεσματα στο appointmnents_results
                
                # μετρηση των δευτερολεπτων απο την διαφορα της διαρκειας του ραντεβου με την ημερομηνια και ωρα του
                # ραντεβου, εμφανιση messagebox και χρηση του total_seconds για να αναδειχθει οτι υπαρχει ραντεβου απο την
                # ημερομηνια του πρωτο ραντεβου που βρεθηκε για total_seconds//60 λεπτα
                appointment_time = datetime.strptime(appointmnents_results[0]['appointment_interval'], "%Y-%m-%d %H:%M:%S")
                appointment_duration = datetime.strptime(appointmnents_results[0]['appointment_date'], "%Y-%m-%d %H:%M:%S")
                total_seconds = (appointment_time - appointment_duration).total_seconds()
                messagebox.showwarning(title="Appointment Time Taken", message=f'''There's already an appointment set on {appointmnents_results[0]['appointment_date']} for {int(total_seconds//60)} minutes''')
            close_connection(self.connection)



    def reschedule_apt_command(self):
        '''Mεθοδος για επαναπρογραμματισμο ενος επιλεγμενου ραντεβου απο τον επιλεγμενο πελατη'''

        # ανακτηση τιμων απο date, time pickers
        selected_date = self.date_picker.selection_get()
        if not self.time_picker.get():
            messagebox.showwarning(title="Missing Parameters", message="You need to choose an appointment time")
        elif not self.time_picker2.get():
            messagebox.showwarning(title="Missing Parameters", message="You need to choose an appointment duration")

        else: # Μολις και αν επιλεχθουν επιτυχως τιμες

            # μετατροπη ολων των τιμων σε datetime αντικειμενα
            selected_time = self.time_picker.get() + ':00'
            time_format = '%H:%M:%S'
            selected_time = datetime.strptime(selected_time, time_format).time()
            apt_min = timedelta(minutes=int(self.time_picker2.get()))
            apt_date = datetime.combine(selected_date, selected_time)
            apt_duration = apt_date + apt_min

            # ελεγχος αν ειναι valid το αντικειμενο
            appointmnents_results = self.check_if_apt_valid(apt_date, apt_duration)

            if not appointmnents_results: # αν ειναι valid
                
                # επαληθευση αλλαγης
                confirm_reschedule = messagebox.askyesno(title="Confirmation", message="Are you sure you want to reschedule this appointment?")

                if confirm_reschedule: # αν γινει δεκτη η επαληθευση
                    
                    self.connection = open_connection()

                    # ανακτηση την συμβολοσειρα του επιλεγμενου ραντεβου απο το listbox απο το πρωτο εως και το εννατο στοιχειο, και προσθεση
                    # σε αυτο το δωδεκατο εως και το εικοστο στοιχειο της συμβολοσειρας του επιλεγμενου ραντεβου για να ανακτηθει μονο το μερος
                    # της συμβολοσειρας που χρειαζομαστε για να δημιουργηθει το ερωτημα αργοτερα
                    selected_apt = self.selected_customer_appointments_listbox.get(self.selected_customer_appointments_listbox.curselection())
                    selected_apt = selected_apt[:10] + selected_apt[12:21]


                    # δημιουργια ερωτηματος με τις νεες ημερομηνιες και ωρες το οποιο αλλαζει μονο το επιλεγμενο ραντεβου και εκτελεση του
                    # commit τις αλλαγες στην βαση, ανανεωση των ραντεβου του επιλεγμενου πελατη στο listbox, και κλεισιμο του connection
                    update_apt_query = f"UPDATE appointments SET appointment_date = '{apt_date}', appointment_interval = '{apt_duration}' WHERE appointment_date = '{selected_apt}'"
                    execute_query(self.connection, update_apt_query)
                    self.connection.commit()
                    self.update_customer_appointments()
                    close_connection(self.connection)

                    # εμφανιση messagebox που αναφερει πως το ραντεβου δημιουργηθηκε επιτυχως και εχει λεπτομεριες του ραντεβου
                    total_seconds = apt_min.total_seconds()
                    messagebox.showinfo(title="Appointment Rescheduled", message=f"Appointment successfully rescheduled at {apt_date} for {int(total_seconds//60)} minutes")
            else: # αν το ραντεβου δεν ειναι valid(υπαρχουν ραντεβου στο appointmnents_results)
                appointment_time = datetime.strptime(appointmnents_results[0]['appointment_interval'], "%Y-%m-%d %H:%M:%S")
                appointment_duration = datetime.strptime(appointmnents_results[0]['appointment_date'], "%Y-%m-%d %H:%M:%S")
                # εμφανιση messagebox που αναφερει πως υπαρχει ηδη ραντεβου στις επιλεγμενες ωρες με λεπτομεριες του ραντεβου
                total_seconds = (appointment_time - appointment_duration).total_seconds()
                messagebox.showwarning(title="Appointment Time Taken", message=f'''There's already an appointment set on {appointmnents_results[0]['appointment_date']} for {int(total_seconds//60)} minutes''')



    def delete_apt_command(self):
        '''Mεθοδος για διαγραφη ενος επιλεγμενου ραντεβου απο τον επιλεγμενο πελατη'''

        # messagebox για επαληθευση διαγραφης
        confirm_delete = messagebox.askyesno(title="Confirmation", message="Are you sure you want to delete this appointment?")

        if confirm_delete: # αν επαληθευτηκε η διαγραφη

            # ανοιγμα συνδεσης με την βαση, δημιουργια ερωτηματος για διαγραφη του επιλεγμενου ραντεβου αφου γινει slicing για να παρουμε το
            # επιθυμιτο αποτελεσμα, δημιουργια του ερωτηματος της διαγραφης με το επιλεγμενο ραντεβου σαν σαν WHERE clause, εκτελεση του
            # ερωτηματος, commit στην βαση, ανανεωση των ραντεβου του επιλεγμενου πελατη οπως και των κουμπιων του επιλεγμενου πελατη
            # και κλεισιμο της συνδεσης με την βαση
            self.connection = open_connection()
            selected_apt = self.selected_customer_appointments_listbox.get(self.selected_customer_appointments_listbox.curselection())
            selected_apt = selected_apt[:10] + selected_apt[12:21]
            delete_apt_query = f"DELETE FROM appointments WHERE appointment_date = '{selected_apt}'"
            execute_query(self.connection, delete_apt_query)
            self.connection.commit()
            self.update_customer_appointments()
            self.update_apt_manage_buttons()
            close_connection(self.connection)