import tkinter as tk

def clear_entry():
    entry.delete(0, tk.END)

root = tk.Tk()

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text="Clear", command=clear_entry)
button.pack()

root.mainloop()
