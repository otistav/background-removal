from pymongo import MongoClient
import requests

def get_database():
    CONNECTION_STRING = "mongodb://localhost:27017/"
    client = MongoClient(CONNECTION_STRING)
    return client['test']

db = get_database()

data = db['images'].find({})
length = len(list(data.clone()))
for doc in data:
    print(f"PROCESSING IMAGE {doc['filename']}", flush=True)

print(length)

img_data = requests.get(f"http://185.105.2.10/1640344114525_image_onmzi0ivvhsuqh3.jpeg")
print(img_data.request.url)