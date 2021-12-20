from flask import Flask, jsonify, request
from ml_service.main import process
app = Flask(__name__)

@app.route('/image', methods=['POST'])
def echo():
    params = jsonify(request.get_json(force=True))

    process(params['input'], params['output'], 'u2net', 'bbd-fastrcnn', 'rtb-bnb')
    return jsonify({"jjj": "eee"})