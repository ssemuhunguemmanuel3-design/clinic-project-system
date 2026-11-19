import os

try:
    import streamlit as st
    MONGO_URI = st.secrets.get("MONGO_URI")
except Exception:
    MONGO_URI = None

MONGO_URI = MONGO_URI or os.getenv("MONGO_URI", "mongodb://localhost:27017/")

DB_NAME = "clinicDB"
CLINIC_NAME = "City Health Clinic"
LOW_STOCK_LEVEL = 10
