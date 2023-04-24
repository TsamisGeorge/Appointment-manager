###   METHODS TO WORK WITH THE WIDGETS ON THE CUSTOMERS TAB   ###
#################################################################
from appointments_methods import *
class Customers_methods():
    def create_customer(self):
        valid_info = 0
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
                close_connection(self.connection)
    

    def search_customer_customers_tab(self, event=None):
        self.connection = open_connection()
        prompt = self.search_customer_entry2.get().lstrip().rstrip()
        if prompt.isalpha() or (not prompt.isdigit() and ('@' not in prompt or '.' not in prompt)):
            messagebox.showwarning(title="Invalid Input", message=f"Invalid Input")
            self.selected_customer_customers_tab.set(f"None")
            self.selected_customer_phone_number_customers_tab = 0
            close_connection(self.connection)
        else:
            search_customer_query = f"SELECT * FROM Clients WHERE phone_number = '{prompt}' OR email = '{prompt}'"
            search_customer_results = fetch_all_dict_list(self.connection, search_customer_query)
            if not search_customer_results:
                messagebox.showwarning(title="Customer not found", message=f"Customer with {'phone number' if prompt.isdigit() else 'email'} {prompt} doesn't exist.")
                self.selected_customer_customers_tab.set(f"None")
                self.selected_customer_phone_number_customers_tab = 0
            else:
                print(f"{search_customer_results[0]['first_name']} {search_customer_results[0]['last_name']}")
                self.selected_customer_customers_tab.set(f"{search_customer_results[0]['first_name']} {search_customer_results[0]['last_name']}")
                self.selected_customer_phone_number_customers_tab = f"{search_customer_results[0]['phone_number']}"
            close_connection(self.connection)