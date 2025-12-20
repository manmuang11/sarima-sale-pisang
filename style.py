# style.py
import streamlit as st

def load_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700;800&display=swap');

        html, body, [class*="css"]{
          font-family: "Plus Jakarta Sans", system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
        }

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

        /* Background (lebih creamy / glow) */
        .stApp{
          background: radial-gradient(1200px 700px at 50% 8%, #FFF3C6 0%, var(--bg) 55%, var(--bg) 100%);
        }

        /* Card feel */
        .stMarkdown, .stDataFrame, .stTable, .stAlert, .stExpander {
          border-radius: 16px;
        }

        /* Buttons */
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

        /* Inputs */
        .stTextInput input, .stSelectbox div[data-baseweb="select"] > div{
          border-radius: 14px !important;
          border: 1px solid var(--border) !important;
          background: #fff !important;
        }

        /* Sidebar (akan muncul setelah login) */
        section[data-testid="stSidebar"]{
          background: #fff;
          border-right: 1px solid var(--border);
        }

        /* =========================
           LOGIN CARD (FIGMA VIBES)
           ========================= */

        .login-wrap{
          min-height: 100vh;
          display:flex;
          align-items:center;
          justify-content:center;
          padding: 0 16px;
        }

        .login-card{
          width: 420px;
          max-width: 92vw;
          background: rgba(255,255,255,0.92);
          border: 1px solid rgba(234,223,203,0.95);
          border-radius: 22px;
          box-shadow: 0 18px 55px rgba(0,0,0,0.12);
          padding: 26px 24px 20px 24px;
          position: relative;
        }

        .login-icon{
          position:absolute;
          left: 50%;
          top: -34px;
          transform: translateX(-50%);
          width: 68px;
          height: 68px;
          border-radius: 999px;
          background: linear-gradient(180deg, #FFF1B8, #F4B400);
          display:flex;
          align-items:center;
          justify-content:center;
          border: 7px solid rgba(251,247,239,0.98);
          box-shadow: 0 12px 32px rgba(0,0,0,0.12);
          font-size: 28px;
        }

        .login-title{
          text-align:center;
          font-weight: 800;
          font-size: 34px;
          margin-top: 18px;
          margin-bottom: 2px;
          color: var(--text);
        }

        .login-sub{
          text-align:center;
          color: var(--muted);
          margin-bottom: 18px;
          font-size: 14px;
        }

        .login-hint{
          text-align:center;
          color: var(--muted);
          font-size: 12.5px;
          margin-top: 14px;
        }

        .login-card [data-testid="stTextInput"]{
          margin: 10px 0 0 0;
        }

        .login-card input{
          height: 46px !important;
          border-radius: 14px !important;
        }

        .login-card [data-testid="stCheckbox"]{
          margin-top: 8px;
        }

        .login-card .stButton > button{
          width: 100%;
          padding: 0.85rem 1rem;
          font-size: 15px;
          border-radius: 16px;
        }

        /* =========================
           FORCE LOGIN CENTER (FINAL)
           ========================= */

        /* MATIIN HEADER STREAMLIT (ruang kosong atas) */
        header[data-testid="stHeader"]{
          display: none;
        }

        /* MATIIN PADDING DEFAULT STREAMLIT */
        div.block-container{
          padding-top: 0 !important;
          padding-bottom: 0 !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
