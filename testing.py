import tkinter as tk
import tkinter.messagebox as messagebox

root = tk.Tk()

# update the string variable (and the label) when a button is clicked
def valid():
    validation = messagebox.askyesno("Title", message= "Temp")
    print(validation)

button = tk.Button(root, text="Click me!", command=valid)
button.pack()

root.mainloop()