import os
import shutil
import subprocess
import sys

def copy_folder(src, dest):
    """
    Recursively copy a folder from src to dest.
    """
    try:
        shutil.copytree(src, dest)
        print(f"Folder copied from {src} to {dest}")
    except shutil.Error as e:
        print(f'Error: {e}')
    except OSError as e:
        print(f'Error: {e}')

def convert_m4a_to_mp3(directory):
    """
    Recursively convert all M4A files found in the directory to MP3 format.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".m4a"):
                m4a_path = os.path.join(root, file)
                mp3_path = os.path.splitext(m4a_path)[0] + '.mp3'
                try:
                    subprocess.run(['ffmpeg', '-i', m4a_path, mp3_path], check=True)
                    print(f"Converted {m4a_path} to {mp3_path}")
                except subprocess.CalledProcessError as e:
                    print(f'Error during conversion: {e}')


def delete_m4a_files(directory):
    """
    Delete all M4A files in the specified directory.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if  ("m4a") in file:
                m4a_path = os.path.join(root, file)
                try:
                    os.remove(m4a_path)
                    print(f"Deleted {m4a_path}")
                except OSError as e:
                    print(f'Error deleting file {m4a_path}: {e}')


if __name__ == "__main__":
    print("=" * 70)
    print("CONVERT AUDIO")
    print("=" * 70)
    print("WHAT THIS DOES:")
    print("  1. Copies the source folder to a destination folder")
    print("  2. Recursively converts all .m4a files to .mp3 format (using ffmpeg)")
    print("  3. Deletes all original .m4a files from the destination")
    print("")
    print("PARAMETERS:")
    print("  <source-folder>  (required) Path to folder containing .m4a files")
    print("  <dest-folder>    (required) Destination folder for converted files")
    print("")
    
    if len(sys.argv) < 3:
        print("ERROR: Missing required parameters")
        print("")
        print("USAGE:")
        print("  python3 convert-audio.py <source-folder> <dest-folder>")
        print("")
        print("EXAMPLE:")
        print("  python3 convert-audio.py data/original data/converted")
        print("  python3 convert-audio.py /path/to/source /path/to/destination")
        print("")
        print("PARAMETER EXPLANATION:")
        print("  <source-folder>: Must be a path to an existing directory containing")
        print("                   .m4a audio files to convert.")
        print("                   Can be relative (e.g., 'data/original') or absolute.")
        print("")
        print("  <dest-folder>:  Destination folder where files will be copied and")
        print("                   converted. Will be created if it doesn't exist.")
        print("                   Can be relative (e.g., 'data/converted') or absolute.")
        sys.exit(1)
    
    source_folder = sys.argv[1]
    destination_folder = sys.argv[2]
    
    # Validate source folder
    if not os.path.isdir(source_folder):
        print(f"ERROR: '{source_folder}' is not a valid directory.")
        print("")
        print("PARAMETER EXPLANATION:")
        print("  <source-folder>: Must be a path to an existing directory containing")
        print("                   .m4a audio files to convert.")
        print("                   Can be relative (e.g., 'data/original') or absolute.")
        sys.exit(1)
    
    print(f"Source folder: {source_folder}")
    print(f"Destination folder: {destination_folder}")
    print("=" * 70)
    print("")
    
    copy_folder(source_folder, destination_folder)
    convert_m4a_to_mp3(destination_folder)
    delete_m4a_files(destination_folder)
