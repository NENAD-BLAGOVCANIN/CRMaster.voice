import os
import wave
import json
import subprocess
from vosk import Model, KaldiRecognizer

# Load the Vosk model (ensure the path to your model directory is correct)
model = Model("models/vosk-model-small-en-us-0.15")

def convert_to_wav(input_file, output_file):
    try:
        command = [
            'ffmpeg',
            '-i', input_file,
            '-ar', '16000',  # Set the sample rate to 16000 Hz
            '-ac', '1',      # Set the number of audio channels to 1 (mono)
            output_file
        ]
        print(f"Running command: {' '.join(command)}")
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"ffmpeg error: {e}")
        raise

def transcribe_audio(file_path):
    converted_path = 'converted_temp.wav'
    try:
        convert_to_wav(file_path, converted_path)

        wf = wave.open(converted_path, "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000, 32000, 44100, 48000]:
            wf.close()
            return {'error': 'Audio file must be WAV format mono PCM.'}, 400

        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)
        transcription = ""

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = rec.Result()
                result_json = json.loads(result)
                transcription += result_json.get('text', '')

        final_result = rec.FinalResult()
        final_result_json = json.loads(final_result)
        transcription += final_result_json.get('text', '')

        wf.close()
        return {'transcription': transcription}, 200
    except Exception as e:
        return {'error': str(e)}, 500
    finally:
        if os.path.exists(converted_path):
            os.remove(converted_path)
