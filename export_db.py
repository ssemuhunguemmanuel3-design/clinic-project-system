from pymongo import MongoClient
from bson import json_util
import os
from config import MONGO_URI, DB_NAME

db = MongoClient(MONGO_URI)[DB_NAME]
os.makedirs("database_export", exist_ok=True)
for name in db.list_collection_names():
    with open(f"database_export/{name}.json", "w", encoding="utf-8") as f:
        f.write(json_util.dumps(list(db[name].find()), indent=2))
    print("Exported", name)
