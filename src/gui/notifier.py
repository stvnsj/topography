import os
import sys
import tkinter as tk

class RedirectToText:
    
    def __init__(self, text_widget):
        self.text_area = text_widget
        self.text_area.tag_config("success", foreground="#33cc33")
        self.text_area.tag_config("error", foreground="#e8121c")
        self.text_area.tag_config("warning", foreground='#ffcc1c')
        #self.text_area.configure(state="normal")
        self.text_area.delete(1.0, tk.END)  # Clear previous output
        #self.text_area.configure(state="disabled")
    
    def write(self, message):
        # Append text to the Text widget
        self.text_area.configure(state="normal")
        self.text_area.insert(tk.END, message)
        self.text_area.see(tk.END)  # Scroll to the end
        
        
        start_index = self.text_area.search(">> Error:", "1.0", tk.END, nocase=True)
        if start_index:
            line_start = f"{start_index} linestart"
            line_end = f"{start_index} lineend"
            self.text_area.tag_add("error", line_start, line_end)
        
        start_index = "1.0"
        while True:
            start_index = self.text_area.search(">> Advertencia:", start_index, tk.END, nocase=True)
            if not start_index:
                break
            end_index = f'{start_index}+{len(">> Advertencia")}c'
            self.text_area.tag_add("warning", start_index, end_index)
            start_index = end_index
        
        start_index = self.text_area.search(">> OPERACION TERMINADA CON EXITO", "1.0", tk.END, nocase=True)
        if start_index:
            line_start = f"{start_index} linestart"
            line_end = f"{start_index} lineend"
            self.text_area.tag_add("success", line_start, line_end)
    
    
    def flush(self):
        pass  # Required for compatibility with Python's stdout


class Notifier:
    
    def __init__ (self,root):
        self.root = root
        self.text_area = None
    
    def open_output_window (self):
        
        new_window = tk.Toplevel(self.root)
        new_window.title("EQC - Reporte")
        new_window.geometry("1100x800")
        
        self.text_area = tk.Text(
            new_window, bg="#202020",
            fg="#eae7d6", wrap="word",
            insertbackground="#ffc90b",
            font=("Courier", 13, "bold")
        )
        
        self.text_area.pack(expand=True, fill="both")
    
    def redirect_stdout (self):
        sys.stdout = RedirectToText(self.text_area)
    
    def redirect_stderr(self):
        sys.stderr = RedirectToText(self.text_area)
    
    def restore_stdout_stderr (self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
