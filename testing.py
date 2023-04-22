import tkinter as tk

class MyGUI:
    def __init__(self, master):
        self.master = master
        
        # Create a list of items to display in the listbox
        self.items = ["Apple", "Banana", "Cherry", "Durian", "Elderberry"]
        
        # Create a listbox, a button, and a delete button
        self.listbox = tk.Listbox(master)
        for item in self.items:
            self.listbox.insert(tk.END, item)
        self.listbox.pack()
        
        self.button = tk.Button(master, text="My Button", state=tk.DISABLED)
        self.button.pack()
        
        self.delete_button = tk.Button(master, text="Delete", command=self.delete_item)
        self.delete_button.pack()
        
        # Bind the listbox to a selection event
        self.listbox.bind("<<ListboxSelect>>", self.update_button_state)
        
    def update_button_state(self, event):
        # Get the number of selected items in the listbox
        num_selected = len(self.listbox.curselection())
        
        # If at least one item is selected, enable the button, otherwise disable it
        if num_selected > 0:
            self.button.config(state=tk.NORMAL)
        else:
            self.button.config(state=tk.DISABLED)
    
    def delete_item(self):
        # Get the index of the selected item(s) in the listbox
        selection = self.listbox.curselection()
        
        # Delete the selected item(s) from the listbox
        for i in reversed(selection):
            self.listbox.delete(i)
        
        # Update the state of the button
        self.update_button_state(None)

root = tk.Tk()
my_gui = MyGUI(root)
root.mainloop()
