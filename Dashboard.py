import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from db import patients, doctors, appointments, visits, medicines, billing
from config import CLINIC_NAME, LOW_STOCK_LEVEL

st.set_page_config(page_title=f"Dashboard | {CLINIC_NAME}", page_icon="📈", layout="wide")
st.title(f"📈 {CLINIC_NAME} Dashboard")
st.caption(datetime.now().strftime("%A, %d %B %Y"))

def money_total(status):
    r = list(billing.aggregate([
        {"$match": {"status": status}},
        {"$group": {"_id": None, "t": {"$sum": "$total"}}}]))
    return r[0]["t"] if r else 0

def chart(title, collection, pipeline, label, kind="bar"):
    st.subheader(title)
    rows = list(collection.aggregate(pipeline))
    if not rows:
        st.info("No data yet.")
        return
    df = pd.DataFrame(rows).rename(columns={"_id": label})
    df[label] = df[label].fillna("Unknown")
    df = df.set_index(label)
    if kind == "line":
        st.line_chart(df)
    else:
        st.bar_chart(df)

today = datetime.combine(datetime.today(), datetime.min.time())
tomorrow = today + timedelta(days=1)

# 1. KPI cards
a1, a2, a3, a4 = st.columns(4)
a1.metric("Patients", patients.count_documents({}))
a2.metric("Doctors", doctors.count_documents({}))
a3.metric("Appointments today", appointments.count_documents({"date": {"$gte": today, "$lt": tomorrow}}))
a4.metric("Upcoming (scheduled)", appointments.count_documents({"date": {"$gte": today}, "status": "Scheduled"}))

b1, b2, b3, b4 = st.columns(4)
b1.metric("Revenue collected (UGX)", f"{money_total('Paid'):,.0f}")
b2.metric("Outstanding (UGX)", f"{money_total('Unpaid'):,.0f}")
b3.metric("Low-stock medicines", medicines.count_documents({"stock": {"$lt": LOW_STOCK_LEVEL}}))
b4.metric("Total visits", visits.count_documents({}))

st.divider()

# 2. Alerts
st.subheader("⚠️ Alerts")
low = list(medicines.find({"stock": {"$lt": LOW_STOCK_LEVEL}}))
expiring = list(medicines.find({"expiryDate": {"$lte": today + timedelta(days=90)}}))
unpaid = billing.count_documents({"status": "Unpaid"})
if not (low or expiring or unpaid):
    st.success("No alerts. Everything is in order.")
if low:
    st.warning("Low stock: " + ", ".join(f"{m['name']} ({m['stock']} left)" for m in low))
if expiring:
    st.error("Expired or expiring within 90 days: " + ", ".join(
        f"{m['name']} ({m['expiryDate']:%Y-%m-%d})" for m in expiring))
if unpaid:
    st.info(f"{unpaid} unpaid bill(s) waiting for payment.")

st.divider()

# 3. Today's appointments
st.subheader("📅 Today's appointments")
rows = [{"Time": a.get("time", ""), "Patient": a["patientName"], "Doctor": a["doctorName"],
         "Reason": a.get("reason", ""), "Status": a["status"]}
        for a in appointments.find({"date": {"$gte": today, "$lt": tomorrow}}).sort("time", 1)]
if rows:
    st.dataframe(pd.DataFrame(rows), use_container_width=True)
else:
    st.info("No appointments scheduled for today.")

st.divider()

# 4. Charts
c1, c2 = st.columns(2)
with c1:
    chart("Appointments per doctor", appointments,
          [{"$group": {"_id": "$doctorName", "total": {"$sum": 1}}}], "Doctor")
with c2:
    chart("Appointments by status", appointments,
          [{"$group": {"_id": "$status", "total": {"$sum": 1}}}], "Status")

c3, c4 = st.columns(2)
with c3:
    chart("Patients by gender", patients,
          [{"$group": {"_id": "$gender", "total": {"$sum": 1}}}], "Gender")
with c4:
    chart("Top 5 diagnoses", visits,
          [{"$group": {"_id": "$diagnosis", "total": {"$sum": 1}}},
           {"$sort": {"total": -1}}, {"$limit": 5}], "Diagnosis")

c5, c6 = st.columns(2)
with c5:
    chart("Revenue per month (UGX)", billing,
          [{"$match": {"status": "Paid"}},
           {"$group": {"_id": {"$dateToString": {"format": "%Y-%m", "date": "$date"}},
                       "revenue": {"$sum": "$total"}}},
           {"$sort": {"_id": 1}}], "Month", kind="line")
with c6:
    chart("New patients per month", patients,
          [{"$match": {"createdAt": {"$exists": True}}},
           {"$group": {"_id": {"$dateToString": {"format": "%Y-%m", "date": "$createdAt"}},
                       "new": {"$sum": 1}}},
           {"$sort": {"_id": 1}}], "Month", kind="line")

st.divider()

# 5. Recent activity
r1, r2 = st.columns(2)
with r1:
    st.subheader("🩺 Latest visits")
    v = [{"Date": x["visitDate"].strftime("%Y-%m-%d"), "Patient": x["patientName"],
          "Diagnosis": x["diagnosis"]} for x in visits.find().sort("visitDate", -1).limit(5)]
    if v:
        st.dataframe(pd.DataFrame(v), use_container_width=True)
    else:
        st.info("No visits yet.")
with r2:
    st.subheader("💰 Latest bills")
    b = [{"Date": x["date"].strftime("%Y-%m-%d"), "Patient": x["patientName"],
          "Total (UGX)": x["total"], "Status": x["status"]}
         for x in billing.find().sort("date", -1).limit(5)]
    if b:
        st.dataframe(pd.DataFrame(b), use_container_width=True)
    else:
        st.info("No bills yet.")

st.button("🔄 Refresh")
