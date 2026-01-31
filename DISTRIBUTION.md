# Distribution Guide for Non-Technical Users

This guide explains how to package these scripts for distribution to non-technical users.

## Option 1: GUI Launcher (Recommended)

The `gui-launcher.py` provides a simple graphical interface that doesn't require command-line knowledge.

### Quick Start on Windows

**If Python is already installed:**
- Double-click `run-gui.bat` to launch the GUI
- Or double-click `gui-launcher.py` and select Python when Windows asks

**To build a Windows executable:**
- Double-click `build-windows.bat` (requires Python + PyInstaller)
- This creates `dist\Theater-Auftakt.exe` that can be distributed

### Building Standalone Executable

**On Windows:**
1. Open Command Prompt in the project folder
2. Run: `build-windows.bat`
   - Or manually: `pyinstaller --onefile --windowed --name "Theater-Auftakt" gui-launcher.py`

**On Linux/Mac:**
1. **Install dependencies:**
   ```bash
   pip install pyinstaller
   ```

2. **Build the GUI executable:**
   ```bash
   pyinstaller --onefile --windowed --name "Theater-Auftakt" gui-launcher.py
   ```

3. **Distribute:**
   - The executable will be in the `dist` folder
   - **Windows:** `dist\Theater-Auftakt.exe` (double-click to run)
   - **Linux/Mac:** `dist/Theater-Auftakt` (may need execute permission)
   - **Note:** ffmpeg must still be installed separately or bundled

### Requirements for End Users

- **Windows:** ffmpeg.exe must be in PATH or same folder as executable
- **Mac/Linux:** ffmpeg must be installed via package manager

## Option 2: Individual Script Executables

Build each script separately:

```bash
# Install PyInstaller
pip install pyinstaller

# Build all scripts
bash build-executables.sh
```

Executables will be in the `dist` folder.

## Option 3: Python Package Distribution

For users who already have Python installed:

1. **Create a package:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run GUI:**
   - **Windows:** Double-click `run-gui.bat` or run `python gui-launcher.py`
   - **Linux/Mac:** Run `python3 gui-launcher.py`

## Distribution Checklist

- [ ] Test GUI on target platform
- [ ] Bundle ffmpeg or provide installation instructions
- [ ] Create user documentation (simplified README)
- [ ] Test all four scripts through GUI
- [ ] Package everything in a zip file
- [ ] Include installation instructions for ffmpeg

## User Instructions Template

For non-technical users, provide:

1. **Download and extract** the package
2. **Install ffmpeg** (link to download page)
3. **Double-click** `Theater-Auftakt.exe` (or run `python3 gui-launcher.py`)
4. **Use the tabs** to select which tool to use
5. **Browse** to select folders/files
6. **Click** the execute button
