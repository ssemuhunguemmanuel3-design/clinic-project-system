# Health Clinic Management System

A database project built with **MongoDB** (back end) and **Python + Streamlit** (front end).

Author: Ssemuhungu Emmanuel

## Features
- Dashboard: KPI cards, alerts, today's appointments, charts, recent activity
- Patients: register, search, edit, delete
- Doctors: register, edit, delete
- Appointments: book (with double-booking check) and update status
- Visits: record symptoms, diagnosis and prescriptions
- Medicines: stock control, low-stock and expiry alerts
- Billing: itemised bills, automatic stock deduction, payment tracking
- Reports: charts and CSV export
- System status page, automated tests, backup and restore

## Technology
| Layer | Tool |
|---|---|
| Database | MongoDB Community Server |
| Driver | PyMongo |
| Front end | Streamlit |
| Data handling | pandas |

## Project structure
    Dashboard.py          Home page (dashboard)
    pages/                Patients, Doctors, Appointments, Visits, Medicines,
                          Billing, Reports, System Status
    config.py             Settings (database address, clinic name)
    db.py                 Database connection and helper functions
    ui.py                 Shared page layout and messages
    setup_database.py     Validation rules, indexes, sample medicines
    seed.py               Sample doctors, patients and appointments
    tests/                Connection test and CRUD test
    docs/                 User manual, database design, presentation guide
    queries.js            Example MongoDB queries for mongosh
    export_db.py          Export data to JSON
    import_db.py          Import data from JSON
    backup.ps1            Timestamped backup
    test.ps1              Runs all tests
    run.ps1               Starts the whole system
    Start-Clinic.bat      Double-click launcher

## Installation
1. Install Python 3.12, MongoDB Community Server and mongosh.
2. Open PowerShell in this folder and run:

        Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
        .\setup.ps1

## Running
    .\run.ps1

Then open http://localhost:8501

To use another MongoDB server, set the MONGO_URI environment variable before running.

## Testing
    .\test.ps1
    mongosh "mongodb://localhost:27017/clinicDB" --file queries.js

## Backup and restore
    .\backup.ps1
    .\venv\Scripts\python.exe import_db.py

## Documentation
See the docs folder: USER_MANUAL.md, DATABASE_DESIGN.md, PRESENTATION_GUIDE.md.

---

title: City Health Clinic
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: "1.49.1"
app_file: app.py
pinned: false

---

## Hosted deployment

The web app can be deployed on Streamlit Community Cloud:

1. Create a MongoDB Atlas cluster and database user.
2. Under **Network Access**, allow `0.0.0.0/0` if the app should be accessible from all networks.
3. Deploy this repository on Streamlit Community Cloud with `app.py` as the main file.
4. In Streamlit: **App settings > Secrets**, add:

       MONGO_URI = "mongodb+srv://USERNAME:PASSWORD@CLUSTER.mongodb.net/clinicDB?retryWrites=true&w=majority"

5. Reboot the app. Streamlit will provide a public URL similar to `https://clinic-project-system.streamlit.app`.
