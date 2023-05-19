import sys, os, time
sys.path.append(os.path.join(os.path.split(__file__)[0], ".."))
import ttkExt.table as table

import tkinter as tk
import tkinter.ttk as ttk

def set_label(event, tab):
    row, col = table.get_row_column(event)
    tab[row,col+1] = f"set by button in ({row},{col})"

def callback_delete_row(event, tab):
    row, col = table.get_row_column(event)
    tab.del_row(row)

a = tk.Tk()
b = table.Table(a, {"buttons":"Button", "labels":"Label", "del":"Button"}, 2, True)
b.set_column(0, command_cell=table.widget_callback_command(lambda event: set_label(event, b)),
             var_row=lambda x: f"Button. Row = {x}")
b.set_column(1, var="")
b.set_column(2, command_cell=table.widget_callback_command(lambda event: callback_delete_row(event, b)),
             var="Del row")
c = ttk.Button(a, text="show row_lables", command=b.show_row_labels)
c.pack(side="top")
d = ttk.Button(a, text="hide row_lables", command=b.hide_row_labels)
d.pack(side="top")
e = ttk.Button(a, text="add row", command=b.add_row)
e.pack(side="top")
b.pack(side="top")
a.mainloop()