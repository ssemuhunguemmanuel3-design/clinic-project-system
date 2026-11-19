import streamlit as st
import pandas as pd
from datetime import datetime
from db import patients, doctors, visits
from ui import page_setup

page_setup("Patient Visits", "🩺")

patient_list = list(patients.find().sort("name", 1))
doctor_list = list(doctors.find().sort("name", 1))

if not patient_list or not doctor_list:
    st.warning("Add at least one patient and one doctor first.")
else:
    with st.expander("➕ Record a visit", expanded=True):
        with st.form("add_visit", clear_on_submit=True):
            p = st.selectbox("Patient", patient_list, format_func=lambda x: x["name"])
            d = st.selectbox("Doctor", doctor_list, format_func=lambda x: x["name"])
            symptoms = st.text_area("Symptoms")
            diagnosis = st.text_input("Diagnosis")
            rx = st.text_area("Prescriptions (one per line: medicine, dosage, days)",
                              placeholder="Amoxicillin, 500mg, 5")
            if st.form_submit_button("Save visit"):
                if not diagnosis:
                    st.error("Diagnosis is required.")
                else:
                    prescriptions = []
                    for line in rx.splitlines():
                        parts = [x.strip() for x in line.split(",")]
                        if parts[0]:
                            prescriptions.append({
                                "medicine": parts[0],
                                "dosage": parts[1] if len(parts) > 1 else "",
                                "days": parts[2] if len(parts) > 2 else ""})
                    visits.insert_one({
                        "patientId": p["_id"], "patientName": p["name"],
                        "doctorId": d["_id"], "doctorName": d["name"],
                        "symptoms": symptoms, "diagnosis": diagnosis,
                        "prescriptions": prescriptions, "visitDate": datetime.now()})
                    st.success("Visit saved.")

names = ["All"] + [p["name"] for p in patient_list]
chosen = st.selectbox("Show visits for", names)
query = {} if chosen == "All" else {"patientName": chosen}

rows = []
for v in visits.find(query).sort("visitDate", -1):
    rows.append({
        "Date": v["visitDate"].strftime("%Y-%m-%d %H:%M"),
        "Patient": v["patientName"], "Doctor": v["doctorName"],
        "Diagnosis": v["diagnosis"],
        "Prescriptions": "; ".join(
            f"{x['medicine']} {x.get('dosage', '')} x{x.get('days', '')}d"
            for x in v.get("prescriptions", []))})
if rows:
    st.dataframe(pd.DataFrame(rows), use_container_width=True)
else:
    st.info("No visits recorded yet.")
