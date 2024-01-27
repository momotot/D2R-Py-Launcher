import pyautogui
import time

class GameJoiner():
    def __init__(self, console):
        self._console = console
        self.__sleep_delay = 0.1
        
    def start_screen_join_read(self, name, position, game_name, password):
        """Joins the game from start screen with method: memory reading"""
        try:
            pyautogui.moveTo(position[0]+755, position[1]+683)
            pyautogui.click(x=position[0]+755, y=position[1]+683) # press enter lobby
            time.sleep(self.__sleep_delay)
            pyautogui.moveTo(position[0]+857, position[1]+137)
            pyautogui.click(x=position[0]+857, y=position[1]+137) # click the game name label to write
            pyautogui.hotkey("ctrl", "a") # mark previous games, otherwise it can get messy..
            time.sleep(self.__sleep_delay)
            pyautogui.typewrite(game_name)
            time.sleep(self.__sleep_delay)
            pyautogui.moveTo(position[0]+1051, position[1]+138)
            pyautogui.click(x=position[0]+1051, y=position[1]+138) # click the password label to write
            pyautogui.hotkey("ctrl", "a")
            time.sleep(self.__sleep_delay)
            pyautogui.typewrite(password)
            pyautogui.press("enter")
            self._console.log_message(f"{name} joined a new game", 1)
        except:
            self._console.log_message(f"{name} failed to join game", 2)

    def lobby_join_read(self, name, position, game_name, password):
        """Joins the game from lobby with method: memory reading"""
        try:
            pyautogui.moveTo(position[0]+857, position[1]+137)
            pyautogui.click(x=position[0]+857, y=position[1]+137) # click the game name label to write
            pyautogui.hotkey("ctrl", "a") # mark previous games, otherwise it can get messy..
            time.sleep(self.__sleep_delay)
            pyautogui.typewrite(game_name)
            time.sleep(self.__sleep_delay)
            pyautogui.moveTo(position[0]+1051, position[1]+138)
            pyautogui.click(x=position[0]+1051, y=position[1]+138) # click the password label to write
            pyautogui.hotkey("ctrl", "a")
            time.sleep(self.__sleep_delay)
            pyautogui.typewrite(password)
            pyautogui.press("enter")
            self._console.log_message(f"{name} joined a new game", 1)
        except:
            self._console.log_message(f"{name} failed to join game", 2)

    def in_game_join_read(self, name, position, game_name, password, legacy):
        """Joins the game from in game with method: memory reading"""
        try:
            if not legacy:
                pyautogui.press("esc")
                time.sleep(self.__sleep_delay)
                pyautogui.moveTo(position[0]+645, position[1]+357)
                pyautogui.click(x=position[0]+645, y=position[1]+357) # coord for left click on exit menu
                time.sleep(self.__sleep_delay)                
                pyautogui.moveTo(position[0]+857, position[1]+137)
                pyautogui.click(x=position[0]+857, y=position[1]+137) # click the game name label to write
                pyautogui.hotkey("ctrl", "a") # mark previous games, otherwise it can get messy..
                time.sleep(self.__sleep_delay)
                pyautogui.typewrite(game_name)
                time.sleep(self.__sleep_delay)
                pyautogui.moveTo(position[0]+1051, position[1]+138)
                pyautogui.click(x=position[0]+1051, y=position[1]+138) # click the password label to write
                pyautogui.hotkey("ctrl", "a")
                time.sleep(self.__sleep_delay)
                pyautogui.typewrite(password)
                pyautogui.press("enter")
                self._console.log_message(f"{name} joined a new game", 1)
            else:
                pyautogui.press("esc")
                time.sleep(self.__sleep_delay)
                pyautogui.moveTo(position[0]+615, position[1]+325)
                pyautogui.click(x=position[0]+615, y=position[1]+325) # coord for left click on exit menu
                time.sleep(self.__sleep_delay)
                pyautogui.moveTo(position[0]+857, position[1]+137)
                pyautogui.click(x=position[0]+857, y=position[1]+137) # click the game name label to write
                pyautogui.hotkey("ctrl", "a") # mark previous games, otherwise it can get messy..
                time.sleep(self.__sleep_delay)
                pyautogui.typewrite(game_name)
                time.sleep(self.__sleep_delay)
                pyautogui.moveTo(position[0]+1051, position[1]+138)
                pyautogui.click(x=position[0]+1051, y=position[1]+138) # click the password label to write
                pyautogui.hotkey("ctrl", "a")
                time.sleep(self.__sleep_delay)
                pyautogui.typewrite(password)
                pyautogui.press("enter")
                self._console.log_message(f"{name} joined a new game", 1)
        except:
            self._console.log_message(f"{name} failed to join game", 2)

    def start_screen_join_friend(self, name, position):
        """Joins the game from start screen with method: friend join"""
        try:
            pyautogui.moveTo(position[0]+755, position[1]+683)
            pyautogui.click(x=position[0]+755, y=position[1]+683) # press enter lobby
            time.sleep(self.__sleep_delay)
            pyautogui.moveTo(position[0]+130, position[1]+546)
            pyautogui.click(x=position[0]+130, y=position[1]+546) # coord for left click on friend list symbol
            time.sleep(self.__sleep_delay)
            pyautogui.moveTo(position[0]+206, position[1]+140)
            pyautogui.click(x=position[0]+206, y=position[1]+140) # coord for left click on friend list bar
            time.sleep(self.__sleep_delay)
            pyautogui.moveTo(position[0]+204, position[1]+166)
            pyautogui.rightClick(x=position[0]+204, y=position[1]+166) # coord for right click on the friend
            time.sleep(self.__sleep_delay)
            pyautogui.moveTo(position[0]+336, position[1]+276)
            pyautogui.click(x=position[0]+336, y=position[1]+276) # coord for left click on join game
            time.sleep(self.__sleep_delay)
            self._console.log_message(f"{name} joined a new game", 1)
        except:
            self._console.log_message(f"{name} failed to join game", 2)

    def lobby_join_friend(self, name, position):
        """Joins the game from lobby with method: friend join"""
        try:
            pyautogui.moveTo(position[0]+130, position[1]+546)
            pyautogui.click(x=position[0]+130, y=position[1]+546) # coord for left click on friend list symbol
            time.sleep(self.__sleep_delay)
            pyautogui.moveTo(position[0]+206, position[1]+140)
            pyautogui.click(x=position[0]+206, y=position[1]+140) # coord for left click on friend list bar
            time.sleep(self.__sleep_delay)
            pyautogui.moveTo(position[0]+204, position[1]+166)
            pyautogui.rightClick(x=position[0]+204, y=position[1]+166) # coord for right click on the friend
            time.sleep(self.__sleep_delay)
            pyautogui.moveTo(position[0]+336, position[1]+276)
            pyautogui.click(x=position[0]+336, y=position[1]+276) # coord for left click on join game
            time.sleep(self.__sleep_delay)
            self._console.log_message(f"{name} joined a new game", 1)
        except:
            self._console.log_message(f"{name} failed to join game", 2)  

    def in_game_join_friend(self, name, position, legacy):
        """Joins the game from in game with method: friend join"""
        if not legacy:
            try:
                time.sleep(self.__sleep_delay)
                pyautogui.press("esc")
                time.sleep(self.__sleep_delay)
                pyautogui.moveTo(position[0]+647, position[1]+365)
                pyautogui.click(x=position[0]+647, y=position[1]+365) # coord for left click on exit menu
                time.sleep(self.__sleep_delay)
                pyautogui.moveTo(position[0]+130, position[1]+546)
                pyautogui.click(x=position[0]+130, y=position[1]+546) # coord for left click on friend list symbol
                time.sleep(self.__sleep_delay)
                pyautogui.moveTo(position[0]+206, position[1]+140)
                pyautogui.click(x=position[0]+206, y=position[1]+140) # coord for left click on friend list bar
                time.sleep(self.__sleep_delay)
                pyautogui.moveTo(position[0]+204, position[1]+166)
                pyautogui.rightClick(x=position[0]+204, y=position[1]+166) # coord for right click on the friend
                time.sleep(self.__sleep_delay)
                pyautogui.moveTo(position[0]+336, position[1]+276)
                pyautogui.click(x=position[0]+336, y=position[1]+276) # coord for left click on join game
                time.sleep(self.__sleep_delay)
                self._console.log_message(f"{name} joined a new game", 1)
            except:
                self._console.log_message(f"{name} failed to join game", 2)
        else:
            try:
                time.sleep(self.__sleep_delay)
                pyautogui.press("esc")
                time.sleep(self.__sleep_delay)
                pyautogui.moveTo(position[0]+615, position[1]+325)
                pyautogui.click(x=position[0]+615, y=position[1]+325) # coord for left click on exit menu
                time.sleep(self.__sleep_delay)
                pyautogui.moveTo(position[0]+130, position[1]+546)
                pyautogui.click(x=position[0]+130, y=position[1]+546) # coord for left click on friend list symbol
                time.sleep(self.__sleep_delay)
                pyautogui.moveTo(position[0]+206, position[1]+140)
                pyautogui.click(x=position[0]+206, y=position[1]+140) # coord for left click on friend list bar
                time.sleep(self.__sleep_delay)
                pyautogui.moveTo(position[0]+204, position[1]+166)
                pyautogui.rightClick(x=position[0]+204, y=position[1]+166) # coord for right click on the friend
                time.sleep(self.__sleep_delay)
                pyautogui.moveTo(position[0]+336, position[1]+276)
                pyautogui.click(x=position[0]+336, y=position[1]+276) # coord for left click on join game
                time.sleep(self.__sleep_delay)
                self._console.log_message(f"{name} joined a new game", 1)
            except:
                self._console.log_message(f"{name} failed to join game", 2)  
