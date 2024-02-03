import tkinter as tk
import datetime
from tkinter import scrolledtext
from platform import system, machine, node

class Console:
    def __init__ (self, root, level=1):
        self._console = tk.Toplevel(root)
        self._console.title("Console")
        self._console.protocol("WM_DELETE_WINDOW", self.close_window)
        self._console.configure(bg="black")
        self.text_area = scrolledtext.ScrolledText(self._console, wrap=tk.WORD, width=85, height=40, bg="black", fg="white", borderwidth=0, highlightthickness=0)
        self.text_area.pack(expand=True, fill="both")
        self.text_area.tag_configure("white_tag", foreground="white")
        self.text_area.tag_configure("yellow_tag", foreground="yellow")
        self.text_area.tag_configure("red_tag", foreground="red")

        if level > 0 and level < 4:
            self.log_level = level
        else:
            self.log_level = 1
        
        self.start_log()
        
    def start_log(self):
        """Start log with computer name, system and machine"""
        start_message = f"{node()} ~ {system()} ~ {machine()}"
        self.log_message(start_message, 1)

    def get_log_level(self, level):
        """Getter for log level"""
        if level == 1:
            return "INFO"
        elif level == 2:
            return "WARN"
        elif level == 3:
            return "ERROR"

    def close_window(self):
        """Close function"""
        self._console.withdraw()
        self.log_message("Hiding console window", 1)
    
    def disable_close(self):
        """Disables the close function so the console window is always running"""
        pass
    
    def show_console(self):
        """Function to show the console"""
        self._console.deiconify()
    
    def hide_console(self):
        """Function to hide the console"""
        self._console.withdraw()

    def log_message(self, message, level):
        """The log message function. Will log white/yellow/red depending on level"""
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