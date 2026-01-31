import os
import shutil
import sys
import re

def pad_all_numbers(text):
    """
    Pad all standalone numbers in the string to 4 digits.
    E.g., 'Scene3', 'Scene (3)', '3_Scene' → 'Scene0003', etc.
    """
    return re.sub(r'(?<!\d)(\d+)(?!\d)', lambda m: f"{int(m.group(1)):04}", text)

def normalize_filename(filename):
    """
    Split filename from extension, pad numbers only in the name part.
    E.g., 'Recording3.m4a' → 'Recording0003.m4a'
    """
    name, ext = os.path.splitext(filename)
    return f"{pad_all_numbers(name)}{ext}"

def copy_and_rename_files(source_folder):
    """Flatten directory structure into '<source>-flat', normalizing names and preserving total order."""
    destination_folder = f"{source_folder}-flat"
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for root, dirs, files in os.walk(source_folder):
        # Normalize and sort folders and files
        dirs[:] = sorted(dirs, key=pad_all_numbers)
        files = sorted(files, key=pad_all_numbers)

        for file in files:
            # Special case: Recording.m4a becomes Recording0001.m4a
            normalized_file = normalize_filename("Recording0001.m4a" if file == "Recording.m4a" else file)

            folder_name = os.path.basename(root)
            normalized_folder_name = pad_all_numbers(folder_name)

            new_file_name = f"{normalized_folder_name}_{normalized_file}"

            old_file_path = os.path.join(root, file)
            new_file_path = os.path.join(destination_folder, new_file_name)

            shutil.copy(old_file_path, new_file_path)
            print(f"Copied: {old_file_path} -> {new_file_path}")

if __name__ == "__main__":
    print("=" * 70)
    print("FLATTEN FOLDER")
    print("=" * 70)
    print("WHAT THIS DOES:")
    print("  Flattens a nested directory structure into a single folder.")
    print("  All files are copied to '<source-folder>-flat' with normalized names:")
    print("  - Numbers in filenames are padded to 4 digits (e.g., '3' → '0003')")
    print("  - Files are prefixed with their folder name (e.g., 'Scene1_file.m4a')")
    print("  - Preserves sorting order by normalizing numbers")
    print("")
    print("PARAMETERS:")
    print("  <source-folder>  (required) Path to folder to flatten")
    print("")
    
    if len(sys.argv) != 2:
        print("ERROR: Missing or incorrect number of parameters")
        print("")
        print("USAGE:")
        print("  python3 flatten-folder.py <source-folder>")
        print("")
        print("EXAMPLE:")
        print("  python3 flatten-folder.py data/my-nested-folder")
        print("")
        print("PARAMETER EXPLANATION:")
        print("  <source-folder>: Must be a path to an existing directory with")
        print("                   nested subdirectories and files to flatten.")
        print("                   Can be relative (e.g., 'data/my-folder') or absolute.")
        print("                   Output will be created as '<source-folder>-flat'")
        sys.exit(1)

    source_folder = sys.argv[1]

    if not os.path.isdir(source_folder):
        print(f"ERROR: '{source_folder}' is not a valid directory.")
        print("")
        print("PARAMETER EXPLANATION:")
        print("  <source-folder>: Must be a path to an existing directory.")
        print("                   Can be relative (e.g., 'data/my-folder') or absolute.")
        sys.exit(1)

    print(f"Source folder: {source_folder}")
    print(f"Output folder: {source_folder}-flat")
    print("=" * 70)
    print("")

    copy_and_rename_files(source_folder)
