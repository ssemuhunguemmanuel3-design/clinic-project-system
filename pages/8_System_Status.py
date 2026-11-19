import streamlit as st
import pandas as pd
from db import client, db
from config import CLINIC_NAME, DB_NAME
from ui import page_setup

page_setup("System Status", "⚙️")
st.write(f"**Clinic:** {CLINIC_NAME}")

try:
    client.admin.command("ping")
    st.success("MongoDB connection: OK")
except Exception as e:
    st.error(f"MongoDB connection failed: {e}")
    st.stop()

rows = [{"Collection": n, "Documents": db[n].count_documents({})}
        for n in sorted(db.list_collection_names())]
st.dataframe(pd.DataFrame(rows), use_container_width=True)

stats = db.command("dbstats")
st.write(f"Database `{DB_NAME}`: {stats['collections']} collections, "
         f"{stats['dataSize'] / 1024:.1f} KB of data, {stats['indexes']} indexes.")
