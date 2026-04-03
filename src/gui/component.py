import config
import level
import tkinter as tk
from tkinter import filedialog
import numpy as np
import reader as rd
import cad
import spreadsheet
import model as md
import os
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from . import action as ax_com

def update_text_from_stringvar(text_area,string_var,var_name, index, operation):
    # Update the Text widget from the StringVar
    text_area.config(state="normal")  # Enable editing
    text_area.delete("1.0", tk.END)  # Clear existing text
    text_area.insert("1.0", string_var.get())  # Insert new text
    text_area.config(state="disabled")  # Disable editing again


from tkinter.filedialog import asksaveasfile

class ButtonFrame(tk.Frame):
    
    def __init__ (self, parent, title="", button_params = [],side="top"):       
        super().__init__(parent,pady=3,padx=3,bd=3,relief="groove")
        self.row = 0
        self.pack(side=side,pady=5)
        if title:
            self.insert_title(title)
        self.frame_grid = tk.Frame(self)
        self.frame_grid.pack()
        for param in button_params:
            self.insert_button(param["label"],param["command"])
            self.row += 1
 
    def insert_title(self, title):
        label_title = tk.Label(self, text = title,font='Helvetica 10 bold', pady=4,padx=4,bd=3, relief="ridge")
        label_title.pack(pady=3,padx=3)
    
    def insert_button (self, text, command=lambda:print("ButtonFrame button")):
        width = len(text) + 1
        label     = tk.Label(self.frame_grid,  text=text, font='Helvetica 10 italic', width=width, anchor="w")
        button    = tk.Button(self.frame_grid, text="Generar", command=command,)    
        button.grid(row=self.row,column=0, sticky='w')        
        label.grid(row=self.row,column=1, sticky='w')






class InputOutputFrame(tk.Frame):
    
    def __init__ (
            self, 
            parent, 
            command = lambda:print("Hello Command"), 
            title="Load File", 
            button_params = [], 
            pady = 3
            ):
        
        super().__init__(parent,pady=pady,padx=3,bd=3,relief="groove")
        self.command = command
        self.row = 0
        self.pack(pady=5)
        self.insert_title(title + "   ")
        self.frame_grid = tk.Frame(self)
        self.frame_grid.pack()
        for param in button_params:
            self.insert_button(param["label"],param["stringvar"],typ=param["type"],field=param['field'])
            self.output_button()
            self.row += 1
 
    def insert_title(self, title):
        label_title = tk.Label(self, text = title, font='Helvetica 10 bold', pady=4,padx=4,bd=3, relief="ridge")
        label_title.pack(pady=3,padx=3)
 
    def insert_button (self, label, stringvar, typ = "file", field="cotas-pr"):
        text_area = tk.Text(self.frame_grid, wrap="word", state="disabled",height=1)
        stringvar.trace_add("write", lambda var_name, index, operation : update_text_from_stringvar(text_area,stringvar,var_name, index, operation))        
        if typ == "file":
            button    = tk.Button(self.frame_grid, text="Cargar", command=lambda:self.load_file_command(stringvar,field))
        elif typ == "dir":
            button    = tk.Button(self.frame_grid, text="Cargar", command=lambda:self.load_dir_command(stringvar,field))
        
        del_button    = tk.Button(self.frame_grid,  text="borrar", command= lambda : ax_com.delete_load_file(field,stringvar))


        #label     = tk.Label(self.frame_grid,   text=label, font='Helvetica 10 italic', width=35, anchor="w")
        label     = tk.Label(self.frame_grid,   text=label)


        button.grid(row=self.row,column = 0)
        del_button.grid(row=self.row, column=1)
        text_area.grid(row=self.row,column=2, padx=13)
        label.grid(row=self.row,column=3)


        # bind the stringvar to the command
        # Initial state
        stringvar.set(config.read_loaded_files(field))
    
    def load_file_command(self,stringvar,field) :
        path = filedialog.askopenfilename(
            title="Seleccione archivo",
            filetypes=(("Text files", "*.csv *.txt *.CSV *.TXT *.xlsx"), ("All files", "*.*"))
        )
        config.write_loaded_files(field,path)
        stringvar.set(path)


    def output_button (self):
        button = tk.Button(self.frame_grid, text="EJECUTAR", command=self.command)
        button.grid(row=self.row,column = 4)

        


 
    

