import requests
import threading
import time
from datetime import datetime

import Data.Areas

class TerrorZones():
    def __init__(self, root, launcher_obj, console):
        self._root = root
        self._launcher_obj = launcher_obj
        self._console = console
        self.previous_tz_info = None
        self.running = True
        self._first_time_info = False
        self.thread = threading.Thread(target=self.get_terror_zone)
        self.thread.start()

    def get_area_name(self, area_number):
        """Function to get the corresponding map for the area number"""
        area_num = Data.Areas.Area_mapping.area_mapping.get(area_number)
        return area_num

    def get_terror_zone(self):
        """Function to get the current terror zone from d2emu"""
        while self.running:
            current_time = datetime.now().time()
            if current_time.hour % 1 == 0 and current_time.minute == 0 and current_time.second in range(20) or not self._first_time_info:
                time_data_obtained = datetime.now().strftime('%I:%M%p')
                self.__tz_uri = "https://www.d2emu.com/api/v1/tz"
                
                try:
                    d2tz_response = requests.get(self.__tz_uri).json()
                    current_tz_list = []
                    next_tz_list = []
                    current_tz = ", ".join(map(str, d2tz_response["current"]))
                    next_tz = ", ".join(map(str, d2tz_response["next"]))
                
                    current_tz = current_tz.split(",")
                    for zone in current_tz:
                        zone = zone.strip()
                        zone_id = int(zone)
                        current_tz_list.append(self.get_area_name(zone_id))
                    
                    next_tz = next_tz.split(",")
                    for zone in next_tz:
                        zone = zone.strip()
                        zone_id = int(zone)
                        next_tz_list.append(self.get_area_name(zone_id))
                    
                    current_tz_str = ', '.join(current_tz_list)
                    next_tz_str = ', '.join(next_tz_list)

                    result_str = f"{current_tz_str} - {next_tz_str}"

                    if result_str != self.previous_tz_info:
                        self._console.log_message(f"Retrieved data at {time_data_obtained}", 1)
                        self._console.log_message(f"Current TZ: {current_tz_list}\nNext TZ: {next_tz_list}", 1)
                        self._launcher_obj.update_terror_zone_label(result_str)
                        self.previous_tz_info = result_str

                    self._first_time_info = True
                    time.sleep(10)
                        
                except Exception as e:
                    self._console.log_message(f"\n   Error retrieving TZ information: {e}", 3)
                    time.sleep(10)
            else:
                time.sleep(1)
        
    def stop_thread(self):
        """Stops the thread.."""
        self.running = False
        self.thread.join()
    
