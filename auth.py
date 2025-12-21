# auth.py
import streamlit as st
import hashlib
import base64
from pathlib import Path

LOGO_PATH = Path("assets") / "logo.png"


def _hash(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()


def _get_users():
    # support Streamlit Cloud secrets.toml
    if "users" in st.secrets:
        return st.secrets["users"]

    # fallback local
    return {
        "admin": {"password_hash": _hash("admin123"), "role": "admin"},
        "umkm": {"password_hash": _hash("umkm123"), "role": "umkm"},
    }


def _logo_base64(path: Path) -> str | None:
    try:
        if path.exists():
            return base64.b64encode(path.read_bytes()).decode("utf-8")
    except Exception:
        pass
    return None


def logout_button():
    if st.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()


def login():
    # already logged in
    if st.session_state.get("logged_in"):
        return st.session_state.get("role")

    users = _get_users()

    # overlay wrapper
    st.markdown('<div class="login-wrap">', unsafe_allow_html=True)

    # center card using columns (ANTI MELEBAR)
    left, mid, right = st.columns([1.2, 1, 1.2], gap="large")
    with mid:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        st.markdown('<div class="login-title">Login</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-sub">Masuk untuk mengakses dashboard.</div>', unsafe_allow_html=True)

        username = st.text_input("", placeholder="Username (admin / umkm)")
        password = st.text_input("", type="password", placeholder="Password")

        remember = st.checkbox("Ingat saya", value=False)
        do_login = st.button("MASUK", use_container_width=True)

        st.markdown(
            '<div class="login-hint">UMKM hanya melihat hasil. Admin mengelola data dan prediksi.</div>',
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)  # end login-card

    st.markdown("</div>", unsafe_allow_html=True)      # end login-wrap

    if do_login:
        username_clean = (username or "").strip()
        if not username_clean or not password:
            st.warning("Username dan password wajib diisi.")
            return None

        u = users.get(username_clean)
        if not u:
            st.error("Username tidak ditemukan.")
            return None

        if _hash(password) != u.get("password_hash", ""):
            st.error("Password salah.")
            return None

        st.session_state["logged_in"] = True
        st.session_state["username"] = username_clean
        st.session_state["role"] = u.get("role", "umkm")
        st.session_state["remember"] = remember
        st.rerun()

    return None
