from pymongo import MongoClient
from bson import json_util
import glob, os
from config import MONGO_URI, DB_NAME

db = MongoClient(MONGO_URI)[DB_NAME]
for path in glob.glob("database_export/*.json"):
    name = os.path.splitext(os.path.basename(path))[0]
    with open(path, encoding="utf-8") as f:
        docs = json_util.loads(f.read())
    if docs and db[name].count_documents({}) == 0:
        db[name].insert_many(docs)
        print("Imported", name)
