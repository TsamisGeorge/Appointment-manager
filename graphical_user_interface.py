from tkinter import *
from tkinter.ttk import *
from tk_tools import *

class Appointment_manager:
    def __init__(self):
        #main app window
        self.main_window = Tk()
        self.main_window.geometry("1000x600")
        self.main_window.title("Appointment Manager")
        icon = PhotoImage(file="time-management.png")
        self.main_window.iconphoto(True, icon)

        #making the notebook object to hold the tabs of the app
        self.notebook = Notebook(self.main_window)
        notebook_style = Style()
        notebook_style.configure('TNotebook.Tab', font=('Segoe UI', 12), padding=[2, 1])
        self.notebook.grid(row=0, column=0)

        #making the frames that will go to the notebook as tabs
        self.new_apt = Frame(self.notebook)
        self.apt_changes = Frame(self.notebook)
        self.del_apt = Frame(self.notebook)
        self.print_apt = Frame(self.notebook)

    def start(self):
        #loading the pictures of the GUI
        new_apt_icon = PhotoImage(file="calendar.png").subsample(30)
        apt_changes_icon = PhotoImage(file="recurrent.png").subsample(30)
        del_apt_icon = PhotoImage(file="del.png").subsample(30)
        print_apt_icon = PhotoImage(file="printing.png").subsample(30)

        #adding the tabs
        self.notebook.add(self.new_apt, text="Make a new appointment", image=new_apt_icon, compound='left')
        self.notebook.add(self.apt_changes, text="Change appointment", image=apt_changes_icon, compound='left')
        self.notebook.add(self.del_apt, text="Delete appointment", image=del_apt_icon, compound='left')
        self.notebook.add(self.print_apt, text="Print appointments", image=print_apt_icon, compound='left')
    
        #mainloop
        self.main_window.mainloop()