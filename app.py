# app.py
import streamlit as st
from style import load_css
from auth import login, logout_button

# (nanti step berikutnya kita isi beneran)
def admin_page_placeholder():
    st.markdown("## 🛠️ Admin")
    st.info("Halaman admin belum diisi. Next step kita bikin admin.py.")

def umkm_page_placeholder():
    st.markdown("## 🍌 UMKM")
    st.info("Halaman UMKM belum diisi. Next step kita bikin umkm.py.")

st.set_page_config(
    page_title="Prediksi Kebutuhan Pisang",
    page_icon="🍌",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()

# Sidebar header
with st.sidebar:
    st.markdown("### 🍌 Prediksi Pisang")
    st.caption("Sistem Prediksi Kebutuhan Pisang")
    st.divider()

role = login()

if role is None:
    st.stop()

# setelah login
with st.sidebar:
    st.success(f"Login sebagai: **{role.upper()}**")
    logout_button()

# routing per role
if role == "admin":
    admin_page_placeholder()
else:
    umkm_page_placeholder()
