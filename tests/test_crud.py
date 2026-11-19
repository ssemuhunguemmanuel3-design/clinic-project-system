import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pymongo import MongoClient
from config import MONGO_URI

# Uses a separate test database so real clinic data is never touched
client = MongoClient(MONGO_URI)
db = client["clinicDB_test"]

def check(label, condition):
    print(("PASS  " if condition else "FAIL  ") + label)
    return condition

ok = True
db.patients.delete_many({})
r = db.patients.insert_one({"name": "Test Patient", "phone": "0700000000"})
ok &= check("CREATE a patient", db.patients.count_documents({}) == 1)
ok &= check("READ the patient", db.patients.find_one({"_id": r.inserted_id})["name"] == "Test Patient")
db.patients.update_one({"_id": r.inserted_id}, {"$set": {"phone": "0711111111"}})
ok &= check("UPDATE the phone", db.patients.find_one({"_id": r.inserted_id})["phone"] == "0711111111")
db.patients.delete_one({"_id": r.inserted_id})
ok &= check("DELETE the patient", db.patients.count_documents({}) == 0)

client.drop_database("clinicDB_test")
print("\nALL TESTS PASSED" if ok else "\nSOME TESTS FAILED")
sys.exit(0 if ok else 1)
