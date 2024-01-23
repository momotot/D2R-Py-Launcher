import tkinter as tk
import time
import datetime as datetime
import threading
import psutil
from queue import Queue

class OverlayPattern:
    def __init__(self, root, console, client_obj, game_tracker, image_obj):
        self.root = None
        self.console = console
        self.label = None
        self.main_root = root
        self.client_obj = client_obj
        self.game_tracker = game_tracker
        self.image_obj = image_obj
        self.window_name = None
        self._process_name = "D2R.exe"
        
        self.stop_event = threading.Event()
        self.queue = Queue()
        self.thread = threading.Thread(target=self.check_process)
        self.thread.start()
        self.run()

    # decorates the overlay window 
    def decorate(self):
        self.root = tk.Toplevel(self.main_root)
        self.root.geometry("350x100+0+0")
        self.root.title("")
        self.root.tk_setPalette("black")
        self.root.wm_overrideredirect(1)
        self.root.wm_attributes("-topmost", True) 
        self.root.wm_attributes("-transparentcolor", "black")

    # creates the label to display the info
    def create_label(self):
        self.label = tk.Label(self.root, text="", fg="red", font=("Helvetica", 10, "bold"))
        self.label.pack(side="top", fill="both", expand=True, padx=5, pady=30)

    # function to destroy the label
    def remove_label(self):
        if self.label and self.root:
            self.root.after(0, self.label.destroy)
            self.label = None
    
    # function to update the label with in game status 
    def update_label(self):
        if self.label:
            if self.game_tracker.in_game:
                text_to_post = self.image_obj.get_area_text()

                self.label.configure(text=f"{text_to_post}",
                                     justify="left")
            else:

                text_to_post = self.image_obj.get_area_text()
                self.label.configure(text=f"{text_to_post}",
                                      justify="left")
    
    # function to update the gui/label to the specific game window
    def update_gui_status(self, process_found):
        self.process_found = process_found
        if process_found and self.root:
            if not self.label:
                self.create_label()
            
            if self.window_name is None:
                for name in self.client_obj.window_names:
                    if "[MAIN]" in name:
                        window_name = name
            self.window_position = self.client_obj.get_window_position(window_name)

            if self.window_position:
                self.root.geometry(f"1000x800+{self.window_position[0]}+{self.window_position[1]}")

        elif not process_found and self.label:
            self.remove_label()
    
    # function to check if the main root window exists
    def check_main_root(self):
        if self.main_root is None:
            self.remove_label()
        else:
            self.root.after(1000, self.check_main_root)
    
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
        self.console.log_message(f"Overlay pattern object created", 1)
        self.decorate()
        self.create_label()
        self.check_main_root()
        self.root.after(0, self.root.mainloop)