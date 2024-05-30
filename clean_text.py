import re

def remove_non_ascii(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Remove characters outside the ASCII range
    cleaned_content = ''.join(char for char in content if ord(char) < 128)

    with open(input_file, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)

def replace_tabs(input_file):
    try:
        with open(input_file, 'r') as file:
            content = file.read()

        modified_content = re.sub(r'\t+', ': ', content)

        with open(input_file, 'w') as file:
            file.write(modified_content)

        print("Tab characters replaced successfully.")
    except IOError:
        print("Error: File not found or cannot be read.")

def remove_leading_and_trailing_spaces(file_path):
    try:
        # Open the file in read mode
        with open(file_path, 'r') as file:
            # Read the content of the file
            lines = file.readlines()

        # Remove leading and trailing spaces from each line
        modified_lines = [line.strip() for line in lines]

        # Open the file in write mode and write the modified content
        with open(file_path, 'w') as file:
            for line in modified_lines:
                file.write(line + '\n')

        print("Leading and trailing spaces removed successfully.")
    except IOError:
        print("Error: File not found or cannot be read.")

def remove_blank_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            # Read the content of the file
            lines = file.readlines()

        modified_lines = [line.strip() for line in lines if line.strip()]

        with open(file_path, 'w') as file:
            for line in modified_lines:
                file.write(line + '\n')

        print("Blank or empty lines removed successfully.")
    except IOError:
        print("Error: File not found or cannot be read.")

def remove_emails_and_html_tags(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()

        content_without_emails = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', content)

        content_without_tags = re.sub(r'<[^>]*>', '', content_without_emails)

        content_without_url = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', content_without_tags)

        with open(file_path, 'w') as file:
            file.write(content_without_url)

        print("Emails and HTML tags removed successfully.")
    except IOError:
        print("Error: File not found or cannot be read.")

def add_full_stop(file_path):
    try:
        # Open the file in read mode
        with open(file_path, 'r') as file:
            # Read the content of the file
            lines = file.readlines()

        # Check each line and add a period if needed
        modified_lines = []
        for line in lines:
            line = line.strip()  # Remove leading and trailing whitespace
            if line and not line.endswith(('?', '!', '.')):
                line = line.rstrip() + '.'  # Remove trailing spaces and add a period at the end
            modified_lines.append(line)

        # Open the file in write mode and write the modified content
        with open(file_path, 'w') as file:
            for line in modified_lines:
                if line:  # Write non-empty lines only
                    file.write(line + '\n')

        print("Full stops added successfully.")
    except IOError:
        print("Error: File not found or cannot be read.")

def clean_text(input_file):
    replace_tabs(input_file)
    remove_leading_and_trailing_spaces(input_file)
    remove_emails_and_html_tags(input_file)
    add_full_stop(input_file)
    remove_blank_lines(input_file)
    remove_non_ascii(input_file)

