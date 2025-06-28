import os
import concurrent.futures
from tqdm import tqdm
from google.cloud import texttospeech
import argparse

# Set up Google Cloud credentials
# Make sure to replace 'path_to_your_service_account_json' with the actual path to your JSON key file.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "temporal-web-401815-23bec0b49588.json"

def text_to_speech(input_file='input.txt', output_audio_file='output', language_code='en-US', voice_name='en-US-Studio-O'):
    """ Converts text from a file to speech using Google Cloud Text-to-Speech API and saves the audio to an MP3 file. """
    client = texttospeech.TextToSpeechClient()
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()
    
    if not text.strip():
        print(f"No text to synthesize in {input_file}")
        return

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code=language_code, name=voice_name, ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    try:
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        if response.audio_content:
            with open(output_audio_file, 'wb') as out:
                out.write(response.audio_content)
            print(f"Audio content written to file {output_audio_file}")
        else:
            print("No audio content received from the API.")
    except Exception as e:
        print(f"Error in text-to-speech conversion for {input_file}: {e}")

def text_to_audiobook(input_folder, output_folder, language_code, voice_name):
    """ Processes all text files in the input folder concurrently using Google's Text-to-Speech API. """
    input_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.txt')]
    if not input_files:
        print("No text files found in the input folder.")
        return

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(text_to_speech, input_file, os.path.join(output_folder, f"{os.path.splitext(os.path.basename(input_file))[0]}.mp3"), language_code, voice_name) for input_file in input_files]

        # tqdm is used to display a progress bar for the audio conversion process
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Processing files"):
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert text files to audio using Google Cloud TTS.')
    parser.add_argument('--input_file', type=str, help='Path to a single .txt file')
    parser.add_argument('--input_folder', type=str, help='Path to a folder containing .txt files')
    parser.add_argument('--output_folder', type=str, default='.', help='Folder to save MP3 files')
    parser.add_argument('--language_code', type=str, default='en-US', help='Language code for TTS')
    parser.add_argument('--voice_name', type=str, default='en-US-Studio-O', help='Voice name for TTS')

    args = parser.parse_args()

    os.makedirs(args.output_folder, exist_ok=True)

    if args.input_file:
        base_name = os.path.splitext(os.path.basename(args.input_file))[0]
        output_file = os.path.join(args.output_folder, f"{base_name}.mp3")
        text_to_speech(args.input_file, output_file, args.language_code, args.voice_name)
    elif args.input_folder:
        text_to_audiobook(args.input_folder, args.output_folder, args.language_code, args.voice_name)
    else:
        print("Please specify either --input_file or --input_folder")
