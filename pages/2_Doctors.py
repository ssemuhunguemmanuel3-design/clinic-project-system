import streamlit as st
from db import doctors, appointments, to_df
from ui import page_setup, flash

SPECIALTIES = ["General", "Pediatrics", "Gynecology", "Dentistry", "Surgery"]

page_setup("Doctors", "🧑‍⚕️")

with st.expander("➕ Register a new doctor"):
    with st.form("add_doctor", clear_on_submit=True):
        name = st.text_input("Doctor name")
        specialty = st.selectbox("Specialty", SPECIALTIES)
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        if st.form_submit_button("Save doctor"):
            if not name:
                st.error("Name is required.")
            else:
                doctors.insert_one({"name": name, "specialty": specialty,
                                    "phone": phone, "email": email})
                st.success("Doctor saved.")

dlist = list(doctors.find().scccccccsort("name", 1))
st.caption(f"{len(dlist)} doctor(s)")

if not dlist:
    st.info("No doctors yet.")
else:
    st.dataframe(to_df(dlist).drop(columns=["_id"]), use_container_width=True)
    label = lambda x: f"{x['name']} ({x['specialty']})"

    st.subheader("✏️ Edit a doctor")
    d = st.selectbox("Select doctor", dlist, format_func=label, key="edit_doc")
    did = str(d["_id"])
    idx = SPECIALTIES.index(d["specialty"]) if d.get("specialty") in SPECIALTIES else 0
    new_spec = st.selectbox("Specialty", SPECIALTIES, index=idx, key=f"sp_{did}")
    new_phone = st.text_input("Phone", value=d.get("phone", ""), key=f"ph_{did}")
    new_email = st.text_input("Email", value=d.get("email", ""), key=f"em_{did}")
    if st.button("Update doctor"):
        doctors.update_one({"_id": d["_id"]}, {"$set": {
            "specialty": new_spec, "phone": new_phone, "email": new_email}})
        flash("Doctor updated.")
        st.rerun()

    st.subheader("🗑️ Delete a doctor")
    dd = st.selectbox("Select doctor to delete", dlist, format_func=label, key="del_doc")
    n = appointments.count_documents({"doctorId": dd["_id"]})
    if n:
        st.warning(f"This doctor has {n} appointment(s). They will be deleted too.")
    ok = st.checkbox("I confirm I want to delete this doctor", key=f"del_ok_{dd['_id']}")
    if st.button("Delete doctor"):
        if not ok:
            st.error("Tick the confirmation box first.")
        else:
            appointments.delete_many({"doctorId": dd["_id"]})
            doctors.delete_one({"_id": dd["_id"]})
            flash("Doctor deleted.")
            st.rerun()
