import os
import json
import uuid
import shutil
from datetime import datetime

def generate_meta_files(source_folder_path, destination_folder_path):
    # Check if the source folder exists
    if not os.path.exists(source_folder_path):
        print("The source folder does not exist.")
        return

    # Create a new main directory for the directory.meta file and card folders
    main_dir_uuid = str(uuid.uuid4())
    main_dir_path = os.path.join(destination_folder_path, main_dir_uuid + '-*')
    os.makedirs(main_dir_path, exist_ok=True)

    # Create directory.meta file for the new main directory
    dir_meta = {
        "name": os.path.basename(source_folder_path),
        "id": main_dir_uuid + '-*'
    }
    with open(os.path.join(main_dir_path, "directory.meta"), "w") as dir_meta_file:
        json.dump(dir_meta, dir_meta_file)

    # Base timestamp for faking the creation date
    base_timestamp = datetime.now().timestamp() * 1000  # Current timestamp in milliseconds

    # Iterate through each subdirectory in the source folder
    for subdir in os.listdir(source_folder_path):
        subdir_path = os.path.join(source_folder_path, subdir)
        if os.path.isdir(subdir_path):
            # Get all audio files in the subdirectory, sorted alphabetically
            audio_files = sorted([f for f in os.listdir(subdir_path) if f.endswith('.m4a')])

            # Ensure there's an even number of files
            if len(audio_files) % 2 != 0:
                print(f"The number of audio files in {subdir} is not even.")
                continue

            # Re-arrange the audio files list so the last file goes first
            audio_files = [audio_files[-1]] + audio_files[:-1]

            # Process the files in pairs
            for i in range(0, len(audio_files), 2):
                # Generate UUID for card
                card_uuid = str(uuid.uuid4())

                # Create a directory for the card in the new main directory
                card_dir_path = os.path.join(main_dir_path, card_uuid + '-[]')
                os.makedirs(card_dir_path, exist_ok=True)

                # Generate new UUIDs for each audio file
                audio1, audio2 = str(uuid.uuid4()), str(uuid.uuid4())

                # Copy the audio files to the card directory with new names based on UUIDs
                audio_file_paths = [os.path.join(subdir_path, audio_files[i]),
                                    os.path.join(subdir_path, audio_files[i+1])]
                new_file_paths = [os.path.join(card_dir_path, audio1 + ".m4a"),
                                  os.path.join(card_dir_path, audio2 + ".m4a")]

                for original, new in zip(audio_file_paths, new_file_paths):
                    shutil.copyfile(original, new)

                # Create card.meta file
                card_meta = {
                    "name": f"C-{i//2 + 1:04d}",
                    "id": card_uuid,
                    "created": int(base_timestamp - (len(audio_files) - i) * 100000),
                    "order": [audio1, audio2]
                }
                with open(os.path.join(card_dir_path, "card.meta"), "w") as card_meta_file:
                    json.dump(card_meta, card_meta_file)

    return f"Meta files generated successfully in: {main_dir_path}"

# Example usage setup
current_directory = os.getcwd()
sub_folder_name = "data/der-besuch-der-alten-dame"
source_folder_path = os.path.join(current_directory, sub_folder_name)
destination_folder_path = current_directory + "/data"
result = generate_meta_files(source_folder_path, destination_folder_path)
print(result)
