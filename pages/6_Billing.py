import streamlit as st
import pandas as pd
from datetime import datetime
from db import patients, medicines, billing
from ui import page_setup, flash

page_setup("Billing", "💰")

def total_for(status):
    r = list(billing.aggregate([
        {"$match": {"status": status}},
        {"$group": {"_id": None, "t": {"$sum": "$total"}}}]))
    return r[0]["t"] if r else 0

c1, c2 = st.columns(2)
c1.metric("Paid (UGX)", f"{total_for('Paid'):,.0f}")
c2.metric("Outstanding (UGX)", f"{total_for('Unpaid'):,.0f}")

patient_list = list(patients.find().sort("name", 1))
med_list = list(medicines.find({"stock": {"$gt": 0}}).sort("name", 1))

st.subheader("🧾 New bill")
if not patient_list:
    st.warning("Add a patient first.")
else:
    p = st.selectbox("Patient", patient_list, format_func=lambda x: x["name"])
    fee = st.number_input("Consultation fee (UGX)", min_value=0, value=20000, step=1000)
    chosen = st.multiselect("Medicines", med_list,
                            format_func=lambda m: f"{m['name']} (stock {m['stock']}, UGX {m['unitPrice']})")
    items, total = [], fee
    for m in chosen:
        qty = st.number_input(f"Quantity of {m['name']}", min_value=1,
                              max_value=int(m["stock"]), value=1, key=f"qty_{m['_id']}")
        line = qty * m["unitPrice"]
        items.append({"medicineId": m["_id"], "name": m["name"], "qty": qty,
                      "unitPrice": m["unitPrice"], "lineTotal": line})
        total += line
    st.subheader(f"Total: UGX {total:,.0f}")
    status = st.selectbox("Payment status", ["Unpaid", "Paid"])
    if st.button("Save bill"):
        billing.insert_one({
            "patientId": p["_id"], "patientName": p["name"],
            "consultationFee": fee, "items": items, "total": total,
            "status": status, "date": datetime.now()})
        for it in items:
            medicines.update_one({"_id": it["medicineId"]}, {"$inc": {"stock": -it["qty"]}})
        flash("Bill saved and stock updated.")
        st.rerun()

st.subheader("All bills")
rows = [{"Date": b["date"].strftime("%Y-%m-%d %H:%M"), "Patient": b["patientName"],
         "Total (UGX)": b["total"], "Status": b["status"]}
        for b in billing.find().sort("date", -1)]
if rows:
    st.dataframe(pd.DataFrame(rows), use_container_width=True)
    unpaid = list(billing.find({"status": "Unpaid"}))
    if unpaid:
        st.subheader("💵 Record a payment")
        b = st.selectbox("Unpaid bill", unpaid,
                         format_func=lambda x: f"{x['patientName']} - UGX {x['total']:,.0f}")
        if st.button("Mark as paid"):
            billing.update_one({"_id": b["_id"]},
                               {"$set": {"status": "Paid", "paidAt": datetime.now()}})
            flash("Payment recorded.")
            st.rerun()
else:
    st.info("No bills yet.")
