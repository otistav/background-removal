from pymongo import MongoClient


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