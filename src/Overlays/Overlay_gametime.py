import tkinter as tk
import time
import datetime as datetime
import threading
import psutil
from queue import Queue

class OverlayGameTime:
    def __init__(self, root, console, client_obj, game_tracker):
        self._root = None
        self._console = console
        self.label = None
        self._main_root = root
        self._client_obj = client_obj
        self._game_tracker = game_tracker
        self.window_name = None
        self._process_name = "D2R.exe"
        
        self.stop_event = threading.Event()
        self.queue = Queue()
        self.thread = threading.Thread(target=self.check_process)
        self.thread.start()

    # decorates the overlay window 
    def decorate(self):
        self._root = tk.Toplevel(self._main_root)
        self._root.geometry("350x100+0+0")
        self._root.title("")
        self._root.tk_setPalette("black")
        self._root.wm_overrideredirect(1)
        self._root.wm_attributes("-topmost", True) 
        self._root.wm_attributes("-transparentcolor", "black")

    # creates the label to display the info
    def create_label(self):
        self.label = tk.Label(self._root, text="", fg="red", font=("Helvetica", 10, "bold"))
        self.label.pack(side="top", fill="both", expand=True, padx=5, pady=30)

    # function to destroy the label
    def remove_label(self):
        if self.label and self._root:
            self._root.after(0, self.label.destroy)
            self.label = None
    
    # function to update the label with in game status 
    def update_label(self):
        if self.label:
            if self._game_tracker.in_game:
                elapsed_time = int(self._game_tracker.get_current_time())
                last_game_time = int(self._game_tracker.get_last_game_time())
                average_game_time = int(self._game_tracker.get_average_time())
                game_count = self._game_tracker.get_game_count()+1
                formatted_time_ingame = self._game_tracker.format_time(elapsed_time)
                formatted_time_lastgame = self._game_tracker.format_time(last_game_time)
                formatted_time_average = self._game_tracker.format_time(average_game_time)
                self.label.configure(text=f"Game #{game_count}\nIn-game time: {formatted_time_ingame}\nLast game time: {formatted_time_lastgame}\nAverage game time: {formatted_time_average}",
                                     justify="left")
            else:
                last_game_time = int(self._game_tracker.get_last_game_time())
                average_game_time = int(self._game_tracker.get_average_time())
                game_count = self._game_tracker.get_game_count()
                formatted_time_lastgame = self._game_tracker.format_time(last_game_time)
                formatted_time_average = self._game_tracker.format_time(average_game_time)
                self.label.configure(text=f"Game count: {game_count}\nIn-game time: Not in game\nLast game time: {formatted_time_lastgame}\nAverage game time: {formatted_time_average}",
                                      justify="left")
    
    # function to update the gui/label to the specific game window
    def update_gui_status(self, process_found):
        self.process_found = process_found
        if process_found and self._root:
            if not self.label:
                self.create_label()
            
            if self.window_name is None:
                for name in self._client_obj.window_names:
                    if "[MAIN]" in name:
                        window_name = name
            self.window_position = self._client_obj.get_window_position(window_name)

            if self.window_position:
                self._root.geometry(f"500x800+{self.window_position[0]}+{self.window_position[1]}")

        elif not process_found and self.label:
            self.remove_label()
    
    # function to check if the main root window exists
    def check_main_root(self):
        if self._main_root is None:
            self.remove_label()
        else:
            self._root.after(1000, self.check_main_root)
    
    # function to continuously check if a specified process is running
    def check_process(self):
        while not self.stop_event.is_set():
            process_found = any(process.info['name'] == self._process_name for process in psutil.process_iter(["pid", "name"]))
            self.update_gui_status(process_found)
            time.sleep(0.1)
        self.queue.put(None)

    # function to stop the process checking thread
    def stop_check_process(self):
        self.stop_event.set()
        self.thread.join()
        self.queue.get()
    
    # initialization of the overlay object
    def run(self):
        self._console.log_message(f"Overlay game time object created", 1)
        self.decorate()
        self.create_label()
        self.check_main_root()
        self._root.after(0, self._root.mainloop)