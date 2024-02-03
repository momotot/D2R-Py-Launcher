import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, font
from datetime import datetime, timedelta

import Client_launcher
import Utils.Reader as Reader
import Utils.Gametime as Gametime
import Utils.Console as Console
import Utils.Help_window as Help_window
import Utils.Settings_window as Settings_window
import Utils.Terror_zone as Terror_zone
import Utils.Battle_order as Battle_order
import Overlays.Overlay_gametime as Overlay_gametime
import Overlays.Overlay_pattern as Overlay_pattern

class Launcher:
    def __init__(self, root):
        self._root = root
        self.client_check = False
        self._console = None
        self._client_obj = None
        self._reader = None
        self._overlay_gametime_obj = None
        self._overlay_pattern_info = None
        self._terror_zone_obj = None
        self._settings_window = None
        self.game_tracker = None
        self.image_bool = False

        self.initiate_app()
        self.decorate_app()
        self.initiate_console()
        self.initiate_settings()
        self.initiate_terror_zone()
        self.initiate_game_tracker()
        self._folder_path = os.path.dirname(os.path.abspath(__file__))
    
    def initiate_app(self):
        """Initiates several parameters of the app"""
        self._root.title("D2R-Py-Launcher 1.1.1")
        self._root.resizable(0,0)
        self._root.configure(bg="black")
        self._root.protocol("WM_DELETE_WINDOW", self.exit_app)
        self.displayed_path = tk.StringVar()
        self.displayed_path.set("Browse D2R")
        self.terror_zone_current = tk.StringVar()
        self.terror_zone_current.set("Current")
        self.terror_zone_next = tk.StringVar()
        self.terror_zone_next.set("Next")
        self.count_down = tk.StringVar()
        self.count_down.set("")
        self.path = tk.StringVar()
        self.path.set("Browse")
        self.client_amount = tk.StringVar()
        self.client_amount.set("")

        # set the app in the middle of the screen
        screen_width = self._root.winfo_screenwidth()
        screen_height = self._root.winfo_screenheight()
        x_coordinate = (screen_width - self._root.winfo_reqwidth()) // 2
        y_coordinate = (screen_height - self._root.winfo_reqheight()) // 2
        self._root.geometry(f"{self._root.winfo_reqwidth()+250}x{self._root.winfo_reqheight()+325}+{x_coordinate-200}+{y_coordinate-200}")
    
    def decorate_app(self):
        """Mostly creation and packing of buttons and menubar"""
        small_font = font.Font(family="Helvetica", size=8)

        self._displayed_path_label = tk.Label(self._root, textvariable=self.displayed_path, bg="black", width=25)
        self._displayed_path_label.grid(row=0, column=0, pady=5, columnspan=3, sticky="ew")

        self._browse_path = tk.Label(self._root, textvariable=self.displayed_path, bg="black", fg="white", width=25)
        self._browse_path.grid_forget()
    
        self._browse_button = tk.Button(self._root, text="Browse .exe", command=self.update_path, bg="grey", width=25)
        self._browse_button.grid(row=1, column=0, pady=5, padx=5, sticky="ew")

        self._info_field = tk.Label(self._root, text="Enter clients below", justify="center", bg="black", fg="white", width=25)
        self._info_field.grid(row=1, column=1, pady=5, padx=5, sticky="ew")

        self._submit_clients = tk.Button(self._root, text="Launch D2R", command=lambda: threading.Thread(target=self.process_clients).start(), bg="grey", width=25)
        self._submit_clients.grid(row=2, column=0, pady=5, padx=5, sticky="ew")

        self._clients = tk.Entry(self._root, textvariable=self.client_amount, justify="center", width=10)
        self._clients.grid(row=2, column=1, pady=5, padx=5, sticky="ew")

        self._console_button = tk.Button(self._root, text="Toggle console", command=self.toggle_console, bg="grey", width=25)
        self._console_button.grid(row=4, column=0, pady=5, padx=5, sticky="ew")

        self._next_game = tk.Button(self._root, text="Join game", command=lambda: threading.Thread(target=self.join_game).start(), bg="grey", width=25)
        self._next_game.grid(row=4, column=1, pady=5, padx=5, sticky="ew")

        self._legacy_button = tk.Button(self._root, text="Legacy", command=lambda: threading.Thread(target=self.legacy_settings).start(), bg="grey", width=25)
        self._legacy_button.grid(row=5, column=0, pady=5, padx=5, sticky="ew")

        self._resize_button = tk.Button(self._root, text="Re-size", command=lambda: threading.Thread(target=self.resize).start(), bg="grey", width=25)
        self._resize_button.grid(row=5, column=1, pady=5, padx=5, sticky="ew")

        self._exit_button = tk.Button(self._root, text="Terminate PID", command=self.exit_diablo, bg="grey", width=25)
        self._exit_button.grid(row=6, column=0, pady=5, padx=5, sticky="ew")

        self._memory_button = tk.Button(self._root, text="Reader", command=lambda: threading.Thread(target=self.read_stats).start(), bg="grey", width=25)
        self._memory_button.grid(row=6, column=1, pady=5, padx=5, sticky="ew")

        self._area_button = tk.Button(self._root, text="Scan area", command=lambda: threading.Thread(target=self.area_func).start(), bg="grey", width=25)
        self._area_button.grid(row=7, column=0, pady=5, padx=5, sticky="ew")

        self._reset_reader_button = tk.Button(self._root, text="Remove reader", command=self.remove_reader, bg="grey", width=25)
        self._reset_reader_button.grid(row=7, column=1, pady=5, padx=5, sticky="ew")

        self._bo_button = tk.Button(self._root, text="BO", command=lambda: threading.Thread(target=self.go_bo).start(), bg="grey", width=25)
        self._bo_button.grid(row=8, column=0, pady=5, padx=5, sticky="ew")

        self._terror_zone_field = tk.Label(self._root, text="Current TZ:", bg="black", fg="white", width=25)
        self._terror_zone_field.grid(row=9, column=0, pady=5, columnspan=3, sticky="ew")

        self._displayed_terror_zone = tk.Label(self._root, textvariable=self.terror_zone_current, bg="black", font=small_font, width=25)
        self._displayed_terror_zone.grid(row=10, column=0, pady=5, columnspan=3, sticky="ew")

        self._terror_zone_field_next = tk.Label(self._root, text="Next TZ:", bg="black", fg="white", width=25)
        self._terror_zone_field_next.grid(row=11, column=0, pady=5, columnspan=3, sticky="ew")

        self._displayed_terror_zone_next = tk.Label(self._root, textvariable=self.terror_zone_next, bg="black", font=small_font, width=25)
        self._displayed_terror_zone_next.grid(row=12, column=0, pady=5, columnspan=3, sticky="ew")

        self._count_down_tz = tk.Label(self._root, textvariable=self.count_down, bg="black", font=small_font, width=25)
        self._count_down_tz.grid(row=13, column=0, pady=5, columnspan=3, sticky="ew")
        
        # menu bar stuff
        self._menubar = tk.Menu(self._root)
        self._root.config(menu=self._menubar)
        self._file_menu = tk.Menu(self._menubar, tearoff=0)
        self._menubar.add_cascade(label="File", menu=self._file_menu)
        self._file_menu.add_command(label="Restart", command=self.restart_app)
        self._file_menu.add_command(label="Help", command=self.show_help)
        self._file_menu.add_command(label="Exit", command=self.exit_app)

        self._settings_menu = tk.Menu(self._menubar, tearoff=0)
        self._menubar.add_cascade(label="Settings", menu=self._settings_menu)
        self._settings_menu.add_command(label="Open Settings", command=self.open_settings_window)
    
    def open_settings_window(self):
        """Creation of the settings window"""
        self._settings_window.show_settings()

    def toggle_console(self):
        """Function to show/hide the console window - will never stop running while app is running"""
        if self._console._console.state() == "withdrawn":
            self._console.show_console()
            self._console.log_message("Displaying console window", 1)
        else:
            self._console.hide_console()
            self._console.log_message("Hiding console window", 1)

    def initiate_settings(self):
        """Initializing the settings object"""
        self._settings_window = Settings_window.SettingsWindow(self._root, self._console)
        self._console.log_message("Settings object created", 1)

    def initiate_console(self):
        """Initializing the console object"""
        self._console = Console.Console(self._root)
        self._console.log_message("Console window created", 1)

    def initiate_terror_zone(self):
        """Initializing the terror zone tracker object"""
        self._terror_zone_obj = Terror_zone.TerrorZones(self._root, self, self._console)
        self._console.log_message("Terror zone object created", 1)
        self._root.after(0, self.update_countdown)
    
    def initiate_game_tracker(self):
        """Initializing the game time tracker object"""
        self.game_tracker = Gametime.GameTimeTracker()
        self._console.log_message("Game tracker created", 1)
    
    def update_terror_zone_label(self, zone_list):
        """Updates the terror zone label"""
        zone_list = zone_list.split("-")
        current_tz = zone_list[0]
        next_tz = zone_list[1]

        self.terror_zone_current.set(current_tz)
        self.terror_zone_next.set(next_tz)
        self._displayed_terror_zone.config(fg="red")
        self._displayed_terror_zone_next.config(fg="red")

    def restart_app(self):
        """Restart function of the app"""
        user_response = messagebox.askquestion("Restart", "Are you sure you want to restart?")

        if user_response == "yes":
            python = sys.executable
            os.execl(python, python, *sys.argv)

    def show_help(self):
        """Initializing the help object"""
        self.help_window = Help_window.Help(self._root, self._console)
        self._console.log_message("Help window launched", 1)
    
    def remove_reader(self):
        """Calling the removal of reader and overlay objects"""
        if self._reader:
            self.destroy_objects()
        else:
            self._console.log_message("No reader object exists", 3)

    def exit_app(self):
        """Exits the app"""
        user_response = messagebox.askquestion("Exit", "Are you sure you want to exit?")

        if user_response == "yes":
            self._root.destroy()

    def exit_diablo(self):
        """Function the runs when client object is created and the Terminate button is pressed"""
        if self.client_check:
            if len(self._client_obj.window_names) == 0:
                self._console.log_message("No window(s) opened", 2)
                return
            else:
                self._client_obj.checkbox()
        else:
            self._console.log_message("You must launch the game first", 3)

    def legacy_settings(self):
        """Calls the change to legacy settings when the Legacy button is pressed"""
        if self.client_check:
            self._client_obj.change_to_legacy()
        else:
            self._console.log_message("You must launch the game first", 3)

    def resize(self):
        """Calls re-size of the windows when the re-size button is pressed"""
        if self.client_check:
            self._client_obj.resize_window_game()
        else:
            self._console.log_message("You must launch the game first", 3)

    def process_clients(self):
        """When the Launch D2R button is pressed it will create the client object if not already existing"""
        if self.client_amount == "" or not "D2R" in self.path.get():
            self._console.log_message("Invalid path for D2R", 2)
            return  
        entered_value = self.client_amount.get()
        try:
            clients = int(entered_value)
            if 0 < clients < 9:
                try:
                    self._console.log_message(f"Launching {clients} client", 1)
                    if self._client_obj is not None:
                        self._client_obj.clients = self.client_amount.get()
                        self._client_obj.parse_config_and_launch()
                        self._client_obj.change_window_title()
                    else:
                        self._client_obj = Client_launcher.Client(self._root, self.client_amount.get(), self._folder_path, self.path.get(), self._console)
                        self.client_amount.set("")
                    if self._client_obj is not None:
                        self.client_check = True
                except:
                    self._console.log_message("Failed to launch client", 3)
            else:
                self._console.log_message("Only 1-8 clients allowed", 2)
        except ValueError:
            self._console.log_message(f"Value error input", 3)
        except:
            self._console.log_message("Other error input", 3)
    
    def update_path(self):
        """Function to browse the D2R.exe when the Browse button is pressed"""
        self._console.log_message("Browsing D2R path", 1)
        path = filedialog.askopenfilename(title="Select D2R.exe")
        if path.lower().endswith("d2r.exe"):
            self.displayed_path.set("Valid D2R Path")
            self._displayed_path_label.config(fg="green")
            self._console.log_message("Valid D2R path set", 1)
        else:
            if path == "":
                self.displayed_path.set("Choose a valid path")
                self._displayed_path_label.config(fg="yellow")
                self._console.log_message("Empty D2R path choice", 2)
            else:
                self.displayed_path.set("Invalid D2R path")
                self._displayed_path_label.config(fg="red")
                self._console.log_message("Invalid D2R path", 2)
        self.path.set(path)
    
    def join_game(self):
        """When the join game button is pressed, this function gets executed if there is an active client object. Uses packet reading and types gamename/pw or friend list clicks depending on settings"""
        if self.client_check:
            current_settings = self._settings_window.get_settings() if self._settings_window else {}
            if current_settings.get("Friend join option", False):
                self._client_obj.join_game_friends()
            elif current_settings.get("Next game join option", False):
                self._client_obj.join_game_reader()
            else:
                self._client_obj.join_game_friends()
        else:
            self._console.log_message("You must launch the game first", 3)
    
    def read_stats(self):
        """When reader is pressed the function creates the overlay and initialize the reader object"""
        if self.client_check:
            if self._reader is None:
                for name, _ in self._client_obj.process_info.items():
                    if "[MAIN]" in name:
                        self._overlay_gametime_obj = Overlay_gametime.OverlayGameTime(self._root, self._console, self._client_obj, self.game_tracker, self._settings_window)
                        self._reader = Reader.MemoryReader(self, self._console, self._client_obj, self.game_tracker, self._overlay_gametime_obj)
                        self._reader.check_in_game_status()
                        break
                else:
                    self._console.log_message("Main char not loaded", 2)
            else:
                self._console.log_message("Reader already initiated", 2)
        else:
            self._console.log_message("You must launch the game first", 3)

    def area_func(self):
        """Initialization of the overlay and image tracker objects (image inside of overlay class)"""
        if self.client_check:
            if self._overlay_pattern_info is None and not self.image_bool:
                for name, _ in self._client_obj.process_info.items():
                    if "[MAIN]" in name:
                        choosen_name = name
                        self._console.log_message(f"Scanning game for {choosen_name}", 1)
                        self.image_bool = True
                        self._overlay_pattern_info = Overlay_pattern.OverlayPatternInfo(self._root, self._console, self._client_obj, self.game_tracker, choosen_name)
                        break
                else:
                    self._console.log_message("Main char not loaded", 2)
            else:
                self._console.log_message("Overlay already initiated", 2)
        else:
            self._console.log_message("You must launch the game first", 3)              

    def destroy_objects(self):
        """Removing the reader and overlay object and resets"""
        if self._overlay_pattern_info is not None:
            self._overlay_pattern_info.remove_label()
            self._overlay_pattern_info = None
            self.image_bool = False
        if self._reader is not None:
            self._reader.stop_event.set()
            self._reader = None
        if self._overlay_gametime_obj is not None:
            self._overlay_gametime_obj.remove_label()
            self._overlay_gametime_obj = None
        self._console.log_message("Destroyed overlay and reader objects", 1)
    
    def set_settings(self, settings):
        """Setter function for settings"""
        self._settings = settings
    
    def get_settings(self):
        """Getter function for settings"""
        return self._settings if hasattr(self, '_settings') else None

    def countdown_to_next(self):
        """Continuously updates the countdown to next hour = next tz"""
        current_time = datetime.now()
        next_hour = (current_time + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)

        remaining_time = next_hour - current_time
        minutes, seconds = divmod(remaining_time.seconds, 60)
        formatted_time_str = f"{minutes:02}:{seconds:02}"

        self.count_down.set(formatted_time_str)
        self._count_down_tz.config(fg="red")
        current_time = datetime.now()

    def update_countdown(self):
        """Start of countdown thread"""
        self.countdown_to_next()
        self._root.after(1000, self.update_countdown)

    def go_bo(self):
        """Initiates the Battle Order function"""
        if self.client_check:
            try:
                warcry_keys = []
                if self._settings_window:
                    warcry_keys = self._settings_window.get_settings().get("WarcriesKeys", [])
                legacy_setting = self._client_obj.get_legacy_status()
                bo_obj = Battle_order.BattleOrder(self._console, self._client_obj, legacy_setting)
                for name in self._client_obj.window_names:
                    if "BO" in name:
                        position = self._client_obj.get_window_position(name)
                        bo_obj.bo_action(position, name, warcry_keys)
                        break               
            except:
                self._console.log_message(f"Error in go_bo", 3)
        else:
            self._console.log_message("You must launch the game first", 3)

if __name__ == "__main__":
    """THE MAIN LOOP"""
    root = tk.Tk()
    app = Launcher(root)
    root.mainloop()  