import win32api
import win32gui
import win32process
import time
import threading
from ctypes import *
from pymem import *

class MemoryReader:
    def __init__(self, parent, console, client_obj, game_tracker, overlay):
        self.parent = parent
        self.console = console
        self.client_obj = client_obj
        self.game_tracker = game_tracker
        self.overlay_obj = overlay
        self.hWnd = None
        self.pid = None
        self.handle = None
        self.__base_address = None
        self.__ingame_address = None
        self.__charname_address = None
        self.__gamename_address = None
        self.__password_address = None
        self.in_game = None
        self.__fail_counter = 0
        
        self.stop_event = threading.Event()
        self.overlay_obj.run()

    # Function to read data from the specified memory address
    def read_memory(self, handle, address, data_type):
        buffer = handle.read_bytes(address, struct.calcsize(data_type))
        return struct.unpack(data_type, buffer)[0]

    # Function to get information about in game status
    def get_in_game_info(self):
        window_name = None
        for name in self.client_obj.window_names:
            if "[MAIN]" in name:
                window_name = name
        self.hWnd = win32gui.FindWindow(0, window_name)
        self.pid = win32process.GetWindowThreadProcessId(self.hWnd)[1]
        self.handle = Pymem()
        self.handle.open_process_from_id(self.pid)

        self.__base_address = self.handle.process_base.lpBaseOfDll
        self.__ingame_address = self.__base_address + 0x2301DA0

        try:
            self.in_game = self.read_memory(self.handle, self.__ingame_address, "i")
            if self.in_game:
                self.game_tracker.in_game = True
                return self.in_game
            else:
                self.game_tracker.in_game = False
                return self.in_game
        except:
            if self.hWnd and self.__fail_counter < 3:
                self.console.log_message(f"Failed to read in game", 3)
                self.__fail_counter += 1
            if self.__fail_counter == 3:
                self.parent.destroy_objects()
            return self.in_game
    
    #  Function to continuously check and update the in-game status
    def check_in_game_status(self):
        reported_in_game = False
        while not self.stop_event.is_set():
            in_game = self.get_in_game_info()

            if in_game and not reported_in_game:
                self.game_tracker.start_tracking()
                reported_in_game = True
            elif not in_game and reported_in_game:
                self.game_tracker.stop_tracking()
                reported_in_game = False
                self.game_tracker.average_time()

            self.game_tracker.update_time()
            self.overlay_obj.update_label()          
            time.sleep(1)
    
    # Function to get char name 
    def get_charname_info(self):
        window_name = None
        for name in self.client_obj.window_names:
            if "[MAIN]" in name:
                window_name = name
        self.hWnd = win32gui.FindWindow(0, window_name)
        self.pid = win32process.GetWindowThreadProcessId(self.hWnd)[1]
        self.handle = Pymem()
        self.handle.open_process_from_id(self.pid)

        self.__base_address = self.handle.process_base.lpBaseOfDll
        self.__charname_address = self.__base_address + 0x25b4460
         
        try:
            pointer_to_charname = self.read_memory(self.handle, self.__charname_address, "P")
            charname = self.handle.read_string(pointer_to_charname)
            return charname
        except:
            self.console.log_message(f"Failed to read char name", 3)
            return ""

    # Function to get the game name
    def get_gamename_info(self):
        window_name = None
        for name in self.client_obj.window_names:
            if "[MAIN]" in name:
                window_name = name
        self.hWnd = win32gui.FindWindow(0, window_name)
        self.pid = win32process.GetWindowThreadProcessId(self.hWnd)[1]
        self.handle = Pymem()
        self.handle.open_process_from_id(self.pid)

        self.__base_address = self.handle.process_base.lpBaseOfDll
        self.__gamename_address = self.__base_address + 0x29f3ce0
        
        try:
            pointer_to_gamename = self.read_memory(self.handle, self.__gamename_address, "P")
            gamename = self.handle.read_string(pointer_to_gamename)
            return gamename
        except:
            self.console.log_message(f"Failed to read game name", 3)
            return ""
        
    # Function to get the game password
    def get_password_info(self):
        window_name = None
        for name in self.client_obj.window_names:
            if "[MAIN]" in name:
                window_name = name
        self.hWnd = win32gui.FindWindow(0, window_name)
        self.pid = win32process.GetWindowThreadProcessId(self.hWnd)[1]
        self.handle = Pymem()
        self.handle.open_process_from_id(self.pid)

        self.__base_address = self.handle.process_base.lpBaseOfDll
        self.__password_address = self.__base_address + 0x29f3d38
        
        try:
            pointer_to_password = self.read_memory(self.handle, self.__password_address, "P")
            password = self.handle.read_string(pointer_to_password)
            return password
        except:
            self.console.log_message(f"Failed to read password", 3)
            return ""
    
    # Function to get load game status
    def load_game_info(self):
        window_name = None
        for name in self.client_obj.window_names:
            window_name = name
            hWnd = win32gui.FindWindow(0, window_name)
            pid = win32process.GetWindowThreadProcessId(hWnd)[1]
            handle = Pymem()
            handle.open_process_from_id(pid)
            base_address = self.__base_address
            self.__load_game_address = base_address + 0x2159E48

            try:
                load_complete = self.read_memory(handle, self.__load_game_address, "i")
                while not load_complete:
                    time.sleep(1)
                else:
                    self.client_obj.resize_window_game()
                    self.client_obj.change_to_legacy()
            except:
                self.console.log_message(f"Failed to read load game info", 3)