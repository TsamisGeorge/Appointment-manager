import tkinter as tk

root = tk.Tk()

# create a list of options for the first selection widget
options_1 = ['Option 1', 'Option 2', 'Option 3']

# create a dictionary of possible options for the second selection widget
options_2 = {
    'Option 1': ['A', 'B', 'C'],
    'Option 2': ['X', 'Y', 'Z'],
    'Option 3': ['1', '2', '3']
}

# create the first selection widget
var_1 = tk.StringVar(value=options_1[0])
widget_1 = tk.OptionMenu(root, var_1, *options_1)
widget_1.pack()

# create the second selection widget
var_2 = tk.StringVar(value=options_2[options_1[0]][0])
widget_2 = tk.OptionMenu(root, var_2, *options_2[var_1.get()])
widget_2.pack()

# function to update options for widget_2 when widget_1 is changed
def update_options(*args):
    widget_2['menu'].delete(0, 'end')
    for option in options_2[var_1.get()]:
        widget_2['menu'].add_command(label=option, command=tk._setit(var_2, option))

# bind the update_options function to changes in widget_1
var_1.trace('w', update_options)

root.mainloop()
