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
    main_dir_path = os.path.join(destination_folder_path, main_dir_uuid + '-_')
    os.makedirs(main_dir_path)

    # Create directory.meta file for the new main directory
    dir_meta = {
        "name": os.path.basename(source_folder_path),
        "id": main_dir_uuid
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

        # Copy the audio files to the card directory
        for file in audio_files[i:i+2]:
            original_file_path = os.path.join(source_folder_path, file)
            new_file_path = os.path.join(card_dir_path, file)
            shutil.copyfile(original_file_path, new_file_path)

        # Create card.meta file
        card_meta = {
            "name": f"C-{i//2 + 1:04d}",
            "id": card_uuid,
            "created": int(base_timestamp - (len(audio_files) - i) * 100000),  # Ensure it's an integer
            "order": [str(uuid.uuid4()), str(uuid.uuid4())]  # Generate new UUIDs for each audio file
        }
        with open(os.path.join(card_dir_path, "card.meta"), "w") as card_meta_file:
            json.dump(card_meta, card_meta_file)

    return "Meta files generated successfully in: " + main_dir_path

current_directory = os.getcwd()
sub_folder_name = "data/der-besuch-der-alten-dame/1-akt-1-szene"
source_folder_path = os.path.join(current_directory, sub_folder_name)
destination_folder_path = current_directory + "/data"
result = generate_meta_files(source_folder_path, destination_folder_path)
print(result)

# Note: The actual file path needs to be provided, and the script should be run in an environment where it can execute.
