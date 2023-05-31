import re
import dns.resolver
from tkinter import messagebox

user_input = "m@g.co"
def validate_email(address):
    valid_regex = bool(re.match(r'^[\w\.-]+@[\w\.-]+\.[A-Za-z]{2,}$', address))
    if(valid_regex):
        domain = user_input.split("@")[-1]
        try:
            answers = dns.resolver.resolve(domain, 'MX')
            record = answers[0].exchange
            print(record)
        except dns.resolver.NoAnswer:
            print("No MX records found for the domain")
        except dns.resolver.NXDOMAIN:
            print("The domain does not exist")
        except dns.resolver.NoNameservers:
            print("Could not reach DNS servers")
        except dns.resolver.Timeout:
            print("DNS query timed out")
    else:
        messagebox.showwarning(title="Email Not Valid", message="Email format is not valid.")
validate_email(user_input)
