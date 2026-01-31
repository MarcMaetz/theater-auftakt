import os
import json
import uuid
import shutil
from datetime import datetime
import re
import zipfile
import sys


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
    """
    Extracts two numbers from a filename:
    - A leading number (e.g., '0003-Szene...')
    - A number in parentheses (e.g., '(0002)')
    
    Returns a tuple (leading_number, inner_number), defaulting to 0 if not found.
    This allows consistent and safe sorting.
    """
    # Try to find a number at the start of the filename
    match1 = re.match(r'(\d+)', filename)
    top_number = int(match1.group(1)) if match1 else 0

    # Try to find a number in parentheses
    match2 = re.search(r'\((\d+)\)', filename)
    inner_number = int(match2.group(1)) if match2 else 0

    return (top_number, inner_number)


def generate_meta_files(source_folder_path, destination_folder_path):
    if not os.path.exists(source_folder_path):
        print("The source folder does not exist.")
        return

    main_dir_uuid = str(uuid.uuid4())
    main_dir_path = os.path.join(destination_folder_path, main_dir_uuid + '-*')
    create_directory(main_dir_path, {"name": os.path.basename(source_folder_path), "id": main_dir_uuid + '-*'})

    base_timestamp = datetime.now().timestamp() * 1000

    # ✅ First: process top-level audio files
    top_audio_files = [f for f in os.listdir(source_folder_path) if f.endswith('.m4a')]
    if top_audio_files:
        sub_dir_uuid = str(uuid.uuid4())
        sub_dir_path = os.path.join(main_dir_path, sub_dir_uuid + '-*')
        create_directory(sub_dir_path, {"name": "_top_level", "id": sub_dir_uuid + '-*'})
        process_audio_files(source_folder_path, sub_dir_path, base_timestamp)

    # ✅ Then: process subdirectories
    for subdir_name in os.listdir(source_folder_path):
        subdir_path = os.path.join(source_folder_path, subdir_name)
        if os.path.isdir(subdir_path):
            sub_dir_uuid = str(uuid.uuid4())
            sub_dir_path = os.path.join(main_dir_path, sub_dir_uuid + '-*')
            create_directory(sub_dir_path, {"name": subdir_name, "id": sub_dir_uuid + '-*'})
            process_audio_files(subdir_path, sub_dir_path, base_timestamp)

    return main_dir_path


def zip_folder(folder_path):
    """
    Zip the contents of a folder to a zip file with the name of the folder.
    
    :param folder_path: Path to the folder to be zipped
    """
    folder_name = os.path.basename(folder_path)
    zip_name = f"{folder_name}.zip"
    zip_path = os.path.join(os.path.dirname(folder_path), zip_name)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))


if __name__ == "__main__":
    print("=" * 70)
    print("GENERATE CARDS")
    print("=" * 70)
    print("WHAT THIS DOES:")
    print("  Generates a card-based structure from audio files:")
    print("  - Processes .m4a files from the input folder and its subdirectories")
    print("  - Pairs audio files (2 files per card)")
    print("  - Creates UUID-based folder structure with meta files")
    print("  - Generates directory.meta and card.meta JSON files")
    print("  - Outputs to 'data/' folder and creates a zip file")
    print("")
    print("PARAMETERS:")
    print("  <input-folder>   (required) Path to folder containing .m4a files")
    print("  <output-folder>  (required) Destination folder for generated cards")
    print("  [--no-zip]       (optional) Skip creating zip file")
    print("")
    
    if len(sys.argv) < 3:
        print("ERROR: Missing required parameters")
        print("")
        print("USAGE:")
        print("  python3 generate-cards.py <input-folder> <output-folder> [--no-zip]")
        print("")
        print("EXAMPLE:")
        print("  python3 generate-cards.py data/twice-in-a-lifetime data/output")
        print("  python3 generate-cards.py /path/to/input /path/to/output --no-zip")
        print("")
        print("PARAMETER EXPLANATION:")
        print("  <input-folder>: Must be a path to an existing directory containing")
        print("                  .m4a audio files (can be in subdirectories).")
        print("                  Can be relative (e.g., 'data/my-folder') or absolute.")
        print("")
        print("  <output-folder>: Destination folder where card structure will be created.")
        print("                   Will be created if it doesn't exist.")
        print("                   Can be relative (e.g., 'data/output') or absolute.")
        print("")
        print("  [--no-zip]:     (optional) If provided, skip creating zip file.")
        print("                  By default, a zip file is created in the output folder.")
        sys.exit(1)

    source_folder_path = sys.argv[1]
    destination_folder_path = sys.argv[2]
    create_zip = "--no-zip" not in sys.argv
    
    # Validate input folder
    if not os.path.isdir(source_folder_path):
        print(f"ERROR: '{source_folder_path}' is not a valid directory.")
        print("")
        print("PARAMETER EXPLANATION:")
        print("  <input-folder>: Must be a path to an existing directory containing")
        print("                  .m4a audio files.")
        print("                  Can be relative (e.g., 'data/my-folder') or absolute.")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    if not os.path.exists(destination_folder_path):
        os.makedirs(destination_folder_path, exist_ok=True)
        print(f"Created output directory: {destination_folder_path}")
    
    print(f"Input folder: {source_folder_path}")
    print(f"Output folder: {destination_folder_path}")
    print(f"Create zip: {create_zip}")
    print("=" * 70)
    print("")
    
    main_dir_path = generate_meta_files(source_folder_path, destination_folder_path)
    if main_dir_path:
        print('')
        print(f"Output folder: {main_dir_path}")
        if create_zip:
            zip_folder(main_dir_path)
            print(f"Zipped to: {main_dir_path}.zip")
