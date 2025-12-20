# app.py
import streamlit as st
from style import load_css
from auth import login, logout_button

from admin import admin_page
from umkm import umkm_page

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Prediksi Kebutuhan Pisang",
    page_icon="🍌",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()

# =========================================================
# SIDEBAR HEADER
# =========================================================
with st.sidebar:
    st.markdown("### 🍌 Prediksi Pisang")
    st.caption("Sistem Prediksi Kebutuhan Pisang")
    st.divider()

# =========================================================
# LOGIN
# =========================================================
role = login()
if role is None:
    st.stop()

# =========================================================
# SIDEBAR AFTER LOGIN
# =========================================================
with st.sidebar:
    st.success(f"Login sebagai: **{role.upper()}**")
    logout_button()

# =========================================================
# ROUTING PER ROLE
# =========================================================
if role == "admin":
    admin_page()
else:
    umkm_page()
