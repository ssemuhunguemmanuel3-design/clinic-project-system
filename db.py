import pandas as pd
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
db = client[DB_NAME]

patients = db["patients"]
doctors = db["doctors"]
appointments = db["appointments"]
visits = db["visits"]
medicines = db["medicines"]
billing = db["billing"]

def to_df(docs):
    df = pd.DataFrame(list(docs))
    if not df.empty and "_id" in df.columns:
        df["_id"] = df["_id"].astype(str)
    return df

