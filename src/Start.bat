@echo off
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command "& {Start-Process python -ArgumentList '%~dp0Launcher.py' -WindowStyle Hidden -Verb RunAs}"
