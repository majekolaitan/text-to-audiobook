import os
import concurrent.futures
from tqdm import tqdm
from google.cloud import texttospeech

# Set up Google Cloud credentials
# Make sure to replace 'path_to_your_service_account_json' with the actual path to your JSON key file.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account-file.json"

def text_to_speech(input_file, output_audio_file, language_code='en-US', voice_name='en-US-Studio-O'):
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

def process_files_concurrently(input_folder, output_folder, language_code, voice_name):
    """ Processes all text files in the input folder concurrently using Google's Text-to-Speech API. """
    input_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.txt')]
    if not input_files:
        print("No text files found in the input folder.")
        return

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(text_to_speech, input_file, os.path.join(output_folder, f"{os.path.basename(input_file)}.mp3"), language_code, voice_name) for input_file in input_files]

        # tqdm is used to display a progress bar for the audio conversion process
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Processing files"):
            pass