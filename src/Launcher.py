import os
import Help_window
import Console
import Client_launcher
import tkinter as tk
from tkinter import filedialog
import threading

class Launcher:
    def __init__(self, root):
        self.root = root
        self.client_check = False
        self.client_obj = None
        self.initiate_app()
        self.decorate_app()
        self.initiate_console()
        self.folder_path = os.path.dirname(os.path.abspath(__file__))
    
    # Initiates several parameters of the app
    def initiate_app(self):
        self.root.title("D2R-Py-Launcher 1.0.0")
        self.root.resizable(0,0)
        self.root.configure(bg="black")
        self.displayed_path = tk.StringVar()
        self.displayed_path.set("Browse D2R")
        self.path = tk.StringVar()
        self.path.set("Browse")
        self.client_amount = tk.StringVar()
        self.client_amount.set("")

        # set the app in the middle of the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = (screen_width - self.root.winfo_reqwidth()) // 2
        y_coordinate = (screen_height - self.root.winfo_reqheight()) // 2
        root.geometry(f"{self.root.winfo_reqwidth()+200}x{self.root.winfo_reqheight()+140}+{x_coordinate-200}+{y_coordinate-200}")
    
    # Mostly creation and packing of buttons and menubar
    def decorate_app(self):
        # buttons and fields for functions
        self.root.grid_rowconfigure(3, minsize=20)

        self.displayed_path_label = tk.Label(self.root, textvariable=self.displayed_path, bg="black", width=20)
        self.displayed_path_label.grid(row=0, column=0, pady=5, columnspan=3, sticky="ew")

        browse_path = tk.Label(self.root, textvariable=self.displayed_path, bg="black", fg="white", width=20)
        browse_path.grid_forget()
    
        browse_button = tk.Button(self.root, text="Browse .exe", command=self.update_path, bg="grey", width=20)
        browse_button.grid(row=1, column=0, pady=5, padx=5, sticky="ew")

        info_field = tk.Label(self.root, text="Enter clients below", justify="center", width=20, bg="black", fg="white")
        info_field.grid(row=1, column=1, pady=5, padx=5, sticky="ew")

        clients = tk.Entry(self.root, textvariable=self.client_amount, justify="center", width=10)
        clients.grid(row=2, column=1, pady=5, padx=5, sticky="ew")

        submit_clients = tk.Button(self.root, text="Launch D2R", command=lambda: threading.Thread(target=self.process_clients).start(), bg="grey", width=20)
        submit_clients.grid(row=2, column=0, pady=5, padx=5, sticky="ew")

        next_game = tk.Button(self.root, text="Next game", command=self.join_game, bg="grey", width=20)
        next_game.grid(row=4, column=1, pady=5, padx=5, sticky="ew")

        legacy_button = tk.Button(self.root, text="Legacy settings", command=self.legacy_settings, bg="grey", width=20)
        legacy_button.grid(row=5, column=0, pady=5, padx=5, sticky="ew")

        resize_button = tk.Button(self.root, text="Re-size", command=self.resize, bg="grey", width=20)
        resize_button.grid(row=5, column=1, pady=5, padx=5, sticky="ew")

        console_button = tk.Button(self.root, text="Toggle console", command=self.toggle_console, bg="grey", width=20)
        console_button.grid(row=4, column=0, pady=5, padx=5, sticky="ew")

        exit_button = tk.Button(self.root, text="Terminate PID", command=self.exit_diablo, bg="grey", width=20)
        exit_button.grid(row=6, column=0, pady=5, padx=5, sticky="ew")

        # menu bar stuff
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Help", command=self.show_help)
        file_menu.add_command(label="Exit", command=self.exit_app)

    # Function to show/hide the console window - will never stop running while app is running
    def toggle_console(self):
        if self.console.console.state() == "withdrawn":
            self.console.show_console()
            self.console.log_message("Displaying console window", 1)
        else:
            self.console.hide_console()
            self.console.log_message("Hiding console window", 1)

    # Initializing the console object
    def initiate_console(self):
        self.console = Console.Console(self.root)
        self.console.log_message("Console window created", 1)
    
    # Initializing the help object
    def show_help(self):
        self.help_window = Help_window.Help(self.root, self.console)
        self.console.log_message("Help window launched", 1)

    # Exits the app
    def exit_app(self):
        self.root.destroy()

    # Function the runs when client object is created and the Terminate button is pressed 
    def exit_diablo(self):
        if self.client_check:
            if len(self.client_obj.window_names) == 0:
                self.console.log_message("No window(s) opened", 2)
                return
            else:
                self.client_obj.checkbox()
        else:
            self.console.log_message("You must launch the game first", 3)

    # Calls the change to legacy settings when the Legacy button is pressed
    def legacy_settings(self):
        if self.client_check:
            self.client_obj.change_to_legacy()
        else:
            self.console.log_message("You must launch the game first", 3)

    # Calls re-size of the windows when the Re-size button is pressed
    def resize(self):
        if self.client_check:
            self.client_obj.resize_window_game()
        else:
            self.console.log_message("You must launch the game first", 3)

    # When the Launch D2R button is pressed it will create the client object if not already existing
    def process_clients(self):
        if self.client_amount == "" or not "D2R" in self.path.get():
            self.console.log_message("Invalid path for D2R", 2)
            return  
        entered_value = self.client_amount.get()
        try:
            clients = int(entered_value)
            if 0 < clients < 9:
                try:
                    self.console.log_message(f"Launching {clients} client", 1)
                    if self.client_obj is not None:
                        self.client_obj.clients = self.client_amount.get()
                        self.client_obj.parse_config_and_launch()
                        self.client_obj.change_window_title()
                    else:
                        self.client_obj = Client_launcher.Client(self.root, self.client_amount.get(), self.folder_path, self.path.get(), self.console)
                        self.client_amount.set("")
                    if self.client_obj is not None:
                        self.client_check = True
                except:
                    self.console.log_message("Failed to launch client", 3)
            else:
                self.console.log_message("Only 1-8 clients allowed", 2)
        except ValueError:
            self.console.log_message(f"Value error input", 3)
        except:
            self.console.log_message("Other error input", 3)
    
    # Function to browse the D2R.exe when the Browse button is pressed
    def update_path(self):
        self.console.log_message("Browsing D2R path", 1)
        path = filedialog.askopenfilename(title="Select D2R.exe")
        if path.lower().endswith("d2r.exe"):
            self.displayed_path.set("Valid D2R Path")
            self.displayed_path_label.config(fg="green")
            self.console.log_message("Valid D2R path set", 1)
        else:
            if path == "":
                self.displayed_path.set("Choose a valid path")
                self.displayed_path_label.config(fg="yellow")
                self.console.log_message("Empty D2R path choice", 2)
            else:
                self.displayed_path.set("Invalid D2R path")
                self.displayed_path_label.config(fg="red")
                self.console.log_message("Invalid D2R path", 2)
        self.path.set(path)
    
    # When next game button is pressed this function gets executed if there is an active client object
    def join_game(self):
        if self.client_check:
            self.client_obj.join_game()
        else:
            self.console.log_message("You must launch the game first", 3)

# MAIN LOOP
if __name__ == "__main__":
    root = tk.Tk()
    app = Launcher(root)
    root.mainloop()