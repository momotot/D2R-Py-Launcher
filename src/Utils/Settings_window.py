import tkinter as tk
from tkinter import ttk
import threading

class SettingsWindow:
    __settings_dict = {
    "Friend join option": True,
    "Next game join option": False,
    "WarcriesKeys": ["F1", "F2", "F3"],
    "Game time overlay pos 1": True,
    "Game time overlay pos 2": False
}  
    
    def __init__(self, root, console):
        self._root = root
        self._console = console
        self._settings_window = None
        self.create_window()
        self._settings_window.withdraw()
        self.update_thread = threading.Thread(target=self.update_settings)
        self.update_thread.daemon = True
        self.update_thread.start()

    def create_window(self):
        if self._settings_window is None:
            self._root.title("D2R-Py-Launcher 1.1.1")
            self._settings_window = tk.Toplevel(self._root)
            x = self._root.winfo_x()
            y = self._root.winfo_y()
            self._settings_window.geometry(f"400x400+{x}+{y}")
            self._settings_window.configure()
            self._settings_window.resizable(0,0)
            self._settings_window.protocol("WM_DELETE_WINDOW", self.on_close)

            self.create_widgets()
            self.load_settings()


    def create_widgets(self):
        """ Creates all checkboxes and buttons"""
        self.__friends_join_var = tk.BooleanVar(value=self.__settings_dict["Friend join option"])
        self._friend_join_checkbox = ttk.Checkbutton(self._settings_window, text="Friend list join", variable=self.__friends_join_var, command=self.disable_game_join)
        self._friend_join_checkbox.pack()

        self.__join_next_game_var = tk.BooleanVar(value=self.__settings_dict["Next game join option"])
        self._join_next_game_checkbox = ttk.Checkbutton(self._settings_window, text="Next game lobby",variable=self.__join_next_game_var, command=self.disable_friend_join)
        self._join_next_game_checkbox.pack()

        self.__game_time_one_var = tk.BooleanVar(value=self.__settings_dict["Game time overlay pos 1"])
        self._game_time_one_checkbox = ttk.Checkbutton(self._settings_window, text="Overlay pos left", variable=self.__game_time_one_var, command=self.disable_pos_two)
        self._game_time_one_checkbox.pack()

        self.__game_time_two_var = tk.BooleanVar(value=self.__settings_dict["Game time overlay pos 2"])
        self._game_time_two_checkbox = ttk.Checkbutton(self._settings_window, text="Overlay pos top center", variable=self.__game_time_two_var, command=self.disable_pos_one)
        self._game_time_two_checkbox.pack()

        self.__warcry_keys_label = ttk.Label(self._settings_window, text="Warcry keys:")
        self.__warcry_keys_label.pack()

        self.__warcries_entry = ttk.Entry(self._settings_window, foreground="black")
        self.__warcries_entry.insert(0, ", ".join(SettingsWindow.__settings_dict["WarcriesKeys"]))
        self.__warcries_entry.pack()

        self._close_button = ttk.Button(self._settings_window, text="Close", command=self.close_settings)
        self._close_button.pack()

    def load_settings(self):
        """Initialization of the checkbox values from the dictionary"""
        join_next_game_value = SettingsWindow.__settings_dict["Next game join option"]
        friends_join_value = SettingsWindow.__settings_dict["Friend join option"]
        game_pos_one_value = SettingsWindow.__settings_dict["Game time overlay pos 1"]
        game_pos_two_value = SettingsWindow.__settings_dict["Game time overlay pos 2"]
        warcry_value = SettingsWindow.__settings_dict["WarcriesKeys"]

        if not (join_next_game_value or friends_join_value):
            join_next_game_value = True
        
        if not (game_pos_one_value or game_pos_two_value):
            game_pos_two_value = True

        self.__join_next_game_var.set(join_next_game_value)
        self.__friends_join_var.set(friends_join_value)
        self.__game_time_one_var.set(game_pos_one_value)
        self.__game_time_two_var.set(game_pos_two_value)

        if friends_join_value:
            self.disable_game_join()
        elif join_next_game_value:
            self.disable_friend_join()

        if game_pos_two_value:
            self.disable_pos_one()
        elif game_pos_one_value:
            self.disable_pos_two()

    def validate_warcry_keys(self, keys_input):
        """Validate the format of the warcry keys string"""
        keys = keys_input.split(",")
        return len(keys) == 3 and all(1 <= len(key.strip()) <= 2 for key in keys)
         
    def close_settings(self):
        """Updates the value from the checkboxes"""
        last_valid_state_join = any([
            SettingsWindow.__settings_dict["Next game join option"],
            SettingsWindow.__settings_dict["Friend join option"],
        ])

        last_valid_state_position = any([
            SettingsWindow.__settings_dict["Game time overlay pos 1"],
            SettingsWindow.__settings_dict["Game time overlay pos 2"]
        ])

        last_valid_state_warcry = self.validate_warcry_keys(self.__warcries_entry.get())

        if last_valid_state_warcry:
            SettingsWindow.__settings_dict["WarcriesKeys"] = [key.strip().upper() for key in self.__warcries_entry.get().split(",")]
        else:
            self.__warcries_entry.delete(0, tk.END)
            self.__warcries_entry.insert(0, ", ".join(SettingsWindow.__settings_dict["WarcriesKeys"]))

        if last_valid_state_join:
            SettingsWindow.__settings_dict["Next game join option"] = self.__join_next_game_var.get()
            SettingsWindow.__settings_dict["Friend join option"] = self.__friends_join_var.get()
        else:
            self.__join_next_game_var.set(SettingsWindow.__settings_dict["Next game join option"])
            self.__friends_join_var.set(SettingsWindow.__settings_dict["Friend join option"])
        
        if last_valid_state_position:
            SettingsWindow.__settings_dict["Game time overlay pos 1"] = self.__game_time_one_var.get()
            SettingsWindow.__settings_dict["Game time overlay pos 2"] = self.__game_time_two_var.get()
        else:
            self.__game_time_one_var.set(SettingsWindow.__settings_dict["Game time overlay pos 1"])
            self.__game_time_two_var.set(SettingsWindow.__settings_dict["Game time overlay pos 2"])

        self._settings_window.withdraw()

    def update_settings(self):
        """Continuously checks for updates"""
        def toggle_values():
            SettingsWindow.__settings_dict["Next game join option"] = not SettingsWindow.__settings_dict["Next game join option"]
            SettingsWindow.__settings_dict["Friend join option"] = not SettingsWindow.__settings_dict["Friend join option"]
            SettingsWindow.__settings_dict["Game time overlay pos 1"] = not SettingsWindow.__settings_dict["Game time overlay pos 1"]
            SettingsWindow.__settings_dict["Game time overlay pos 2"] = not SettingsWindow.__settings_dict["Game time overlay pos 2"]
            warcry_input = self.__warcries_entry.get()
            if self.validate_warcry_keys(warcry_input):
                SettingsWindow.__settings_dict["WarcriesKeys"] = [key.strip().upper() for key in warcry_input.split(",")]
            self._settings_window.after(1000, toggle_values)
        
        toggle_values()

    def on_close(self):
        """Close function to update and destroy window"""
        self.close_settings()
        self.update_thread.join()
        self.update_launcher_settings()
    
    def show_settings(self):
        self._settings_window.deiconify()

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

    def disable_pos_one(self):
        """Disables position two when position one is selected"""
        if self.__game_time_two_var.get():
            self.__game_time_one_var.set(False)
            self._game_time_one_checkbox["state"] = "disabled"
        else:
            self._game_time_one_checkbox["state"] = "normal"

    def disable_pos_two(self):
        """Disables position one when position two is selected"""
        if self.__game_time_one_var.get():
            self.__game_time_two_var.set(False)
            self._game_time_two_checkbox["state"] = "disabled"
        else:
            self._game_time_two_checkbox["state"] = "normal"

    def update_launcher_settings(self):
        """Update the launcher settings with the values and destroy after"""
        self._root.set_settings(self.get_settings())
        self._settings_window.withdraw()
    
    def get_settings(self):
        """Get current settings from checkboxes"""
        return {
            "Friend join option": self.__friends_join_var.get(),
            "Next game join option": self.__join_next_game_var.get(),
            "Game time overlay pos 1": self.__game_time_one_var.get(),
            "Game time overlay pos 2": self.__game_time_two_var.get(),
            "WarcriesKeys": SettingsWindow.__settings_dict["WarcriesKeys"]
        }