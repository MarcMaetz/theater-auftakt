import os
import shutil
import subprocess

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

src_folder = '/path/to/source/folder'  # Replace with your source folder path
dest_folder = '/path/to/destination/folder'  # Replace with your destination folder path

copy_folder(src_folder, dest_folder)
convert_m4a_to_mp3(dest_folder)
