# auth.py
import streamlit as st
import hashlib

def _hash(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

def _get_users():
    """
    Prioritas:
    1) st.secrets["users"] (kalau di Streamlit Cloud / secrets.toml)
    2) fallback hardcode (buat development)
    """
    if "users" in st.secrets:
        return st.secrets["users"]

    return {
        "admin": {"password_hash": _hash("admin123"), "role": "admin"},
        "umkm": {"password_hash": _hash("umkm123"), "role": "umkm"},
    }

def logout_button():
    if st.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

def login():
    """
    Return role: "admin" / "umkm" atau None kalau belum login.
    """
    if st.session_state.get("logged_in"):
        return st.session_state.get("role")

    users = _get_users()

    # --- Center Login Card ---
    st.markdown('<div class="login-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="login-card">', unsafe_allow_html=True)

    st.markdown('<div class="login-icon">👤</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-title">Login</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-sub">Masuk untuk mengakses dashboard.</div>', unsafe_allow_html=True)

    username = st.text_input("Username", placeholder="admin / umkm", label_visibility="collapsed")
    password = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")

    remember = st.checkbox("Ingat saya", value=False)
    do_login = st.button("MASUK", use_container_width=True)

    st.markdown('<div class="login-hint">UMKM hanya melihat hasil. Admin mengelola data dan prediksi.</div>', unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)
    # --- End Card ---

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
        st.session_state["remember"] = remember
        st.success("Login berhasil!")
        st.rerun()

    return None
