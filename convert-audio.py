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


def delete_m4a_files(directory):
    """
    Delete all M4A files in the specified directory.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".m4a"):
                m4a_path = os.path.join(root, file)
                try:
                    os.remove(m4a_path)
                    print(f"Deleted {m4a_path}")
                except OSError as e:
                    print(f'Error deleting file {m4a_path}: {e}')



current_directory = os.getcwd()
sub_folder_name = "data/der-besuch-der-alten-dame"
source_folder_path = os.path.join(current_directory, sub_folder_name)
destination_folder_path = current_directory + "/data/converted"

# copy_folder(source_folder_path, destination_folder_path)
# convert_m4a_to_mp3(destination_folder_path)
delete_m4a_files(destination_folder_path)
