import os
import configparser
import subprocess
import time
import pyautogui
import pygetwindow
import win32gui
import win32process
import win32con
import win32api
import psutil
import re
import tkinter as tk
from tkinter import ttk
import threading
import cv2
import numpy as np
from pathlib import Path
import random
from Utils.Reader import MemoryReader

class Client:   
    def __init__ (self, root, clients, folder_path, path, console):
        self._root = root
        self.clients = clients
        self._folder_path = folder_path
        self.diablo_path = path
        self._console = console

        self.legacy = False  
        self.process_dict = {}
        self.window_names = [] 
        self.process_info = {}
        self.parse_config_and_launch()

        self.check_process_thread = threading.Thread(target=self.check_active_processes, daemon=True)
        self.check_process_thread.start()
    
    def read_config(self):
        """Reads the config.ini"""
        config = configparser.ConfigParser()
        config.read("src/config.ini")
        return config
    
    def parse_config_and_launch(self):
        """Parses the config.ini and launches the game with the config parameters"""
        active_pids = self.get_pids() # check to sync active pids with the list 
        potentially_remove = []
        for name, pid in self.process_info.items():
            if pid not in active_pids and name in self.window_names:
                    potentially_remove.append(name)
                    
        for name in potentially_remove:
            self.window_names.remove(name)
            del self.process_info[name]
            
        config = self.read_config()
        clients_launched = 0
        main_char_launched = any("[MAIN]" in item for item in self.process_info.keys())
        for name in config.sections():
            name_string = f"[MAIN] - {name}"         
            if name in self.process_info.keys() or name_string in self.process_info.keys():
                continue   

            if clients_launched == int(self.clients):
                break

            if "user" in name:
                break

            username = config.get(name, "username")
            password = config.get(name, "password")
            region = config.get(name, "region")

            if username == "" or password == "" or region == "":
                break

            command = f"{self.diablo_path} -username {username} -password {password} -region {region}"
            pid = ""
            try:
                process = subprocess.Popen(command)
                self._console.log_message(f"D2R #{clients_launched+1} launched", 1)

                if not main_char_launched:
                    pid = process.pid
                    self.process_dict["[MAIN] - " + name] = process.pid
                    self.process_info["[MAIN] - " + name] = process.pid
                    self.window_names.append("[MAIN] - " + name)
                    main_char_launched = True
                else:
                    pid = process.pid
                    self.process_dict[name] = process.pid
                    self.process_info[name] = process.pid
                    self.window_names.append(name)
            except:
                self._console.log_message(f"Failed to launch D2R #{clients_launched+1}", 3)

            clients_launched += 1
            time.sleep(1)
            self.terminate_handle(name, pid)
            count = 0
            while not self.is_start_image_present():
                pyautogui.press("space")
                time.sleep(0.1)
                pyautogui.press("space")
                count += 1
                self.resize_window_start()
                if count == 30:
                    break
            self._console.log_message(f"{name} at start screen", 1)
            self.change_window_title()
            self.enter_lobby(name)
        self.focus_main_window()

    def terminate_handle(self, name, pid):
        """Find the handle and terminate it to be able to run several d2r's"""
        self._console.log_message(f"Closing handle for {name}, PID: {pid}", 1)
        handle64_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'handle64.exe')

        # Run handle64.exe to get handle info
        handle_command = rf'"{handle64_path}" -accepteula -a -p D2R.exe > "{os.path.dirname(os.path.realpath(__file__))}\d2r_handles.txt"'
        subprocess.run(handle_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, text=True)

        proc_id_populated = ""
        handle_id_populated = ""

        # Parse d2r_handles.txt to get process ID and handle ID
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'd2r_handles.txt'), 'r') as handle_file:
            for line in handle_file:
                proc_match = re.match(r'^D2R.exe pid: (?P<g1>.+) ', line)
                handle_match = re.match(r'^(?P<g2>.+): Event.*DiabloII Check For Other Instances', line)

                if proc_match:
                    proc_id_populated = proc_match.group('g1')

                if handle_match:
                    handle_id_populated = handle_match.group('g2')
                    handle_command = rf'"{handle64_path}" -p {proc_id_populated} -c {handle_id_populated} -y'
                    result = subprocess.run(handle_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, text=True)
                    
                    if result.returncode != 0:
                        self._console.log_message(f"Error: Unable to close handle for {proc_id_populated} {handle_id_populated}", 3)

    def change_window_title(self):
        """Change window titles to names in config"""
        try:
            while self.process_dict:
                def callback(hwnd, _):
                    window_text = win32gui.GetWindowText(hwnd)
                    _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                    
                    if "Diablo II: Resurrected" in window_text and found_pid in self.process_dict.values():
                        for name, pid in list(self.process_dict.items()):
                            if pid == found_pid:
                                try:
                                    if win32gui.GetWindowText(hwnd) != name:
                                        win32gui.SetWindowText(hwnd, f"{name}")
                                        self._console.log_message(f"Changed window name to {name}", 1)
                                        del self.process_dict[name]
                                except:
                                    self._console.log_message(f"Failed to change name to {name}", 3)
                win32gui.EnumWindows(callback, None)
        except:
            self._console.log_message(f"Error in change_window_title", 3)
    
    def get_window_front(self, window_name):
        """Make the window appear in the foreground to perform actions"""
        hwnd = win32gui.FindWindow(None, window_name)
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
    
    def get_to_start_screen(self):
        """Spams space upon start to get to start screen"""
        time.sleep(0.5)
        for _ in range(25):
            pyautogui.press("space")
            time.sleep(0.2)
    
    def get_window_position(self, window_name):
        """Gets the current window position relative to the full monitor resolution"""
        try:
            window = pygetwindow.getWindowsWithTitle(window_name)[0]
            return window.left, window.top, window.width, window.height
        except:
            return None
    
    def join_game_reader(self):
        """Actions performed with pyautogui to join the game via gamename/password from memory read. Utilized through the "Next game" button"""
        try:
            if len(self.window_names) == 0:
                self._console.log_message("No window(s) opened", 2)
                return
            sleep_delay = 0.1
            for name in self.window_names:
                if "MAIN" in name: # main character should not join, only create
                    continue

                position = self.get_window_position(name)
                self.get_window_front(name)
                current_location = self.check_if_lobby(name)

                self._reader_object = MemoryReader.return_current_object()
                if self._reader_object is None:
                    self._console.log_message("Reader object doesnt exist, you must active 'Game time'", 2)
                    return
                self._console.log_message("Attempting next game join", 1)
                game_name = self._reader_object.get_gamename_info()
                password = self._reader_object.get_password_info()

                if current_location == "start": # is at start screen
                    if position:
                        pyautogui.moveTo(position[0]+755, position[1]+683)
                        pyautogui.click(x=position[0]+755, y=position[1]+683) # press enter lobby
                        time.sleep(sleep_delay)
                        pyautogui.moveTo(position[0]+857, position[1]+137)
                        pyautogui.click(x=position[0]+857, y=position[1]+137) # click the game name label to write
                        pyautogui.hotkey("ctrl", "a") # mark previous games, otherwise it can get messy..
                        time.sleep(sleep_delay)
                        pyautogui.typewrite(game_name)
                        time.sleep(sleep_delay)
                        pyautogui.moveTo(position[0]+1051, position[1]+138)
                        pyautogui.click(x=position[0]+1051, y=position[1]+138) # click the password label to write
                        pyautogui.hotkey("ctrl", "a")
                        time.sleep(sleep_delay)
                        pyautogui.typewrite(password)
                        pyautogui.press("enter")
                        self._console.log_message(f"{name} joined a new game", 1)
                    else:
                        self._console.log_message("No valid window position", 3) 
                elif current_location == "lobby":
                    if position:
                        pyautogui.moveTo(position[0]+857, position[1]+137)
                        pyautogui.click(x=position[0]+857, y=position[1]+137) # click the game name label to write
                        pyautogui.hotkey("ctrl", "a") # mark previous games, otherwise it can get messy..
                        time.sleep(sleep_delay)
                        pyautogui.typewrite(game_name)
                        time.sleep(sleep_delay)
                        pyautogui.moveTo(position[0]+1051, position[1]+138)
                        pyautogui.click(x=position[0]+1051, y=position[1]+138) # click the password label to write
                        pyautogui.hotkey("ctrl", "a")
                        time.sleep(sleep_delay)
                        pyautogui.typewrite(password)
                        pyautogui.press("enter")
                        self._console.log_message(f"{name} joined a new game", 1)
                    else:
                        self._console.log_message("No valid window position", 3) 
                else:
                    if position:
                        if not self.legacy:
                            pyautogui.press("esc")
                            time.sleep(sleep_delay)
                            pyautogui.moveTo(position[0]+645, position[1]+357)
                            pyautogui.click(x=position[0]+645, y=position[1]+357) # coord for left click on exit menu
                            time.sleep(sleep_delay)                
                            pyautogui.moveTo(position[0]+857, position[1]+137)
                            pyautogui.click(x=position[0]+857, y=position[1]+137) # click the game name label to write
                            pyautogui.hotkey("ctrl", "a") # mark previous games, otherwise it can get messy..
                            time.sleep(sleep_delay)
                            pyautogui.typewrite(game_name)
                            time.sleep(sleep_delay)
                            pyautogui.moveTo(position[0]+1051, position[1]+138)
                            pyautogui.click(x=position[0]+1051, y=position[1]+138) # click the password label to write
                            pyautogui.hotkey("ctrl", "a")
                            time.sleep(sleep_delay)
                            pyautogui.typewrite(password)
                            pyautogui.press("enter")
                            self._console.log_message(f"{name} joined a new game", 1)
                        else:
                            pyautogui.press("esc")
                            time.sleep(sleep_delay)
                            pyautogui.moveTo(position[0]+615, position[1]+325)
                            pyautogui.click(x=position[0]+615, y=position[1]+325) # coord for left click on exit menu
                            time.sleep(sleep_delay)
                            pyautogui.moveTo(position[0]+857, position[1]+137)
                            pyautogui.click(x=position[0]+857, y=position[1]+137) # click the game name label to write
                            pyautogui.hotkey("ctrl", "a") # mark previous games, otherwise it can get messy..
                            time.sleep(sleep_delay)
                            pyautogui.typewrite(game_name)
                            time.sleep(sleep_delay)
                            pyautogui.moveTo(position[0]+1051, position[1]+138)
                            pyautogui.click(x=position[0]+1051, y=position[1]+138) # click the password label to write
                            pyautogui.hotkey("ctrl", "a")
                            time.sleep(sleep_delay)
                            pyautogui.typewrite(password)
                            pyautogui.press("enter")
                            self._console.log_message(f"{name} joined a new game", 1)
                    else:
                        self._console.log_message("No valid window position", 3) 
            self.legacy = False
            
            for name in self.window_names:
                if "MAIN" in name:
                    self.get_window_front(name)
                    break
               
            self.resize_window_game()
            
        except:
            self._console.log_message("Failed to join next game", 3)
            

    def join_game_friends(self):
        """Actions performed with pyautogui to join the game via friend list. Utilized through the "Next game" button"""
        try:
            if len(self.window_names) == 0:
                self._console.log_message("No window(s) opened", 2)
                return
            self._console.log_message("Attempting next game join", 1)
            sleep_delay = 0.1
            for name in self.window_names:
                if "MAIN" in name: # main character should not join, only create
                    continue
                position = self.get_window_position(name)
                self.get_window_front(name)
                current_location = self.check_if_lobby(name)
                if current_location == "start": # is at start screen
                    if position:
                        pyautogui.moveTo(position[0]+755, position[1]+683)
                        pyautogui.click(x=position[0]+755, y=position[1]+683) # press enter lobby
                        time.sleep(sleep_delay)
                        pyautogui.moveTo(position[0]+130, position[1]+546)
                        pyautogui.click(x=position[0]+130, y=position[1]+546) # coord for left click on friend list symbol
                        time.sleep(sleep_delay)
                        pyautogui.moveTo(position[0]+206, position[1]+140)
                        pyautogui.click(x=position[0]+206, y=position[1]+140) # coord for left click on friend list bar
                        time.sleep(sleep_delay)
                        pyautogui.moveTo(position[0]+204, position[1]+166)
                        pyautogui.rightClick(x=position[0]+204, y=position[1]+166) # coord for right click on the friend
                        time.sleep(sleep_delay)
                        pyautogui.moveTo(position[0]+336, position[1]+276)
                        pyautogui.click(x=position[0]+336, y=position[1]+276) # coord for left click on join game
                        time.sleep(sleep_delay)
                        self._console.log_message(f"{name} joined a new game", 1)
                    else:
                        self._console.log_message("No valid window position", 3)  
                elif current_location == "lobby": # is in lobby
                    if position:
                        pyautogui.moveTo(position[0]+130, position[1]+546)
                        pyautogui.click(x=position[0]+130, y=position[1]+546) # coord for left click on friend list symbol
                        time.sleep(sleep_delay)
                        pyautogui.moveTo(position[0]+206, position[1]+140)
                        pyautogui.click(x=position[0]+206, y=position[1]+140) # coord for left click on friend list bar
                        time.sleep(sleep_delay)
                        pyautogui.moveTo(position[0]+204, position[1]+166)
                        pyautogui.rightClick(x=position[0]+204, y=position[1]+166) # coord for right click on the friend
                        time.sleep(sleep_delay)
                        pyautogui.moveTo(position[0]+336, position[1]+276)
                        pyautogui.click(x=position[0]+336, y=position[1]+276) # coord for left click on join game
                        time.sleep(sleep_delay)
                        self._console.log_message(f"{name} joined a new game", 1)
                    else:
                        self._console.log_message("No valid window position", 3)  
                else:
                    if position:
                        # coordinates are on 1280x720 windows
                        if not self.legacy: # positions for non-legacy
                            time.sleep(sleep_delay)
                            pyautogui.press("esc")
                            time.sleep(sleep_delay)
                            pyautogui.moveTo(position[0]+645, position[1]+357)
                            pyautogui.click(x=position[0]+645, y=position[1]+357) # coord for left click on exit menu
                            time.sleep(sleep_delay)
                            pyautogui.moveTo(position[0]+130, position[1]+546)
                            pyautogui.click(x=position[0]+130, y=position[1]+546) # coord for left click on friend list symbol
                            time.sleep(sleep_delay)
                            pyautogui.moveTo(position[0]+206, position[1]+140)
                            pyautogui.click(x=position[0]+206, y=position[1]+140) # coord for left click on friend list bar
                            time.sleep(sleep_delay)
                            pyautogui.moveTo(position[0]+204, position[1]+166)
                            pyautogui.rightClick(x=position[0]+204, y=position[1]+166) # coord for right click on the friend
                            time.sleep(sleep_delay)
                            pyautogui.moveTo(position[0]+336, position[1]+276)
                            pyautogui.click(x=position[0]+336, y=position[1]+276) # coord for left click on join game
                            time.sleep(sleep_delay)
                            self._console.log_message(f"{name} joined a new game", 1)
                        else: # positions for legacy
                            time.sleep(sleep_delay)
                            pyautogui.press("esc")
                            time.sleep(sleep_delay)
                            pyautogui.moveTo(position[0]+615, position[1]+325)
                            pyautogui.click(x=position[0]+615, y=position[1]+325) # coord for left click on exit menu
                            time.sleep(sleep_delay)
                            pyautogui.moveTo(position[0]+130, position[1]+546)
                            pyautogui.click(x=position[0]+130, y=position[1]+546) # coord for left click on friend list symbol
                            time.sleep(sleep_delay)
                            pyautogui.moveTo(position[0]+206, position[1]+140)
                            pyautogui.click(x=position[0]+206, y=position[1]+140) # coord for left click on friend list bar
                            time.sleep(sleep_delay)
                            pyautogui.moveTo(position[0]+204, position[1]+166)
                            pyautogui.rightClick(x=position[0]+204, y=position[1]+166) # coord for right click on the friend
                            time.sleep(sleep_delay)
                            pyautogui.moveTo(position[0]+336, position[1]+276)
                            pyautogui.click(x=position[0]+336, y=position[1]+276) # coord for left click on join game
                            time.sleep(sleep_delay)
                            self._console.log_message(f"{name} joined a new game", 1)
                    else:
                        self._console.log_message("No valid window position", 3)      
            self.legacy = False
            
            for name in self.window_names:
                if "MAIN" in name:
                    self.get_window_front(name)
                    break
               
            self.resize_window_game()
            
        except:
            self._console.log_message("Failed to join next game", 3)
    
    def change_to_legacy(self):
        """Performs the change by pressing the change graphic key for each window. Utilized through the "legacy" button"""
        if len(self.window_names) == 0:
            self._console.log_message("No window(s) opened", 2)
            return
        self._console.log_message("Attempting to change to legacy graphics", 1)
        for name in self.window_names:
            if "MAIN" in name:
                continue
            try:
                position = self.get_window_position(name)

                coordinates_dict = {
                    "1": (870,300),
                    "2": (591,490),
                    "3": (669,255),
                    "4": (290,304)
                    }

                random_coordinate = random.choice(list(coordinates_dict.values()))
                self.get_window_front(name)
                time.sleep(0.1)
                pyautogui.press("'") # Make sure this key is your key to change graphics
                time.sleep(0.1)
                pyautogui.moveTo(position[0]+random_coordinate[0], position[1]+random_coordinate[1])
                pyautogui.click(x=position[0]+random_coordinate[0], y=position[1]+random_coordinate[1]) # coord for left click on exit menu
                time.sleep(0.1)
                self._console.log_message(f"Changed {name} to legacy graphic", 1)
            except:
                self._console.log_message(f"Error changing to legacy for {name}", 3)
        self.legacy = True
        
        for name in self.window_names:
            if "MAIN" in name:
                self.get_window_front(name)
                break

    def focus_main_window(self):
        """Focus the main window"""
        try:
            for name in self.window_names:
                if "MAIN" in name:
                    self.get_window_front(name)
                    break
        except:
            self._console.log_message(f"Failed to focus {name}", 2)

    def resize_window_start(self):
        """Used to re-size the window at start if its not 1920x1080"""
        try:
            status = False
            window = pygetwindow.getWindowsWithTitle("Diablo II: Resurrected")[0]
            current_width, current_height = window.size
            if current_width != 1280 or current_height != 720 and not status:
                window.resizeTo(1280,720)
                status = True
        except:
            self._console.log_message(f"Failed to re-size window", 3)

    def resize_window_game(self):
        """Re-sizes all "joiners" when they are in-game by pressing the "Legacy" button"""
        try:
            if len(self.window_names) == 0:
                self._console.log_message("No window(s) opened", 2)
                return
            self._console.log_message("Attempting to re-size window(s)", 1)
            for name in self.window_names:
                if not "MAIN" in name:
                    window = pygetwindow.getWindowsWithTitle(name)[0]
                    current_width, current_height = window.size
                    if current_width != 1280 or current_height != 720:
                        window.resizeTo(1280,720)
                        self._console.log_message(f"Re-sized {name} to 1280x720", 1)
                elif "MAIN" in name:
                    window = pygetwindow.getWindowsWithTitle(name)[0]
                    current_width, current_height = window.size
                    if current_width != 1920 or current_height != 1080:
                        window.resizeTo(1920,1080)
                        self._console.log_message(f"Re-sized {name} to 1920x1080", 1)
            for name in self.window_names:
                if "MAIN" in name:
                    self.get_window_front(name)
                    break
        except:
            self._console.log_message(f"Failed to re-size {name}", 2)
    
    def get_pids(self):
        """Iterates the processes to get active D2R's and their PID's"""
        pids = []
        for process in psutil.process_iter(["pid", "name"]):
            if process.info["name"] == "D2R.exe":
                pids.append(process.info["pid"])
        return pids
    
    def terminate_pid(self):
        """Terminates the selected process"""
        try:
            self._console.log_message("Attempting to terminate PID(s)", 1)
            terminated_names = []
            for name, var in self.checkbox_dict.items():
                if var.get() == 1:
                    pid = self.process_info.get(name)
                    if pid is not None:
                        handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, pid)
                        win32process.TerminateProcess(handle, 0)
                        win32api.CloseHandle(handle)
                        self._console.log_message(f"PID: {pid} for {name} terminated", 1)
                        terminated_names.append(name)
            # remove the clients from the lists if terminated
            for name in terminated_names:
                del self.process_info[name]
                if name in self.window_names:
                    self.window_names.remove(name)
            terminated_names = []
            self._console.log_message("Checkbox for termination closed", 1)
            self.checkbox_window.destroy()
        except:
            self._console.log_message(f"Failed to terminate PID", 3)

    def check_active_processes(self):
        """continuously scans for processes to remove the in-active pids"""
        while True:
            try:
                items_to_remove = []
                for name, pid in self.process_info.items():
                    try:
                        process = psutil.Process(pid)
                        continue
                    except psutil.NoSuchProcess:
                        items_to_remove.append(name)
                
                for name in items_to_remove:
                    del self.process_info[name]
                    if name in self.window_names:
                        self.window_names.remove(name)
                    self._console.log_message(f"Removed {name} because not active", 2)
            except:
                self._console.log_message(f"Error checking active processes", 3)
            time.sleep(1)

    def checkbox(self):
        """Checkbox window to list all active PID's and selection for termination"""
        self.checkbox_window = tk.Toplevel(self._root)
        self.checkbox_window.title("Select clients")
        x = self._root.winfo_x()
        y = self._root.winfo_y()
        self.checkbox_window.geometry(f"400x400+{x}+{y}")
        self.checkbox_window.configure()
        self.checkbox_window.resizable(0,0)
        self.checkbox_dict = {}

        for name, pid in self.process_info.items():
            if pid in self.get_pids():
                var = tk.IntVar(value=0)
                self.checkbox_dict[name] = var

                checkbox = ttk.Checkbutton(self.checkbox_window, text=name, variable=var)
                checkbox.pack()

        terminate_button = ttk.Button(self.checkbox_window, text="Terminate Selected", command=self.terminate_pid)
        terminate_button.pack()
        self.checkbox_window.protocol("WM_DELETE_WINDOW", self.close_checkbox)
        self._console.log_message("Checkbox for termination opened", 1)
    
    def close_checkbox(self):
        """Just a close function"""
        self._console.log_message("Checkbox for termination closed", 1)
        self.checkbox_window.destroy()
    
    def enter_lobby(self, name):
        """Function to just enter the lobby for all except main char"""
        for key in self.process_info.keys():
            if "[MAIN]" and name in key:
                name = key
        if "[MAIN]" in name:
            return
        position = self.get_window_position(name)
        pyautogui.moveTo(position[0]+755, position[1]+683)
        pyautogui.click(x=position[0]+755, y=position[1]+683) # press enter lobby
        self._console.log_message(f"{name} in lobby", 1)

    def is_start_image_present(self):
        """Function to read the image at start screen"""
        window_name = "Diablo II: Resurrected"
        target_image_path = Path(__file__).parent / "Pictures" / "Start.png"
        target_image_path_two = Path(__file__).parent / "Pictures" / "Start2.png"

        target_image = cv2.imread(str(target_image_path))
        target_image_two = cv2.imread(str(target_image_path_two))

        window = pygetwindow.getWindowsWithTitle(window_name)[0]
        x, y, w, h = window.left, window.top, 1280, 720
        roi = pyautogui.screenshot(region=(x, y, w, h))
        #roi.save("loading_debug.png")

        screenshot = np.array(roi)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

        result = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)
        result_two = result = cv2.matchTemplate(screenshot, target_image_two, cv2.TM_CCOEFF_NORMED)

        threshold = 0.8
        loc = np.where(result >= threshold)
        loc_two = np.where(result_two >= threshold)
        
        if len(loc[0]) > 0 or len(loc_two[0] > 0):
            return True
        
        return False
    
    def check_if_lobby(self, name):
        """Function to check if its in game, in start screen or lobby"""
        self.get_window_front(name)
        time.sleep(0.1)
        start_screen_path = Path(__file__).parent / "Pictures" / "Start.png"
        start_screen_path_two = Path(__file__).parent / "Pictures" / "Start2.png"
        lobby_path = Path(__file__).parent / "Pictures" / "lobby.png"

        start_image = cv2.imread(str(start_screen_path))
        start_image_two = cv2.imread(str(start_screen_path_two))
        lobby_image = cv2.imread(str(lobby_path))

        window = pygetwindow.getWindowsWithTitle(name)[0]
        x, y, w, h = window.left, window.top, 1280, 720
        roi = pyautogui.screenshot(region=(x,y, w, h))

        screenshot = np.array(roi)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

        result_start = cv2.matchTemplate(screenshot, start_image, cv2.TM_CCOEFF_NORMED)
        result_start_two = cv2.matchTemplate(screenshot,start_image_two, cv2.TM_CCOEFF_NORMED)
        result_lobby = cv2.matchTemplate(screenshot, lobby_image, cv2.TM_CCOEFF_NORMED)

        threshold_start = 0.7
        threshold_lobby = 0.7
        loc_start = np.where(result_start >= threshold_start)
        loc_start_two = np.where(result_start_two >= threshold_start)
        loc_lobby = np.where(result_lobby >= threshold_lobby)
        
        if len(loc_start[0]) > 0 or len(loc_start_two[0] > 0):
            return "start"
        elif len(loc_lobby[0]) > 0:
            return "lobby"
        else:
            return ""