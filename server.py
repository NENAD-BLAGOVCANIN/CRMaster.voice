from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/transcribe', methods=['POST'])
def transcribe():
    file = request.files['file']
    transcription = "Transcribed text"
    return jsonify({'transcription': transcription})

    

if __name__ == '__main__':
    app.run(port=5000)