class LoadFileFrame(tk.Frame):
    
    def __init__ (self, parent, title="Load File", button_params = [], pady = 3):
        super().__init__(parent,pady=pady,padx=3,bd=3,relief="groove")
        self.row = 0
        self.pack(pady=5)
        self.insert_title(title)
        self.frame_grid = tk.Frame(self)
        self.frame_grid.pack()
        for param in button_params:
            self.insert_button(param["label"],param["stringvar"],typ=param["type"],field=param['field'])
            self.row += 1
 
    def insert_title(self, title):
        label_title = tk.Label(self, text = title,font='Helvetica 10 bold', pady=4,padx=4,bd=3, relief="ridge")
        label_title.pack(pady=3,padx=3)
 
    def insert_button (self, label, stringvar, typ = "file", field="cotas-pr"):
        text_area = tk.Text(self.frame_grid, wrap="word", state="disabled",height=1)
        stringvar.trace_add("write", lambda var_name, index, operation : update_text_from_stringvar(text_area,stringvar,var_name, index, operation))        
        if typ == "file":
            button    = tk.Button(self.frame_grid, text="Cargar", command=lambda:self.load_file_command(stringvar,field))
        elif typ == "dir":
            button    = tk.Button(self.frame_grid, text="Cargar", command=lambda:self.load_dir_command(stringvar,field))
        
        del_button    = tk.Button(self.frame_grid,  text="borrar", command= lambda : ax_com.delete_load_file(field,stringvar))
        label     = tk.Label(self.frame_grid,   text=label, font='Helvetica 10 italic', width=35, anchor="w")
        button.grid(row=self.row,column = 0)
        del_button.grid(row=self.row, column=1)
        text_area.grid(row=self.row,column=2, padx=13)
        label.grid(row=self.row,column=3)
        
        # bind the stringvar to the command
        # Initial state
        stringvar.set(config.read_loaded_files(field))
    
    def load_file_command(self,stringvar,field) :
        path = filedialog.askopenfilename(
            title="Seleccione archivo",
            filetypes=(("Text files", "*.csv *.txt *.CSV *.TXT *.xlsx"), ("All files", "*.*"))
        )
        config.write_loaded_files(field,path)
        stringvar.set(path)
 
    def load_dir_command(self,stringvar,field) :
        path = filedialog.askdirectory(title="Seleccionar Directorio")
        config.write_loaded_files(field,path)
        stringvar.set(path)


class InputFrame(tk.Frame):
    
    def __init__ (self, parent , title="Input Frame", entry_params = [], command=lambda x:print("HELLO WORLD"),side="top",button=True):
        
        super().__init__(parent,pady=3,padx=3,bd=3,relief="groove")
        self.row = 0
        self.pack(side=side,pady=5, padx=20)
        self.insert_title(title)
        self.inputs = []
        self.frame_grid = tk.Frame(self)
        self.frame_grid.pack()
        
        for param in entry_params:
            self.inputs.append(self.insert_entry(param["label"],param["var"]))
            self.row += 1
        if button:
            self.insert_button(command=command) 
 
    def insert_entry(self,label,var):
        
        entry_box   = tk.Entry(self.frame_grid, textvariable = var)
        entry_label = tk.Label(self.frame_grid, text = label, width=23, anchor="w")
        
        entry_box.grid(row=self.row,column = 0)
        entry_label.grid(row=self.row,column=1)
        return entry_box
    
    def insert_title(self, title):
        label_title = tk.Label(self, text = title, font='Helvetica 10 bold', pady=4,padx=4,bd=3, relief="ridge")
        label_title.pack(pady=3,padx=3)
 
 
    def insert_button(self,command,text="Generar"):
        
        button = tk.Button(self, text=text, command=command, pady=5)
        button.pack()
        
    
    def get_input(self,i):
        return self.inputs[i]




class ScrollableFrame(tk.Frame):

    # Container would be tab 7
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        # Create a canvas
        self.canvas = tk.Canvas(self)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Add a scrollbar to the canvas
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        
        # Configure canvas to work with the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Create a frame inside the canvas
        self.inner_frame = tk.Frame(self.canvas)
        self.inner_frame.bind("<Configure>", self._on_frame_configure)
        
        # Add the frame to the canvas
        #self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
    
    def _on_frame_configure(self, event):
        """Adjust the scroll region to fit the inner frame."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def get_inner_frame (self) :
        return self.inner_frame


# # Create the scrollable frame
# scrollable_frame = ScrollableFrame(root)
# scrollable_frame.pack(fill="both", expand=True)





