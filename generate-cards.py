import os
import json
import uuid
import shutil
from datetime import datetime
import re
import zipfile

def create_directory(path, meta_info):
    """Create a directory and its directory.meta file."""
    os.makedirs(path, exist_ok=True)
    meta_path = os.path.join(path, "directory.meta")
    with open(meta_path, "w") as meta_file:
        json.dump(meta_info, meta_file)

def copy_and_rename_audio_files(source_paths, destination_dir, uuids):
    """Copy and rename audio files to the destination directory with UUID names."""
    for original_path, uuid_name in zip(source_paths, uuids):
        new_path = os.path.join(destination_dir, f"{uuid_name}.m4a")
        shutil.copyfile(original_path, new_path)

def generate_card_meta(card_dir_path, card_name, card_uuid, base_timestamp, audio_uuids, pair_index):
    """Generate and save a card.meta file."""
    card_meta = {
        "name": card_name,
        "id": card_uuid,
        "created": int(base_timestamp - (len(audio_uuids) - pair_index) * 100000),
        "order": audio_uuids
    }
    meta_path = os.path.join(card_dir_path, "card.meta")
    with open(meta_path, "w") as meta_file:
        json.dump(card_meta, meta_file)

def process_audio_files(subdir_path, destination_dir, base_timestamp):
    """Process all audio files in a subdirectory, creating card folders and meta files."""
    audio_files = sorted(f for f in os.listdir(subdir_path) if f.endswith('.m4a'))
    if len(audio_files) % 2 != 0:
        audio_files.append(None)  # Ensure even number of files for pairing

    audio_files = sorted(audio_files, key=extract_number)

    for i in range(0, len(audio_files), 2):
        card_uuid = str(uuid.uuid4())
        card_dir_path = os.path.join(destination_dir, card_uuid + '-[]')
        os.makedirs(card_dir_path, exist_ok=True)

        audio_uuids = [str(uuid.uuid4()), str(uuid.uuid4())]
        source_paths = [os.path.join(subdir_path, audio_files[i]) if audio_files[i] else "",
                        os.path.join(subdir_path, audio_files[i+1]) if audio_files[i+1] else ""]
        source_paths = [path for path in source_paths if path]  # Filter out empty paths

        copy_and_rename_audio_files(source_paths, card_dir_path, audio_uuids)
        generate_card_meta(card_dir_path, f"C-{i//2 + 1:04d}", card_uuid, base_timestamp, audio_uuids, i)

def extract_number(filename):
    match = re.search(r'\((\d+)\)', filename)
    return int(match.group(1)) if match else 1

def generate_meta_files(source_folder_path, destination_folder_path):
    if not os.path.exists(source_folder_path):
        print("The source folder does not exist.")
        return

    main_dir_uuid = str(uuid.uuid4())
    main_dir_path = os.path.join(destination_folder_path, main_dir_uuid + '-*')
    create_directory(main_dir_path, {"name": os.path.basename(source_folder_path), "id": main_dir_uuid + '-*'})

    base_timestamp = datetime.now().timestamp() * 1000

    for subdir_name in os.listdir(source_folder_path):
        subdir_path = os.path.join(source_folder_path, subdir_name)
        if os.path.isdir(subdir_path):
            sub_dir_uuid = str(uuid.uuid4())
            sub_dir_path = os.path.join(main_dir_path, sub_dir_uuid + '-*')
            create_directory(sub_dir_path, {"name": subdir_name, "id": sub_dir_uuid + '-*'})
            process_audio_files(subdir_path, sub_dir_path, base_timestamp)

    return main_dir_path

def zip_folder(folder_path, zip_path):
    """
    Zip the contents of a folder to a zip file.
    
    :param folder_path: Path to the folder to be zipped
    :param zip_path: Path to the output zip file
    """
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))



# Adjusted example usage setup
current_directory = os.getcwd()
sub_folder_name = "data/der-besuch-der-alten-dame"
source_folder_path = os.path.join(current_directory, sub_folder_name)
destination_folder_path = os.path.join(current_directory, "data")
main_dir_path = generate_meta_files(source_folder_path, destination_folder_path)
output_zip = os.path.join(destination_folder_path, 'der-besuch-der-alten-dame.zip')
zip_folder(main_dir_path, output_zip)
