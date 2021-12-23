import time
from main import process
import requests
from flask import Flask, jsonify, request
from pymongo import MongoClient
import pymongo

import datetime
app = Flask(__name__)
def get_database():
    CONNECTION_STRING = "mongodb://localhost:27017/"
    client = MongoClient(CONNECTION_STRING)
    return client['test']

def download_image(imgpath):
  img_data = requests.get(f"http://0.0.0.0:3000/{imgpath}").content
  with open(imgpath, 'wb') as handler:
      handler.write(img_data)

@app.route('/image', methods=['POST'])
def echo():
    params = request.json
    new_id = f"processed_{params['filename']}"
    download_image(params["filename"])
    process(params["filename"], new_id, 'u2net', 'bbd-fastrcnn', 'rtb-bnb')
    db = get_database()
    data = db['images'].find_one({"filename": params['filename']})
    db['images'].update_one({
      '_id': data['_id']
    },{
      '$set': {
        'processed': True,
      }
    }, upsert=False)
    return jsonify({"status": "ok"})

@app.route('/test', methods=['GET'])
def test():
    imgpath = request.args.get('path')
    img_data = requests.get(f"http://{request.args.get('path')}:3000/{imgpath}").content
    return img_data
#     # return {"data": [doc for doc in db['images'].find()]}

app.run(debug=True,host='0.0.0.0')
