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
# LOAD CSS (WAJIB PALING ATAS)
# =========================================================
load_css()

# =========================================================
# LOGIN PAGE (HIDE HEADER + SIDEBAR TOTAL)
# =========================================================
st.markdown(
    """
    <style>
    /* HILANGIN HEADER KOSONG STREAMLIT */
    header[data-testid="stHeader"]{display:none;}

    /* HILANGIN HAMBURGER */
    [data-testid="stSidebarCollapsedControl"]{display:none;}

    /* HILANGIN SIDEBAR */
    section[data-testid="stSidebar"]{display:none;}
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# RENDER LOGIN CARD
# =========================================================
role = login()

# STOP DI SINI KALO BELUM LOGIN
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
