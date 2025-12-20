# style.py
import streamlit as st

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700;800&display=swap');

    html, body {
      margin: 0;
      padding: 0;
      height: 100%;
      font-family: "Plus Jakarta Sans", system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      background: radial-gradient(1200px 700px at 50% 8%, #FFF3C6 0%, #FBF7EF 55%, #FBF7EF 100%);
    }

    /* MATIIN SEMUA LAYOUT STREAMLIT */
    header[data-testid="stHeader"]{display:none;}
    section[data-testid="stSidebar"]{display:none;}
    [data-testid="stSidebarCollapsedControl"]{display:none;}
    div.block-container{
      padding: 0 !important;
      margin: 0 !important;
      max-width: none !important;
    }

    /* =========================
       LOGIN FIXED CENTER (ANTI JATUH)
       ========================= */
    .login-wrap{
      position: fixed;
      inset: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 9999;
    }

    .login-card{
      width: 420px;
      max-width: 92vw;
      background: rgba(255,255,255,0.95);
      border: 1px solid #EADFCB;
      border-radius: 22px;
      box-shadow: 0 18px 55px rgba(0,0,0,0.15);
      padding: 26px 24px 22px;
      position: relative;
    }

    .login-icon{
      position:absolute;
      top:-34px;
      left:50%;
      transform:translateX(-50%);
      width:68px;
      height:68px;
      border-radius:999px;
      background: linear-gradient(180deg, #FFF1B8, #F4B400);
      display:flex;
      align-items:center;
      justify-content:center;
      border:7px solid #FBF7EF;
      font-size:28px;
    }

    .login-title{
      text-align:center;
      font-weight:800;
      font-size:34px;
      margin-top:18px;
      margin-bottom:4px;
    }

    .login-sub{
      text-align:center;
      color:#6E665C;
      font-size:14px;
      margin-bottom:18px;
    }

    .login-hint{
      text-align:center;
      font-size:12.5px;
      color:#6E665C;
      margin-top:14px;
    }

    .login-card input{
      height:46px !important;
      border-radius:14px !important;
    }

    .login-card .stButton>button{
      width:100%;
      padding:0.85rem;
      border-radius:16px;
      font-weight:800;
      background:#F4B400;
      border:1px solid #E0B84C;
    }
    </style>
    """, unsafe_allow_html=True)
