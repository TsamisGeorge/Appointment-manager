import tkinter as tk

root = tk.Tk()

# create a listbox widget
listbox = tk.Listbox(root)
listbox.pack()

# insert some items into the listbox
listbox.insert(0, "Item 1")
listbox.insert(1, "Item 2")
listbox.insert(2, "Item 3")

# update the listbox to ensure all items are drawn
listbox.update()

# get the y-coordinate of the second item in the listbox
y = listbox.bbox(1)[2]

print(y)

root.mainloop()
