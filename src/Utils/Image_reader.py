import cv2
import numpy as np
import pytesseract
import pyautogui
import time
import pygetwindow
from fuzzywuzzy import fuzz
import re
import threading
import os

import Data.GameAreas as GameAreas
import Data.Pattern_info as pattern_info

class ImageReader():
    def __init__(self, overlay_pattern, console, window_name):
        self._console = console
        self._overlay_pattern = overlay_pattern
        self._area_text = "None"
        self._console.log_message("Image reader instance created", 1)
        self._window = pygetwindow.getWindowsWithTitle(window_name)[0]
        self.stop_event = threading.Event()
        self._overlay_pattern.run()

    # function to parse the image at the specific coords (top right corner) for 1920x1080 and get the area
    def get_current_area(self):
        tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        if not os.path.exists(tesseract_path):
            self._console.log_message("Tesseract path not found!", 3)
            return
        
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

        try:
            x, y, w, h = self._window.left + 1650, self._window.top + 71, 250, 30 
            roi = pyautogui.screenshot(region=(x, y, w, h))
            #roi.save("debug_prints/screenshot_debug.png") # enable if you want to debug
        except pygetwindow.PyGetWindowException as e:
            self._console.log_message(f"Image reader object destroyed", 1)
            self.stop_scan_for_area()
            return

        gray_roi = cv2.cvtColor(np.array(roi), cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray_roi, 120, 255, cv2.THRESH_BINARY)
        resized_roi = cv2.resize(gray_roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        #cv2.imwrite("debug_prints/thresh_debug.png", thresh)  # enable if you want to debug

        text = pytesseract.image_to_string(resized_roi).strip()

        # some words to exclude from the reading
        words_to_remove = ["Difficulty", "DieeicuLtty", "Dieseicutty", "Dreeicurty", "Dieseicurtty" ,"Dieeicutty", 
                           "Dieseicutty~", "DIeeicutty", "Disseicurty", "Diseicurty", "Diesercutty", "DieseicuLtty",
                            "HELL", "NIGHTMARE", "NigutTmarRe", "NigutTmare", "NORMAL", ":"]

        # parse the text from unwanted words
        def remove_words(text, words):
            for word in words:
                text = re.sub(re.escape(word), "", text, flags=re.IGNORECASE)
            return text.strip()
        
        cleaned_text = remove_words(text, words_to_remove)
        cleaned_text = cleaned_text.replace("@", "o")

        lines = cleaned_text.split('\n')
        if "Game" in lines[0] or "Gamé" in lines[0] or "Gar" in lines[0] or "GAME" in lines[0]:
            lines.pop(0)
        elif len(lines) >= 2:
            lines.pop(1)
        cleaned_text = '\n'.join(lines)
    
        best_match = None
        best_score = 0

        for area in GameAreas.GameAreas:
            score = fuzz.ratio(area.value[1].lower(), cleaned_text.lower())
            if score > best_score:
                best_score = score
                best_match = area
        
        similarity_threshold = 50
        if best_score >= similarity_threshold:
            return best_match
        else:
            return None

    # function to keep scanning every second
    def continuously_scan_for_area(self):
        while not self.stop_event.is_set():
            current_area = self.get_current_area()

            if current_area:
                area_name = current_area.name
                text_for_area = pattern_info.PatternInfo.area_texts.get(area_name, f"Text for {area_name}")
                self._area_text = text_for_area
            else:
                self._area_text = ""

            self._overlay_pattern.update_label()
            time.sleep(1)
    
    # function to stop scanning
    def stop_scan_for_area(self):
        self.stop_event.set()

    # getter function for the area text
    def get_area_text(self):
        return self._area_text