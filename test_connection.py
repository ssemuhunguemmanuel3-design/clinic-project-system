from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
try:
    print("Connected! Databases:", client.list_database_names())
except Exception as e:
    print("Connection FAILED:", e)
