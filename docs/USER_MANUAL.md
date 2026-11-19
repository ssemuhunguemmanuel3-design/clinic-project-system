# User Manual

## Starting the system
Run `run.ps1` (or double-click Start-Clinic.bat). Edge opens at http://localhost:8501.

## Pages
| Page | What you can do |
|---|---|
| Dashboard | See totals, alerts, today's appointments, charts and recent activity |
| Patients | Register, search, edit and delete patients |
| Doctors | Register, edit and delete doctors |
| Appointments | Book appointments (double-booking is blocked) and update their status |
| Visits | Record a visit with symptoms, diagnosis and prescriptions |
| Medicines | Add medicines, restock, delete, see low-stock warnings |
| Billing | Create a bill, deduct stock automatically, record payments |
| Reports | View charts and download data as CSV |
| System Status | Check the database connection and record counts |

## Daily workflow
1. Register the patient.
2. Book an appointment with a doctor.
3. Record the visit (diagnosis and prescriptions).
4. Create the bill with consultation fee and medicines.
5. Mark the bill as paid when the patient pays.

## Stopping the system
Click the PowerShell window and press Ctrl + C.

## Backup
Run `backup.ps1`. Backups are saved in the backups folder with the date and time.
