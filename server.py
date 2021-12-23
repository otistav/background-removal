import time
from main import process
from flask import Flask, jsonify, request
# from pymongo import MongoClient
# import pymongo

import datetime
app = Flask(__name__)

# def get_database():
#     CONNECTION_STRING = "mongodb://localhost:27017/"
#     client = MongoClient(CONNECTION_STRING)
#     return client['test']# from main import process

# db = get_database()
# print([doc for doc in db['images'].find()])

# try:
#     resume_token = None
#     pipeline = [{'$match': {'operationType': 'insert'}}]
#     with db.images.watch(pipeline) as stream:
#         for insert_change in stream:
#             print(insert_change)
#             resume_token = stream.resume_token
# except pymongo.errors.PyMongoError as error:
#     # The ChangeStream encountered an unrecoverable error or the
#     # resume attempt failed to recreate the cursor.
#     if resume_token is None:
#       print(error)
#         # There is no usable resume token because there was a
#         # failure during ChangeStream initialization.

#     else:
#         # Use the interrupted ChangeStream's resume token to create
#         # a new ChangeStream. The new stream will continue from the
#         # last seen insert change without missing any events.
#         with db.collection.watch(
#                 pipeline, resume_after=resume_token) as stream:
#             for insert_change in stream:
#                 print(insert_change)

@app.route('/image', methods=['POST'])
def echo():
    params = request.json
    new_id = f"processed_{params['filename']}"
    process(f"../uploads/{params['filename']}", new_id, 'u2net', 'bbd-fastrcnn', 'rtb-bnb')
    return jsonify({"jjj": "eee"})

app.run()
