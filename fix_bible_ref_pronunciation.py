import re
import json
import os

def get_list_bible_ref_in_file(input_file):

    pattern = r'\b[a-zA-Z]+\.\s\d+:\d+\b'

    with open(input_file, 'r') as input_file:
        file_contents = input_file.read()

    matches = re.findall(pattern, file_contents)

    return matches

def create_dict_from_list_bible_ref(input_array, output_file):
    regex_pattern = r'\b[a-zA-Z]+\.'
    # Initialize an empty dictionary to store the unique values
    unique_values_dict = {}

    try:
        # Find all matches of the regex pattern in the input array
        all_matches = []
        for item in input_array:
            matches = re.findall(regex_pattern, item)
            all_matches.extend(matches)

        # Remove duplicates by converting the list of matches to a set
        unique_matches = set(all_matches)

        # Create dictionary entries for each unique match
        for match in unique_matches:
            unique_values_dict[match] = ''

        # Write the dictionary to a file
        with open(output_file, 'w') as output:
            json.dump(unique_values_dict, output)

    except Exception as e:
        print(f"Error: {e}")

    # Wait for the user to type "done" before ending the function
    print(f"Please enter the values for the keys in {output_file}. You can use ChatGPT to fill in the values. Type 'done' when finished.")
    user_input = input()
    while user_input.lower() != "done":
        user_input = input()

    return unique_values_dict

def rewrite_source_with_dic_values(input_file, json_dict_file):
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
        with open(input_file, 'w') as output:
            output.write(text)

        print("Replacement completed successfully.")

    except FileNotFoundError:
        print("Error: File not found.")

def rewrite_source_with_colon_replacement(input_file):
    # Define the corrected regex pattern
    pattern = r'\d+\s*:\s*\d+'

    # Read content from the input file
    with open(input_file, 'r') as f:
        content = f.read()

    # Replace the pattern with ","
    modified_content = re.sub(pattern, lambda x: x.group().replace(':', ','), content)

    # Write the modified content to the output file
    with open(input_file, 'w') as f:
        f.write(modified_content)

def fix_bible_ref_pron(input_file):
    source_bible_ref_dic='source_bible_ref_dic.json'
    list_bible_ref = get_list_bible_ref_in_file(input_file)
    create_dict_from_list_bible_ref(list_bible_ref, source_bible_ref_dic)
    rewrite_source_with_dic_values(input_file, source_bible_ref_dic)
    rewrite_source_with_colon_replacement(input_file)



    