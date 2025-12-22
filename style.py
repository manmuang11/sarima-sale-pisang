# style.py
import streamlit as st

def load_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700;800&display=swap');

        :root{
          --bg:#FBF7EF;
          --card:#FFFFFF;
          --border:#EADFCB;
          --text:#1F1F1F;
          --muted:#6E665C;
          --yellow:#F4B400;
          --yellow-soft:#FFF1B8;
          --yellow-border:#E0B84C;
        }

        html, body, [class*="css"]{
          font-family: "Plus Jakarta Sans", system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
        }

        /* ================= BACKGROUND ================= */
        .stApp{
          background: radial-gradient(
            1200px 700px at 50% 8%,
            #FFF3C6 0%,
            var(--bg) 55%,
            var(--bg) 100%
          );
        }

        /* Hide default header */
        header[data-testid="stHeader"]{display:none;}

        /* Jangan bikin page super lebar */
        div.block-container{
          padding-top: 0 !important;
          padding-bottom: 0 !important;
          max-width: 1200px !important;
        }

        /* ================= BUTTONS ================= */
        .stButton > button{
          background: var(--yellow);
          color: #1f1f1f;
          border: 1px solid var(--yellow-border);
          border-radius: 14px;
          padding: 0.6rem 1rem;
          font-weight: 800;
          box-shadow: 0 6px 18px rgba(0,0,0,0.08);
          transition: all 0.15s ease;
        }
        .stButton > button:hover{
          transform: translateY(-1px);
          filter: brightness(0.98);
        }
        .stButton > button:disabled{
          opacity: 0.55;
        }

        /* ================= INPUTS ================= */
        .stTextInput input,
        .stSelectbox div[data-baseweb="select"] > div{
          border-radius: 14px !important;
          border: 1px solid var(--border) !important;
          background: #fff !important;
        }

        /* ================= SIDEBAR ================= */
        section[data-testid="stSidebar"]{
          background: #fff;
          border-right: 1px solid var(--border);
        }

        /* ======================================================
           LOGIN PAGE (SAFE OVERLAY)  ✅ FIX: button bisa diklik
           ====================================================== */
        .login-wrap{
          position: fixed;
          inset: 0;
          display: flex;
          align-items: center;
          justify-content: center;

          /* jangan ekstrem biar ga nabrak layer Streamlit */
          z-index: 10;
          padding: 18px;

          /* KUNCI: wrapper full-screen JANGAN nangkep klik */
          pointer-events: none !important;
        }

        /* kunci lebar kolom tengah (tetap rapi kayak punya kamu) */
        .login-wrap div[data-testid="stHorizontalBlock"]{
          justify-content: center !important;
        }
        .login-wrap
        div[data-testid="stHorizontalBlock"]
        > div[data-testid="column"]:nth-child(2){
          max-width: 420px !important;
          flex: 0 0 420px !important;
        }

        .login-card{
          background: rgba(255,255,255,0.98);
          border: 2px solid rgba(234,223,203,0.95);
          border-radius: 22px;
          box-shadow: 0 16px 45px rgba(0,0,0,0.10);
          padding: 28px 26px 22px;
          position: relative;

          /* KUNCI: yang boleh diklik cuma card + isinya */
          pointer-events: auto !important;
        }

        /* ================= TEXT ================= */
        .login-title{
          text-align: center;
          font-weight: 800;
          font-size: 34px;
          margin: 0 0 4px 0;
          color: var(--text);
        }

        .login-sub{
          text-align: center;
          color: var(--muted);
          font-size: 14px;
          margin-bottom: 18px;
        }

        .login-hint{
          text-align: center;
          font-size: 12.5px;
          color: var(--muted);
          margin-top: 14px;
        }

        /* ================= FORM SPACING ================= */
        .login-card [data-testid="stTextInput"]{
          margin-top: 10px !important;
        }

        .login-card input{
          height: 46px !important;
          border-radius: 14px !important;
        }

        .login-card [data-testid="stCheckbox"]{
          margin-top: 10px !important;
        }

        /* ================= FULL BUTTON ================= */
        .login-card .stButton > button{
          width: 100% !important;
          padding: 0.85rem 1rem !important;
          border-radius: 16px !important;
          font-weight: 800 !important;
        }

        /* PAKSA HILANGIN PILL/DEKOR NYASAR DI LOGIN */
        .login-wrap::before,
        .login-wrap::after,
        .login-card::before,
        .login-card::after{
          content: none !important;
          display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
