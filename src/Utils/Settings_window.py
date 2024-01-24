import tkinter as tk
from tkinter import ttk
import threading

class SettingsWindow:

    __settings_dict = {
    "Toggle console option": True,
    "Next game join option": True,
    "Legacy toggle option": True,
    "Re-size option": True,
    "Terminate PID option": True,
    "Display game time option": True,
    "Pattern info from area option": True}  
    
    def __init__(self, root):
        self._root = root
        self._root.title("Settings")
        self._settings_window = tk.Toplevel(self._root)
        x = self._root.winfo_x()
        y = self._root.winfo_y()
        self._settings_window.geometry(f"400x400+{x}+{y}")
        self._settings_window.configure()
        self._settings_window.resizable(0,0)
        self._settings_window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.create_widgets()
        self.load_settings()

        self.update_thread = threading.Thread(target=self.update_settings)
        self.update_thread.daemon = True
        self.update_thread.start()

    def create_widgets(self):
        """ Creates all checkboxes and buttons"""
        self.__toggle_console_var = tk.BooleanVar(value=self.__settings_dict["Toggle console option"])
        self._toggle_console_checkbox = ttk.Checkbutton(self._settings_window, text="Toggle console option", variable=self.__toggle_console_var)
        self._toggle_console_checkbox.pack()

        self.__join_next_game_var = tk.BooleanVar(value=self.__settings_dict["Next game join option"])
        self._join_next_game_checkbox = ttk.Checkbutton(self._settings_window, text="Next game join option", variable=self.__join_next_game_var)
        self._join_next_game_checkbox.pack()

        self.__legacy_switch_var = tk.BooleanVar(value=self.__settings_dict["Legacy toggle option"])
        self._legacy_switch_checkbox = ttk.Checkbutton(self._settings_window, text="Legacy toggle option", variable=self.__legacy_switch_var)
        self._legacy_switch_checkbox.pack()

        self.__resize_var = tk.BooleanVar(value=self.__settings_dict["Re-size option"])
        self._resize_checkbox = ttk.Checkbutton(self._settings_window, text="Re-size option", variable=self.__resize_var)
        self._resize_checkbox.pack()

        self.__terminate_pid_var = tk.BooleanVar(value=self.__settings_dict["Terminate PID option"])
        self._terminate_pid_checkbox = ttk.Checkbutton(self._settings_window, text="Terminate PID option", variable=self.__terminate_pid_var)
        self._terminate_pid_checkbox.pack()

        self.__display_gametime_var = tk.BooleanVar(value=self.__settings_dict["Display game time option"])
        self._gametime_checkbox = ttk.Checkbutton(self._settings_window, text="Display game time option", variable=self.__display_gametime_var)
        self._gametime_checkbox.pack()

        self.__pattern_area_var = tk.BooleanVar(value=self.__settings_dict["Pattern info from area option"])
        self._area_checkbox = ttk.Checkbutton(self._settings_window, text="Pattern info from area option", variable=self.__pattern_area_var)
        self._area_checkbox.pack()

        self._close_button = ttk.Button(self._settings_window, text="Close", command=self.close_settings)
        self._close_button.pack()

    def load_settings(self):
        """Initialization of the checkbox values from the dictionary"""
        self.__toggle_console_var.set(SettingsWindow.__settings_dict["Toggle console option"])
        self.__join_next_game_var.set(SettingsWindow.__settings_dict["Next game join option"])
        self.__legacy_switch_var.set(SettingsWindow.__settings_dict["Legacy toggle option"])
        self.__resize_var.set(SettingsWindow.__settings_dict["Re-size option"])
        self.__terminate_pid_var.set(SettingsWindow.__settings_dict["Terminate PID option"])
        self.__display_gametime_var.set(SettingsWindow.__settings_dict["Display game time option"])
        self.__pattern_area_var.set(SettingsWindow.__settings_dict["Pattern info from area option"])

    def close_settings(self):
        """Updates the value from the checkbox"""
        SettingsWindow.__settings_dict["Toggle console option"] = self.__toggle_console_var.get()
        SettingsWindow.__settings_dict["Next game join option"] = self.__join_next_game_var.get()
        SettingsWindow.__settings_dict["Legacy toggle option"] = self.__legacy_switch_var.get()
        SettingsWindow.__settings_dict["Re-size option"] = self.__resize_var.get()
        SettingsWindow.__settings_dict["Terminate PID option"] = self.__terminate_pid_var.get()
        SettingsWindow.__settings_dict["Display game time option"] = self.__display_gametime_var.get()
        SettingsWindow.__settings_dict["Pattern info from area option"] = self.__pattern_area_var.get()
        self._settings_window.destroy()

    def update_settings(self):
        """Continuously checks for updates"""
        def toggle_values():
            SettingsWindow.__settings_dict["Toggle console option"] = not SettingsWindow.__settings_dict["Toggle console option"]
            SettingsWindow.__settings_dict["Next game join option"] = not SettingsWindow.__settings_dict["Next game join option"]
            SettingsWindow.__settings_dict["Legacy toggle option"] = not SettingsWindow.__settings_dict["Legacy toggle option"]
            SettingsWindow.__settings_dict["Re-size option"] = not SettingsWindow.__settings_dict["Re-size option"]
            SettingsWindow.__settings_dict["Terminate PID option"] = not SettingsWindow.__settings_dict["Terminate PID option"]
            SettingsWindow.__settings_dict["Display game time option"] = not SettingsWindow.__settings_dict["Display game time option"]
            SettingsWindow.__settings_dict["Pattern info from area option"] = not SettingsWindow.__settings_dict["Pattern info from area option"]
            self._settings_window.after(1000, toggle_values)

    def on_close(self):
        """Close function to update and destroy window"""
        self.close_settings()
        self.update_thread.join()
        self._settings_window.destroy()