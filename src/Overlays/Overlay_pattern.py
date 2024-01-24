import tkinter as tk
import time
import threading
import psutil
from queue import Queue

import Utils.Image_reader as Image_reader

class OverlayPatternInfo:
    def __init__(self, root, console, client_obj, game_tracker, choosen_name):
        self._root = None
        self._main_root = root
        self._console = console
        self.label = None
        self._client_obj = client_obj
        self._game_tracker = game_tracker
        self.window_name = None
        self._process_name = "D2R.exe"
        self._choosen_name = choosen_name
        self._image_scanner = Image_reader.ImageReader(self, self._console, self._choosen_name)
        self.stop_event = threading.Event()
        self.queue = Queue()
        self.thread = threading.Thread(target=self.check_process)
        self.thread.start()
        self._image_scanner.continuously_scan_for_area()

    def decorate(self):
        """Decorates the overlay window """
        self._root = tk.Toplevel(self._main_root)
        self._root.geometry("350x100+0+0")
        self._root.title("")
        self._root.tk_setPalette("black")
        self._root.wm_overrideredirect(1)
        self._root.wm_attributes("-topmost", True) 
        self._root.wm_attributes("-transparentcolor", "black")
    
    def create_label(self):
        """Creates the label to display the info"""
        self.label = tk.Label(self._root, text="Loading", fg="red", font=("Helvetica", 10, "bold"))
        self.label.pack(side="top", fill="both", expand=True, padx=5, pady=30)

    def remove_label(self):
        """Function to destroy the label"""
        if self.label and self._root:
            self._root.after(0, self.label.destroy)
            self.label = None
    
    def update_label(self):
        """Function to update the label with the area text"""
        if self.label:

            text_to_post = self._image_scanner.get_area_text()
            self.label.configure(text=f"{text_to_post}", justify="left")

    def update_gui_status(self, process_found):
        """Function to update the gui/label to the specific game window"""
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
                self._root.geometry(f"500x1000+{self.window_position[0]}+{self.window_position[1]}")
        
        elif not process_found and self.label:
            self.remove_label()

    def check_main_root(self):
        """Function to check if the main root window exists"""
        if self._main_root is None:
            self.remove_label()
        else:
            self._root.after(1000, self.check_main_root)

    def check_process(self):
        """Function to continuously check if a specified process is running"""
        while not self.stop_event.is_set():
            process_found = any(process.info['name'] == self._process_name for process in psutil.process_iter(["pid", "name"]))
            self.update_gui_status(process_found)
            time.sleep(0.1)
        self.queue.put(None)
    
    def stop_check_process(self):
        """Function to stop the process checking thread"""
        self.stop_event.set()
        self._image_scanner = None
        self.thread.join()
        self.queue.get()

    def run(self):
        """Initialization of the overlay object"""
        self._console.log_message(f"Overlay pattern info object created", 1)
        self.decorate()
        self.create_label()
        self.check_main_root()
        self._root.after(0, self._root.mainloop) 