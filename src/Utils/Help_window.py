import tkinter as tk
from tkinter import scrolledtext

class Help:
    def __init__(self, parent, console):
        self.parent = parent
        self.console = console
        self.help_window = tk.Toplevel(self.parent)
        self.help_window.resizable(0, 0)
        self.help_window.title("Help")
        
        text_widget = scrolledtext.ScrolledText(self.help_window, wrap=tk.WORD, width=60, height=20, bg="black", fg="white")
        text_widget.insert(tk.END, self.info_text())
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(expand=True, fill="both")

        self.center_help_window()
        self.help_window.protocol("WM_DELETE_WINDOW", lambda: self.close_help_window())
    
    def info_text(self):
        """The text that is displayed inside the help window"""
        return "1. Choose D2R.exe path\n2. Enter how many clients you want to launch\n3. Press Launch button and wait until done\n\
4. Go into game with your main char\n5. Select in settings your join method\n6. You can use legacy settings (recommended) via the Legacy button\n7. Press Join game to join with leechers\n\
8. You can use the game time button to display in game time and game count\n9. You can use the area button to have known patterns displayed\n\
10. You can use the BO button to use battle orders at river wp\n11.Enjoy!"

    def close_help_window(self):
        """Close function of the help window"""
        self.console.log_message("Help window closed", 1)
        self.help_window.destroy()

    def center_help_window(self):
        """Centralizes the window upon launch"""
        screenWidth = self.help_window.winfo_screenwidth()
        screenHeight = self.help_window.winfo_screenheight()
        x_coordinate = (screenWidth - self.help_window.winfo_reqwidth()) // 2
        y_coordinate = (screenHeight - self.help_window.winfo_reqheight()) // 2
        self.help_window.geometry(f"{400}x{600}+{x_coordinate}+{y_coordinate}")