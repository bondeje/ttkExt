import tkinter as tk
import tkinter.ttk as ttk

class LabeledCombobox(ttk.Frame):
    def __init__(self, master = None, **kw):
        label_orientation = kw.pop('label_orientation', 'top')
        ttk.Frame.__init__(self, master, **kw)
        self.Label = ttk.Label(self, width = self['width'], text = "Label not yet configured")
        self.Label.pack(side = label_orientation)
        self.Combobox = ttk.Combobox(self, width = round((self['width']-2)), justify = tk.LEFT, \
                                     values = tuple())
        self.Combobox.set("Combobox not yet configured")
        self.Combobox.pack(side = label_orientation)

class LabeledEntry(ttk.Frame):
    def __init__(self, master = None, **kw):
        label_orientation = kw.pop('label_orientation', 'top')
        ttk.Frame.__init__(self, master, **kw)
        self.Label = ttk.Label(self, width = self['width'], text = "Label not yet configured")
        self.Label.pack(side = label_orientation)
        self.Entry = ttk.Entry(self, width = self['width'], justify = tk.LEFT)
        self.Entry.insert(tk.END, "Combobox not yet configured")
        self.Entry.pack(side = label_orientation)