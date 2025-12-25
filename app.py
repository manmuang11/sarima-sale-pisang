# app.py (FULL - versi debug: CSS dimatiin dulu biar tombol bisa diklik)
import streamlit as st
# from style import load_css   # <-- sementara MATIIN CSS dulu
from auth import login, logout_button
from admin import admin_page
from umkm import umkm_page

st.set_page_config(
    page_title="Prediksi Kebutuhan Pisang",
    page_icon="🍌",
    layout="wide",
)

# load_css()  # <-- sementara MATIIN CSS dulu (ini biang tombol gak bisa diklik)

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
