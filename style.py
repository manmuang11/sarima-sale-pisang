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
          --yellow-border:#E0B84C;
        }

        html, body, [class*="css"]{
          font-family: "Plus Jakarta Sans", system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
        }

        .stApp{
          background: radial-gradient(1200px 700px at 50% 8%, #FFF3C6 0%, var(--bg) 55%, var(--bg) 100%);
        }

        header[data-testid="stHeader"]{display:none;}

        div.block-container{
          max-width: 1200px !important;
          padding-top: 1.2rem !important;
          padding-bottom: 2rem !important;
        }

        /* buttons */
        .stButton > button{
          background: var(--yellow);
          color: #1f1f1f;
          border: 1px solid var(--yellow-border);
          border-radius: 14px;
          padding: 0.6rem 1rem;
          font-weight: 800;
          box-shadow: 0 6px 18px rgba(0,0,0,0.08);
        }

        /* inputs */
        .stTextInput input{
          border-radius: 14px !important;
          border: 1px solid var(--border) !important;
          background: #fff !important;
          height: 46px !important;
        }

        section[data-testid="stSidebar"]{
          background: #fff;
          border-right: 1px solid var(--border);
        }

        /* login card (NORMAL, BUKAN overlay) */
        .login-page{
          display: flex;
          justify-content: center;
          margin-top: 36px;
        }
        .login-card{
          width: 420px;
          background: rgba(255,255,255,0.98);
          border: 2px solid rgba(234,223,203,0.95);
          border-radius: 22px;
          box-shadow: 0 16px 45px rgba(0,0,0,0.10);
          padding: 28px 26px 22px;
        }
        .login-title{
          text-align:center;
          font-weight: 800;
          font-size: 34px;
          margin: 0 0 4px 0;
          color: var(--text);
        }
        .login-sub{
          text-align:center;
          color: var(--muted);
          font-size: 14px;
          margin-bottom: 18px;
        }
        .login-card .stButton > button{
          width: 100% !important;
          padding: 0.85rem 1rem !important;
          border-radius: 16px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
