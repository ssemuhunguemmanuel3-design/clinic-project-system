import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import client, db

expected = ["patients", "doctors", "appointments", "medicines"]
try:
    client.admin.command("ping")
    print("PASS  MongoDB is reachable")
except Exception as e:
    print("FAIL  Cannot reach MongoDB:", e)
    sys.exit(1)

existing = db.list_collection_names()
for name in expected:
    status = "PASS" if name in existing else "FAIL"
    print(f"{status}  collection '{name}' ({db[name].count_documents({})} documents)")
