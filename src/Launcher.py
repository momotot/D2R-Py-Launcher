import os
import Client_launcher
import tkinter as tk
from tkinter import filedialog
import threading
import Utils.Reader as Reader
import Utils.Gametime as Gametime
import Utils.Console as Console
import Utils.Help_window as Help_window
import Utils.Image_reader as Image_reader
import Overlays.Overlay_gametime as Overlay_gametime
import Overlays.Overlay_pattern as Overlay_pattern

class Launcher:
    def __init__(self, root):
        self._root = root
        self.client_check = False
        self._client_obj = None
        self._reader = None
        self._overlay_gametime_obj = None
        self.game_tracker = None
        self._image_scanner = None
        self.image_bool = False

        self.initiate_app()
        self.decorate_app()
        self.initiate_console()
        self.initiate_game_tracker()
        self._folder_path = os.path.dirname(os.path.abspath(__file__))
    
    # Initiates several parameters of the app
    def initiate_app(self):
        self._root.title("D2R-Py-Launcher 1.1.0")
        self._root.resizable(0,0)
        self._root.configure(bg="black")
        self.displayed_path = tk.StringVar()
        self.displayed_path.set("Browse D2R")
        self.path = tk.StringVar()
        self.path.set("Browse")
        self.client_amount = tk.StringVar()
        self.client_amount.set("")

        # set the app in the middle of the screen
        screen_width = self._root.winfo_screenwidth()
        screen_height = self._root.winfo_screenheight()
        x_coordinate = (screen_width - self._root.winfo_reqwidth()) // 2
        y_coordinate = (screen_height - self._root.winfo_reqheight()) // 2
        self._root.geometry(f"{self._root.winfo_reqwidth()+200}x{self._root.winfo_reqheight()+140}+{x_coordinate-200}+{y_coordinate-200}")
    
    # Mostly creation and packing of buttons and menubar
    def decorate_app(self):
        # buttons and fields for functions
        self._root.grid_rowconfigure(3, minsize=20)

        self._displayed_path_label = tk.Label(self._root, textvariable=self.displayed_path, bg="black", width=20)
        self._displayed_path_label.grid(row=0, column=0, pady=5, columnspan=3, sticky="ew")

        self._browse_path = tk.Label(self._root, textvariable=self.displayed_path, bg="black", fg="white", width=20)
        self._browse_path.grid_forget()
    
        self._browse_button = tk.Button(self._root, text="Browse .exe", command=self.update_path, bg="grey", width=20)
        self._browse_button.grid(row=1, column=0, pady=5, padx=5, sticky="ew")

        self._info_field = tk.Label(self._root, text="Enter clients below", justify="center", width=20, bg="black", fg="white")
        self._info_field.grid(row=1, column=1, pady=5, padx=5, sticky="ew")

        self._clients = tk.Entry(self._root, textvariable=self.client_amount, justify="center", width=10)
        self._clients.grid(row=2, column=1, pady=5, padx=5, sticky="ew")

        self._submit_clients = tk.Button(self._root, text="Launch D2R", command=lambda: threading.Thread(target=self.process_clients).start(), bg="grey", width=20)
        self._submit_clients.grid(row=2, column=0, pady=5, padx=5, sticky="ew")

        self._next_game = tk.Button(self._root, text="Next game", command=lambda: threading.Thread(target=self.join_game).start(), bg="grey", width=20)
        self._next_game.grid(row=4, column=1, pady=5, padx=5, sticky="ew")

        self._legacy_button = tk.Button(self._root, text="Legacy settings", command=lambda: threading.Thread(target=self.legacy_settings).start(), bg="grey", width=20)
        self._legacy_button.grid(row=5, column=0, pady=5, padx=5, sticky="ew")

        self._resize_button = tk.Button(self._root, text="Re-size", command=lambda: threading.Thread(target=self.resize).start(), bg="grey", width=20)
        self._resize_button.grid(row=5, column=1, pady=5, padx=5, sticky="ew")

        self._console_button = tk.Button(self._root, text="Toggle console", command=self.toggle_console, bg="grey", width=20)
        self._console_button.grid(row=4, column=0, pady=5, padx=5, sticky="ew")

        self._memory_button = tk.Button(self._root, text="Game time", command=lambda: threading.Thread(target=self.read_stats).start(), bg="grey", width=20)
        self._memory_button.grid(row=6, column=1, pady=5, padx=5, sticky="ew")

        self._reset_reader_button = tk.Button(self._root, text="Remove game time", command=self.remove_reader, bg="grey", width=20)
        self._reset_reader_button.grid(row=7, column=1, pady=5, padx=5, sticky="ew")

        self._area_button = tk.Button(self._root, text="Area", command=lambda: threading.Thread(target=self.area_func).start(), bg="grey", width=20)
        self._area_button.grid(row=7, column=0, pady=5, padx=5, sticky="ew")

        self._exit_button = tk.Button(self._root, text="Terminate PID", command=self.exit_diablo, bg="grey", width=20)
        self._exit_button.grid(row=6, column=0, pady=5, padx=5, sticky="ew")

        # menu bar stuff
        self._menubar = tk.Menu(self._root)
        self._root.config(menu=self._menubar)
        self._file_menu = tk.Menu(self._menubar, tearoff=0)
        self._menubar.add_cascade(label="File", menu=self._file_menu)
        self._file_menu.add_command(label="Help", command=self.show_help)
        self._file_menu.add_command(label="Exit", command=self.exit_app)

    # Function to show/hide the console window - will never stop running while app is running
    def toggle_console(self):
        if self.console._console.state() == "withdrawn":
            self.console.show_console()
            self.console.log_message("Displaying console window", 1)
        else:
            self.console.hide_console()
            self.console.log_message("Hiding console window", 1)

    # Initializing the console object
    def initiate_console(self):
        self.console = Console.Console(self._root)
        self.console.log_message("Console window created", 1)
    
    def initiate_game_tracker(self):
        self.game_tracker = Gametime.GameTimeTracker()
        self.console.log_message("Game tracker created", 1)
    
    # Initializing the help object
    def show_help(self):
        self.help_window = Help_window.Help(self._root, self.console)
        self.console.log_message("Help window launched", 1)
    
    # Calling the removal of reader and overlay objects
    def remove_reader(self):
        if self._reader:
            self.destroy_objects()
        else:
            self.console.log_message("No reader object exists", 3)

    # Exits the app
    def exit_app(self):
        self.root.destroy()

    # Function the runs when client object is created and the Terminate button is pressed 
    def exit_diablo(self):
        if self.client_check:
            if len(self._client_obj.window_names) == 0:
                self.console.log_message("No window(s) opened", 2)
                return
            else:
                self._client_obj.checkbox()
        else:
            self.console.log_message("You must launch the game first", 3)

    # Calls the change to legacy settings when the Legacy button is pressed
    def legacy_settings(self):
        if self.client_check:
            self._client_obj.change_to_legacy()
        else:
            self.console.log_message("You must launch the game first", 3)

    # Calls re-size of the windows when the Re-size button is pressed
    def resize(self):
        if self.client_check:
            self._client_obj.resize_window_game()
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
                    if self._client_obj is not None:
                        self._client_obj.clients = self.client_amount.get()
                        self._client_obj.parse_config_and_launch()
                        self._client_obj.change_window_title()
                    else:
                        self._client_obj = Client_launcher.Client(self._root, self.client_amount.get(), self._folder_path, self.path.get(), self.console)
                        self.client_amount.set("")
                    if self._client_obj is not None:
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
            self._displayed_path_label.config(fg="green")
            self.console.log_message("Valid D2R path set", 1)
        else:
            if path == "":
                self.displayed_path.set("Choose a valid path")
                self._displayed_path_label.config(fg="yellow")
                self.console.log_message("Empty D2R path choice", 2)
            else:
                self.displayed_path.set("Invalid D2R path")
                self._displayed_path_label.config(fg="red")
                self.console.log_message("Invalid D2R path", 2)
        self.path.set(path)
    
    # When next game button is pressed this function gets executed if there is an active client object
    def join_game(self):
        if self.client_check:
            self._client_obj.join_game()
        else:
            self.console.log_message("You must launch the game first", 3)
    
    # When game time is pressed the function creates the overlay and initialize the reader object
    def read_stats(self):
        if self.client_check:
            if self._reader is None:
                for name, _ in self._client_obj.process_info.items():
                    if "[MAIN]" in name:
                        self._overlay_gametime_obj = Overlay_gametime.OverlayGameTime(self._root, self.console, self._client_obj, self.game_tracker)
                        self._reader = Reader.MemoryReader(self, self.console, self._client_obj, self.game_tracker, self._overlay_gametime_obj)
                        self._reader.check_in_game_status()
                        break
                else:
                    self.console.log_message("Main char not loaded", 2)
            else:
                self.console.log_message("Reader already initiated", 2)
        else:
            self.console.log_message("You must launch the game first", 3)

    def area_func(self):
        if self.client_check:
            if self._image_scanner is None and not self.image_bool:
                for name, _ in self._client_obj.process_info.items():
                    if "[MAIN]" in name:
                        choosen_name = name
                        self.console.log_message(f"Scanning game for {choosen_name}", 1)
                        self.image_bool = True
                        self._overlay_pattern_info = Overlay_pattern.OverlayPatternInfo(self._root, self.console, self._client_obj, self.game_tracker, choosen_name)
                        break
            else:
                self.console.log_message("Image scanner already loaded", 2)
        else:
            self.console.log_message("You must launch the game first", 3)              

    # removing the reader and overlay object and resets
    def destroy_objects(self):
        self._reader.stop_event.set()
        self._overlay_gametime_obj.remove_label()
        self._reader = None
        self._overlay_gametime_obj = None
        self.console.log_message("Destroyed overlay and reader object", 1)

# MAIN LOOP
if __name__ == "__main__":
    root = tk.Tk()
    app = Launcher(root)
    root.mainloop()  