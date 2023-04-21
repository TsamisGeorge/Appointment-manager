import tkinter as tk

root = tk.Tk()

string = "world"
string2 = "Hello, "
string3 = string

label = tk.Label(root, text=f"{string2}{string3}", font=("Arial", 12))
label.pack()

label.config(justify="left")

label.config(compound="left")

label.config(fg="black")

label.config(font=("Arial", 12, "bold"), anchor="w", width=30)

root.mainloop()
