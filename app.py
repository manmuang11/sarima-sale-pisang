# app.py
import streamlit as st
from auth import login, logout_button
from admin import admin_page
from umkm import umkm_page

st.set_page_config(
    page_title="Prediksi Kebutuhan Pisang",
    page_icon="🍌",
    layout="wide",
)

# ===== EMERGENCY CSS: matiin overlay gelap yang nyangkut (tanpa style.py) =====
st.markdown(
    """
    <style>
    /* overlay/backdrop internal streamlit (variasi versi) */
    div[data-testid="stOverlay"],
    div[data-testid="stModal"],
    div[data-testid="stDialog"]{
      opacity: 0 !important;
      background: transparent !important;
      pointer-events: none !important;
    }

    /* dialog backdrop (kalau browser bikin) */
    dialog::backdrop{
      background: transparent !important;
    }

    /* tembak fullscreen fixed layer gelap yang kadang nyangkut */
    body > div[style*="position: fixed"][style*="inset: 0"]{
      opacity: 0 !important;
      background: transparent !important;
      pointer-events: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
