from datetime import datetime, timedelta
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

db = MongoClient(MONGO_URI)[DB_NAME]
if db.doctors.count_documents({}) == 0 and db.patients.count_documents({}) == 0:
    today = datetime.combine(datetime.today(), datetime.min.time())
    docs = db.doctors.insert_many([
        {"name": "Dr. Sarah Namutebi", "specialty": "General", "phone": "0700100200", "email": "sarah@clinic.ug"},
        {"name": "Dr. Peter Okello", "specialty": "Pediatrics", "phone": "0700300400", "email": "peter@clinic.ug"},
        {"name": "Dr. Grace Atim", "specialty": "Dentistry", "phone": "0700500600", "email": "grace@clinic.ug"},
    ]).inserted_ids
    pats = db.patients.insert_many([
        {"name": "Jane Nakato", "gender": "Female", "dob": datetime(1998, 4, 12), "phone": "0700123456", "address": "Namugongo", "allergies": ["Penicillin"], "createdAt": datetime.now()},
        {"name": "John Okello", "gender": "Male", "dob": datetime(1990, 8, 3), "phone": "0700111222", "address": "Kampala", "allergies": [], "createdAt": datetime.now()},
        {"name": "Mary Achieng", "gender": "Female", "dob": datetime(2015, 1, 20), "phone": "0700333444", "address": "Entebbe", "allergies": ["Peanuts"], "createdAt": datetime.now()},
    ]).inserted_ids
    names_p = ["Jane Nakato", "John Okello", "Mary Achieng"]
    names_d = ["Dr. Sarah Namutebi", "Dr. Peter Okello", "Dr. Grace Atim"]
    reasons = ["Fever and headache", "Child vaccination", "Tooth pain"]
    for i in range(3):
        db.appointments.insert_one({
            "patientId": pats[i], "patientName": names_p[i],
            "doctorId": docs[i], "doctorName": names_d[i],
            "date": today + timedelta(days=i), "time": f"{9 + i:02d}:00",
            "reason": reasons[i], "status": "Scheduled"})
    print("Sample data added.")
else:
    print("Data already exists.")
