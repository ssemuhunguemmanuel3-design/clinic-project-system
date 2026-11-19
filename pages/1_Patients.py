import re
import streamlit as st
from datetime import datetime
from db import patients, appointments, to_df
from ui import page_setup, flash

page_setup("Patients", "👥")

with st.expander("➕ Register a new patient"):
    with st.form("add_patient", clear_on_submit=True):
        name = st.text_input("Full name")
        gender = st.selectbox("Gender", ["Female", "Male"])
        dob = st.date_input("Date of birth", value=datetime(2000, 1, 1),
                            min_value=datetime(1920, 1, 1), max_value=datetime.today())
        phone = st.text_input("Phone")
        address = st.text_input("Address")
        allergies = st.text_input("Allergies (separate with commas)")
        if st.form_submit_button("Save patient"):
            if not (name and phone):
                st.error("Name and phone are required.")
            elif patients.find_one({"phone": phone}):
                st.error("A patient with this phone number already exists.")
            else:
                patients.insert_one({
                    "name": name, "gender": gender,
                    "dob": datetime.combine(dob, datetime.min.time()),
                    "phone": phone, "address": address,
                    "allergies": [a.strip() for a in allergies.split(",") if a.strip()],
                    "createdAt": datetime.now()})
                st.success("Patient saved.")

search = st.text_input("🔍 Search by name or phone")
query = {}
if search:
    s = re.escape(search)
    query = {"$or": [{"name": {"$regex": s, "$options": "i"}}, {"phone": {"$regex": s}}]}
plist = list(patients.find(query).sort("name", 1))
st.caption(f"{len(plist)} patient(s)")

if not plist:
    st.info("No patients found.")
else:
    st.dataframe(to_df(plist).drop(columns=["_id"]), use_container_width=True)
    label = lambda x: f"{x['name']} ({x['phone']})"

    st.subheader("✏️ Edit a patient")
    p = st.selectbox("Select patient", plist, format_func=label, key="edit_sel")
    pid = str(p["_id"])
    new_phone = st.text_input("Phone", value=p.get("phone", ""), key=f"ph_{pid}")
    new_addr = st.text_input("Address", value=p.get("address", ""), key=f"ad_{pid}")
    new_all = st.text_input("Allergies (comma separated)",
                            value=", ".join(p.get("allergies", [])), key=f"al_{pid}")
    if st.button("Update patient"):
        if not new_phone:
            st.error("Phone is required.")
        else:
            patients.update_one({"_id": p["_id"]}, {"$set": {
                "phone": new_phone, "address": new_addr,
                "allergies": [a.strip() for a in new_all.split(",") if a.strip()]}})
            flash("Patient updated.")
            st.rerun()

    st.subheader("🗑️ Delete a patient")
    dp = st.selectbox("Select patient to delete", plist, format_func=label, key="del_sel")
    n = appointments.count_documents({"patientId": dp["_id"]})
    if n:
        st.warning(f"This patient has {n} appointment(s); they will be deleted too. "
                   "Visits and bills are kept for the records.")
    ok = st.checkbox("I confirm the deletion", key=f"del_ok_{dp['_id']}")
    if st.button("Delete patient"):
        if not ok:
            st.error("Tick the confirmation box first.")
        else:
            appointments.delete_many({"patientId": dp["_id"]})
            patients.delete_one({"_id": dp["_id"]})
            flash("Patient deleted.")
            st.rerun()
