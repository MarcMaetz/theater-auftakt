# Running the GUI in WSL

Yes, you can run the GUI directly in WSL! Here's how:

## Prerequisites

1. **Install tkinter** (required for GUI):
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3-tk
   ```

2. **Install Python dependencies** (if not already installed):
   ```bash
   pip3 install -r requirements.txt
   ```

## Running the GUI

### Option 1: WSLg (Windows 11 - Recommended)

If you're on **Windows 11**, WSLg is built-in and GUI apps work automatically:

```bash
cd /home/marc/code/theater-auftakt
python3 gui-launcher.py
```

The GUI window should appear automatically!

### Option 2: X11 Forwarding (Windows 10 or if WSLg doesn't work)

For **Windows 10** or if WSLg isn't working, you need an X server:

1. **Install an X server on Windows:**
   - [VcXsrv](https://sourceforge.net/projects/vcxsrv/) (recommended)
   - [X410](https://x410.dev/) (paid, but works well)
   - [Xming](https://sourceforge.net/projects/xming/)

2. **Start the X server** (VcXsrv example):
   - Launch "XLaunch"
   - Select "Multiple windows"
   - Select "Start no client"
   - Check "Disable access control" (for simplicity)
   - Finish

3. **Set DISPLAY variable in WSL:**
   ```bash
   export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0.0
   ```
   
   Or add to `~/.bashrc` to make it permanent:
   ```bash
   echo 'export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0.0' >> ~/.bashrc
   source ~/.bashrc
   ```

4. **Run the GUI:**
   ```bash
   cd /home/marc/code/theater-auftakt
   python3 gui-launcher.py
   ```

## Quick Test

Test if tkinter works:
```bash
python3 -c "import tkinter; tkinter.Tk().mainloop()"
```

If a window appears, you're all set!

## Troubleshooting

**"No module named 'tkinter'"**
- Install: `sudo apt-get install python3-tk`

**"Cannot connect to X server"**
- Make sure X server is running on Windows
- Check DISPLAY variable: `echo $DISPLAY`
- Try: `export DISPLAY=:0.0`

**Window doesn't appear**
- On Windows 11, WSLg should work automatically
- On Windows 10, ensure X server is running and DISPLAY is set correctly

## Advantages of Running in WSL

- ✅ No UNC path issues
- ✅ Native Linux environment
- ✅ All dependencies work naturally
- ✅ Can use Linux tools alongside the GUI
