#smtp and email usage etc

import os
import smtplib
from email.message import EmailMessage
from search_methods import *

EMAIL_ADDRESS=os.environ.get('MAIL_USER')
EMAIL_PASSWORD=os.environ.get('MAIL_PWD')


class SMTP_Methods():
    #function για retrieve data fm treeview
    def extraction_data(self):
        data1=[]
        for item_id in self.tree.get_children():
            data = self.tree.item(item_id)
            data1.append(data['values'])
        return(data1)


    #function του πλήκτρου send notification
    def send_notification(self):
        info=self.extraction_data()
    
        for i in range(len(info)):
            msg=EmailMessage()
            msg['Subject'] = "Appointment Reminder"
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = info[i][2]
            msg.set_content(f"Mr/Mrs {info[i][0]} {info[i][1]} your appointment is scheduled for {info[i][4]} at: {info[i][3]}")

            with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
                smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD) 
                smtp.send_message(msg)

        show_email_info=showinfo(message='Emails were sent')