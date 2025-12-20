# auth.py
import streamlit as st
import hashlib

def _hash(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

def _get_users():
    """
    Prioritas:
    1) st.secrets["users"] kalau ada (lebih aman)
    2) fallback hardcode (buat development)
    Format users:
      {
        "admin": {"password_hash": "...", "role": "admin"},
        "umkm":  {"password_hash": "...", "role": "umkm"}
      }
    """
    if "users" in st.secrets:
        return st.secrets["users"]

    # fallback dev (ganti password sesuai mau kamu)
    return {
        "admin": {"password_hash": _hash("admin123"), "role": "admin"},
        "umkm": {"password_hash": _hash("umkm123"), "role": "umkm"},
    }

def logout_button():
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()

def login():
    """
    Return role: "admin" / "umkm" atau None jika belum login.
    """
    if st.session_state.get("logged_in"):
        return st.session_state.get("role")

    users = _get_users()

    st.markdown("## 🔐 Login")
    st.caption("Masuk sebagai Admin atau UMKM")

    username = st.text_input("Username", placeholder="admin / umkm")
    password = st.text_input("Password", type="password", placeholder="••••••••")

    colA, colB = st.columns([1, 2])
    with colA:
        do_login = st.button("Masuk")

    if do_login:
        u = users.get(username)
        if not u:
            st.error("Username tidak ditemukan.")
            return None

        if _hash(password) != u["password_hash"]:
            st.error("Password salah.")
            return None

        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        st.session_state["role"] = u.get("role", "umkm")
        st.success("Login berhasil!")
        st.rerun()

    return None
