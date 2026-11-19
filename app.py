import runpy
import streamlit as st

try:
    runpy.run_path("Dashboard.py", run_name="__main__")
except Exception as exc:
    st.set_page_config(page_title="City Health Clinic", page_icon="🏥", layout="wide")
    st.title("🏥 City Health Clinic")
    st.error("The application could not connect to MongoDB.")
    st.info(
        "For a hosted deployment, add an `MONGO_URI` secret containing the MongoDB Atlas "
        "connection string. Do not use `localhost` on a cloud server."
    )
    with st.expander("Technical details"):
        st.code(str(exc))
