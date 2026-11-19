import re
import streamlit as st
from datetime import datetime
from db import medicines, to_df
from config import LOW_STOCK_LEVEL
from ui import page_setup, flash

page_setup("Medicines & Stock", "💊")

low = list(medicines.find({"stock": {"$lt": LOW_STOCK_LEVEL}}))
if low:
    st.warning("Low stock: " + ", ".join(f"{m['name']} ({m['stock']})" for m in low))

with st.expander("➕ Add a medicine"):
    with st.form("add_med", clear_on_submit=True):
        name = st.text_input("Medicine name")
        category = st.selectbox("Category", ["Antibiotic", "Painkiller", "Antimalarial", "Vitamin", "Other"])
        stock = st.number_input("Stock quantity", min_value=0, value=50, step=1)
        price = st.number_input("Unit price (UGX)", min_value=0, value=1000, step=100)
        expiry = st.date_input("Expiry date")
        if st.form_submit_button("Save medicine"):
            if not name:
                st.error("Medicine name is required.")
            elif medicines.find_one({"name": {"$regex": f"^{re.escape(name)}$", "$options": "i"}}):
                st.error("That medicine already exists. Use Restock below.")
            else:
                medicines.insert_one({"name": name, "category": category, "stock": stock,
                                      "unitPrice": price,
                                      "expiryDate": datetime.combine(expiry, datetime.min.time())})
                st.success("Medicine saved.")

med_list = list(medicines.find().sort("name", 1))
if not med_list:
    st.info("No medicines yet.")
else:
    st.dataframe(to_df(med_list).drop(columns=["_id"]), use_container_width=True)

    st.subheader("📦 Restock")
    m = st.selectbox("Medicine", med_list,
                     format_func=lambda x: f"{x['name']} (stock {x['stock']})", key="restock")
    qty = st.number_input("Quantity to add", min_value=1, value=10, step=1)
    if st.button("Add stock"):
        medicines.update_one({"_id": m["_id"]}, {"$inc": {"stock": qty}})
        flash(f"Added {qty} to {m['name']}.")
        st.rerun()

    st.subheader("🗑️ Delete a medicine")
    d = st.selectbox("Medicine to delete", med_list, format_func=lambda x: x["name"], key="delete")
    ok = st.checkbox("I confirm the deletion", key=f"del_ok_{d['_id']}")
    if st.button("Delete medicine"):
        if not ok:
            st.error("Tick the confirmation box first.")
        else:
            medicines.delete_one({"_id": d["_id"]})
            flash("Medicine deleted.")
            st.rerun()
