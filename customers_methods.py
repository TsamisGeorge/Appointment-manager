###   METHODS TO WORK WITH THE WIDGETS ON THE CUSTOMERS TAB   ###
#################################################################


from appointments_methods import *

# Parent Κλαση της κλασης Appointment_manager που δινει τις
# μεθοδους διαχειρισης ενος πελατη

class Customers_methods():

    # Μεθοδος δημιουργιας ενος πελατη
    # καλειται απο το κουμπι self.create_customer_button απο το αρχειο GUI
    # μεσα σε try except κανει τους λογικους ελεγχους για να υπαρχει valid
    # input, αν υπαρχει οποιοδηποτε λαθος κατα την εισαγωγη σηκωνει ValueError
    # με το εκαστοτε λαθος και το τυπωνει σαν warning messagebox με την περιγραφη
    # του λαθους, αν ολα πανε καλα τοτε το valid_infο γινεται 1 και συνεχιζει η 
    # εκτελεση της μεθοδου, αλλιως κλεινει η μεθοδος
    def create_customer(self):
        valid_info = 0
        try:
            name = self.first_name_entry.get().lstrip().rstrip()
            if not name.isalpha() or len(name) > 26:
                raise ValueError(f"'{name}' is not a valid name.\n")
            surname = self.surname_entry.get().lstrip().rstrip()
            if not surname.isalpha() or len(surname) > 26:
                raise ValueError(f"'{surname}' is not a valid surname.")
            email = self.email_entry.get().rstrip().lstrip()
            #temp validation, could be done with regex and only smtp
            if not validate_email(email).email or len(email)> 50:
                raise ValueError(f"'{email}' is not a valid email.")
            phone_number = self.phone_number_entry.get().lstrip().rstrip()
            if not phone_number.isalnum() or len(phone_number) != 10:
                raise ValueError(f"'{phone_number}' is not a valid phone number.")
            valid_info = 1
        except ValueError as e:
            messagebox.showwarning(title = "Invalid Input", message=f"{e}")

        # ανοιγμα του connection, δημιουγια του ενος ερωτηματος στην βαση το οποιο
        # ελεγχει αν υπαρχει πελατης με το ιδιο ονομα η κινητο, αν το fetch_results δεν
        # φερει τιποτα σημαινει πως δεν υπαρχει πελατης, οποτε συνεχιζει με την εκτελεση
        # αλλιως βγαζει μυνημα λαθους σε μορφη messagebox και κλεινει το connection
        if valid_info:
            self.connection = open_connection()
            fetch_query = f"SELECT * FROM clients WHERE phone_number = '{phone_number}' OR email = '{email}'"
            fetch_results = fetch_all_dict_list(self.connection, fetch_query)
            print(fetch_results)
            if fetch_results:
                messagebox.showinfo(title="Customer exists",message=f"Customer {fetch_results[0]['first_name']} {fetch_results[0]['last_name']} already exists")
                close_connection(self.connection)
            else:
                # Δημιουργια ερωτηματος που θα φερει το τελευταιο client_id απο την βαση δεδομενων
                # αν υπαρχει επιστρεφομενο client_id στο last_entry_id(υπαρχουν καταγραφες) τοτε δημιουργει query με\
                # τα στοιχεια που πηρε απο τα entries και προσθετει τον πελατη με client_id αυτο που πηρε αυξανομενο κατα 1
                # αν δεν υπαρχουν καταγραφες τοτε δημιουργει τον πρωτο πελατη με client_id 1
                last_customer_query = f"SELECT client_id FROM clients ORDER BY client_id desc LIMIT 1"
                last_entry_id = fetch_all_dict_list(self.connection, last_customer_query)
                if not last_entry_id:
                    final_query = f"INSERT INTO clients(client_id, first_name, last_name, phone_number, email) VALUES(1,'{name}','{surname}','{phone_number}','{email}')"
                else:
                    inserting_query1 = f"INSERT INTO clients(client_id, first_name, last_name, phone_number, email)"
                    inserting_query2 = f" VALUES({int(last_entry_id[0]['client_id']) + 1},'{name}','{surname}','{phone_number}','{email}')"
                    final_query = inserting_query1 + inserting_query2
                execute_query(self.connection, final_query)
                self.connection.commit()
                messagebox.showinfo(title="Inserted successfully",message=f"Customer {name} {surname} has been inserted successfully")
                # Κληση της self.clear_customers_entry() αν δημιουργηθει επιτυχως ενας πελατης για να αδιασουν τα entry boxes
                # και κλεισιμο του connection
                self.clear_customers_entry()
                close_connection(self.connection)
    
    # Μεθοδος για να αδειαζουν τα entry boxes του customers_tab
    # Χρηση της .delete πανω στα entries με ορισμα την αρχη και το τελος
    def clear_customers_entry(self):
        self.first_name_entry.delete(0, tk.END)
        self.surname_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_number_entry.delete(0, tk.END)


    # Μεθοδος για αναζητηση ενος πελατη στο customers_tab
    # εχει ορισμα event=None ωστε να μπορει να χρησιμοποιηθει και σαν binded event αλλα και σαν συναρτηση
    # καλειται οταν ο χρηστης παταει enter εχοντας επιλεγμενο το self.search_customer_entry2 η οταν παταει
    # το κουμπι self.search_customer_button2 στο customers_tab
    def search_customer_customers_tab(self, event=None):
        # Ανοιγμα του connection, το prompt γινεται οτι υπηρχε στο self.search_customer_entry2 αφου εχει γινει lstrip
        # και rstrip για τα κενα αριστερα και δεξια απο το input
        self.connection = open_connection()
        prompt = self.search_customer_entry2.get().lstrip().rstrip()

        # λογικοι ελεγχοι του prompt, αν δεν ειναι εγκυρο εμφανιζει messagebox που γραφει invalid input, 
        # ανανεωνοι τις τιμες των μεταβλητων για την διαχειριση του επιλεγμενου
        # πελατη και μετα κλεινει το connection
        if prompt.isalpha() or "\\" in prompt or (not prompt.isdigit() and ('@' not in prompt or '.' not in prompt)):
            messagebox.showwarning(title="Invalid Input", message=f"Invalid Input")
            self.selected_customer_customers_tab.set("None")
            self.selected_customer_phone_number_customers_tab = 0
            close_connection(self.connection)
        else: 
            # αν το prompt ειναι valid, τοτε φτιαχνει query και ψαχνει τους πελατες οι οποιοι εχουν ιδιο 
            # κινητο η email με το prompt
            # αν δεν φερει πελατες το search_customer_results μετα την εκτελεση του ερωτηματος τοτε
            # ανανεωνει τις τιμες των μεταβλητων του επιλεγμενου πελατη αναλογως για να δειξει πως
            # δεν επιλεχθηκε καποιος πελατης και βγαζει μυνημα οτι ο πελατης με το συγκεκριμενο αναγνωριστικο
            # αναλογα και την μορφη του αναγνωριστικου δεν υπαρχει   
            search_customer_query = f"SELECT * FROM clients WHERE phone_number = '{prompt}' OR email = '{prompt}'"
            search_customer_results = fetch_all_dict_list(self.connection, search_customer_query)
            if not search_customer_results:
                messagebox.showwarning(title="Customer not found", message=f"Customer with {'phone number' if prompt.isdigit() else 'email'} {prompt} doesn't exist.")
                self.selected_customer_customers_tab.set("None")
                self.selected_customer_phone_number_customers_tab = 0
            else:
                # αν ο πελατης υπαρχει κανονικα τοτε αλλαζει τις τιμες των μεταβλητων του επιλεγμενου πελατη ωστε
                # να μπορει να φανει αλλα και να χρησιμοποιηθει η τιμη του self.selected_customer_phone_number_customers_tab
                # αργοτερα στις υπολοιπες μεθοδους
                print(f"{search_customer_results[0]['first_name']} {search_customer_results[0]['last_name']}")
                self.selected_customer_customers_tab.set(f"{search_customer_results[0]['first_name']} {search_customer_results[0]['last_name']}")
                self.selected_customer_phone_number_customers_tab = f"{search_customer_results[0]['phone_number']}"
            close_connection(self.connection)
        # σε καθε περιπτωση ανανεωση των κουμπιων του customers_tab στο τελος
        self.update_customer_buttons()
    

    # μεθοδος που ανανεωνει τα κουμπια στο customers_tab αναλογως με το αν εχει
    # επιλεχθει επιτυχως ενας πελατης η οχι, κανοντας τον ελεγχο αν το 
    # self.selected_customer_phone_number_customers_tab ειναι ισο με 0 η οχι
    def update_customer_buttons(self):
        if self.selected_customer_phone_number_customers_tab == 0:
            self.delete_customer_button.configure(state="disabled",relief="sunken")
            self.change_first_name_button.configure(state="disabled", relief="sunken")
            self.change_surname_button.configure(state="disabled", relief="sunken")
            self.change_email_button.configure(state="disabled", relief="sunken")
            self.change_phone_number_button.configure(state="disabled", relief="sunken")
        else:
            self.delete_customer_button.configure(state="normal",relief="raised")
            self.change_first_name_button.configure(state="normal", relief="raised")
            self.change_surname_button.configure(state="normal", relief="raised")
            self.change_email_button.configure(state="normal", relief="raised")
            self.change_phone_number_button.configure(state="normal", relief="raised")


    # μεθοδος διαγραφης ενος πελατη
    # κληση της datetime.now() και format σε μορφη DATETIMΕ αντικειμενου της SQL ωστε
    # να χρισημοποιηθει σε επομενο ερωτημα
    def delete_customer_command(self):
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        # ανοιγμα της συνδεσης με την βαση, δημιουργια του ερωτηματος για τον επιλεγμενο πελατη
        # με χρηση της μεταβλητης self.selected_customer_phone_number_customers_tab που θα εχει
        # μη μηδενικη τιμη επειδη για να μπορει να πατηθει αυτο το κουμπι σημαινει πως εχει επιλεχθει
        # επιτυχως ενας πελατης
        self.connection = open_connection()
        picked_customer_query = f"SELECT * FROM clients WHERE phone_number = '{self.selected_customer_phone_number_customers_tab}'"
        picked_customer_results = fetch_all_dict_list(self.connection, picked_customer_query)
        # δημιουργια ερωτηματος για την ανακτηση ολων των ραντεβου του επιλεγμενου πελατη, τα οποια ειναι μεταγενεστερα της datetime.now(),
        # της τωρινης δηλαδη ημερομηνιας, και αποθηκευση τους στο appointments_results 
        # ωστε να δουμε αν ο πελατης εχει ραντεβου τα οποια δεν εχουν ολοκληρωθει ακομα
        appointments_query = f"SELECT * FROM appointments WHERE client_id = {picked_customer_results[0]['client_id']} AND appointment_interval > '{formatted_datetime}'"
        appointments_results = fetch_all_dict_list(self.connection, appointments_query)
        if not appointments_results: # αν δεν υπαρχουν ραντεβου τα οποια δεν ειναι ολοκληρωμενα
            # δημιουργια messagebox για ερωτηση επιβεβαιωσης
            confirmation = messagebox.askyesno(title="Confirmation", message=f"Are you sure you want to delete customer {picked_customer_results[0]['first_name']} {picked_customer_results[0]['last_name']} ?")
            if confirmation: # αν ο χρηστης επιβεβαιωσε την διαγραφη του πελατη
                
                # δημιουργια ερωτηματος για την διαγραφη των προηγουμενων ραντεβου του συγκεκριμενου
                # πελατη αν υπαρχουν, ωστε να μην υπαρχουν καταγραφες στα ραντεβου με ξενο
                # κλειδι client_id το id του πελατη προς διαγραφη, και εκτελεση του ερωτηματος
                delete_apt_query = f"DELETE FROM appointments WHERE client_id = {picked_customer_results[0]['client_id']}"
                execute_query(self.connection, delete_apt_query)

                # δημιουργια ερωτηματος για διαγραφη του επιλεγμενου πελατη με χρηση το id του και εκτελεση του ερωτηματος
                delete_customer_query = f"DELETE FROM clients WHERE client_id = {picked_customer_results[0]['client_id']}"
                execute_query(self.connection, delete_customer_query)

                # χρηση της .commit() στο connection αντικειμενο ωστε να γινουν οι αλλαγες στην βαση
                self.connection.commit()
                
                # εμφανιση messagebox που δειχνει πως ο πελατης με το συγκεκριμενο ονομα και επιθετο διαγραφτηκε επιτυχως
                messagebox.showinfo(title="Customer Deleted", message=f"Customer {picked_customer_results[0]['first_name']} {picked_customer_results[0]['last_name']} has been successfully deleted")

                # ανανεωση των μεταβλητων του επιλεγμενου πελατη ωστε να μην υπαρχει επιλεγμενος πελατης μετα την διαγραφη
                self.selected_customer_phone_number_customers_tab = 0
                self.selected_customer_customers_tab.set("None")
                # ανανεωση των κουμπιων
                self.update_customer_buttons()
        else: # αν υπαρχουν ραντεβου τα οποια ειναι μεταγενεστερα της τωρινης ημερας και ωρας, δεν διαγραφει τον πελατη
            messagebox.showwarning(title="Unable To Delete", message="Cannot delete a customer that has appointments due")
        close_connection(self.connection)


    # συναρτηση που φτιαχνει ενα toplevel window αφου πατηθει ενα απο τα 4 κουμπια
    # διαχειρισης των credential ενος πελατη
    # παιρνει ως ορισμα το ονομα του κουμπιου που πατηθηκε για το χρισημοποιησει για αλλα αντικειμενα
    # γραφικου περιβαλλοντος
    def make_toplevel_window(self, button_name):

        # δημιουργια του toplevel window
        self.change_customer_info_window = tk.Toplevel()

        # δημιουργια των διαστασεων του παραθυρου
        window_width = 330
        window_height = 120
        screen_width = self.change_customer_info_window.winfo_screenwidth()
        screen_height = self.change_customer_info_window.winfo_screenheight()
        x = int((screen_width/2) - (window_width/2))
        y = int((screen_height/2) - (window_height/2))
        self.change_customer_info_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.change_customer_info_window.minsize(window_width, window_height)
        self.change_customer_info_window.maxsize(window_width, window_height)

        # Frame που διευκολυνει την εμφανιση του επομενου label
        self.toplevel_window_frame = tk.Frame(self.change_customer_info_window, relief="raised", borderwidth=6, padx=14, pady=1)
        self.toplevel_window_frame.pack()
        # Label το οποιο εχει το ονομα του κουμπιου που πατηθηκε αφου γινει .title
        self.toplevel_window_label = tk.Label(self.toplevel_window_frame, text=f"{button_name.title()}", font=("Segoe UI",10))
        self.toplevel_window_label.pack()
        # Εntry για να δεχθει input για την αλλαγη για το εκαστοτε credential απο την επιλογη του κουμπιου
        self.change_customer_info_entry = tk.Entry(self.change_customer_info_window,width=36)
        self.change_customer_info_entry.place(x=56,y=66)
        # Κουμπι το οποιο καλει την self.commit_changes(button_name), το περασμα της συγκεκριμενης μεθοδου σαν command 
        # γινεται με την χρηση lambda συναρτησης ωστε να μην κλειθει η συναρτηση κατα την δημιουργια του κουμπιου, αλλα
        # μονο οταν πατηθει το κουμπι
        self.change_customer_info_button = tk.Button(self.change_customer_info_window, image = self.check_icon, command=lambda: self.commit_changes(button_name))
        self.change_customer_info_button.place(x=280,y=60)
        # bind του self.change_customer_info_entry με το <Return> ωστε οταν ειναι highlighed το συγκεκριμενο entry και 
        # πατηθει το enter να κλειθει σαν lambda function event η μεθοδος self.commit_changes με ορισμα το εκαστοτε κουμπι που δημιουργησε το 
        # toplevel window
        self.change_customer_info_entry.bind("<Return>", lambda event: self.commit_changes(button_name, event))


    # συναρτησεις που καλουν την self.make_toplevel_window με ορισμα το ονομα του κουμπιου 
    # που πατηθηκε, οι συναρτησεις αυτες ειναι command συναρτησεις των τεσσαρων κουμπιων 
    # διαχειρισης των στοιχειων ενος επιλεγμενου πελατη
    def change_customer_first_name(self):
        self.make_toplevel_window(self.change_first_name_button.winfo_name())
    def change_customer_surname(self):
        self.make_toplevel_window(self.change_surname_button.winfo_name())
    def change_customer_email(self):
        self.make_toplevel_window(self.change_email_button.winfo_name())
    def change_customer_phone_number(self):
        self.make_toplevel_window(self.change_phone_number_button.winfo_name())




    # συναρτηση για δευσμευση της αλλαγης και αρχης των λογικων ελεγχων
    # παιρνει ως ορισμα το ονομα του κουμπιου και σαν μη αναγκαστικο ορισμα event
    # ωστε να μπορει να χρησιμοποιηθει και σαν command σε κουμπι αλλα και σαν bind
    def commit_changes(self, button_name, event=None):
        # δημιουργια ενος ερωτηματος που αλλαζει αναλογα το ονομα του κουμπιου
        # που εχει πατηθει, ανοιγμα του connection και ανακτηση του user_input απο το
        # self.change_customer_info_entry, μετα απο lstrip και rstrip ωστε να φυγουν τα περιττα
        # κενα απο το input του χρηστη
        mod_query = "UPDATE clients SET"
        self.connection = open_connection()
        user_input = self.change_customer_info_entry.get().rstrip().lstrip()

        # δημιουργια ερωτηματος για ανακτηση δεδομενων του επιλεγμενου πελατη, με χρηση του μοναδικου
        # κινητου του αφου εχει ηδη επιλεχθει και αποθηκευση τους στο selected_customer_results
        selected_customer_query = f"SELECT * FROM clients WHERE phone_number = '{self.selected_customer_phone_number_customers_tab}'"
        selected_customer_results = fetch_all_dict_list(self.connection, selected_customer_query)

        # απο τις επομενες 4 περιπτωσεις θα γινει μονο μια αναλογα με το ονομα του κουμπιου
        # που επιλεχθηκε, θα αλλαξει το mod ερωτημα ωστε να γινει σωστη αλλαγη του εκαστοτε στοιχειου
        # παντα γινεται ελεγχος στο αν ειναι valid το user input
        # μονο αν αφορα αλλαγη κινητου ή email γινεται ελεγχος αν υπαρχει ηδη στην βαση αυτο το στοιχειο
        # αν υπαρχει ενημερωνει αναλογως και δεν γινεται αλλαγη, σε καθε περιπτωση ζηταει confirmation

        # αλλαγη ονοματος
        if button_name == "change first name":
            if user_input.isalpha() and len(user_input) <= 26:
                mod_query += f" first_name = '{user_input}' WHERE phone_number = '{self.selected_customer_phone_number_customers_tab}'"
                confirmation = messagebox.askyesno(title="Confirmation", message=f"Are you sure you want to change Customer {selected_customer_results[0]['first_name']} {selected_customer_results[0]['last_name']} first name to '{user_input}' ?")
                if confirmation:
                    execute_query(self.connection, mod_query)
                    self.connection.commit()
                    messagebox.showinfo(title="Changed Successfully", message="First name has been changed successfully")
                    self.selected_customer_customers_tab.set(f"{user_input} {selected_customer_results[0]['last_name']}")
            else:
                messagebox.showwarning(title="Invalid First Name", message=f"'{user_input}' is not a valid first name")

        # αλλαγη επιθετου
        elif button_name == "change surname":
            if user_input.isalpha() and len(user_input) <= 26:
                mod_query += f" last_name = '{user_input}' WHERE phone_number = '{self.selected_customer_phone_number_customers_tab}'"
                confirmation = messagebox.askyesno(title="Confirmation", message = f"Are you sure you want to change Customer {selected_customer_results[0]['first_name']} {selected_customer_results[0]['last_name']} surname to '{user_input}' ?")
                if confirmation:
                    execute_query(self.connection, mod_query)
                    self.connection.commit()
                    messagebox.showinfo(title="Changed Successfully", message="Last name has been changed successfully")
                    self.selected_customer_customers_tab.set(f"{selected_customer_results[0]['first_name']} {user_input}")
            else:
                messagebox.showwarning(title="Invalid Surname", message=f"'{user_input}' is not a valid surname")

        # αλλαγη email
        elif button_name == "change email":
            try:
                if not validate_email(user_input).email or len(user_input) > 50:
                    raise ValueError
                see_if_email_exists_query = f"SELECT * FROM clients WHERE email = '{user_input}'"
                see_if_email_exists_results = fetch_all_dict_list(self.connection, see_if_email_exists_query)
                if not see_if_email_exists_results:
                    mod_query += f" email = '{user_input}' WHERE phone_number = '{self.selected_customer_phone_number_customers_tab}'"
                    confirmation = messagebox.askyesno(title= "Confirmation", message=f"Are you sure you want to change Customer {selected_customer_results[0]['first_name']} {selected_customer_results[0]['last_name']} email to '{user_input}'")
                    if confirmation:
                        execute_query(self.connection, mod_query)
                        self.connection.commit()
                        messagebox.showinfo(title="Changed Successfully", message="Email has been changed successfully")
                else:
                    messagebox.showwarning(title="Email Taken", message=f"Email is taken from Customer {see_if_email_exists_results[0]['first_name']} {see_if_email_exists_results[0]['last_name']}")
            except ValueError as e:
                messagebox.showwarning(title="Invalid Email", message=f"{e}")

        # αλλαγη κινητου
        elif button_name == "change phone number":
            if user_input.isalnum() and len(user_input) == 10:
                see_if_phone_exists_query = f"SELECT * FROM clients WHERE phone_number = '{user_input}'"
                see_if_phone_exists_results = fetch_all_dict_list(self.connection, see_if_phone_exists_query)
                if not see_if_phone_exists_results:
                    mod_query += f" phone_number = '{user_input}' WHERE phone_number = '{self.selected_customer_phone_number_customers_tab}'"
                    confirmation = messagebox.askyesno(title="Confirmation", message = f"Are you sure you want to change Customer {selected_customer_results[0]['first_name']} {selected_customer_results[0]['last_name']} phone number to '{user_input}' ?")
                    if confirmation:
                        execute_query(self.connection, mod_query)
                        self.connection.commit()
                        messagebox.showinfo(title="Changed Successfully", message="Phone number has been changed successfully")
                        self.selected_customer_phone_number_customers_tab = f"{user_input}"
                        self.update_customer_buttons()
            else:
                messagebox.showwarning(title="Invalid Phone Number", message=f"'{user_input}' is not a valid phone number")
        close_connection(self.connection)




########################################################################################################################################################################################################################################################################
########################################################################################################################################################################################################################################################################
                            ###Functions for Search Tab###

########################################################################################################################################################################################################################################################################


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
            query=f"SELECT first_name,last_name,email\
                FROM amdb.clients\
                JOIN appointments ON clients.client_id = appointments.client_id\
                WHERE DATE(appointments.appointment_date)='{rv_date}'"
            cursor.execute(query)
            rows=cursor.fetchall()
            set_rows={values for values in rows}
            list_rows=list(set_rows)
            return(list_rows)                       

            cursor.close()
        except MYSQL.Error as e:
            print(e)
        close_connection(self.connection)

    
    #function gia erase to stoixeion apo to treeview

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
        self.selected_date=date(int(year_combo),int(month_combo),int(day_combo))     
        self.add_info(self.appointment_date(self.selected_date))

               
        

    
 