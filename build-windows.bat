@echo off
REM Build script for Windows executables
REM Handle UNC paths (WSL network paths) by using pushd
pushd "%~dp0"

echo Building Theater-Auftakt for Windows...
echo.

REM Check if PyInstaller is installed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

echo.
echo Building executable...
pyinstaller --onefile --windowed --name "Theater-Auftakt" gui-launcher.py

if exist "dist\Theater-Auftakt.exe" (
    echo.
    echo SUCCESS! Executable created: dist\Theater-Auftakt.exe
    echo You can now distribute this .exe file to users.
) else (
    echo.
    echo ERROR: Build failed. Check the output above for errors.
)

pause
popd