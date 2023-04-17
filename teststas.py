import tkinter as tk
import tkinter.ttk as ttk
from datetime import *

time = datetime.now()
root = tk.Tk()
hour = 24 -(24-time.hour)
print(hour)
time_var = tk.StringVar()
#time_picker = ttk.Combobox(root, textvariable=time_var, values=['{:02d}:{:02d}'.format(h, m) for h in range(24 - int(time.hour)) for m in range(int(time.hour), 60, 10)])
time_picker = ttk.Combobox(root, textvariable = time_var, values = [f'{str(h).zfill(2)}:{str(m).zfill(2)}' for h in range (hour+1,24) for m in range(0,60,10)])
time_picker.pack()

root.mainloop()