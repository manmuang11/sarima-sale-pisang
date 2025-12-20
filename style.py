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

        /* Background */
        .stApp{
          background: radial-gradient(1200px 700px at 50% 8%, #FFF3C6 0%, var(--bg) 55%, var(--bg) 100%);
        }

        /* Card feel */
        .stMarkdown, .stDataFrame, .stTable, .stAlert, .stExpander {
          border-radius: 16px;
        }

        /* Buttons global */
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

        /* Inputs global */
        .stTextInput input, .stSelectbox div[data-baseweb="select"] > div{
          border-radius: 14px !important;
          border: 1px solid var(--border) !important;
          background: #fff !important;
        }

        /* Sidebar style (nanti muncul setelah login) */
        section[data-testid="stSidebar"]{
          background: #fff;
          border-right: 1px solid var(--border);
        }

        /* ======================================================
           FORCE CLEAN LAYOUT (BIAR LOGIN NGGAK KEBAWAH)
           ====================================================== */
        header[data-testid="stHeader"]{display:none;}
        div.block-container{
          padding-top: 0 !important;
          padding-bottom: 0 !important;
          max-width: none !important;
        }

        /* ======================================================
           LOGIN PAGE (CARD FIXED CENTER)
           ====================================================== */
        .login-wrap{
          position: fixed;
          inset: 0;
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 9999;
          padding: 18px;
        }

        /* CARD: kunci lebar biar ga melebar */
        .login-card{
          width: 420px !important;
          max-width: 92vw !important;
          background: rgba(255,255,255,0.95);
          border: 1px solid var(--border);
          border-radius: 22px;
          box-shadow: 0 18px 55px rgba(0,0,0,0.15);
          padding: 26px 24px 22px;
          position: relative;
        }

        /* Icon/logo bulat di atas card */
        .login-icon{
          position:absolute;
          top:-34px;
          left:50%;
          transform:translateX(-50%);
          width:68px;
          height:68px;
          border-radius:999px;
          background: linear-gradient(180deg, var(--yellow-soft), var(--yellow));
          display:flex;
          align-items:center;
          justify-content:center;
          border:7px solid var(--bg);
          box-shadow: 0 12px 32px rgba(0,0,0,0.12);
          overflow: hidden; /* biar logo rapi */
        }

        .login-title{
          text-align:center;
          font-weight:800;
          font-size:34px;
          margin-top:18px;
          margin-bottom:4px;
          color: var(--text);
        }

        .login-sub{
          text-align:center;
          color: var(--muted);
          font-size:14px;
          margin-bottom:18px;
        }

        .login-hint{
          text-align:center;
          font-size:12.5px;
          color: var(--muted);
          margin-top:14px;
        }

        /* Paksa semua komponen streamlit di dalam card jadi rapih */
        .login-card [data-testid="stForm"],
        .login-card [data-testid="stTextInput"],
        .login-card .stButton,
        .login-card [data-testid="stCheckbox"]{
          width: 100% !important;
        }

        .login-card input{
          height:46px !important;
          border-radius:14px !important;
        }

        .login-card .stButton > button{
          width:100% !important;
          padding:0.85rem 1rem !important;
          border-radius:16px !important;
          font-weight:800 !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
