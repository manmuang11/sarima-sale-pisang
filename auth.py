# auth.py
import streamlit as st
import hashlib

def _hash(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

def _get_users():
    if "users" in st.secrets:
        return st.secrets["users"]
    return {
        "admin": {"password_hash": _hash("admin123"), "role": "admin"},
        "umkm": {"password_hash": _hash("umkm123"), "role": "umkm"},
    }

def login():
    if st.session_state.get("logged_in", False):
        return st.session_state.get("role")

    users = _get_users()

    st.markdown('<div class="login-wrap is-active">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">Login</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-sub">Masuk untuk mengakses dashboard</div>', unsafe_allow_html=True)

        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Masuk", key="login_btn"):
            u = (username or "").strip()
            pw = password or ""
            if u in users and users[u]["password_hash"] == _hash(pw):
                st.session_state.logged_in = True
                st.session_state.role = users[u]["role"]
                st.rerun()
            else:
                st.error("❌ Username / password salah")

        st.markdown('<div class="login-hint">Gunakan akun admin / umkm</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    return None

def logout_button():
    if st.button("Logout", key="logout_btn"):
        st.session_state.clear()
        st.rerun()
