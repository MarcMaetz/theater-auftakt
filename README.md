# Theater Auftakt Audio Processing Scripts

This repository contains Python scripts for processing audio files for theater productions. All scripts are designed to be run from the command line with explicit parameters - nothing is hard-coded.

## Quick Start for Non-Technical Users

**For users who prefer a graphical interface**, use the GUI launcher:

```bash
python3 gui-launcher.py
```

This provides a simple point-and-click interface for all four tools. See [DISTRIBUTION.md](DISTRIBUTION.md) for instructions on creating standalone executables.

## Prerequisites

- **Python 3** (tested with Python 3.x)
- **pydub** - For audio manipulation
  ```bash
  pip install pydub
  ```
- **ffmpeg** - Required for audio conversion (used by `convert-audio.py`)
  - Install via your system package manager or download from [ffmpeg.org](https://ffmpeg.org/)

## Scripts Overview

1. **flatten-folder.py** - Flattens nested directory structures
2. **convert-audio.py** - Converts M4A files to MP3 format
3. **concatenate-audio.py** - Concatenates multiple audio files into one
4. **generate-cards.py** - Generates card-based structure with meta files

---

## 1. flatten-folder.py

**What it does:**
Flattens a nested directory structure into a single folder. All files are copied to the destination with normalized names:
- Numbers in filenames are padded to 4 digits (e.g., '3' → '0003')
- Files are prefixed with their original folder name (e.g., 'Scene1_file.m4a')
- Preserves sorting order by normalizing numbers

**Usage:**
```bash
python3 flatten-folder.py <source-folder> <dest-folder>
```

**Parameters:**
- `<source-folder>` (required) - Path to folder with nested subdirectories to flatten
- `<dest-folder>` (required) - Destination folder for flattened files (will be created if it doesn't exist)

**Examples:**
```bash
# Relative paths
python3 flatten-folder.py data/my-nested-folder data/flattened

# Absolute paths
python3 flatten-folder.py /path/to/source /path/to/destination
```

**Notes:**
- Source folder must exist
- Destination folder will be created automatically if it doesn't exist
- Original files are copied, not moved (source files remain unchanged)

---

## 2. convert-audio.py

**What it does:**
Converts all M4A audio files to MP3 format. The script:
1. Copies the source folder to the destination folder
2. Recursively converts all `.m4a` files to `.mp3` format (using ffmpeg)
3. Deletes all original `.m4a` files from the destination

**Usage:**
```bash
python3 convert-audio.py <source-folder> <dest-folder>
```

**Parameters:**
- `<source-folder>` (required) - Path to folder containing `.m4a` files to convert
- `<dest-folder>` (required) - Destination folder for converted files (will be created if it doesn't exist)

**Examples:**
```bash
# Relative paths
python3 convert-audio.py data/original data/converted

# Absolute paths
python3 convert-audio.py /path/to/source /path/to/destination
```

**Notes:**
- Requires `ffmpeg` to be installed and available in PATH
- Source folder is copied first, then conversion happens in the destination
- Original `.m4a` files are deleted from destination after conversion
- Source folder remains unchanged

---

## 3. concatenate-audio.py

**What it does:**
Concatenates all `.m4a` audio files from subdirectories into a single output file. Files are processed in sorted order:
- Subdirectories are processed in alphabetical order
- Files within each subdirectory are sorted by number in parentheses (e.g., `audio (1).m4a`, `audio (2).m4a`)

**Usage:**
```bash
python3 concatenate-audio.py <source-folder> <output-file>
```

**Parameters:**
- `<source-folder>` (required) - Path to folder containing subdirectories with `.m4a` files
- `<output-file>` (required) - Full path where the concatenated audio will be saved

**Examples:**
```bash
# Relative paths
python3 concatenate-audio.py data/twice-in-a-lifetime ./final_audio.m4a

# Absolute paths
python3 concatenate-audio.py data/twice-in-a-lifetime /path/to/output.m4a
```

**Notes:**
- Only processes `.m4a` files in subdirectories (not top-level files)
- Output directory will be created if it doesn't exist
- Output format is MP4 (M4A container)

---

## 4. generate-cards.py

**What it does:**
Generates a card-based structure from audio files for use in theater production systems. The script:
- Processes `.m4a` files from the input folder and its subdirectories
- Pairs audio files (2 files per card)
- Creates UUID-based folder structure with meta files
- Generates `directory.meta` and `card.meta` JSON files
- Optionally creates a zip file of the output

**Usage:**
```bash
python3 generate-cards.py <input-folder> <output-folder> [--no-zip]
```

**Parameters:**
- `<input-folder>` (required) - Path to folder containing `.m4a` files (can be in subdirectories)
- `<output-folder>` (required) - Destination folder for generated cards (will be created if it doesn't exist)
- `[--no-zip]` (optional) - Skip creating zip file (zip is created by default)

**Examples:**
```bash
# With zip file (default)
python3 generate-cards.py data/twice-in-a-lifetime data/output

# Without zip file
python3 generate-cards.py data/twice-in-a-lifetime data/output --no-zip

# Absolute paths
python3 generate-cards.py /path/to/input /path/to/output
```

**Notes:**
- Processes top-level `.m4a` files first, then subdirectories
- Files are paired (2 per card) based on sorted order
- Each card gets a unique UUID and folder structure
- Output includes JSON meta files for directory and card information
- Zip file is created in the output folder by default

---

## Common Workflow

A typical workflow might be:

1. **Flatten** nested recordings into a single folder:
   ```bash
   python3 flatten-folder.py data/recordings data/flattened
   ```

2. **Convert** M4A files to MP3 (if needed):
   ```bash
   python3 convert-audio.py data/flattened data/converted
   ```

3. **Generate cards** for the production system:
   ```bash
   python3 generate-cards.py data/flattened data/cards
   ```

4. **Concatenate** all audio into a single file (for review):
   ```bash
   python3 concatenate-audio.py data/flattened ./final_review.m4a
   ```

---

## Error Handling

All scripts include built-in validation and will display helpful error messages if:
- Required parameters are missing
- Specified folders/files don't exist
- Paths are invalid

Each script will show usage instructions and parameter explanations when run incorrectly.

---

## Notes

- All scripts support both relative and absolute paths
- Output directories are created automatically if they don't exist
- Source files are never modified (only copied/converted in destination)
- All scripts can be run independently - there's no required execution order
