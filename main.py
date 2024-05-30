from clean_text import clean_text
from fix_bible_ref_pronunciation import fix_bible_ref_pron
from split_text_max_char import split_text_max_char
from rename_output_files import rename_output_files
from text_to_audiobook import text_to_audiobook

def copy_source(source_file, source_file_copy):
    try:
        with open(source_file, 'r') as file:
            content = file.read()

        with open(source_file_copy, 'w') as file:
            file.write(content)

        print("Made a copy of source file successfully.")
    except IOError:
        print("Error: File not found or cannot be read.")


if __name__ == "__main__":
    source_file='source_file2.txt'
    source_file_copy='source_file_copy.txt'
    source_file_chunks='source_file_chunks'
    heading_regex = r'^Section.+?(\d+)'
    heading_text = 'Section'

    # copy_source(source_file, source_file_copy)
    # clean_text(source_file_copy)
    # fix_bible_ref_pron(source_file_copy)
    # split_text_max_char(source_file_copy, source_file_chunks, 4998)
    # rename_output_files(source_file_chunks, heading_regex, heading_text)
    text_to_audiobook(source_file_chunks, 'audio_output', 'en-US', 'en-US-Studio-O')