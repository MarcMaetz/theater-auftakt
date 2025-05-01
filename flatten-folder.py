import os
import shutil
import sys

def copy_and_rename_files(source_folder):
    """Flatten directory structure into '<source>-flat', normalizing names and preserving total order."""
    # Destination: append "-flat" to the source folder name
    destination_folder = f"{source_folder}-flat"
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for root, dirs, files in os.walk(source_folder):
        dirs.sort()
        files.sort()

        for file in files:
            # Normalize 'Recording.m4a' → 'Recording (0).m4a'
            normalized_file = "Recording (0).m4a" if file == "Recording.m4a" else file

            folder_name = os.path.basename(root)
            new_file_name = f"{folder_name}_{normalized_file}"

            old_file_path = os.path.join(root, file)
            new_file_path = os.path.join(destination_folder, new_file_name)

            shutil.copy(old_file_path, new_file_path)
            print(f"Copied: {old_file_path} -> {new_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 flatten-folder.py <source-folder>")
        sys.exit(1)

    source_folder = sys.argv[1]

    if not os.path.isdir(source_folder):
        print(f"Error: '{source_folder}' is not a valid directory.")
        sys.exit(1)

    copy_and_rename_files(source_folder)
