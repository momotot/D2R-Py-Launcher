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

class Client:   
    def __init__ (self, parent, clients, folder_path, path, console):
        self.parent = parent
        self.clients = clients
        self.folder_path = folder_path
        self.diablo_path = path
        self.console = console

        self.legacy = False  
        self.process_dict = {}
        self.window_names = [] 
        self.process_info = {}
        self.parse_config_and_launch()

        self.check_process_thread = threading.Thread(target=self.check_active_processes, daemon=True)
        self.check_process_thread.start()
    
    # Reads the config.ini
    def read_config(self):
        config = configparser.ConfigParser()
        config.read("src/config.ini")
        return config
    
    # Parses the config.ini and launches the game with the config parameters
    def parse_config_and_launch(self):
        # check to sync active pids with the list 
        active_pids = self.get_pids()
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
                self.console.log_message(f"D2R #{clients_launched+1} launched", 1)

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
                self.console.log_message(f"Failed to launch D2R #{clients_launched+1}", 3)

            clients_launched += 1
            time.sleep(1)
            self.terminate_handle(name, pid)
            #self.get_to_start_screen()
            while not self.is_target_image_present_two():
                pyautogui.press("space")
                time.sleep(0.2)
            self.console.log_message(f"{name} at start screen", 1)
            self.change_window_title()
            self.enter_lobby(name)
        self.resize_window_start() 

    # Find the handle and terminate it to be able to run several d2r's
    def terminate_handle(self,name, pid):
        self.console.log_message(f"Closing handle for {name}, PID: {pid}", 1)
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
                        self.console.log_message(f"Error: Unable to close handle for {proc_id_populated} {handle_id_populated}", 3)

    # Change window titles to names in config
    def change_window_title(self):
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
                                        self.console.log_message(f"Changed window name to {name}", 1)
                                        del self.process_dict[name]
                                except:
                                    self.console.log_message(f"Failed to change name to {name}", 3)
                win32gui.EnumWindows(callback, None)
        except:
            self.console.log_message(f"Error in change_window_title", 3)
    
    # Make the window appear in the foreground to perform actions
    def get_window_front(self, window_name):
        hwnd = win32gui.FindWindow(None, window_name)
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
    
    # Spams space upon start to get to start screen
    def get_to_start_screen(self):
        time.sleep(0.5)
        for _ in range(25):
            pyautogui.press("space")
            time.sleep(0.2)
    
    # Gets the current window position relative to the full monitor resolution
    def get_window_position(self, window_name):
        try:
            window = pygetwindow.getWindowsWithTitle(window_name)[0]
            return window.left, window.top
        except:
            return None
    
    # Actions performed with pyautogui to join the game from inside another game. Needs to have entered the lobby from start screen to be able to work. Utilized through the "Next game" button
    def join_game(self):
        try:
            if len(self.window_names) == 0:
                self.console.log_message("No window(s) opened", 2)
                return
            self.console.log_message("Attempting next game join", 1)
            sleep_delay = 0.1
            for name in self.window_names:
                if "MAIN" in name: # main character should not join, only create
                    continue
                position = self.get_window_position(name)
                self.get_window_front(name)
                if position:
                    # coordinates are on 1920x1080 windows
                    if not self.legacy: # positions for non-legacy
                        time.sleep(sleep_delay)
                        pyautogui.press("esc")
                        time.sleep(sleep_delay)
                        pyautogui.moveTo(position[0]+644, position[1]+353)
                        pyautogui.click(x=position[0]+644, y=position[1]+353) # coord for left click on exit menu
                        time.sleep(sleep_delay)
                        pyautogui.moveTo(position[0]+258, position[1]+540)
                        pyautogui.click(x=position[0]+258, y=position[1]+540) # coord for left click on friend list symbol
                        time.sleep(sleep_delay)
                        pyautogui.moveTo(position[0]+355, position[1]+128)
                        pyautogui.click(x=position[0]+355, y=position[1]+128) # coord for left click on friend list bar
                        time.sleep(sleep_delay)
                        pyautogui.moveTo(position[0]+350, position[1]+159)
                        pyautogui.rightClick(x=position[0]+350, y=position[1]+159) # coord for right click on the friend
                        time.sleep(sleep_delay)
                        pyautogui.moveTo(position[0]+430, position[1]+271)
                        pyautogui.click(x=position[0]+430, y=position[1]+271) # coord for left click on join game
                        time.sleep(sleep_delay)
                        self.console.log_message(f"{name} joined a new game", 1)
                    else: # positions for legacy
                        time.sleep(sleep_delay)
                        pyautogui.press("esc")
                        time.sleep(sleep_delay)
                        pyautogui.moveTo(position[0]+386, position[1]+279)
                        pyautogui.click(x=position[0]+386, y=position[1]+279) # coord for left click on exit menu
                        time.sleep(sleep_delay)
                        pyautogui.moveTo(position[0]+258, position[1]+540)
                        pyautogui.click(x=position[0]+258, y=position[1]+540) # coord for left click on friend list symbol
                        time.sleep(sleep_delay)
                        pyautogui.moveTo(position[0]+355, position[1]+128)
                        pyautogui.click(x=position[0]+355, y=position[1]+128) # coord for left click on friend list bar
                        time.sleep(sleep_delay)
                        pyautogui.moveTo(position[0]+350, position[1]+159)
                        pyautogui.rightClick(x=position[0]+350, y=position[1]+159) # coord for right click on the friend
                        time.sleep(sleep_delay)
                        pyautogui.moveTo(position[0]+430, position[1]+271)
                        pyautogui.click(x=position[0]+430, y=position[1]+271) # coord for left click on join game
                        time.sleep(sleep_delay)
                        self.console.log_message(f"{name} joined a new game", 1)
                else:
                    self.console.log_message("No valid window position", 3)      
            self.legacy = False
            
            for name in self.window_names:
                if "MAIN" in name:
                    self.get_window_front(name)
                    break
               
            self.resize_window_game()
            
        except:
            self.console.log_message("Failed to join next game", 3)
    
    # Performs the change by pressing the change graphic key for each window. Utilized through the "legacy" button
    def change_to_legacy(self):
        if len(self.window_names) == 0:
            self.console.log_message("No window(s) opened", 2)
            return
        self.console.log_message("Attempting to change to legacy graphics", 1)
        for name in self.window_names:
            if "MAIN" in name:
                continue
            try:
                position = self.get_window_position(name)
                self.get_window_front(name)
                time.sleep(0.1)
                pyautogui.press("'") # Make sure this key is your key to change graphics
                time.sleep(0.1)
                pyautogui.moveTo(position[0]+534, position[1]+392)
                pyautogui.click(x=position[0]+534, y=position[1]+392) # coord for left click on exit menu
                time.sleep(0.1)
                self.console.log_message(f"Changed {name} to legacy graphic", 1)
            except:
                self.console.log_message(f"Error changing to legacy for {name}", 3)
        self.legacy = True
        
        for name in self.window_names:
            if "MAIN" in name:
                self.get_window_front(name)
                break
    
    # Re-sizes all windows to 1920x1080 currently to be able to go into games
    def resize_window_start(self):
        try:
            self.console.log_message("Attempting to re-size window(s)", 1)
            for name in self.window_names:
                window = pygetwindow.getWindowsWithTitle(name)[0]
                current_width, current_height = window.size
                if current_width != 1920 or current_height != 1080:
                    window.resizeTo(1920,1080)
                    self.console.log_message(f"Re-sized {name} to 1920x1080", 1)
                    
            for name in self.window_names:
                if "MAIN" in name:
                    self.get_window_front(name)
                    break

        except:
            self.console.log_message(f"Failed to re-size {name} on launch", 2)

    # Re-sizes all "joiners" when they are in-game by pressing the "Legacy" button
    def resize_window_game(self):
        try:
            if len(self.window_names) == 0:
                self.console.log_message("No window(s) opened", 2)
                return
            self.console.log_message("Attempting to re-size window(s)", 1)
            for name in self.window_names:
                if not "MAIN" in name:
                    window = pygetwindow.getWindowsWithTitle(name)[0]
                    window.resizeTo(800,600)
                    self.console.log_message(f"Re-sized {name} to 800x600", 1)
            for name in self.window_names:
                if "MAIN" in name:
                    self.get_window_front(name)
                    break
        except:
            self.console.log_message(f"Failed to re-size {name}", 2)
    
    # iterates the processes to get active D2R's and their PID's
    def get_pids(self):
        pids = []
        for process in psutil.process_iter(["pid", "name"]):
            if process.info["name"] == "D2R.exe":
                pids.append(process.info["pid"])
        return pids
    
    # Terminates the selected process
    def terminate_pid(self):
        try:
            self.console.log_message("Attempting to terminate PID(s)", 1)
            terminated_names = []
            for name, var in self.checkbox_dict.items():
                if var.get() == 1:
                    pid = self.process_info.get(name)
                    if pid is not None:
                        handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, pid)
                        win32process.TerminateProcess(handle, 0)
                        win32api.CloseHandle(handle)
                        self.console.log_message(f"PID: {pid} for {name} terminated", 1)
                        terminated_names.append(name)
            # remove the clients from the lists if terminated
            for name in terminated_names:
                del self.process_info[name]
                if name in self.window_names:
                    self.window_names.remove(name)
            terminated_names = []
            self.console.log_message("Checkbox for termination closed", 1)
            self.checkbox_window.destroy()
        except:
            self.console.log_message(f"Failed to terminate PID", 3)

    # continuously scans for processes to remove the in-active pids
    def check_active_processes(self):
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
                    self.console.log_message(f"Removed {name} because not active", 2)
            except:
                self.console.log_message(f"Error checking active processes", 3)
            time.sleep(1)


    # Checkbox window to list all active PID's and selection for termination
    def checkbox(self):
        self.checkbox_window = tk.Toplevel(self.parent)
        self.checkbox_window.title("Select clients")
        x = self.parent.winfo_x()
        y = self.parent.winfo_y()
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
        self.console.log_message("Checkbox for termination opened", 1)
    
    # Just a close function
    def close_checkbox(self):
        self.console.log_message("Checkbox for termination closed", 1)
        self.checkbox_window.destroy()
    
    def enter_lobby(self, name):
        for key in self.process_info.keys():
            if "[MAIN]" and name in key:
                name = key
        if "[MAIN]" in name:
            return
        position = self.get_window_position(name)
        pyautogui.moveTo(position[0]+1104, position[1]+975)
        pyautogui.click(x=position[0]+1104, y=position[1]+975) # press enter lobby
        time.sleep(0.1)
        pyautogui.moveTo(position[0]+1227, position[1]+289)
        pyautogui.click(x=position[0]+1227, y=position[1]+289) # press first game
        pyautogui.click(x=position[0]+1227, y=position[1]+289) 
        pyautogui.click(x=position[0]+1227, y=position[1]+289) 
        self.console.log_message(f"{name} in game", 1)

    def is_target_image_present_two(self):
        
        target_image_path = Path(__file__).parent / "Pictures" / "Start.png"
        target_image = cv2.imread(str(target_image_path))

        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
        result = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)
        
        threshold = 0.8
        loc = np.where(result >= threshold)
        
        if len(loc[0]) > 0:
            return True
        
        return False