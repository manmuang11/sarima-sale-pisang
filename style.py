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
          background: radial-gradient(1200px 600px at 50% 10%, #FFF3C6 0%, var(--bg) 55%, var(--bg) 100%);
        }

        .block-container { padding-top: 1.2rem; padding-bottom: 2.5rem; }

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

        /* Sidebar */
        section[data-testid="stSidebar"]{
          background: #fff;
          border-right: 1px solid var(--border);
        }

        /* =========================
           LOGIN CARD (FIGMA VIBES)
           ========================= */
        .login-wrap{
          min-height: 72vh;
          display:flex;
          align-items:center;
          justify-content:center;
        }

        .login-card{
          width: min(520px, 92vw);
          background: rgba(255,255,255,0.88);
          border: 1px solid rgba(234,223,203,0.9);
          border-radius: 22px;
          box-shadow: 0 18px 55px rgba(0,0,0,0.10);
          padding: 28px 28px 22px 28px;
          backdrop-filter: blur(10px);
        }

        .login-icon{
          width: 64px;
          height: 64px;
          border-radius: 999px;
          background: linear-gradient(180deg, #FFF1B8, #F4B400);
          display:flex;
          align-items:center;
          justify-content:center;
          margin: -54px auto 10px auto;
          border: 6px solid rgba(251,247,239,0.95);
          box-shadow: 0 10px 30px rgba(0,0,0,0.10);
          font-size: 28px;
        }

        .login-title{
          text-align:center;
          font-weight: 800;
          font-size: 34px;
          margin: 4px 0 2px 0;
          color: var(--text);
        }

        .login-sub{
          text-align:center;
          color: var(--muted);
          margin-bottom: 18px;
        }

        .login-hint{
          text-align:center;
          color: var(--muted);
          font-size: 13px;
          margin-top: 14px;
        }

        /* Rapihin input spacing di dalam card */
        .login-card [data-testid="stTextInput"]{
          margin-top: 6px;
        }

        /* Biar button Masuk full */
        .login-card .stButton > button{
          width: 100%;
          padding: 0.75rem 1rem;
          font-size: 16px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
