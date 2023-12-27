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
    
    # The text that is displayed inside the help window
    def info_text(self):
        return "1. Choose D2R.exe path\n2. Enter how many clients you want to launch\n3. Press Launch button and wait until done\n\
4. Go into game with your main char\n5. Go to the lobby with leechers and join a random game\n6. Re-size for the next game to work properly\n\
7. You can use legacy settings (recommanded) via the Legacy button\n8. Press Next button to join your main char\n9. Enjoy!"

    # Close function of the help window
    def close_help_window(self):
        self.console.log_message("Help window closed", 1)
        self.help_window.destroy()

    # Centralizes the window upon launch
    def center_help_window(self):
        screenWidth = self.help_window.winfo_screenwidth()
        screenHeight = self.help_window.winfo_screenheight()
        x_coordinate = (screenWidth - self.help_window.winfo_reqwidth()) // 2
        y_coordinate = (screenHeight - self.help_window.winfo_reqheight()) // 2
        self.help_window.geometry(f"{400}x{400}+{x_coordinate}+{y_coordinate}")