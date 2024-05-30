import os

def split_text_max_char(input_file, output_folder, max_chars):
    """
    Recursively copy text from an input file to output files in a specified folder.
    Each output file will contain up to max_chars characters.
    If the last character is not a sentence-ending punctuation mark, look backward
    to the nearest such punctuation mark.
    """

    # Cleanup output folder
    if os.path.exists(output_folder):
        try:
            for filename in os.listdir(output_folder):
                file_path = os.path.join(output_folder, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"Deleted {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")
        except Exception as e:
            print(f"Failed to delete files in {output_folder}: {e}")
    else:
        print(f"Cleanup: The director '{output_folder}' does not exist.")

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Read the input file
    with open(input_file, 'r') as f:
        text = f.read()

    # Define sentence-ending punctuation marks
    end_punctuation = ['.', '?', '!']

    # Initialize variables
    start = 0
    end = max_chars
    file_count = 1
    total_char_count = 0

    while start < len(text):
        # Check if the end index is within the bounds of the string
        if end <= len(text):
            # Check if the last character is a sentence-ending punctuation mark
            if text[end - 1] in end_punctuation:
                # Write the text to an output file
                output_file = os.path.join(output_folder, f'output_{str(file_count).zfill(2)}.txt')
                with open(output_file, 'w') as out_file:
                    file_text = text[start:end]
                    out_file.write(file_text)
                    file_char_count = len(file_text)
                    total_char_count += file_char_count
                    print(f"File '{output_file}' has {file_char_count} characters.")

                # Update the start and end indices for the next file
                start = end
                end = start + max_chars
            else:
                # Find the nearest sentence-ending punctuation mark backward
                while end > start and text[end - 1] not in end_punctuation:
                    end -= 1

                # Write the text up to the found punctuation mark to an output file
                output_file = os.path.join(output_folder, f'output_{str(file_count).zfill(2)}.txt')
                with open(output_file, 'w') as out_file:
                    file_text = text[start:end]
                    out_file.write(file_text)
                    file_char_count = len(file_text)
                    total_char_count += file_char_count
                    print(f"File '{output_file}' has {file_char_count} characters.")

                # Update the start and end indices for the next file
                start = end
                end = start + max_chars

            # Update the file count
            file_count += 1
        else:
            # If the end index is out of bounds, write the remaining text to a file
            output_file = os.path.join(output_folder, f'output_{str(file_count).zfill(2)}.txt')
            with open(output_file, 'w') as out_file:
                file_text = text[start:]
                out_file.write(file_text)
                file_char_count = len(file_text)
                total_char_count += file_char_count
                print(f"File '{output_file}' has {file_char_count} characters.")
            break

    # Print the total character count across all output files
    print(f"Total characters across all output files: {total_char_count}")

    # Verify the total character count with the input file
    input_char_count = len(text)
    if total_char_count == input_char_count:
        print("The total character count across all output files matches the input file.")
    else:
        print("The total character count across all output files does not match the input file.")


