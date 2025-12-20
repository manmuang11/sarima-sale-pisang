# umkm.py
from pathlib import Path
import pandas as pd
import streamlit as st
import altair as alt

DATA_PATH = Path("data") / "data_umkm.xlsx"
OUTPUT_PATH = Path("data") / "hasil_prediksi.xlsx"

def _load_actual() -> pd.DataFrame:
    if not DATA_PATH.exists():
        return pd.DataFrame(columns=["tanggal", "nilai"])
    df = pd.read_excel(DATA_PATH)
    return df

def _load_forecast() -> pd.DataFrame:
    if not OUTPUT_PATH.exists():
        return pd.DataFrame(columns=["tanggal", "prediksi"])
    df = pd.read_excel(OUTPUT_PATH)
    return df

def _chart_actual(df: pd.DataFrame):
    if df.empty:
        return None
    df2 = df.copy()
    df2["tanggal"] = pd.to_datetime(df2["tanggal"], errors="coerce")
    df2["nilai"] = pd.to_numeric(df2["nilai"], errors="coerce")
    df2 = df2.dropna()

    c = (
        alt.Chart(df2)
        .mark_line()
        .encode(
            x=alt.X("tanggal:T", title="Tanggal"),
            y=alt.Y("nilai:Q", title="Nilai"),
            tooltip=[
                alt.Tooltip("tanggal:T", title="Tanggal"),
                alt.Tooltip("nilai:Q", title="Nilai"),
            ],
        )
        .properties(height=320)
        .interactive()
    )
    return c

def _chart_actual_vs_forecast(actual_df: pd.DataFrame, forecast_df: pd.DataFrame):
    if actual_df.empty or forecast_df.empty:
        return None

    a = actual_df.copy()
    f = forecast_df.copy()

    a["tanggal"] = pd.to_datetime(a["tanggal"], errors="coerce")
    a["nilai"] = pd.to_numeric(a["nilai"], errors="coerce")
    a = a.dropna()

    f["tanggal"] = pd.to_datetime(f["tanggal"], errors="coerce")
    f["prediksi"] = pd.to_numeric(f["prediksi"], errors="coerce")
    f = f.dropna()

    c1 = (
        alt.Chart(a)
        .mark_line()
        .encode(
            x=alt.X("tanggal:T", title="Tanggal"),
            y=alt.Y("nilai:Q", title="Nilai"),
            tooltip=[
                alt.Tooltip("tanggal:T", title="Tanggal"),
                alt.Tooltip("nilai:Q", title="Aktual"),
            ],
        )
    )

    c2 = (
        alt.Chart(f)
        .mark_line(strokeDash=[6, 4])
        .encode(
            x="tanggal:T",
            y=alt.Y("prediksi:Q", title="Nilai / Prediksi"),
            tooltip=[
                alt.Tooltip("tanggal:T", title="Tanggal"),
                alt.Tooltip("prediksi:Q", title="Prediksi"),
            ],
        )
    )

    return (c1 + c2).properties(height=340).interactive()

def umkm_page():
    st.markdown("## 🍌 Dashboard UMKM")
    st.caption("Lihat data historis & hasil prediksi (read-only)")

    df_actual = _load_actual()
    df_forecast = _load_forecast()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Data historis", 0 if df_actual.empty else len(df_actual))
    with col2:
        st.metric("Prediksi tersedia", "Ya" if not df_forecast.empty else "Belum")
    with col3:
        if not df_actual.empty:
            last_date = pd.to_datetime(df_actual["tanggal"], errors="coerce").max()
            st.metric("Periode terakhir", "-" if pd.isna(last_date) else last_date.strftime("%Y-%m"))
        else:
            st.metric("Periode terakhir", "-")

    st.divider()

    st.markdown("### 📌 Grafik Data Historis")
    c_actual = _chart_actual(df_actual)
    if c_actual is None:
        st.warning("Data historis belum tersedia. Hubungi Admin untuk upload data.")
    else:
        st.altair_chart(c_actual, use_container_width=True)

    st.markdown("### 📈 Grafik Aktual vs Prediksi")
    c_mix = _chart_actual_vs_forecast(df_actual, df_forecast)
    if c_mix is None:
        if df_forecast.empty:
            st.info("Prediksi belum tersedia. Admin perlu menjalankan SARIMA dulu.")
        else:
            st.info("Tidak bisa menampilkan grafik gabungan (cek format data).")
    else:
        st.altair_chart(c_mix, use_container_width=True)

    st.markdown("### 📄 Tabel Hasil Prediksi")
    if df_forecast.empty:
        st.info("Belum ada hasil prediksi.")
    else:
        st.dataframe(df_forecast, use_container_width=True)

        st.download_button(
            "⬇️ Download hasil_prediksi.xlsx",
            data=OUTPUT_PATH.read_bytes(),
            file_name="hasil_prediksi.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
