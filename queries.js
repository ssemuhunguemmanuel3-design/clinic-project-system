print("--- 1. Patient names and phones ---");
printjson(db.patients.find({}, {name: 1, phone: 1, _id: 0}).toArray());

print("--- 2. Patients who have allergies ---");
printjson(db.patients.find({allergies: {$ne: []}}, {name: 1, allergies: 1, _id: 0}).toArray());

print("--- 3. Appointments sorted by date ---");
printjson(db.appointments.find({}, {patientName: 1, doctorName: 1, date: 1, _id: 0}).sort({date: 1}).toArray());

print("--- 4. Appointments per doctor (aggregation) ---");
printjson(db.appointments.aggregate([{$group: {_id: "$doctorName", total: {$sum: 1}}}]).toArray());

print("--- 5. Join appointments with patients ($lookup) ---");
printjson(db.appointments.aggregate([
  {$lookup: {from: "patients", localField: "patientId", foreignField: "_id", as: "patient"}},
  {$unwind: "$patient"},
  {$project: {_id: 0, doctorName: 1, reason: 1, "patient.name": 1, "patient.phone": 1}}
]).toArray());

print("--- 6. Medicines with low stock ---");
printjson(db.medicines.find({stock: {$lt: 10}}, {name: 1, stock: 1, _id: 0}).toArray());

print("--- 7. Top medicines sold ($unwind on embedded bill items) ---");
printjson(db.billing.aggregate([
  {$unwind: "$items"},
  {$group: {_id: "$items.name", sold: {$sum: "$items.qty"}}},
  {$sort: {sold: -1}}
]).toArray());

print("--- 8. Index check: documents examined for a phone search ---");
print(db.patients.find({phone: "0700123456"}).explain("executionStats").executionStats.totalDocsExamined);
