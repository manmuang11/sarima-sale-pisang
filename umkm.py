# umkm.py
from pathlib import Path
import pandas as pd
import streamlit as st
import altair as alt

DATA_PATH = Path("data") / "data_umkm.xlsx"

# tetap dukung excel lama (opsional)
OUTPUT_XLSX = Path("data") / "hasil_prediksi.xlsx"
# utama: csv baru (lebih ringan & dipakai UMKM)
PRED_CSV = Path("data") / "prediksi_sarima.csv"


def _load_actual() -> pd.DataFrame:
    if not DATA_PATH.exists():
        return pd.DataFrame(columns=["tanggal", "nilai"])
    df = pd.read_excel(DATA_PATH)
    return df


def _load_forecast() -> pd.DataFrame:
    """
    Prioritas baca CSV baru (pred_sisir/pred_kg + CI).
    Fallback ke excel kalau CSV belum ada.
    """
    if PRED_CSV.exists():
        df = pd.read_csv(PRED_CSV)
        return df

    # fallback lama (kalau masih pakai excel)
    if OUTPUT_XLSX.exists():
        df = pd.read_excel(OUTPUT_XLSX)
        return df

    # default kosong
    return pd.DataFrame(columns=["tanggal", "pred_sisir", "pred_kg"])


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
            y=alt.Y("nilai:Q", title="Nilai (Sisir)"),
            tooltip=[
                alt.Tooltip("tanggal:T", title="Tanggal"),
                alt.Tooltip("nilai:Q", title="Nilai (sisir)"),
            ],
        )
        .properties(height=320)
        .interactive()
    )
    return c


def _chart_actual_vs_forecast(actual_df: pd.DataFrame, forecast_df: pd.DataFrame):
    """
    Gabungan aktual (nilai) vs prediksi (pred_sisir).
    """
    if actual_df.empty or forecast_df.empty:
        return None

    a = actual_df.copy()
    f = forecast_df.copy()

    a["tanggal"] = pd.to_datetime(a["tanggal"], errors="coerce")
    a["nilai"] = pd.to_numeric(a["nilai"], errors="coerce")
    a = a.dropna()

    f["tanggal"] = pd.to_datetime(f["tanggal"], errors="coerce")

    # Support output baru (pred_sisir). Kalau file lama punya 'prediksi', pakai itu.
    if "pred_sisir" in f.columns:
        f["pred_sisir"] = pd.to_numeric(f["pred_sisir"], errors="coerce")
        y_field = "pred_sisir"
        y_title = "Prediksi (sisir)"
        tip_title = "Prediksi (sisir)"
    elif "prediksi" in f.columns:
        f["prediksi"] = pd.to_numeric(f["prediksi"], errors="coerce")
        y_field = "prediksi"
        y_title = "Prediksi"
        tip_title = "Prediksi"
    else:
        return None

    f = f.dropna()

    c1 = (
        alt.Chart(a)
        .mark_line()
        .encode(
            x=alt.X("tanggal:T", title="Tanggal"),
            y=alt.Y("nilai:Q", title="Sisir"),
            tooltip=[
                alt.Tooltip("tanggal:T", title="Tanggal"),
                alt.Tooltip("nilai:Q", title="Aktual (sisir)"),
            ],
        )
    )

    c2 = (
        alt.Chart(f)
        .mark_line(strokeDash=[6, 4])
        .encode(
            x="tanggal:T",
            y=alt.Y(f"{y_field}:Q", title=y_title),
            tooltip=[
                alt.Tooltip("tanggal:T", title="Tanggal"),
                alt.Tooltip(f"{y_field}:Q", title=tip_title),
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

    st.markdown("### 📈 Grafik Aktual vs Prediksi (Sisir)")
    c_mix = _chart_actual_vs_forecast(df_actual, df_forecast)
    if c_mix is None:
        if df_forecast.empty:
            st.info("Prediksi belum tersedia. Admin perlu menjalankan SARIMA dulu.")
        else:
            st.info("Tidak bisa menampilkan grafik gabungan (cek format kolom prediksi).")
    else:
        st.altair_chart(c_mix, use_container_width=True)

    st.markdown("### 📄 Tabel Hasil Prediksi")
    if df_forecast.empty:
        st.info("Belum ada hasil prediksi.")
        return

    # Normalisasi tabel output:
    df_show = df_forecast.copy()
    if "tanggal" in df_show.columns:
        df_show["tanggal"] = pd.to_datetime(df_show["tanggal"], errors="coerce")
        df_show = df_show.dropna(subset=["tanggal"])

    # kalau output baru, tampilkan lengkap (kg & sisir + CI)
    cols_new = ["tanggal", "pred_kg", "low_kg", "up_kg", "pred_sisir", "low_sisir", "up_sisir"]
    if all(c in df_show.columns for c in cols_new):
        df_show = df_show[cols_new].copy()
        # biar rapi angka
        for c in ["pred_kg", "low_kg", "up_kg", "pred_sisir", "low_sisir", "up_sisir"]:
            df_show[c] = pd.to_numeric(df_show[c], errors="coerce").round(0).astype("Int64")

        df_show = df_show.rename(columns={
            "pred_kg": "Perkiraan (kg)",
            "low_kg": "Min (kg)",
            "up_kg": "Maks (kg)",
            "pred_sisir": "Perkiraan (sisir)",
            "low_sisir": "Min (sisir)",
            "up_sisir": "Maks (sisir)",
        })

    st.dataframe(df_show, use_container_width=True)

    # download: prefer CSV baru (paling cocok utk UMKM)
    if PRED_CSV.exists():
        st.download_button(
            "⬇️ Download prediksi_sarima.csv",
            data=PRED_CSV.read_bytes(),
            file_name="prediksi_sarima.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # tetap kasih download excel kalau ada
    if OUTPUT_XLSX.exists():
        st.download_button(
            "⬇️ Download hasil_prediksi.xlsx",
            data=OUTPUT_XLSX.read_bytes(),
            file_name="hasil_prediksi.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
