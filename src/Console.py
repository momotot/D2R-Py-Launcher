import tkinter as tk
import datetime
from tkinter import scrolledtext
from platform import system, machine, node

class Console:
    def __init__ (self, parent, level=1):
        self.parent = parent
        self.console = tk.Toplevel(parent)
        self.console.title("Console")
        self.console.resizable(0,0)
        self.console.protocol("WM_DELETE_WINDOW", self.disable_close)
        self.console.configure(bg="black")
        self.text_area = scrolledtext.ScrolledText(self.console, wrap=tk.WORD, width=85, height=60, bg="black", fg="white", borderwidth=0, highlightthickness=0)
        self.text_area.pack(expand=True, fill="both")
        self.text_area.tag_configure("white_tag", foreground="white")
        self.text_area.tag_configure("yellow_tag", foreground="yellow")
        self.text_area.tag_configure("red_tag", foreground="red")

        if level > 0 and level < 4:
            self.log_level = level
        else:
            self.log_level = 1
        
        self.start_log()
        
    # Start log with computer name, system and machine
    def start_log(self):
        start_message = f"{node()} ~ {system()} ~ {machine()}"
        self.log_message(start_message, 1)

    # Getter for log level
    def get_log_level(self, level):
        if level == 1:
            return "INFO"
        elif level == 2:
            return "WARN"
        elif level == 3:
            return "ERROR"

    # Close function
    def close_window(self):
        self.console.destroy()
    
    # Disables the close function so the console window is always running
    def disable_close(self):
        pass
    
    # Function to show the console
    def show_console(self):
        self.console.deiconify()
    
    # Function to hide the console 
    def hide_console(self):
        self.console.withdraw()

    # The log message function. Will log white/yellow/red depending on level
    def log_message(self, message, level):
        time_stamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        message_to_log = f"[{self.get_log_level(level)}] ~ [{time_stamp}] ~ {message}\n"

        if level == 1:
            text_color = "white"
        elif level == 2:
            text_color = "yellow"
        elif level == 3:
            text_color = "red"
        else:
            text_color = "white"

        self.text_area.insert(tk.END, message_to_log, f"{text_color}_tag")
        self.text_area.yview(tk.END)