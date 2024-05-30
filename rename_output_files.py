import os
import re

def rename_output_files(folder_path, heading_regex, heading_text):

    # Regular expression pattern to match the lesson number
    pattern = re.compile(heading_regex, re.MULTILINE)
    
    # Initialize variables to keep track of last lesson number
    last_lesson_number = 0
    last_part_numbers = {}
    
    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Check if the path is a file
        if os.path.isfile(file_path):
            # Open and read the file
            with open(file_path, 'r') as file:
                content = file.read()
                
                # Find all matches in the content
                matches = re.findall(pattern, content)
                
                # If matches are found, extract the lesson number from the first match
                if matches:
                    lesson_number = int(matches[0])
                else:
                    # If no match found, use the last lesson number from the previous file
                    lesson_number = last_lesson_number
                
                # Determine the part number for the lesson
                if lesson_number in last_part_numbers:
                    last_part_numbers[lesson_number] += 1
                else:
                    last_part_numbers[lesson_number] = 1
                
                part_number = last_part_numbers[lesson_number]
                
                # Update the last lesson number
                last_lesson_number = lesson_number
                
            # Close the file handle
            file.close()
                
            # Rename the file with the captured group
            new_filename = f"{heading_text}_{str(lesson_number).zfill(2)}_Part_{str(part_number).zfill(2)}.txt"
            new_file_path = os.path.join(folder_path, new_filename)
                
            # Attempt to rename the file
            try:
                os.rename(file_path, new_file_path)
                print(f"Renamed {filename} to {new_filename}")
            except PermissionError:
                print(f"Could not rename {filename}. File in use by another process.")


