import os
import clean_text
import split_text_max_char
import fix_bible_ref_pronunciation
import text_to_audiobook
from rename_output_files import *

def main():
    source_file='source_file.txt'
    cleaned_file = 'source_cleaned_file.txt'
    output_folder = 'output'

    source_file = "source_file.txt"
    list_bible_ref="source_list_bible_ref_in_file.txt"
    bible_ref_dic = 'source_bible_ref_dic'
    bible_ref_dic_filled = bible_ref_dic + '_chatgpt_fill.json'
    removed_abbr = 'source_removed_abbr.txt'
    removed_colon = 'source_removed_colon.txt'

    clean_text.copy_source(source_file, cleaned_file)
    clean_text.replace_tabs(cleaned_file)
    clean_text.remove_leading_and_trailing_spaces(cleaned_file)
    clean_text.remove_emails_and_html_tags(cleaned_file)
    clean_text.add_full_stop(cleaned_file)
    clean_text.remove_blank_lines(cleaned_file)

    fix_bible_ref_pronunciation.list_bible_ref_in_file(cleaned_file, list_bible_ref)
    fix_bible_ref_pronunciation.create_dict_from_list_bible_ref(list_bible_ref, bible_ref_dic)

    if not os.path.exists(bible_ref_dic_filled):
        print(f"The file '{bible_ref_dic_filled}' does not exist. Create it and fill the dictionary values using ChatGPT.")
        exit()

    fix_bible_ref_pronunciation.rewrite_source_with_dic_values(cleaned_file, removed_abbr, bible_ref_dic_filled)
    fix_bible_ref_pronunciation.rewrite_source_with_colon_replacement(removed_abbr, removed_colon)
    
    # try:
    #     os.remove(bible_ref_dic_filled)
    #     print(f"Deleted {bible_ref_dic_filled}")
    # except FileNotFoundError:
    #     print(f"File {bible_ref_dic_filled} not found.")
    # except Exception as e:
    #     print(f"An error occurred while deleting {bible_ref_dic_filled}: {e}")

    split_text_max_char.delete_files_in_output(output_folder)
    split_text_max_char.split_text_max_char(removed_colon, output_folder, 4998)

    input_folder = "output"  # Path to the folder containing the text files
    output_folder = "audio"  # Path to the folder where the audio files will be saved
    
    rename_output_files(input_folder)

    language_code = "en-US"
    voice_name = "en-US-Studio-O"

    # text_to_audiobook.process_files_concurrently(input_folder, output_folder, language_code, voice_name)


if __name__ == "__main__":
    main()