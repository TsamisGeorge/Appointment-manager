from tkinter import *
from tkinter.ttk import *
from tk_util import *



#main window of the application
main_window = Tk()
main_window.geometry("800x600")
main_window.title("Appointment Manager")
icon = PhotoImage(file = "main_icon.png")
main_window.iconphoto(True, icon)

#making the notebook object to hold the tabs of the app
notebook = Notebook(main_window)
notebook_style = Style()
notebook_style.configure('TNotebook.Tab', font=('Segoe UI', 11), padding=[5, 4])
notebook.grid(row=0,column=0)

#making the frames that will go to the notebook as tabsa
new_apt = Frame(notebook)
apt_changes = Frame(notebook)
del_apt = Frame(notebook)
print_apt = Frame(notebook)

#adding the tabs
notebook.add(new_apt,text = "Make a new appointment")
notebook.add(apt_changes,text = "Change appointment")
notebook.add(del_apt, text = "Delete appointment")
notebook.add(print_apt, text = "Print appointments")



#mainloop
main_window.mainloop()