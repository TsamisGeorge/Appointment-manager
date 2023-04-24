import tkinter as tk

class ButtonReliefs(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        reliefs = ['flat', 'raised', 'sunken', 'groove', 'ridge']
        for r in reliefs:
            tk.Button(self.master, text=r, relief=r).pack(side='left', padx=5, pady=5)

root = tk.Tk()
app = ButtonReliefs(master=root)
app.mainloop()
