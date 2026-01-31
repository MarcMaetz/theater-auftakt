#!/bin/bash

# Check if the destination folder is provided as an argument
if [ $# -lt 1 ]; then
    echo "Usage: $0 <destination-folder>"
    exit 1
fi

# Get the destination folder from the first argument
dest_folder="$1"

# Check if the destination folder exists
if [ ! -d "$dest_folder" ]; then
    echo "Error: Destination folder does not exist."
    exit 1
fi

# Iterate through all folders in the destination directory
for folder in "$dest_folder"/*/; do
    # Remove the trailing slash from the folder name
    folder_name=$(basename "$folder")

    # Check if the folder name contains ". " and rename it
    if [[ "$folder_name" =~ \. ]]; then
        new_folder_name=$(echo "$folder_name" | sed 's/\. /-/')

        # Rename the folder in the destination directory
        mv "$folder" "$dest_folder/$new_folder_name"

        echo "Renamed: '$folder_name' -> '$new_folder_name'"
    fi
done
