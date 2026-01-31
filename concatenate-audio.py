import os
import re
import sys
from pydub import AudioSegment

def extract_number(filename):
    """Extracts the number from filenames like 'audio (123).m4a' for correct sorting."""
    match = re.search(r'\((\d+)\)', filename)
    return int(match.group(1)) if match else 1  # Default to 1 if no number is found

def concatenate_audio(source_folder_path, output_path):
    """Concatenates all audio files in the same order as they would be processed."""
    full_audio = AudioSegment.silent(duration=0)  # Start with silence

    # Ensure the source folder exists
    if not os.path.exists(source_folder_path):
        print("Error: Source folder does not exist.")
        return

    # Process subdirectories in sorted order (as in original script)
    for subdir_name in sorted(os.listdir(source_folder_path)):
        subdir_path = os.path.join(source_folder_path, subdir_name)
        if os.path.isdir(subdir_path):
            audio_files = sorted(
                (f for f in os.listdir(subdir_path) if f.endswith('.m4a')),
                key=extract_number
            )

            # Process files one by one (instead of pairs)
            for audio_file in audio_files:
                source_path = os.path.join(subdir_path, audio_file)

                if os.path.exists(source_path):
                    audio_segment = AudioSegment.from_file(source_path, format="m4a")
                    full_audio += audio_segment  # Append in order

    # Export final concatenated audio
    full_audio.export(output_path, format="mp4")
    print(f"Final concatenated audio saved at: {output_path}")

if __name__ == "__main__":
    print("=" * 70)
    print("CONCATENATE AUDIO")
    print("=" * 70)
    print("WHAT THIS DOES:")
    print("  Concatenates all .m4a audio files from subdirectories into a single")
    print("  output file. Files are processed in sorted order (by subdirectory")
    print("  name, then by number in parentheses in filename).")
    print("")
    print("PARAMETERS:")
    print("  <source-folder>  (required) Path to folder containing subdirectories")
    print("                    with .m4a files to concatenate")
    print("  <output-file>    (required) Full path to output file (e.g., ./output.m4a)")
    print("")
    
    if len(sys.argv) < 3:
        print("ERROR: Missing required parameters")
        print("")
        print("USAGE:")
        print("  python3 concatenate-audio.py <source-folder> <output-file>")
        print("")
        print("EXAMPLE:")
        print("  python3 concatenate-audio.py data/twice-in-a-lifetime ./final_audio.m4a")
        print("  python3 concatenate-audio.py data/twice-in-a-lifetime /path/to/output.m4a")
        print("")
        print("PARAMETER EXPLANATION:")
        print("  <source-folder>: Must be a path to an existing directory containing")
        print("                   subdirectories with .m4a audio files.")
        print("                   Can be relative (e.g., 'data/my-folder') or absolute.")
        print("")
        print("  <output-file>:   Full path where the concatenated audio will be saved.")
        print("                   Can be relative (e.g., './output.m4a') or absolute.")
        print("                   Directory will be created if it doesn't exist.")
        sys.exit(1)
    
    source_folder = sys.argv[1]
    output_file = sys.argv[2]
    
    # Validate source folder
    if not os.path.isdir(source_folder):
        print(f"ERROR: '{source_folder}' is not a valid directory.")
        print("")
        print("PARAMETER EXPLANATION:")
        print("  <source-folder>: Must be a path to an existing directory containing")
        print("                   subdirectories with .m4a audio files.")
        print("                   Can be relative (e.g., 'data/my-folder') or absolute.")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        print(f"Created output directory: {output_dir}")
    
    print(f"Source folder: {source_folder}")
    print(f"Output file: {output_file}")
    print("=" * 70)
    print("")
    
    concatenate_audio(source_folder, output_file)
