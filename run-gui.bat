@echo off
REM Windows batch file to launch the GUI
REM Handle UNC paths (WSL network paths) by using pushd
pushd "%~dp0"

REM Try different Python commands (Windows may use py, python3, or python)
python gui-launcher.py 2>nul
if errorlevel 1 (
    py gui-launcher.py 2>nul
    if errorlevel 1 (
        python3 gui-launcher.py 2>nul
        if errorlevel 1 (
            echo.
            echo Python not found! Please install Python 3 from python.org
            echo Or make sure Python is in your PATH
            echo.
            echo Tried: python, py, python3
            pause
        )
    )
)

popd
