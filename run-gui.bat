@echo off
REM Windows batch file to launch the GUI
python gui-launcher.py
if errorlevel 1 (
    echo.
    echo Python not found! Please install Python 3 from python.org
    echo Or make sure Python is in your PATH
    pause
)
