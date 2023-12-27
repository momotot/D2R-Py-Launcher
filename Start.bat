@echo off
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command "& {Start-Process python -ArgumentList '.\src\Launcher.py' -WindowStyle Hidden -Verb RunAs}"
