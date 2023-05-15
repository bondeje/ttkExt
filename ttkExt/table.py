import tkinter as tk
import tkinter.ttk as ttk
import collections.abc as cabc
from functools import partial

TABLE_WIDGETS = {}

# add name to TABLE_WIDGETS
def define_table_widget(name, class_, opts, var):
    TABLE_WIDGETS[name] = {'class': class_,
                           'opts': opts,
                           'var': var}
    
def get_row_column(event):
    info = event.widget.grid_info()
    return info['row'], info['column']

define_table_widget('Button', ttk.Button, {}, ['textvariable', tk.StringVar, 'Not yet configured'])
define_table_widget('Bheckbutton', ttk.Checkbutton, {}, ['variable', tk.IntVar, 0])
define_table_widget('Combobox', ttk.Combobox, {}, ['textvariable', tk.StringVar, 'Not yet configured'])
define_table_widget('Entry', ttk.Entry, {}, ['textvariable', tk.StringVar, 'Not yet configured'])
define_table_widget('tkEntry', tk.Entry, {}, ['textvariable', tk.StringVar, 'Not yet configured'])
define_table_widget('Label', ttk.Label, {}, ['textvariable', tk.StringVar, 'Not yet configured'])
define_table_widget('Radiobutton', ttk.Radiobutton, {'text':'','value':0}, ['variable', tk.IntVar, 0])

#TODO: only fills in the widget for making the event. need all attributes from Event
def build_widget_callback_command(widget, callback):
    event = tk.Event()
    event.widget = widget
    def command():
        return callback(event)
    return command

def widget_callback_command(callback):
    return partial(build_widget_callback_command, callback=callback)
        
