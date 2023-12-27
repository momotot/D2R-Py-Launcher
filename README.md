# D2R-Py-Launcher 1.0.0

## Table of Contents

- [Description](#Description)
- [Features](#Features)
- [Requirements](#Requirements)
- [Installation / Usage](#Installation)
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
- - [Handle 64](https://learn.microsoft.com/en-us/sysinternals/downloads/handle): 


## Installation / Usage

1. **Clone Repository:**
   ```bash
   git clone https://github.com/your-username/d2r-launcher.git
   cd d2r-launcher

3. **Install dependencies:**
   ```bash
   pip install pyautogui PyGetWindow psutil pywin32
4. **Handle64**
   ```bash
   Make sure you have handle64.exe and d2r_handle.txt in your src folder to be able to launch multiple D2R

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
## Troubleshooting

- Invalid D2R path: `ensure that you have selected the correct D2R.exe`
- Python version compatibility: `make sure that you are using Python 3.6 or later`

## License

This project is licensed under the MIT License.

## Acknowledgements

Thanks to Chobot@d2jsp for the original powershell script for handling the d2r processes.