from flask import Flask, jsonify, request
from flask_cors import CORS
from transcriber import transcribe_audio
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/transcribe', methods=['POST'])
def transcribe():
    file = request.files['file']
    file_path = 'temp.wav'
    file.save(file_path)

    transcription_result, status_code = transcribe_audio(file_path)
    
    os.remove(file_path)
    
    return jsonify(transcription_result), status_code

    

if __name__ == '__main__':
    app.run(port=5000)