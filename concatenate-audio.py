import os
import re
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

# Example usage
if __name__ == "__main__":
    current_directory = os.getcwd()
    sub_folder_name = "data/twice-in-a-lifetime"  # Change if needed
    source_folder_path = os.path.join(current_directory, sub_folder_name)

    concatenate_audio(source_folder_path)
