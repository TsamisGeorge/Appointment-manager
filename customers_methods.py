###   METHODS TO WORK WITH THE WIDGETS ON THE CUSTOMERS TAB   ###
#################################################################
from appointments_methods import *
class Customers_methods():
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
        if valid_info:
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
                execute_query(self.connection, final_query)
                self.connection.commit()
                messagebox.showinfo(title="Inserted successfully",message=f"Customer {name} {surname} has been inserted successfully")
                self.clear_customers_entry()
                close_connection(self.connection)
    
    def clear_customers_entry(self):
        self.first_name_entry.delete(0, tk.END)
        self.surname_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_number_entry.delete(0, tk.END)



    def search_customer_customers_tab(self, event=None):
        self.connection = open_connection()
        prompt = self.search_customer_entry2.get().lstrip().rstrip()
        if prompt.isalpha() or (not prompt.isdigit() and ('@' not in prompt or '.' not in prompt)):
            messagebox.showwarning(title="Invalid Input", message=f"Invalid Input")
            self.selected_customer_customers_tab.set("None")
            self.selected_customer_phone_number_customers_tab = 0
            close_connection(self.connection)
        else:
            search_customer_query = f"SELECT * FROM Clients WHERE phone_number = '{prompt}' OR email = '{prompt}'"
            search_customer_results = fetch_all_dict_list(self.connection, search_customer_query)
            if not search_customer_results:
                messagebox.showwarning(title="Customer not found", message=f"Customer with {'phone number' if prompt.isdigit() else 'email'} {prompt} doesn't exist.")
                self.selected_customer_customers_tab.set("None")
                self.selected_customer_phone_number_customers_tab = 0
            else:
                print(f"{search_customer_results[0]['first_name']} {search_customer_results[0]['last_name']}")
                self.selected_customer_customers_tab.set(f"{search_customer_results[0]['first_name']} {search_customer_results[0]['last_name']}")
                self.selected_customer_phone_number_customers_tab = f"{search_customer_results[0]['phone_number']}"
            close_connection(self.connection)
        self.update_customer_buttons()
    

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

    def make_toplevel_window(self, button_name):
        self.change_customer_info_window = tk.Toplevel()

        window_width = 330
        window_height = 120
        screen_width = self.change_customer_info_window.winfo_screenwidth()
        screen_height = self.change_customer_info_window.winfo_screenheight()
        x = int((screen_width/2) - (window_width/2))
        y = int((screen_height/2) - (window_height/2))
        self.change_customer_info_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.change_customer_info_window.minsize(window_width, window_height)
        self.change_customer_info_window.maxsize(window_width, window_height)

        self.toplevel_window_frame = tk.Frame(self.change_customer_info_window, relief="raised", borderwidth=6, padx=14, pady=1)
        self.toplevel_window_frame.pack()
        self.toplevel_window_label = tk.Label(self.toplevel_window_frame, text=f"{button_name.title()}", font=("Segoe UI",10))
        self.toplevel_window_label.pack()
        self.change_customer_info_entry = tk.Entry(self.change_customer_info_window,width=36)
        self.change_customer_info_entry.place(x=56,y=66)
        self.change_customer_info_button = tk.Button(self.change_customer_info_window, image = self.check_icon)
        self.change_customer_info_button.place(x=280,y=60)



    def change_customer_first_name(self):
        self.make_toplevel_window(self.change_first_name_button.winfo_name())
    def change_customer_surname(self):
        self.make_toplevel_window(self.change_surname_button.winfo_name())
    def change_customer_email(self):
        self.make_toplevel_window(self.change_email_button.winfo_name())
    def change_customer_phone_number(self):
        self.make_toplevel_window(self.change_phone_number_button.winfo_name())