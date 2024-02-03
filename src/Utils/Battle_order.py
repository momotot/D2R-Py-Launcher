import pyautogui
import pygetwindow
import time
import cv2
import numpy as np
from pathlib import Path

class BattleOrder():
    images_to_scan = ["act1", "act4", "wp", "pand", "rof", "portal", "rof_wp", "rogue_wp", "corner", "leg_act1",
                      "leg_act4_wp", "leg_corner", "leg_pand", "leg_portal", "leg_rof", "leg_rogue_wp", "leg_wp",
                      "leg_rof_wp"]

    def __init__(self, console, client_obj, legacy=None):
        self._console = console
        self._client_obj = client_obj
        self._legacy = legacy
        self.__sleep_delay = 1.25
        self.__bo_delay = 0.35

    def bo_action(self, position, name, warcry_keys):
        """Searches the area and does actions depending on where it is to cast bo at River of Flames"""
        self._legacy = self._client_obj.get_legacy_status()
        # Actions for non-legacy
        if not self._legacy:
            result = self.read_bo_image(name, conditions=["act1", "act4"])
            # Act1 was found
            if result and "act1" in result: 
                pyautogui.moveTo(position[0]+1186, position[1]+573)
                pyautogui.click(x=position[0]+1186, y=position[1]+573)
                time.sleep(self.__sleep_delay+0.5)
                find_rogue_wp = self.read_bo_image(name, conditions=["rogue_wp"])

                # First layout of wp in act1
                if find_rogue_wp and "rogue_wp" in find_rogue_wp:
                    rogue_x, rogue_y = find_rogue_wp["rogue_wp"]
                    pyautogui.moveTo(position[0]+rogue_x, position[1]+rogue_y)
                    pyautogui.click(x=position[0]+rogue_x, y=position[1]+rogue_y)
                    time.sleep(self.__sleep_delay)

                    self.non_legacy_act1_to_act4(position, name, warcry_keys)
            
                # Second layout of wp act1
                else:
                    pyautogui.moveTo(position[0]+290, position[1]+209)
                    pyautogui.click(x=position[0]+290, y=position[1]+209)
                    time.sleep(self.__sleep_delay)
                    pyautogui.moveTo(position[0]+663, position[1]+73)
                    pyautogui.click(x=position[0]+663, y=position[1]+73)
                    time.sleep(self.__sleep_delay)

                    find_rogue_wp = self.read_bo_image(name, conditions=["rogue_wp"])

                    if find_rogue_wp and "rogue_wp" in find_rogue_wp:
                        rogue_x, rogue_y = find_rogue_wp["rogue_wp"]
                        pyautogui.moveTo(position[0]+rogue_x, position[1]+rogue_y)
                        pyautogui.click(x=position[0]+rogue_x, y=position[1]+rogue_y)
                        time.sleep(self.__sleep_delay)

                        self.non_legacy_act1_to_act4(position, name, warcry_keys)

                for name in self._client_obj.window_names:
                    if "MAIN" in name:
                        self._client_obj.get_window_front(name)
                        break

            # Act4 was found
            elif result and "act4" in result:
                act4_result_x, act4_result_y = result["act4"]
                pyautogui.moveTo(position[0] + act4_result_x, position[1] + act4_result_y)
                pyautogui.click(x=position[0] + act4_result_x, y=position[1] + act4_result_y)
                time.sleep(self.__sleep_delay)

                self.non_legacy_act4(position, name, warcry_keys)

            for name in self._client_obj.window_names:
                if "MAIN" in name:
                    self._client_obj.get_window_front(name)
                    break
        # Actions for legacy
        else:
            result = self.read_bo_image(name, conditions=["leg_act1", "leg_corner"])
            # Act1 was found
            if result and "leg_act1" in result:
                pyautogui.moveTo(position[0]+911, position[1]+478)
                pyautogui.click(x=position[0]+911, y=position[1]+478)
                time.sleep(self.__sleep_delay)
                pyautogui.moveTo(position[0]+989, position[1]+410)
                pyautogui.click(x=position[0]+989, y=position[1]+410)
                time.sleep(self.__sleep_delay)
                find_rogue_wp = self.read_bo_image(name, conditions=["leg_rogue_wp"])
                # First layout of wp in act1
                if find_rogue_wp and "leg_rogue_wp" in find_rogue_wp:
                    rogue_x, rogue_y = find_rogue_wp["leg_rogue_wp"]
                    pyautogui.moveTo(position[0]+rogue_x, position[1]+rogue_y)
                    pyautogui.click(x=position[0]+rogue_x, y=position[1]+rogue_y)
                    time.sleep(self.__sleep_delay)

                    self.legacy_act1_to_act4(position, name, warcry_keys)

                # Second layout of wp in act1
                else:
                    pyautogui.moveTo(position[0]+208, position[1]+322)
                    pyautogui.click(x=position[0]+208, y=position[1]+322)
                    time.sleep(self.__sleep_delay-0.25)
                    pyautogui.moveTo(position[0]+632, position[1]+70)
                    pyautogui.click(x=position[0]+632, y=position[1]+70)
                    time.sleep(self.__sleep_delay)
                    pyautogui.moveTo(position[0]+518, position[1]+220)
                    pyautogui.click(x=position[0]+518, y=position[1]+220)
                    time.sleep(self.__sleep_delay-0.25)
                    find_rogue_wp = self.read_bo_image(name, conditions=["leg_rogue_wp"])

                    if find_rogue_wp and "leg_rogue_wp" in find_rogue_wp:
                        rogue_x, rogue_y = find_rogue_wp["leg_rogue_wp"]
                        pyautogui.moveTo(position[0]+rogue_x, position[1]+rogue_y)
                        pyautogui.click(x=position[0]+rogue_x, y=position[1]+rogue_y)
                        time.sleep(self.__sleep_delay)

                        self.legacy_act1_to_act4(position, name, warcry_keys)

                for name in self._client_obj.window_names:
                    if "MAIN" in name:
                        self._client_obj.get_window_front(name)
                        break

            # Act4 was found
            elif result and "leg_corner" in result:
                act4_result_x, act4_result_y = result["leg_corner"]
                pyautogui.moveTo(position[0] + act4_result_x, position[1] + act4_result_y)
                pyautogui.click(x=position[0] + act4_result_x, y=position[1] + act4_result_y)
                time.sleep(self.__sleep_delay)

                self.legacy_act4(position, name, warcry_keys)

                for name in self._client_obj.window_names:
                    if "MAIN" in name:
                        self._client_obj.get_window_front(name)
                        break
     
    def non_legacy_act1_to_act4(self, position, name, warcry_keys):
        """Actions from act1 to battle order for non-legacy graphics"""
        find_act4 = self.read_bo_image(name, conditions=["wp"])

        if find_act4 and "wp" in find_act4:
            act4_x, act4_y = find_act4["wp"]
            pyautogui.moveTo(position[0]+act4_x, position[1]+act4_y)
            pyautogui.click(x=position[0]+act4_x, y=position[1]+act4_y)
            time.sleep(self.__sleep_delay)
            find_rof = self.read_bo_image(name, conditions=["rof"])

            if find_rof and "rof" in find_rof:
                rof_x, rof_y = find_rof["rof"]
                pyautogui.moveTo(position[0] + rof_x, position[1] + rof_y)
                pyautogui.click(x=position[0] + rof_x, y=position[1] + rof_y)
                time.sleep(self.__sleep_delay)
                self.cast_battle_orders(warcry_keys)

                find_portal_or_wp = self.read_bo_image(name, conditions=["portal", "rof_wp"])

                if find_portal_or_wp and "portal" in find_portal_or_wp:
                    portal_x, portal_y = find_portal_or_wp["portal"]
                    pyautogui.moveTo(position[0] + portal_x, position[1] + portal_y)
                    pyautogui.click(x=position[0] + portal_x, y=position[1] + portal_y)
                    time.sleep(self.__sleep_delay)
                    pyautogui.moveTo(position[0]+858, position[1]+251)
                    pyautogui.click(x=position[0]+858, y=position[1]+251)
                    self._console.log_message("BO done", 1)

                elif find_portal_or_wp and "rof_wp" in find_portal_or_wp:
                    wp_x, wp_y = find_portal_or_wp["rof_wp"]
                    pyautogui.moveTo(position[0] + wp_x, position[1] + wp_y)
                    pyautogui.click(x=position[0] + wp_x, y=position[1] + wp_y)
                    time.sleep(self.__sleep_delay)
                    find_pand = self.read_bo_image(name, conditions=["pand"])

                    if find_pand and "pand" in find_pand:
                        pand_x, pand_y = find_pand["pand"]
                        pyautogui.moveTo(position[0] + pand_x, position[1] + pand_y)
                        pyautogui.click(x=position[0] + pand_x, y=position[1] + pand_y)
                        time.sleep(self.__sleep_delay)
                        pyautogui.moveTo(position[0] + 517, position[1] + 506)
                        pyautogui.click(x=position[0] + 517, y=position[1] + 506)
                        self._console.log_message("BO done", 1)
                else:                  
                    pyautogui.moveTo(position[0]+551, position[1]+234)
                    pyautogui.click(x=position[0]+551, y=position[1]+234)
                    time.sleep(self.__sleep_delay)
                    find_pand = self.read_bo_image(name, conditions=["pand"])

                    if find_pand and "pand" in find_pand:
                        pand_x, pand_y = find_pand["pand"]
                        pyautogui.moveTo(position[0] + pand_x, position[1] + pand_y)
                        pyautogui.click(x=position[0] + pand_x, y=position[1] + pand_y)
                        time.sleep(self.__sleep_delay)
                        pyautogui.moveTo(position[0] + 517, position[1] + 506)
                        pyautogui.click(x=position[0] + 517, y=position[1] + 506)
                        self._console.log_message("BO done", 1)

    def legacy_act1_to_act4(self, position, name, warcry_keys):
        """Actions from act1 to battle order for legacy graphics"""
        find_act4 = self.read_bo_image(name, conditions=["leg_wp"])

        if find_act4 and "leg_wp" in find_act4:
            act4_x, act4_y = find_act4["leg_wp"]
            pyautogui.moveTo(position[0]+act4_x, position[1]+act4_y)
            pyautogui.click(x=position[0]+act4_x, y=position[1]+act4_y)
            time.sleep(self.__sleep_delay)
            find_rof = self.read_bo_image(name, conditions=["leg_rof"])

            if find_rof and "leg_rof" in find_rof:
                rof_x, rof_y = find_rof["leg_rof"]
                pyautogui.moveTo(position[0] + rof_x, position[1] + rof_y)
                pyautogui.click(x=position[0] + rof_x, y=position[1] + rof_y)
                time.sleep(self.__sleep_delay)
                self.cast_battle_orders(warcry_keys)

                find_portal_or_wp = self.read_bo_image(name, conditions=["leg_portal", "leg_rof_wp"])

                if find_portal_or_wp and "leg_portal" in find_portal_or_wp:
                    portal_x, portal_y = find_portal_or_wp["leg_portal"]
                    pyautogui.moveTo(position[0] + portal_x, position[1] + portal_y)
                    pyautogui.click(x=position[0] + portal_x, y=position[1] + portal_y)
                    self._console.log_message("BO done", 1)

                elif find_portal_or_wp and "leg_rof_wp" in find_portal_or_wp:
                    wp_x, wp_y = find_portal_or_wp["leg_rof_wp"]
                    pyautogui.moveTo(position[0] + wp_x, position[1] + wp_y)
                    pyautogui.click(x=position[0] + wp_x, y=position[1] + wp_y)
                    time.sleep(self.__sleep_delay)
                    find_pand = self.read_bo_image(name, conditions=["leg_pand"])

                    if find_pand and "leg_pand" in find_pand:
                        pand_x, pand_y = find_pand["leg_pand"]
                        pyautogui.moveTo(position[0] + pand_x, position[1] + pand_y)
                        pyautogui.click(x=position[0] + pand_x, y=position[1] + pand_y)
                        self._console.log_message("BO done", 1)
                else:                  
                    pyautogui.moveTo(position[0]+563, position[1]+280) #
                    pyautogui.click(x=position[0]+563, y=position[1]+280) #
                    time.sleep(self.__sleep_delay)
                    find_pand = self.read_bo_image(name, conditions=["leg_pand"])

                    if find_pand and "leg_pand" in find_pand:
                        pand_x, pand_y = find_pand["leg_pand"]
                        pyautogui.moveTo(position[0] + pand_x, position[1] + pand_y)
                        pyautogui.click(x=position[0] + pand_x, y=position[1] + pand_y)
                        self._console.log_message("BO done", 1)
    
    def non_legacy_act4(self, position, name, warcry_keys):
        """Actions from act4 to battle order for non-legacy graphics"""
        find_rof = self.read_bo_image(name, conditions=["rof"])

        if find_rof and "rof" in find_rof:
            rof_x, rof_y = find_rof["rof"]
            pyautogui.moveTo(position[0] + rof_x, position[1] + rof_y)
            pyautogui.click(x=position[0] + rof_x, y=position[1] + rof_y)
            time.sleep(self.__sleep_delay)
            self.cast_battle_orders(warcry_keys)

            find_portal_or_wp = self.read_bo_image(name, conditions=["portal", "rof_wp"])

            if find_portal_or_wp and "portal" in find_portal_or_wp:
                portal_x, portal_y = find_portal_or_wp["portal"]
                pyautogui.moveTo(position[0] + portal_x, position[1] + portal_y)
                pyautogui.click(x=position[0] + portal_x, y=position[1] + portal_y)
                time.sleep(self.__sleep_delay)
                pyautogui.moveTo(position[0]+858, position[1]+251)
                pyautogui.click(x=position[0]+858, y=position[1]+251)
                self._console.log_message("BO done", 1)

            elif find_portal_or_wp and "rof_wp" in find_portal_or_wp:
                wp_x, wp_y = find_portal_or_wp["rof_wp"]
                pyautogui.moveTo(position[0] + wp_x, position[1] + wp_y)
                pyautogui.click(x=position[0] + wp_x, y=position[1] + wp_y)
                time.sleep(self.__sleep_delay)
                find_pand = self.read_bo_image(name, conditions=["pand"])

                if find_pand and "pand" in find_pand:
                    pand_x, pand_y = find_pand["pand"]
                    pyautogui.moveTo(position[0] + pand_x, position[1] + pand_y)
                    pyautogui.click(x=position[0] + pand_x, y=position[1] + pand_y)
                    time.sleep(self.__sleep_delay)
                    pyautogui.moveTo(position[0] + 517, position[1] + 506)
                    pyautogui.click(x=position[0] + 517, y=position[1] + 506)
                    self._console.log_message("BO done", 1)
            else:                  
                pyautogui.moveTo(position[0]+551, position[1]+234)
                pyautogui.click(x=position[0]+551, y=position[1]+234)
                time.sleep(self.__sleep_delay)
                find_pand = self.read_bo_image(name, conditions=["pand"])

                if find_pand and "pand" in find_pand:
                    pand_x, pand_y = find_pand["pand"]
                    pyautogui.moveTo(position[0] + pand_x, position[1] + pand_y)
                    pyautogui.click(x=position[0] + pand_x, y=position[1] + pand_y)
                    time.sleep(self.__sleep_delay)
                    pyautogui.moveTo(position[0] + 517, position[1] + 506)
                    pyautogui.click(x=position[0] + 517, y=position[1] + 506)
                    self._console.log_message("BO done", 1)

    def legacy_act4(self, position, name, warcry_keys):
        """Actions from act4 to battle order for legacy graphics"""
        find_act4_wp = self.read_bo_image(name, conditions=["leg_act4_wp"])

        if find_act4_wp and "leg_act4_wp" in find_act4_wp:
            act4_wp_x, act4_wp_y = find_act4_wp["leg_act4_wp"]
            pyautogui.moveTo(position[0] + act4_wp_x, position[1] + act4_wp_y)
            pyautogui.click(x=position[0] + act4_wp_x, y=position[1] + act4_wp_y)
            time.sleep(self.__sleep_delay)

            find_rof = self.read_bo_image(name, conditions=["leg_rof"])

            if find_rof and "leg_rof" in find_rof:
                rof_x, rof_y = find_rof["leg_rof"]
                pyautogui.moveTo(position[0] + rof_x, position[1] + rof_y)
                pyautogui.click(x=position[0] + rof_x, y=position[1] + rof_y)
                time.sleep(self.__sleep_delay)
                self.cast_battle_orders(warcry_keys)

                find_portal_or_wp = self.read_bo_image(name, conditions=["leg_portal", "leg_rof_wp"])

                if find_portal_or_wp and "leg_portal" in find_portal_or_wp:
                    portal_x, portal_y = find_portal_or_wp["leg_portal"]
                    pyautogui.moveTo(position[0] + portal_x, position[1] + portal_y)
                    pyautogui.click(x=position[0] + portal_x, y=position[1] + portal_y)
                    self._console.log_message("BO done", 1)

                elif find_portal_or_wp and "leg_rof_wp" in find_portal_or_wp:
                    wp_x, wp_y = find_portal_or_wp["leg_rof_wp"]
                    pyautogui.moveTo(position[0] + wp_x, position[1] + wp_y)
                    pyautogui.click(x=position[0] + wp_x, y=position[1] + wp_y)
                    time.sleep(self.__sleep_delay)
                    find_pand = self.read_bo_image(name, conditions=["leg_pand"])

                    if find_pand and "leg_pand" in find_pand:
                        pand_x, pand_y = find_pand["leg_pand"]
                        pyautogui.moveTo(position[0] + pand_x, position[1] + pand_y)
                        pyautogui.click(x=position[0] + pand_x, y=position[1] + pand_y)
                        self._console.log_message("BO done", 1)
                else:
                    pyautogui.moveTo(position[0]+563, position[1]+280) 
                    pyautogui.click(x=position[0]+563, y=position[1]+280) 
                    time.sleep(self.__sleep_delay)
                    find_pand = self.read_bo_image(name, conditions=["leg_pand"])

                    if find_pand and "leg_pand" in find_pand:
                        pand_x, pand_y = find_pand["leg_pand"]
                        pyautogui.moveTo(position[0] + pand_x, position[1] + pand_y)
                        pyautogui.click(x=position[0] + pand_x, y=position[1] + pand_y)
                        self._console.log_message("BO done", 1)

    def cast_battle_orders(self, warcry_keys):
        """Battle orders action"""
        self._console.log_message("Warcries now!", 1)
        for key in warcry_keys:
            pyautogui.press(f"{key}")
            pyautogui.rightClick()
            time.sleep(self.__bo_delay)

    def read_bo_image(self, name, conditions):
        """Searches for specific locations in act1/4 based on conditions"""
        self._client_obj.get_window_front(name)
        time.sleep(0.1)

        current_directory = Path(__file__).parent.parent
        image_templates = {}

        for condition in conditions:
            image_path = current_directory / "Pictures" / ("legacy" if "leg_" in condition else "") / f"{condition}.png"
            template = cv2.imread(str(image_path), cv2.IMREAD_COLOR).astype(np.uint8)
            image_templates[condition] = template

        window = pygetwindow.getWindowsWithTitle(name)[0]
        x, y, w, h = window.left, window.top, 1280, 720
        roi = pyautogui.screenshot(region=(x, y, w, h))

        screenshot = np.array(roi)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR).astype(np.uint8)

        results = {}

        for condition, template in image_templates.items():
            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.7
            loc = np.where(result >= threshold)

            if len(loc[0]) > 0:
                center_x = loc[1][0] + template.shape[1] // 2
                center_y = loc[0][0] + template.shape[0] // 2

                results[condition] = (center_x, center_y)

        if results:
            return results
        else:
            return None