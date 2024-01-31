import os
import json
import uuid
import shutil
from datetime import datetime

def generate_meta_files(source_folder_path, destination_folder_path):
    if not os.path.exists(source_folder_path):
        print("The source folder does not exist.")
        return

    # Create a new main directory for the directory.meta file
    main_dir_uuid = str(uuid.uuid4())
    main_dir_path = os.path.join(destination_folder_path, main_dir_uuid + '-*')
    os.makedirs(main_dir_path, exist_ok=True)

    dir_meta = {
        "name": os.path.basename(source_folder_path),
        "id": main_dir_uuid + '-*'
    }
    with open(os.path.join(main_dir_path, "directory.meta"), "w") as dir_meta_file:
        json.dump(dir_meta, dir_meta_file)

    base_timestamp = datetime.now().timestamp() * 1000

    for subdir in os.listdir(source_folder_path):
        subdir_path = os.path.join(source_folder_path, subdir)
        if os.path.isdir(subdir_path):
            audio_files = sorted([f for f in os.listdir(subdir_path) if f.endswith('.m4a')])
            
            if len(audio_files) % 2 != 0:
                print(f"The number of audio files in {subdir} is not even.")
                continue

            audio_files = [audio_files[-1]] + audio_files[:-1]

            # Create a subdirectory for each source subdirectory within the main directory
            sub_dir_uuid = str(uuid.uuid4())
            sub_dir_path = os.path.join(main_dir_path, sub_dir_uuid + '-*')
            os.makedirs(sub_dir_path, exist_ok=True)

            # Replicate directory.meta for the subdirectory
            subdir_meta = {
                "name": subdir,
                "id": sub_dir_uuid + '-*'
            }
            with open(os.path.join(sub_dir_path, "directory.meta"), "w") as subdir_meta_file:
                json.dump(subdir_meta, subdir_meta_file)

            for i in range(0, len(audio_files), 2):
                card_uuid = str(uuid.uuid4())
                card_dir_path = os.path.join(sub_dir_path, card_uuid + '-[]')
                os.makedirs(card_dir_path, exist_ok=True)

                audio1, audio2 = str(uuid.uuid4()), str(uuid.uuid4())
                audio_file_paths = [os.path.join(subdir_path, audio_files[i]),
                                    os.path.join(subdir_path, audio_files[i+1])]
                new_file_paths = [os.path.join(card_dir_path, audio1 + ".m4a"),
                                  os.path.join(card_dir_path, audio2 + ".m4a")]

                for original, new in zip(audio_file_paths, new_file_paths):
                    shutil.copyfile(original, new)

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
