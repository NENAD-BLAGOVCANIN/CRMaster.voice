from vosk import Model, KaldiRecognizer
import pyaudio
import os

if not os.path.exists("model"):
    print ("Model folder not present in the project folder!")
    exit (1)

model = Model("model")
recognizer = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()

try:
    while True:
        data = stream.read(1024)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            print(result)
except Exception as e:
    print("Error:", e)

stream.stop_stream()
stream.close()
mic.terminate()
