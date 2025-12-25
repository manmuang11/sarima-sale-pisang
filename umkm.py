import streamlit as st
import pandas as pd
from pathlib import Path

PRED_CSV_PATH = Path("data") / "prediksi_sarima.csv"

def umkm_page():
    st.markdown("## 👩‍🍳 Dashboard UMKM")
    st.caption("Lihat hasil prediksi yang dibuat admin.")

    if not PRED_CSV_PATH.exists():
        st.warning("Belum ada hasil prediksi. Minta admin jalankan SARIMA dulu.")
        st.stop()

    df = pd.read_csv(PRED_CSV_PATH)
    st.success("✅ Hasil prediksi tersedia.")
    st.dataframe(df, use_container_width=True)

    st.download_button(
        "⬇️ Download prediksi_sarima.csv",
        data=PRED_CSV_PATH.read_bytes(),
        file_name="prediksi_sarima.csv",
        mime="text/csv",
    )
