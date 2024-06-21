from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import wave
import json
import subprocess
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment
AudioSegment.converter = "C:\\ffmpeg\\ffmpeg\\bin\\ffmpeg.exe"
AudioSegment.ffmpeg = "C:\\ffmpeg\\ffmpeg\\bin\\ffmpeg.exe"
AudioSegment.ffprobe ="C:\\ffmpeg\\ffmpeg\\bin\\ffprobe.exe"

app = Flask(__name__)
CORS(app)

model = Model("models/vosk-model-small-en-us-0.15")

def transcribe_audio(file_path):
    
    print(f"Converting file {file_path} to compliant WAV format")
    absolute_file_path = os.path.abspath(file_path)
    converted_path = absolute_file_path.replace(file_path.split('.')[-1], 'wav')

    command = f'ffmpeg -i "{absolute_file_path}" -ar 16000 -ac 1 -sample_fmt s16 "{converted_path}"'
    subprocess.run(command, shell=True, check=True)

    # Open the WAV file
    wf = wave.open(converted_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
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