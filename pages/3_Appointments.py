import streamlit as st
from datetime import datetime, time as dtime
from db import patients, doctors, appointments
from ui import page_setup, flash

page_setup("Appointments", "📅")

patient_list = list(patients.find().sort("name", 1))
doctor_list = list(doctors.find().sort("name", 1))

if not patient_list or not doctor_list:
    st.warning("Add at least one patient and one doctor first.")
else:
    with st.expander("➕ Book an appointment", expanded=True):
        with st.form("add_appt", clear_on_submit=True):
            p = st.selectbox("Patient", patient_list, format_func=lambda x: x["name"])
            d = st.selectbox("Doctor", doctor_list,
                             format_func=lambda x: f"{x['name']} ({x['specialty']})")
            date = st.date_input("Date", min_value=datetime.today())
            time = st.time_input("Time", value=dtime(9, 0))
            reason = st.text_area("Reason for visit")
            if st.form_submit_button("Book appointment"):
                when = datetime.combine(date, datetime.min.time())
                slot = time.strftime("%H:%M")
                clash = appointments.find_one({"doctorId": d["_id"], "date": when,
                                               "time": slot, "status": {"$ne": "Cancelled"}})
                if clash:
                    st.error(f"{d['name']} already has an appointment at {slot} on {date}.")
                else:
                    appointments.insert_one({
                        "patientId": p["_id"], "patientName": p["name"],
                        "doctorId": d["_id"], "doctorName": d["name"],
                        "date": when, "time": slot, "reason": reason, "status": "Scheduled"})
                    st.success("Appointment booked.")

status_filter = st.selectbox("Show", ["All", "Scheduled", "Completed", "Cancelled"])
query = {} if status_filter == "All" else {"status": status_filter}
alist = list(appointments.find(query).sort([("date", 1), ("time", 1)]))
st.caption(f"{len(alist)} appointment(s)")

if not alist:
    st.info("No appointments found.")
else:
    import pandas as pd
    rows = [{"Date": a["date"].strftime("%Y-%m-%d"), "Time": a.get("time", ""),
             "Patient": a["patientName"], "Doctor": a["doctorName"],
             "Reason": a.get("reason", ""), "Status": a["status"]} for a in alist]
    st.dataframe(pd.DataFrame(rows), use_container_width=True)

    st.subheader("🔄 Update status")
    a = st.selectbox("Appointment", alist,
                     format_func=lambda x: f"{x['date']:%Y-%m-%d} {x.get('time', '')} - {x['patientName']} - {x['doctorName']}")
    new_status = st.selectbox("New status", ["Scheduled", "Completed", "Cancelled"])
    if st.button("Update"):
        appointments.update_one({"_id": a["_id"]}, {"$set": {"status": new_status}})
        flash("Status updated.")
        st.rerun()
