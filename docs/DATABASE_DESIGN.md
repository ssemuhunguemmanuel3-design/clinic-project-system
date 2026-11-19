# Database Design

Database name: clinicDB

## Collections
| Collection | Main fields | Notes |
|---|---|---|
| patients | name, gender, dob, phone, address, allergies[] | allergies embedded as an array |
| doctors | name, specialty, phone, email | referenced by appointments and visits |
| appointments | patientId, doctorId, patientName, doctorName, date, time, reason, status | references patients and doctors |
| visits | patientId, doctorId, symptoms, diagnosis, prescriptions[], visitDate | prescriptions embedded |
| medicines | name, category, stock, unitPrice, expiryDate | unique index on name |
| billing | patientId, items[], consultationFee, total, status, date | line items embedded |

## Embedding or referencing
- **Embedded:** data always read together with its parent (prescriptions in a visit, items in a bill, allergies in a patient).
- **Referenced:** data shared by many documents (patients and doctors are referenced by their _id).
- Names are also copied into appointments and bills so lists display quickly without a join.

## Indexes
| Index | Reason |
|---|---|
| patients.phone | fast patient lookup by phone |
| patients.name | fast search and sorting by name |
| appointments.date | fast sorting by date |
| visits.patientId, billing.patientId | fast history per patient |
| medicines.name (unique) | prevents duplicate medicines |

## Validation ($jsonSchema)
- patients: name and phone required (strings)
- doctors: name and specialty required
- medicines: name, stock, unitPrice required; stock and price cannot be negative
- billing: total cannot be negative; status must be Paid or Unpaid

## Business rules in the application
- A patient cannot be registered twice with the same phone number.
- A doctor cannot have two active appointments at the same date and time.
- Saving a bill reduces medicine stock automatically.
- Deleting a patient or doctor also deletes their appointments (visits and bills are kept).

## Relationships
    patients 1 --- many appointments many --- 1 doctors
    patients 1 --- many visits
    patients 1 --- many billing
    billing.items many --- 1 medicines
