from main import process
import requests
from flask import Flask, json, jsonify, request, send_file, send_from_directory
from pymongo import MongoClient
import pymongo

import datetime
app = Flask(__name__)

def manage_image(filename):
    new_filename = '.'.join(filename.split('.')[:-1])
    new_id = f"processed_{new_filename}.png"
    result = download_image(filename)
    if result == "error":
      return
    process(filename, new_id, 'u2net', 'bbd-fastrcnn', 'rtb-bnb')
    db = get_database()
    data = db['images'].find_one({"filename": filename})
    db['images'].update_one({
      '_id': data['_id']
    },{
      '$set': {
        'processed': True,
      }
    }, upsert=False)
    return True


def get_database():
    CONNECTION_STRING = "mongodb://mongo:27017/"
    client = MongoClient(CONNECTION_STRING)
    return client['test']

def manage_worker():
    db = get_database()
    data = db['images'].find({ "processed": False })
    for doc in data:
      manage_image(doc["filename"])



def download_image(imgpath):
  img_data = requests.get(f"http://server:3000/{imgpath}")
  if img_data.status_code == 404:
    return "error"
  with open(imgpath, 'wb') as handler:
      handler.write(img_data.content)
      return "ok"

@app.route('/image', methods=['POST'])
def echo():
    manage_worker()
    return jsonify({"status": "ok"})

@app.route('/img/<path:path>')
def send_js(path):
    return send_from_directory('.', path)

@app.route('/count')
def count():
    db = get_database()
    cursor = db['images'].find({ "processed": False })
    return jsonify({"len": len(list(cursor))})

app.run(debug=True,host='0.0.0.0')
