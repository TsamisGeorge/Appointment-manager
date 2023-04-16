from tkinter import *
from tkinter.ttk import *
from tk_tools import *



#main window of the application
main_window = Tk()
main_window.geometry("1000x600")
main_window.title("Appointment Manager")
icon = PhotoImage(file = "time-management.png")
main_window.iconphoto(True, icon)

#making the notebook object to hold the tabs of the app
notebook = Notebook(main_window)
notebook_style = Style()
notebook_style.configure('TNotebook.Tab', font=('Segoe UI', 12), padding=[2, 1])
notebook.grid(row=0, column=0)

#making the frames that will go to the notebook as tabsa
new_apt = Frame(notebook)
apt_changes = Frame(notebook)
del_apt = Frame(notebook)
print_apt = Frame(notebook)

#add icons to the tabs
new_apt_icon = PhotoImage(file="calendar.png").subsample(30)
apt_changes_icon = PhotoImage(file="recurrent.png").subsample(30)
del_apt_icon = PhotoImage(file="del.png").subsample(30)
print_apt_icon = PhotoImage(file="printing.png").subsample(30)

#adding the tabs
notebook.add(new_apt,text = "Make a new appointment",image=new_apt_icon, compound='left')
notebook.add(apt_changes,text = "Change appointment",image=apt_changes_icon, compound='left')
notebook.add(del_apt, text = "Delete appointment",image=del_apt_icon, compound='left')
notebook.add(print_apt, text = "Print appointments",image=print_apt_icon, compound='left')



#mainloop
main_window.mainloop()