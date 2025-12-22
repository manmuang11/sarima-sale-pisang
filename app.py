# app.py
import streamlit as st
# from style import load_css   # <-- MATIIN DULU biar ga gelap & ga nge-block klik
from auth import login, logout_button
from admin import admin_page
from umkm import umkm_page

st.set_page_config(
    page_title="Prediksi Kebutuhan Pisang",
    page_icon="🍌",
    layout="wide",
)

# load_css()  # <-- MATIIN DULU

role = login()
if role is None:
    st.stop()

with st.sidebar:
    st.markdown("### 🍌 Prediksi Pisang")
    st.caption("Sistem Prediksi Kebutuhan Pisang")
    st.success(f"Login sebagai: **{role.upper()}**")
    logout_button()

if role == "admin":
    admin_page()
else:
    umkm_page()
