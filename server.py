from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/transcribe", methods=['POST'])
def transcribe():
    response = "<p>Hello, World!</p>"
    return jsonify(response)
    

app.run(debug=True)