from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from transcriber import transcribe_audio
import uuid
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(filename='/var/log/crmaster_voice.log', level=logging.INFO)


project_path = "/var/www/CRMaster.voice/"

@app.route('/', methods=['GET'])
def home():
    return("Hello World")

@app.route('/transcribe', methods=['POST'])
def transcribe():

    file = request.files['file']

    random_uuid = uuid.uuid4()
    file_extension = ".webm"

    file_path = project_path + str(random_uuid) + file_extension
    file.save(file_path)

    transcription_result = transcribe_audio(file_path)

    logging.info(transcription_result)

    if os.path.exists(file_path):
        os.remove(file_path)

    return jsonify(transcription_result)

if __name__ == '__main__':
    app.run(debug=True)
