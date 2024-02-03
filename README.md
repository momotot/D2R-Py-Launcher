# D2R-Py-Launcher 1.1.1

![D2R-Py-Launcher](https://i.imgur.com/IrNneH6.png)
![D2R-Py-Launcher](https://i.imgur.com/NvEeKhT.png)

## Table of Contents

- [Description](#Description)
- [Disclaimer](#Disclaimer)
- [Features](#Features)
- [Requirements](#Requirements)
- [Installation / Usage](#Installation-Usage)
- [Troubleshooting](#troubleshooting)
- [License](#License)
- [Acknowledgements](#Acknowledgements)


## Description

D2R-Py-Launcher is a Python-based application to simplify the process of launching multiple instances of Diablo II: Resurrected (D2R).
Using keyboard inputs and mouse clicks to execute actions without write operations to game memory. Possible to monitor in-game time by reading game memory.
Display known map patterns and keep track of current and next terror zones.
Memory reading working for version 1.6.77312.

# Disclaimer

**Use at your own risk**

The software provided in this repository is distributed "as is" and with no warranties. The author and contributors are not responsible for any misuse, damage, loss of data, or any other consequences resulting from the use of this software.
The author disclaims any liability for any consequences arising from the us or misuse of this software.

## Features

- Launch multiple D2R clients.
- Automatic joining for leechers to your main characters game. Two seperate methods to choose from.
- Automatic BO (Battle Order) at River of Flames waypoint (Start from act1 or act4).
- Option to active overlay to monitor in-game time.
- Option to present known patterns in an overlay based on current area via tesseract OCR.
- Tracker of current and next TZ through d2emu.com.
- Console log for monitoring.
- Legacy settings option.
- Window resizing option.
- Termination of specific processes through the GUI.

## Requirements

- **Python Version:** Python 3.6 or later
- **External Modules:**
  - [pyautogui](https://pypi.org/project/PyAutoGUI/)
  - [PyGetWindow](https://pypi.org/project/PyGetWindow/)
  - [psutil](https://pypi.org/project/psutil/)
  - [pywin32](https://pypi.org/project/pywin32/)
  - [opencv-python](https://pypi.org/project/opencv-python/)
  - [numpy](https://pypi.org/project/numpy/)
  - [pymem](https://pypi.org/project/Pymem/)
  - [fuzzywuzzy](https://pypi.org/project/fuzzywuzzy/)
  - [requests](https://pypi.org/project/requests/)
  - Install via ```pip install -r requirements.txt``` 
- **Handle 64**
  - [Handle 64](https://learn.microsoft.com/en-us/sysinternals/downloads/handle): `Download it from microsoft`
- **Tesseract OCR**
  - [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)`Download it from the site linked`


## Installation-Usage

1. **Clone Repository:**
   ```bash
   git clone https://github.com/momotot/D2R-Py-Launcher.git
   cd D2R-Py-Launcher

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
4. **Handle64**
   ```bash
   Make sure to download handle64.exe and place it in the src folder

5. **Tesseract OCR**
   ```bash
   Download and install tesseract ocr: https://github.com/UB-Mannheim/tesseract/wiki

6. **Config setup**
   ```bash
   Setup your config.ini with your name, accountname, password and region/realm
   
   Example of config.ini:
   [momotot]
   username=momotot@D2R-Py-Launcher.com
   password=yourpassword
   region=eu.actual.battle.net (eu / na /kr)
   
7. **Run the app**
   ```bash
   Run the Start.bat file

8. **Joining games**
   ```bash
   After update its now possible to be in lobby, in start screen or in game when pressing next game.
   The only requirement is that the resolution of the joiners are 1280x720 for the pixel clicks to work.
   You can choose in the settings tab what method you prefer.
   If you have friend list join:
   - Joining is through friend list so the main char must be the only added account to the leechers friend list
   - The main character must be online (green status) on battle.net - this can sometimes be buggy!
   - You can be in either d2r or legacy graphic mode, both will work

9. **Battle Orders**
   ```bash
   Possibility to press BO button to let your Barbarian give you BO at River of Flames wp.
   Works from act1 or act4 in both non-legacy and legacy settings.
   You must have your Barbarian named as "BO" in the config.ini for it to work.
   BC must be set to the key F1, BO to F2 and Shout to F3.

## Troubleshooting

- Invalid D2R path: `ensure that you have selected the correct D2R.exe`
- Python version compatibility: `make sure that you are using Python 3.6 or later`

## License

This project is licensed under the MIT License.

## Acknowledgements

Thanks to Chobot@d2jsp for the original powershell script for handling the d2r processes.
Thanks to d2emu for the terror zone tracking.
