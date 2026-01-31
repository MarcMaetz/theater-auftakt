#!/bin/bash
# Build script to create standalone executables for all scripts
# Requires: pip install pyinstaller

echo "Building executables for theater-auftakt scripts..."
echo ""

# Install PyInstaller if not already installed
pip install pyinstaller --quiet

# Build each script
echo "Building concatenate-audio..."
pyinstaller --onefile --name concatenate-audio concatenate-audio.py

echo "Building convert-audio..."
pyinstaller --onefile --name convert-audio convert-audio.py

echo "Building flatten-folder..."
pyinstaller --onefile --name flatten-folder flatten-folder.py

echo "Building generate-cards..."
pyinstaller --onefile --name generate-cards generate-cards.py

echo ""
echo "Executables created in 'dist' folder"
echo "Note: ffmpeg must be installed separately or bundled manually"
