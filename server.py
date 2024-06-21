from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from transcriber import transcribe_audio

app = Flask(__name__)
CORS(app)

@app.route('/transcribe', methods=['POST'])
def transcribe():

    file = request.files['file']

    file_path = "recording.webm"
    file.save(file_path)

    transcription_result = transcribe_audio(file_path)
    return jsonify(transcription_result)

if __name__ == '__main__':
    app.run(debug=True)
