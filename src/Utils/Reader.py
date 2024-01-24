#import win32api
import win32gui
import win32process
import time
import threading
from ctypes import *
from pymem import *

class MemoryReader:
    def __init__(self, root, console, client_obj, game_tracker, overlay):
        self._root = root
        self._console = console
        self._client_obj = client_obj
        self._game_tracker = game_tracker
        self._overlay_gametime_obj = overlay
        self.hWnd = None
        self.pid = None
        self.handle = None
        self._base_address = None
        self._ingame_address = None
        self._charname_address = None
        self._gamename_address = None
        self._password_address = None
        self.in_game = None
        self._fail_counter = 0
        
        self.stop_event = threading.Event()
        self._overlay_gametime_obj.run()

    def read_memory(self, handle, address, data_type):
        """Function to read data from the specified memory address"""
        buffer = handle.read_bytes(address, struct.calcsize(data_type))
        return struct.unpack(data_type, buffer)[0]

    def get_in_game_info(self):
        """Function to get information about in game status"""
        window_name = None
        for name in self._client_obj.window_names:
            if "[MAIN]" in name:
                window_name = name
        self.hWnd = win32gui.FindWindow(0, window_name)
        self.pid = win32process.GetWindowThreadProcessId(self.hWnd)[1]
        self.handle = Pymem()
        self.handle.open_process_from_id(self.pid)

        self._base_address = self.handle.process_base.lpBaseOfDll
        self._ingame_address = self._base_address + 0x2301DA0

        try:
            self.in_game = self.read_memory(self.handle, self._ingame_address, "i")
            if self.in_game:
                self._game_tracker.in_game = True
                return self.in_game
            else:
                self._game_tracker.in_game = False
                return self.in_game
        except:
            if self.hWnd and self._fail_counter < 3:
                self._console.log_message(f"Failed to read in game", 3)
                self._fail_counter += 1
            if self._fail_counter == 3:
                self._root.destroy_objects()
            return self.in_game

    def check_in_game_status(self):
        """Function to continuously check and update the in-game status"""
        reported_in_game = False
        while not self.stop_event.is_set():
            in_game = self.get_in_game_info()

            if in_game and not reported_in_game:
                self._game_tracker.start_tracking()
                reported_in_game = True
            elif not in_game and reported_in_game:
                self._game_tracker.stop_tracking()
                reported_in_game = False
                self._game_tracker.average_time()

            self._game_tracker.update_time()
            self._overlay_gametime_obj.update_label()          
            time.sleep(1)
     
    def get_charname_info(self):
        """Function to get char name"""
        window_name = None
        for name in self._client_obj.window_names:
            if "[MAIN]" in name:
                window_name = name
        self.hWnd = win32gui.FindWindow(0, window_name)
        self.pid = win32process.GetWindowThreadProcessId(self.hWnd)[1]
        self.handle = Pymem()
        self.handle.open_process_from_id(self.pid)

        self._base_address = self.handle.process_base.lpBaseOfDll
        self._charname_address = self._base_address + 0x25b4460
         
        try:
            pointer_to_charname = self.read_memory(self.handle, self._charname_address, "P")
            charname = self.handle.read_string(pointer_to_charname)
            return charname
        except:
            self._console.log_message(f"Failed to read char name", 3)
            return ""

    def get_gamename_info(self):
        """Function to get the game name"""
        window_name = None
        for name in self._client_obj.window_names:
            if "[MAIN]" in name:
                window_name = name
        self.hWnd = win32gui.FindWindow(0, window_name)
        self.pid = win32process.GetWindowThreadProcessId(self.hWnd)[1]
        self.handle = Pymem()
        self.handle.open_process_from_id(self.pid)

        self._base_address = self.handle.process_base.lpBaseOfDll
        self._gamename_address = self._base_address + 0x29f3ce0
        
        try:
            pointer_to_gamename = self.read_memory(self.handle, self._gamename_address, "P")
            gamename = self.handle.read_string(pointer_to_gamename)
            return gamename
        except:
            self._console.log_message(f"Failed to read game name", 3)
            return ""
        
    def get_password_info(self):
        """Function to get the game password"""
        window_name = None
        for name in self._client_obj.window_names:
            if "[MAIN]" in name:
                window_name = name
        self.hWnd = win32gui.FindWindow(0, window_name)
        self.pid = win32process.GetWindowThreadProcessId(self.hWnd)[1]
        self.handle = Pymem()
        self.handle.open_process_from_id(self.pid)

        self._base_address = self.handle.process_base.lpBaseOfDll
        self._password_address = self._base_address + 0x29f3d38
        
        try:
            pointer_to_password = self.read_memory(self.handle, self._password_address, "P")
            password = self.handle.read_string(pointer_to_password)
            return password
        except:
            self._console.log_message(f"Failed to read password", 3)
            return ""
    
    def load_game_info(self):
        """Function to get load game status"""
        window_name = None
        for name in self._client_obj.window_names:
            window_name = name
            hWnd = win32gui.FindWindow(0, window_name)
            pid = win32process.GetWindowThreadProcessId(hWnd)[1]
            handle = Pymem()
            handle.open_process_from_id(pid)
            base_address = self._base_address
            self._load_game_address = base_address + 0x2159E48

            try:
                load_complete = self.read_memory(handle, self._load_game_address, "i")
                while not load_complete:
                    time.sleep(1)
                else:
                    self._client_obj.resize_window_game()
                    self._client_obj.change_to_legacy()
            except:
                self._console.log_message(f"Failed to read load game info", 3)