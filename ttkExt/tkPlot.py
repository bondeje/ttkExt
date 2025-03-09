import tkinter as tk
import tkinter.ttk as ttk
from functools import partial

DEFAULT_FACECOLOR=[0.9411764705882353, 0.9411764705882353, 0.9411764705882353]

import matplotlib
try:
    matplotlib.use('TKAgg')
except ImportError: # for some fucking reason, setting the backend will almost always fail the first time (whether it is the kernel reload or what, I do not know) and I have to try again. tkinter taking to long to load?
    print("TkAgg load error, re-loading program")
    matplotlib.rcParams['backend'] = 'TkAgg'
    matplotlib.use('TKAgg')
#import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # probably redundant
#from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.figure import Figure

class tkPlots(ttk.Frame):
    def __init__(self, master=None, *args, axes=None, width=None, height=None, variable=None, **kwargs):
        # set background color. GraphDisplay_tplvl is the current app TopLevel
        super().__init__(master)
        tl = None
        if master:
            tl = master.winfo_toplevel()
        if tl:
            rgb_max = 2**16-1
            self.rgb = [x/rgb_max for x in tl.winfo_rgb(tl.cget('bg'))]
        else:
            self.rgb = DEFAULT_FACECOLOR

        if not width:
            width = matplotlib.rcParams["figure.figsize"][0]

        if not height:
            height = matplotlib.rcParams["figure.figsize"][1]
        
        if axes:
            self.Figure = axes.get_figure()
            self.Figure.set_size_inches(width, height)
        else:
            self.Figure = Figure(figsize=(width, height), facecolor=self.rgb)
        self.Canvas = FigureCanvasTkAgg(self.Figure, self)
        ax = self.Figure.gca()
        ax.set_ylim(auto=True)
        ax.set_xlim(auto=True)
        self.variable = variable
        self.draw()
        self.Canvas.get_tk_widget().pack(side = 'top')
        
        tkagg.NavigationToolbar2Tk(self.Canvas, tl)
    def draw(self):
        self.Figure.clear()
        ax = self.Figure.gca()
        for pl in self.variable:
            args = pl[0]
            kwargs = pl[1]
            ax.plot(*pl[0], **pl[1])
        self.Canvas.draw()

def tkPlotVar_value(*args, **kwargs):
    return (args, kwargs)
        
class tkPlotVar(tk.BooleanVar):
    def __init__(self, master=None, value=None, name=None):
        if not isinstance(value, list):
            value = [value]
        self.value_ = value
        super().__init__(master, value = False, name=name)
    def __getitem__(self, key):
        return self.value_[key]
    def __setitem__(self, key, value):
        self.value_[key] = value
        # so that triggers assigned to superclass are triggered
        super().set(not super().get())
    def __len__(self):
        return len(self.value_)
    def get(self):
        val = super().get()
        return self.value_
    def set(self, value):
        if not isinstance(value, list):
            value = [value]
        self.value_ = value
        # so that triggers assigned to superclass are triggered
        super().set(not super().get())
        return self.value_
    
def setplotvar(var, index, val):
    print("triggered setplotvar")
    var[index] = val

def update_plot(plot, *args):
    plot.draw()
    
if __name__ == "__main__":
    tl = tk.Tk()
    dvar = tkPlotVar_value([1, 2, 3, 4, 5], [1, 4, 9, 16, 25])
    dvar2 = tkPlotVar_value([1, 2, 3, 4, 5], [-1, -4, -9, -16, -25])
    dvar3 = tkPlotVar_value([1, 2, 3, 4, 5], [1, -4, 9, -16, 25])
    plotvar = tkPlotVar(value=[dvar, dvar2])
    p = tkPlots(tl, variable=plotvar)
    plotvar.trace_add('write', partial(update_plot, p))
    p.pack(side="top")
    bt = ttk.Button(tl, text="update data", command=partial(setplotvar, plotvar, 0, dvar3))
    bt.pack(side="top")
    tl.mainloop()