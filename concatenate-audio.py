import os
import re
import sys
from pydub import AudioSegment

def extract_number(filename):
    """Extracts the number from filenames like 'audio (123).m4a' for correct sorting."""
    match = re.search(r'\((\d+)\)', filename)
    return int(match.group(1)) if match else 1  # Default to 1 if no number is found

def concatenate_audio(source_folder_path, output_filename="final_audio.m4a"):
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

    # Export final concatenated audio to the script execution directory
    output_path = os.path.join(os.getcwd(), output_filename)
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
    print("  <output-file>    (optional) Output filename (default: final_audio.m4a)")
    print("")
    
    if len(sys.argv) < 2:
        print("ERROR: Missing required parameter <source-folder>")
        print("")
        print("USAGE:")
        print("  python3 concatenate-audio.py <source-folder> [output-file]")
        print("")
        print("EXAMPLE:")
        print("  python3 concatenate-audio.py data/twice-in-a-lifetime")
        print("  python3 concatenate-audio.py data/twice-in-a-lifetime my_output.m4a")
        sys.exit(1)
    
    source_folder = sys.argv[1]
    output_filename = sys.argv[2] if len(sys.argv) > 2 else "final_audio.m4a"
    
    # Validate source folder
    if not os.path.isdir(source_folder):
        print(f"ERROR: '{source_folder}' is not a valid directory.")
        print("")
        print("PARAMETER EXPLANATION:")
        print("  <source-folder>: Must be a path to an existing directory containing")
        print("                   subdirectories with .m4a audio files.")
        print("                   Can be relative (e.g., 'data/my-folder') or absolute.")
        sys.exit(1)
    
    print(f"Source folder: {source_folder}")
    print(f"Output file: {output_filename}")
    print("=" * 70)
    print("")
    
    concatenate_audio(source_folder, output_filename)
