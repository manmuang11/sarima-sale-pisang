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

        .stApp { background: var(--bg); }
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
        </style>
        """,
        unsafe_allow_html=True,
    )
