import tkinter as tk
from PIL import Image, ImageTk




root = tk.Tk()

searching = Image.open("searching.png")
searching = searching.resize((26,26), Image.ANTIALIAS)
searching = ImageTk.PhotoImage(searching)
# create an image object
icon = tk.PhotoImage(file="searching.png")

# create a label widget with an icon
button = tk.Button(root, compound=tk.LEFT, image=searching)
button.pack(padx=10, pady=10)

root.mainloop()