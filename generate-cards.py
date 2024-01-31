import os
import json
import uuid
import shutil
from datetime import datetime

def generate_meta_files(source_folder_path, destination_folder_path):
    # Check if the source folder exists
    if not os.path.exists(source_folder_path):
        return "The source folder does not exist."

    # Get all audio files in the source folder, sorted alphabetically
    audio_files = sorted([f for f in os.listdir(source_folder_path) if f.endswith('.m4a')])

    # Ensure there's an even number of files
    if len(audio_files) % 2 != 0:
        return "The number of audio files is not even."

    # Create a new main directory for the directory.meta file and card folders
    main_dir_uuid = str(uuid.uuid4())
    main_dir_path = os.path.join(destination_folder_path, main_dir_uuid + '-*')
    os.makedirs(main_dir_path)

    # Create directory.meta file for the new main directory
    dir_meta = {
        "name": os.path.basename(source_folder_path),
        "id": main_dir_uuid + '-*'
    }
    with open(os.path.join(main_dir_path, "directory.meta"), "w") as dir_meta_file:
        json.dump(dir_meta, dir_meta_file)

    # Base timestamp for faking the creation date
    base_timestamp = datetime.now().timestamp() * 1000  # Current timestamp in milliseconds

    # Process the files in pairs
    for i in range(0, len(audio_files), 2):
        # Generate UUID for card
        card_uuid = str(uuid.uuid4())

        # Create a directory for the card in the new main directory
        card_dir_path = os.path.join(main_dir_path, card_uuid + '-[]')
        os.makedirs(card_dir_path)

        # Generate new UUIDs for each audio file
        audio1 = str(uuid.uuid4())
        audio2 = str(uuid.uuid4())

        # Copy the audio files to the card directory with new names based on UUIDs
        audio_file_paths = [os.path.join(source_folder_path, audio_files[i]),
                            os.path.join(source_folder_path, audio_files[i+1])]
        new_file_paths = [os.path.join(card_dir_path, audio1 + ".m4a"),
                          os.path.join(card_dir_path, audio2 + ".m4a")]

        for original, new in zip(audio_file_paths, new_file_paths):
            shutil.copyfile(original, new)

        # Create card.meta file
        card_meta = {
            "name": f"C-{i//2 + 1:04d}",
            "id": card_uuid,
            "created": int(base_timestamp - (len(audio_files) - i) * 100000),  # Ensure it's an integer
            "order": [audio1, audio2]  
        }
        with open(os.path.join(card_dir_path, "card.meta"), "w") as card_meta_file:
            json.dump(card_meta, card_meta_file)

    return "Meta files generated successfully in: " + main_dir_path

# Example usage setup
current_directory = os.getcwd()
sub_folder_name = "data/der-besuch-der-alten-dame/1-akt-1-szene"
source_folder_path = os.path.join(current_directory, sub_folder_name)
destination_folder_path = current_directory + "/data"
result = generate_meta_files(source_folder_path, destination_folder_path)
print(result)
