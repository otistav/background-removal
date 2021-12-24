from main import process
import requests
from flask import Flask, json, jsonify, request, send_file, send_from_directory
from pymongo import MongoClient
import pymongo
from urllib.parse import urlparse


import datetime
app = Flask(__name__)

def download_image(imgpath):
  try:
      o = urlparse(request.base_url)
      host = o.hostname
      img_data = requests.get(f"http://{host}/{imgpath}")
  except Exception as e:
      # print(f"REQUEST URL: {img_data.request.url}", flush=True)
      print(f"ERROR OCCURED {e}", flush=True)
      return "error"
  if img_data.status_code == 404:
      return "error"
  with open(imgpath, 'wb') as handler:
      handler.write(img_data.content)
      return "ok"

def manage_image(filename):
    new_filename = '.'.join(filename.split('.')[:-1])
    new_id = f"processed_{new_filename}.png"
    print(f"FILENAME:: {filename}", flush=True)
    result = download_image(filename)
    if result == "error":
      print(f"cant process image {filename}", flush=True)
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
    cursor = db['images'].find({ "processed": False })
    length = len(list(cursor.clone()))
    for doc in cursor:
        print(f"PROCESSING IMAGE {doc['filename']}", flush=True)
        manage_image(doc["filename"])
        print(f"DONE WITH IMAGE {doc['filename']}", flush=True)
    if length == 0:
      return
    # manage_worker()





@app.route('/image', methods=['POST'])
def echo():
    manage_worker()
    return jsonify({"status": "ok"})

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('.', path)

@app.route('/count')
def count():
    db = get_database()
    cursor = db['images'].find({ "processed": False })
    return jsonify({"len": len(list(cursor))})

@app.route('/test/<path:path>')
def test(path):
  o = urlparse(request.base_url)
  host = o.hostname
  print(f"HOST: {host}", flush=True)
  # return jsonify({ "result": o })
  try:
      img_data = requests.get(f"http://{host}/{path}")
      print(f"IMGDATA {img_data}", flush=True)
      return { "Ok": "Ok"}
  except Exception as e:
      print(f"EXCEPTION TEST {e}")




# manage_worker()
app.run(debug=True,host='0.0.0.0')
