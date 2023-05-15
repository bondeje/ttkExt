import tkinter as tk
import tkinter.ttk as ttk

class ScrolledText(ttk.Frame):
    DEFAULT_WIDTH = 100
    DEFAULT_HEIGHT = 3
    def __init__(self, master = None, **kw):
        horizontal = kw.pop('horizontal', False)
        vertical = kw.pop('vertical', True)
        _width = kw.pop('textwidth', ScrolledText.DEFAULT_WIDTH)
        _height = kw.pop('textheight', ScrolledText.DEFAULT_HEIGHT)
        ttk.Frame.__init__(self, master, **kw)
        
        if horizontal:
            _wrap = tk.NONE
        else:
            _wrap = tk.WORD
        
        self.Text = tk.Text(self, width=_width, height=_height, wrap=_wrap)
        
        if vertical:
            self.Vscroll = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.Text.yview)
            self.Text.configure(yscrollcommand=self.Vscroll.set)
            self.Vscroll.grid(row=0, column=1, sticky=tk.NS)
        else:
            self.Vscroll = None
            
        if horizontal:
            self.Hscroll = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.Text.xview)
            self.Text.configure(xscrollcommand=self.Hscroll.set)
            self.Hscroll.grid(row=1, column=0,sticky=tk.EW)
        
        self.Text.grid(row=0, column=0, sticky=tk.NSEW)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)