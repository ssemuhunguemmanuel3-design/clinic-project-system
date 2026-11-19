import streamlit as st
import pandas as pd
from db import patients, doctors, appointments, visits, medicines, billing, to_df
from ui import page_setup

page_setup("Reports", "📊")

def bar(title, collection, pipeline, label):
    st.subheader(title)
    rows = list(collection.aggregate(pipeline))
    if rows:
        df = pd.DataFrame(rows).rename(columns={"_id": label})
        df[label] = df[label].fillna("Unknown")
        st.bar_chart(df.set_index(label))
    else:
        st.info("No data yet.")

bar("Revenue per month (paid bills, UGX)", billing,
    [{"$match": {"status": "Paid"}},
     {"$group": {"_id": {"$dateToString": {"format": "%Y-%m", "date": "$date"}},
                 "revenue": {"$sum": "$total"}}},
     {"$sort": {"_id": 1}}], "Month")

bar("Top 5 medicines sold", billing,
    [{"$unwind": "$items"},
     {"$group": {"_id": "$items.name", "sold": {"$sum": "$items.qty"}}},
     {"$sort": {"sold": -1}}, {"$limit": 5}], "Medicine")

bar("Doctor workload (appointments)", appointments,
    [{"$group": {"_id": "$doctorName", "total": {"$sum": 1}}}], "Doctor")

bar("Top 5 diagnoses", visits,
    [{"$group": {"_id": "$diagnosis", "total": {"$sum": 1}}},
     {"$sort": {"total": -1}}, {"$limit": 5}], "Diagnosis")

st.subheader("⬇️ Export data (CSV)")
for label, col in [("Patients", patients), ("Doctors", doctors),
                   ("Appointments", appointments), ("Medicines", medicines),
                   ("Bills", billing)]:
    st.download_button(f"Download {label}", to_df(col.find()).to_csv(index=False),
                       f"{label.lower()}.csv", "text/csv", key=f"dl_{label}")
