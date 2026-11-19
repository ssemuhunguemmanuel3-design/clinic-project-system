# Presentation Guide (about 8 minutes)

## Order
1. Problem (1 min): paper records in clinics are slow and easy to lose.
2. Solution and architecture (1 min): Streamlit page -> Python -> PyMongo -> MongoDB.
3. Database design (1 min): show docs/DATABASE_DESIGN.md or the collections in Compass.
4. Live demo (3 min): start on the Dashboard, add a patient, book an appointment, record a visit, create a bill, watch the stock go down, refresh the Dashboard.
5. MongoDB features (1 min): run `mongosh "mongodb://localhost:27017/clinicDB" --file queries.js`.
6. Quality (30 sec): run `.\test.ps1`, show the README and folder structure.
7. Conclusion (30 sec): what was achieved and future work (staff login, PDF receipts).

## Questions you may be asked
**Why MongoDB instead of SQL?**
Documents hold lists (allergies, prescriptions) directly, the schema is flexible, and it is easy to extend.

**What is the difference between embedding and referencing?**
Embedding stores related data inside one document for fast reading. Referencing stores an _id that points to another collection, used for shared data.

**What is an index?**
A data structure that lets MongoDB find documents without scanning the whole collection. See query 8 in queries.js.

**How do you keep the data clean?**
$jsonSchema validation rules, a unique index on medicine names, and checks in the application (duplicate phone, double-booking).

**What is aggregation?**
A pipeline ($match, $group, $unwind, $sort) that transforms and summarises data. It powers the Dashboard and the Reports page.

**How would you improve security?**
Add staff login with roles, enable MongoDB authentication, and use encrypted connections.

**How would you scale it?**
Replica sets for availability and sharding for very large data.
