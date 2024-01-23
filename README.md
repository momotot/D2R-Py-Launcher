# D2R-Py-Launcher 1.1.0

![D2R-Py-Launcher](https://i.imgur.com/rRtsjvu.png)
![D2R-Py-Launcher](https://i.imgur.com/r55eIRt.png)

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

D2R-Py-Launcher is a Python-based application to simplify the process of launching multiple instances of Diablo II: Resurrected (D2R) on a single machine.
Using keyboard inputs and mouse clicks to execute actions without write operations to game memory. Possible to monitor in-game time by reading game memory.
Packet reading working for version 1.6.77312.

# Disclaimer

**Use at your own risk**

The software provided in this repository is distributed "as is" and with no warranties. The author and contributors are not responsible for any misuse, damage, loss of data, or any other consequences resulting from the use of this software.
The author disclaims any liability for any consequences arising from the us or misuse of this software.

## Features

- Launch multiple D2R clients.
- Automatic joining for leechers to your main characters game.
- Console log for monitoring.
- Termination of specific processes through the GUI.
- Legacy settings option.
- Window resizing option.
- Option to active overlay to monitor in-game time.
- Option to present known patterns in an overlay based on current area via tesseract OCR.

## Requirements

- **Python Version:** Python 3.6 or later
- **External Modules:**
  - [pyautogui](https://pypi.org/project/PyAutoGUI/): `pip install pyautogui`
  - [PyGetWindow](https://pypi.org/project/PyGetWindow/): `pip install PyGetWindow`
  - [psutil](https://pypi.org/project/psutil/): `pip install psutil`
  - [pywin32](https://pypi.org/project/pywin32/): `pip install pywin32`
- **Handle 64:**
  - [Handle 64](https://learn.microsoft.com/en-us/sysinternals/downloads/handle): `Download it from microsoft`
- **Tesseract OCR:**
  - [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)`Download it from the site linked`


## Installation-Usage

1. **Clone Repository:**
   ```bash
   git clone https://github.com/momotot/D2R-Py-Launcher.git
   cd D2R-Py-Launcher

3. **Install dependencies:**
   ```bash
   pip install pyautogui PyGetWindow psutil pywin32
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
   In order to make the joining of next game to work there are some prerequisite:
   - All "leechers/joiners" must have entered lobby and joined a game from there
   - Joining is through friend list so the main char must be the only added account to the leechers friend list
   - The main character must be online (green status) on battle.net
   - You can be in either d2r or legacy graphic mode, both will work
   - Currently it will only work when you have re-sized with the re-size button

## Troubleshooting

- Invalid D2R path: `ensure that you have selected the correct D2R.exe`
- Python version compatibility: `make sure that you are using Python 3.6 or later`

## License

This project is licensed under the MIT License.

## Acknowledgements

Thanks to Chobot@d2jsp for the original powershell script for handling the d2r processes.
