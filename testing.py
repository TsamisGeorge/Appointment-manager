import tkinter as tk

# Create a Tkinter window
root = tk.Tk()
root.title("Relief Demo")

# Create a frame to contain each relief option label
raised_frame = tk.Frame(root, relief="raised", borderwidth=5, padx=10, pady=10)
raised_frame.pack(side="left", padx=10)

# Create a label for each relief option and add it to the corresponding frame
tk.Label(raised_frame, text="Raised").pack()

root.mainloop()
