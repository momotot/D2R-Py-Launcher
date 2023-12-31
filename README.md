# D2R-Py-Launcher 1.0.0

![D2R-Py-Launcher](https://i.imgur.com/Hj3DrG3.png)

## Table of Contents

- [Description](#Description)
- [Features](#Features)
- [Requirements](#Requirements)
- [Installation / Usage](#Installation-Usage)
- [Troubleshooting](#troubleshooting)
- [License](#License)
- [Acknowledgements](#Acknowledgements)


## Description

D2R-Py-Launcher is a Python-based application to simplify the process of launching multiple instances of Diablo II: Resurrected (D2R) on a single machine.
Using keyboard inputs and mouse clicks to execute actions without read/write operations to game memory.

## Features

- Launch multiple D2R clients.
- Automatic joining for leechers to your main characters game.
- Console log for monitoring.
- Termination of specific processes through the GUI.
- Legacy settings option.
- Window resizing option.

## Requirements

- **Python Version:** Python 3.6 or later
- **External Modules:**
  - [pyautogui](https://pypi.org/project/PyAutoGUI/): `pip install pyautogui`
  - [PyGetWindow](https://pypi.org/project/PyGetWindow/): `pip install PyGetWindow`
  - [psutil](https://pypi.org/project/psutil/): `pip install psutil`
  - [pywin32](https://pypi.org/project/pywin32/): `pip install pywin32`
- **Handle 64:**
- - [Handle 64](https://learn.microsoft.com/en-us/sysinternals/downloads/handle): `Download it from microsoft`


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

5. **Config setup**
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
```
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
