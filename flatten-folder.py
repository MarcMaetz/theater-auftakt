import os
import shutil

def copy_and_rename_files(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            # Get the current folder name
            folder_name = os.path.basename(root)
            # Construct the new file name with the folder name prepended
            new_file_name = f"{folder_name}_{file}"
            # Define full paths
            old_file_path = os.path.join(root, file)
            new_file_path = os.path.join(destination_folder, new_file_name)
            # Copy and rename the file
            shutil.copy(old_file_path, new_file_path)
            print(f"Copied: {old_file_path} -> {new_file_path}")

# Example usage
current_directory = os.getcwd()
sub_folder_name = "data/twice-in-a-lifetime"
source_folder_path = os.path.join(current_directory, sub_folder_name)
destination_folder_path = current_directory + "/data/twice-in-a-lifetime-flat"
copy_and_rename_files(source_folder_path, destination_folder_path)
