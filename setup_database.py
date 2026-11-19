from datetime import datetime
from pymongo import MongoClient, ASCENDING
from config import MONGO_URI, DB_NAME

db = MongoClient(MONGO_URI)[DB_NAME]
NUM = ["int", "long", "double"]

validators = {
    "patients": {"bsonType": "object", "required": ["name", "phone"],
                 "properties": {"name": {"bsonType": "string"},
                                "phone": {"bsonType": "string"}}},
    "doctors": {"bsonType": "object", "required": ["name", "specialty"],
                "properties": {"name": {"bsonType": "string"},
                               "specialty": {"bsonType": "string"}}},
    "medicines": {"bsonType": "object", "required": ["name", "stock", "unitPrice"],
                  "properties": {"name": {"bsonType": "string"},
                                 "stock": {"bsonType": NUM, "minimum": 0},
                                 "unitPrice": {"bsonType": NUM, "minimum": 0}}},
    "billing": {"bsonType": "object", "required": ["patientName", "total", "status"],
                "properties": {"total": {"bsonType": NUM, "minimum": 0},
                               "status": {"enum": ["Paid", "Unpaid"]}}},
}

existing = db.list_collection_names()
for name, schema in validators.items():
    if name in existing:
        db.command("collMod", name, validator={"$jsonSchema": schema},
                   validationLevel="moderate")
    else:
        db.create_collection(name, validator={"$jsonSchema": schema})
print("Validation rules applied.")

db.patients.create_index("phone")
db.patients.create_index([("name", ASCENDING)])
db.appointments.create_index("date")
db.visits.create_index("patientId")
db.billing.create_index("patientId")
db.medicines.create_index("name", unique=True)
print("Indexes created.")

if db.medicines.count_documents({}) == 0:
    db.medicines.insert_many([
        {"name": "Paracetamol 500mg", "category": "Painkiller", "stock": 200, "unitPrice": 500, "expiryDate": datetime(2027, 12, 31)},
        {"name": "Amoxicillin 500mg", "category": "Antibiotic", "stock": 120, "unitPrice": 1000, "expiryDate": datetime(2027, 6, 30)},
        {"name": "Artemether-Lumefantrine", "category": "Antimalarial", "stock": 8, "unitPrice": 7000, "expiryDate": datetime(2027, 3, 31)},
        {"name": "Vitamin C 100mg", "category": "Vitamin", "stock": 90, "unitPrice": 300, "expiryDate": datetime(2028, 1, 31)},
    ])
    print("Sample medicines added.")