class Table(ttk.Frame):
    JUSTIFY_TO_ANCHOR = {tk.LEFT:tk.W, tk.CENTER:tk.CENTER, tk.RIGHT:tk.E}
    def __init__(self, master=None, col_specs=None, n_rows=0, show_row_labels=False, **kw):
        super().__init__(master)
        self.Canvas = tk.Canvas(self, borderwidth=0)
        self.Frame = ttk.Frame(self.Canvas)

        #TODO: need to add horizontal as well
        self.VerticalScrollbar = ttk.Scrollbar(self, command=self.Canvas.yview)
        self.Canvas.config(yscrollcommand=self.VerticalScrollbar.set)

        # add scrollbar TODO: make optional
        self.VerticalScrollbar.pack(side="right", fill="y")
        self.Canvas.pack(side="left", fill="both", expand=True)
        self.Canvas.create_window((4,4), window=self.Frame, anchor="nw")
        # col_specs is a dictionary with key:value pairs -- column header string:widget type string
        # use map_column to apply configurations over all rows in hte same column
        self.n_rows = 0
        self._show_row_labels = show_row_labels
        self.n_cols = len(col_specs)
        self.col_types = list(col_specs.values())
        self.column_configs = [{} for _ in range(self.n_cols)]

        self.col_headers = []
        for ic, header in enumerate(col_specs.keys()):
            self.col_headers.append(ttk.Label(self.Frame, text=header))
            self.col_headers[-1].grid(row=0, column=ic+1)

        self.row_labels = []

        self.cells = []

        for ir in range(n_rows):
            self.add_row()

        #TODO need a variable to hold current non-default configurations for each column
        
        self.Frame.pack(side="left")
        self.VerticalScrollbar.pack_forget()
        self.Canvas.bind("<Configure>", self.reconfig)

    def reconfig(self, event):
        self.Canvas.config(scrollregion=self.bbox("all"))

    def show_row_labels(self):
        self._show_row_labels=True
        N = len(self.row_labels)
        for ir in range(self.n_rows):
            if ir >= N:
                self.row_labels.append(ttk.Label(self.Frame, text=str(ir)))
            self.row_labels[ir].grid(row=ir+1, column=0)

    def hide_row_labels(self):
        for ir in range(self.n_rows):
            self.row_labels[ir].grid_forget()
        self._show_row_labels=False

    def _process_config(self, row, column, config, filter_loc=False):
        out_config = {}
        for k in list(config.keys()):
            if k.endswith("_cell"):
                v = config.pop(k)
                if not filter_loc:
                    config[k[:-len("_cell")]] = v(self._get_widget(row, column))
                else:
                    out_config[k] = v
            elif k.endswith("_row"):
                v = config.pop(k)
                config[k[:-len("_row")]] = v(row)
            elif k.endswith("_col"):
                v = config.pop(k)
                config[k[:-len("_col")]] = v(column)
        var_config = {}
        if "var" in config:
            var_config["var"] = config.pop("var")
        
        return out_config, var_config
    
    def _apply_var_config(self, row, column, config):
        if config and "var" in config and self.cells[row][column][1]:
            self.cells[row][column][1].set(config.pop("var"))

    def set_column(self, column, **kwargs):
        # a better way to do this is to separate the callable values into a different dictionary 
        # and run each of them separately so that .configure is only called at most 2x
        self.column_configs[column].update(kwargs)
        for row in range(self.n_rows):
            cfg = dict(kwargs)
            dep, var = self._process_config(row, column, cfg)
            self._apply_var_config(row, column, var)
            self.cells[row][column][0].configure(**cfg)
    
    # NOTE that the row+1 is so that the table is 0-indexed for contents in both row and column. 
    # To get header information, use get_header(column)
    def _get_widget(self, row, column):
        return self.cells[row][column][0]
    
    def get_header(self, column):
        return self.col_headers[column]
    
    # config is a dictionary of configuration options
    def table_widget_factory(self, row, column):
        table_widget = TABLE_WIDGETS[self.col_types[column]]
        config = dict(table_widget['opts'])
        config.update(self.column_configs[column])
        dep_config, var_config = self._process_config(row, column, config, filter_loc=True)
        widget = table_widget['class'](self.Frame, **config)
        var = None
        if table_widget['var']:
            var = table_widget['var'][1]()
            if len(table_widget['var']) > 2:
                var.set(table_widget['var'][2])
            widget.configure(**{table_widget['var'][0]:var})
        return widget, var, dep_config, var_config
    
    # row and column must be a valid entry for the table
    def _new_cell(self, row, column):
        if self.cells[row][column]:
            self.cells[row][column][0].destroy()
            self.cells[row][column] = None # does this leak the variable?
        ID = self.table_widget_factory(row, column)
        self.cells[row][column] = (ID[0], ID[1])
        self.cells[row][column][0].grid(row=row+1, column=column+1)
        return ID
    
    def add_row(self):
        ir = self.n_rows
        self.cells.append([None]*self.n_cols)
        dep = []
        for ic in range(self.n_cols):
            dep.append(self._new_cell(ir, ic))
        
        for ic in range(self.n_cols):
            if dep[ic][2]:
                dc,dvc = self._process_config(ir,ic, dep[ic][2])
                dep[ic][3].update(dvc)
                dep[ic][0].configure(**dep[ic][2])
            if dep[ic][3]:
                self._apply_var_config(ir, ic, dep[ic][3])
                
        dep.clear()
        self.n_rows += 1
        if self._show_row_labels:
            self.show_row_labels()
        return self.n_rows
    
    def del_row(self, row):
        if row >= self.n_rows:
            return
        table_row = self.cells.pop(row)
        for cell in table_row:
            cell[0].destroy()
        self.n_rows -= 1
        if self._show_row_labels:
            self.row_labels.pop().destroy()
        for ir in range(row, self.n_rows):
            for ic in range(self.n_cols):
                self.cells[ir][ic][0].grid(row=ir+1, column=ic+1)
        
    
    # TODO:
    # def delete_row(self, row):
    
    # returns a variable if valid else None
    def _clean_key(self, key):
        if not isinstance(key, tuple) or len(key) != 2:
            raise TypeError(f"{key} in Table[key] must be a (row, column) tuple")
            return None
        # TODO: this method requires specifically key to be a tuple of integers...need to fix to allow column identification by headers
        cell = self.cells[key[0]][key[1]]
        if cell:
            return cell[1]
        return cell
    
    def __getitem__(self, key):
        var = self._clean_key(key)
        if var:
            return var.get()
        else:
            raise ValueError(f"Table[{key[0]}, {key[1]}] does not point to a valid variable to fetch")
    
    def __setitem__(self, key, value):
        var = self._clean_key(key)
        if var:
            var.set(value)
        else:
            raise ValueError(f"Table[{key[0]}, {key[1]}] does not point to a valid variable for assignment")
        
