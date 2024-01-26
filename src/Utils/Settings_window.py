import tkinter as tk
from tkinter import ttk
import threading

class SettingsWindow:
    __settings_dict = {
    "Friend join option": True,
    "Next game join option": False
}  
    
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
        self.__friends_join_var = tk.BooleanVar(value=self.__settings_dict["Friend join option"])
        self._friend_join_checkbox = ttk.Checkbutton(self._settings_window, text="Friend list join", variable=self.__friends_join_var, command=self.disable_game_join)
        self._friend_join_checkbox.pack()

        self.__join_next_game_var = tk.BooleanVar(value=self.__settings_dict["Next game join option"])
        self._join_next_game_checkbox = ttk.Checkbutton(self._settings_window, text="Next game lobby",variable=self.__join_next_game_var, command=self.disable_friend_join)
        self._join_next_game_checkbox.pack()

        self._close_button = ttk.Button(self._settings_window, text="Close", command=self.close_settings)
        self._close_button.pack()

    def load_settings(self):
        """Initialization of the checkbox values from the dictionary"""
        join_next_game_value = SettingsWindow.__settings_dict["Next game join option"]
        friends_join_value = SettingsWindow.__settings_dict["Friend join option"]

        if not (join_next_game_value or friends_join_value):
            join_next_game_value = True

        self.__join_next_game_var.set(join_next_game_value)
        self.__friends_join_var.set(friends_join_value)

        if friends_join_value:
            self.disable_game_join()
        elif join_next_game_value:
            self.disable_friend_join()

    def close_settings(self):
        """Updates the value from the checkbox"""
        last_valid_state = any([
            SettingsWindow.__settings_dict["Next game join option"],
            SettingsWindow.__settings_dict["Friend join option"]
        ])

        if last_valid_state:
            SettingsWindow.__settings_dict["Next game join option"] = self.__join_next_game_var.get()
            SettingsWindow.__settings_dict["Friend join option"] = self.__friends_join_var.get()
        else:
            self.__join_next_game_var.set(SettingsWindow.__settings_dict["Next game join option"])
            self.__friends_join_var.set(SettingsWindow.__settings_dict["Friend join option"])

        self._settings_window.destroy()

    def update_settings(self):
        """Continuously checks for updates"""
        def toggle_values():
            SettingsWindow.__settings_dict["Next game join option"] = not SettingsWindow.__settings_dict["Next game join option"]
            SettingsWindow.__settings_dict["Friend join option"] = not SettingsWindow.__settings_dict["Friend join option"]
            self._settings_window.after(1000, toggle_values)
        toggle_values()

    def on_close(self):
        """Close function to update and destroy window"""
        self.close_settings()
        self.update_thread.join()
        self.update_launcher_settings()

    def disable_friend_join(self):
        """Disables friend list join when game join is selected"""
        if self.__join_next_game_var.get():
            self.__friends_join_var.set(False)
            self._friend_join_checkbox["state"] = "disabled"
        else:
            self._friend_join_checkbox["state"] = "normal"

    def disable_game_join(self):
        """Disables game join when friend list join is selected"""
        if self.__friends_join_var.get():
            self.__join_next_game_var.set(False)
            self._join_next_game_checkbox["state"] = "disabled"
        else:
            self._join_next_game_checkbox["state"] = "normal"
    
    def update_launcher_settings(self):
        """Update the launcher settings with the values and destroy after"""
        self._root.set_settings(self.get_settings())
        self._settings_window.destroy()
    
    def get_settings(self):
        """Get current settings from checkboxes"""
        return {
            "Friend join option": self.__friends_join_var.get(),
            "Next game join option": self.__join_next_game_var.get()
        }