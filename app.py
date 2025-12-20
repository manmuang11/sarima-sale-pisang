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

# =========================================================
# LOAD CSS (WAJIB SEBELUM LOGIN)
# =========================================================
load_css()

# =========================================================
# LOGIN PAGE (HIDE SIDEBAR TOTAL)
# =========================================================
st.markdown(
    """
    <style>
    /* hide hamburger */
    [data-testid="stSidebarCollapsedControl"]{display:none;}

    /* hide sidebar */
    section[data-testid="stSidebar"]{display:none;}
    </style>
    """,
    unsafe_allow_html=True
)

# render login card
role = login()

# kalau belum login, STOP di sini (jangan render apa pun lagi)
if role is None:
    st.stop()

# =========================================================
# SIDEBAR SETELAH LOGIN
# =========================================================
with st.sidebar:
    st.markdown("### 🍌 Prediksi Pisang")
    st.caption("Sistem Prediksi Kebutuhan Pisang")
    st.divider()
    st.success(f"Login sebagai: **{role.upper()}**")
    logout_button()

# =========================================================
# ROUTING HALAMAN
# =========================================================
if role == "admin":
    admin_page()
else:
    umkm_page()
