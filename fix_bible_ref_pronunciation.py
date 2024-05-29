import re
import json
import os

def list_bible_ref_in_file(input_file, output_file):

    # Define the regular expression pattern
    pattern = r'\b[a-zA-Z]+\.\s\d+:\d+\b'

    # Open the input file for reading
    with open(input_file, 'r') as input_file:
        # Read the contents of the input file
        file_contents = input_file.read()

    # Find all matches of the pattern in the file contents
    matches = re.findall(pattern, file_contents)

    # Open the output file for writing
    with open(output_file, 'w') as output_file:
        # Write each match to the output file, separated by a newline
        output_file.write('\n'.join(matches))

def create_dict_from_list_bible_ref(input_file, output_file):
    regex_pattern = r'\b[a-zA-Z]+\.'
    # Initialize an empty dictionary to store the unique values
    unique_values_dict = {}

    try:
        # Open the file in read mode
        with open(input_file, 'r') as file:
            # Read the contents of the file
            file_contents = file.read()
            
            # Find all matches of the regex pattern in the file contents
            matches = re.findall(regex_pattern, file_contents)
            
            # Remove duplicates by converting the list of matches to a set
            unique_matches = set(matches)
            
            # Create dictionary entries for each unique match
            for match in unique_matches:
                unique_values_dict[match] = ''
        # Write the dictionary to a file
        with open(output_file, 'w') as output:
            json.dump(unique_values_dict, output)

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")

    return unique_values_dict

def rewrite_source_with_dic_values(input_file, output_file, json_dict_file):
    try:
        # Open the JSON dictionary file and load its contents
        with open(json_dict_file, 'r') as json_file:
            json_dict = json.load(json_file)
        
        # Open the input text file to be processed
        with open(input_file, 'r') as file:
            text = file.read()
            
            # Iterate over each key-value pair in the dictionary
            for key, value in json_dict.items():
                # Use regular expression to find the key as a whole word in the text and replace it with the corresponding value
                text = text.replace(key, str(value))

        # Write the modified text to the output file
        with open(output_file, 'w') as output:
            output.write(text)

        print("Replacement completed successfully. Output written to", output_file)

    except FileNotFoundError:
        print("Error: File not found.")

import re

def rewrite_source_with_colon_replacement(input_file, output_file):
    # Define the corrected regex pattern
    pattern = r'\d+\s*:\s*\d+'

    # Read content from the input file
    with open(input_file, 'r') as f:
        content = f.read()

    # Replace the pattern with ","
    modified_content = re.sub(pattern, lambda x: x.group().replace(':', ','), content)

    # Write the modified content to the output file
    with open(output_file, 'w') as f:
        f.write(modified_content)



    