###      METHODS TO WORK WITH THE WIDGETS ON THE APPOINTMENT TAB ###
####################################################################
from apt_imports import *
class Appointment_methods():
    def update_time_picker(self, event):
        date_string = f'{self.date_picker.selection_get()}'
        date_format = '%Y-%m-%d'
        date_obj = datetime.strptime(date_string, date_format).date()
        
        if date_obj == datetime.today().date():
            self.time_picker.destroy()
            hour = 24 -(24-datetime.now().hour)
            self.time_picker = ttk.Combobox(self.appointments_tab, values=[f"{str(h).zfill(2)}:{str(m).zfill(2)}" for h in range(9+hour+1, 24) for m in range(0, 60, 10)])
            self.time_picker.place(x = 260, y =260)
            self.time_picker.configure(state="readonly")
        else:
            self.time_picker.destroy()
            hour = 0
            self.time_picker = ttk.Combobox(self.appointments_tab, values=[f"{str(h).zfill(2)}:{str(m).zfill(2)}" for h in range(9, 21) for m in range(0, 60, 10)])
            self.time_picker['values'] +=("21:00",)
            self.time_picker.place(x = 260, y =260)
            self.time_picker.configure(state="readonly")

    def search_customer(self):
        self.connection = open_connection()
        prompt = self.search_customer_entry.get().lstrip().rstrip()
        if prompt.isalpha() or (not prompt.isdigit() and ('@' not in prompt or '.' not in prompt)):
            messagebox.showwarning(title="Invalid Input", message=f"Invalid Input")
            self.selected_customer_full_name.set(f"None")
            self.selected_customer_phone_number = 0
            self.create_apt_button.configure(state="disabled",relief="sunken")
            self.selected_customer_appointments_listbox.delete(0, tk.END)
            close_connection(self.connection)
        else:
            search_customer_query = f"SELECT * FROM Clients WHERE phone_number = '{prompt}' OR email = '{prompt}'"
            search_customer_results = fetch_all_dict_list(self.connection, search_customer_query)
            if not search_customer_results:
                messagebox.showwarning(title="Customer not found", message=f"Customer with {'phone number' if prompt.isdigit() else 'email'} {prompt} doesn't exist.")
                self.selected_customer_full_name.set(f"None")
                self.selected_customer_phone_number = 0
                self.create_apt_button.configure(state="disabled",relief="sunken")
                self.selected_customer_appointments_listbox.delete(0, tk.END)
                close_connection(self.connection)
            else:
                print(f"{search_customer_results[0]['first_name']} {search_customer_results[0]['last_name']}")
                self.selected_customer_full_name.set(f"{search_customer_results[0]['first_name']} {search_customer_results[0]['last_name']}")
                self.selected_customer_phone_number = f"{search_customer_results[0]['phone_number']}"
                self.create_apt_button.configure(state="normal",relief="raised")
                self.update_customer_appointments()
                close_connection(self.connection)

    def search_customer_enter(self, event):
        self.connection = open_connection()
        prompt = self.search_customer_entry.get().lstrip().rstrip()
        if prompt.isalpha() or (not prompt.isdigit() and ('@' not in prompt or '.' not in prompt)):
            messagebox.showwarning(title="Invalid Input", message=f"Invalid Input")
            self.selected_customer_full_name.set(f"None")
            self.selected_customer_phone_number = 0
            self.create_apt_button.configure(state="disabled",relief="sunken")
            self.selected_customer_appointments_listbox.delete(0, tk.END)
            close_connection(self.connection)
        else:
            search_customer_query = f"SELECT * FROM Clients WHERE phone_number = '{prompt}' OR email = '{prompt}'"
            search_customer_results = fetch_all_dict_list(self.connection, search_customer_query)
            if not search_customer_results:
                messagebox.showwarning(title="Customer not found", message=f"Customer with {'phone number' if prompt.isdigit() else 'email'} {prompt} doesn't exist.")
                self.selected_customer_full_name.set(f"None")
                self.selected_customer_phone_number = 0
                self.create_apt_button.configure(state="disabled",relief="sunken")
                self.selected_customer_appointments_listbox.delete(0, tk.END)
                close_connection(self.connection)
            else:
                print(f"{search_customer_results[0]['first_name']} {search_customer_results[0]['last_name']}")
                self.selected_customer_full_name.set(f"{search_customer_results[0]['first_name']} {search_customer_results[0]['last_name']}")
                self.selected_customer_phone_number = f"{search_customer_results[0]['phone_number']}"
                self.create_apt_button.configure(state="normal",relief="raised")
                self.update_customer_appointments()
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
                if last_appointment_id:
                    apt_creation_query = f'''INSERT INTO appointments(appointment_id, appointment_date, appointment_interval, client_id) VALUES({last_appointment_id[0]['appointment_id'] + 1},'{apt_date}', '{apt_duration}', {current_customer_results[0]['client_id']})'''
                else:
                    apt_creation_query = f'''INSERT INTO appointments(appointment_id, appointment_date, appointment_interval, client_id) VALUES(1,'{apt_date}', '{apt_duration}', {current_customer_results[0]['client_id']})'''
                validation = messagebox.askyesno("Validation", message= "Are you sure you want to schedule this appointment?")
                if validation:
                    insert_query(self.connection, apt_creation_query)
                    self.connection.commit()
                    messagebox.showinfo(title="Appointment Scheduled", message = f'''An appointment has been scheduled for customer {current_customer_results[0]['first_name']} {current_customer_results[0]['last_name']} at {apt_date} with duration {int(self.time_picker2.get())} minutes''')
            else:
                messagebox.showwarning(title="Appointment Time Taken", message=f'''There's already an appointment set on {appointmnents_results[0]['appointment_date']} until {appointmnents_results[0]['appointment_interval']}''')
            close_connection(self.connection)
    

    def update_customer_appointments(self):
        curr_customer_query = f"SELECT * FROM Clients WHERE phone_number = '{self.selected_customer_phone_number}'"
        self.connection = open_connection()
        curr_customer_results = fetch_all_dict_list(self.connection, curr_customer_query)
        curr_customer_appointments_query = f"SELECT * FROM Appointments WHERE client_id = {curr_customer_results[0]['client_id']}"
        curr_customer_appointments_results = fetch_all_dict_list(self.connection, curr_customer_appointments_query)
        print(len(curr_customer_appointments_results), curr_customer_appointments_results)
        if curr_customer_appointments_results:
            self.selected_customer_appointments_listbox.delete(0, tk.END)
            for appointment in curr_customer_appointments_results:
                appointment_duration = appointment['appointment_interval'].strftime('%H:%M:%S')
                self.selected_customer_appointments_listbox.insert(tk.END, f"{appointment['appointment_date'].date()}   {appointment['appointment_date'].time()}  - {appointment_duration}")
        else:
            self.selected_customer_appointments_listbox.delete(0, tk.END)
        close_connection(self.connection)

    def reschedule_apt_command(self):
        print(1)
    def delete_apt_command(self):
        pass