import streamlit as st
from config import CLINIC_NAME

def flash(message):
    """Remember a message to show after the page reloads."""
    st.session_state["_flash"] = message

def page_setup(title, icon):
    st.set_page_config(page_title=f"{title} | {CLINIC_NAME}", page_icon=icon, layout="wide")
    st.title(f"{icon} {title}")
    st.sidebar.caption(CLINIC_NAME)
    message = st.session_state.pop("_flash", None)
    if message:
        st.success(message)
