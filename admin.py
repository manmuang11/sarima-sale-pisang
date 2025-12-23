# admin.py
from pathlib import Path
import pandas as pd
import streamlit as st
import altair as alt

from sarima_model import fit_sarima_and_forecast

DATA_PATH = Path("data") / "data_umkm.xlsx"

# tetap simpan excel (buat download)
OUTPUT_PATH = Path("data") / "hasil_prediksi.xlsx"
# tambah csv (buat dibaca UMKM, lebih ringan)
PRED_CSV_PATH = Path("data") / "prediksi_sarima.csv"

# PARAM FIX dari Colab (dikunci)
FIX_STEPS = 12
FIX_ORDER = (0, 0, 0)
FIX_SEASONAL_ORDER = (0, 1, 0, 12)

# Patokan skripsi: 1 kg ≈ 2 sisir => 1 sisir ≈ 0.5 kg
KG_PER_SISIR = 0.5


def _load_data_from_repo() -> pd.DataFrame:
    if not DATA_PATH.exists():
        return pd.DataFrame(columns=["tanggal", "nilai"])
    return pd.read_excel(DATA_PATH)


def _save_uploaded_file_to_repo(uploaded_file) -> None:
    # simpan upload jadi data/data_umkm.xlsx
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_PATH, "wb") as f:
        f.write(uploaded_file.getbuffer())


def _save_forecast(forecast_df: pd.DataFrame) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    # simpan excel untuk download
    forecast_df.to_excel(OUTPUT_PATH, index=False)
    # simpan csv untuk dibaca UMKM
    forecast_df.to_csv(PRED_CSV_PATH, index=False)


def _chart_actual(df: pd.DataFrame):
    if df.empty:
        return None
    df2 = df.copy()
    df2["tanggal"] = pd.to_datetime(df2["tanggal"])
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
                alt.Tooltip("nilai:Q", title="Nilai"),
            ],
        )
        .properties(height=320)
        .interactive()
    )
    return c


def _chart_forecast(actual_df: pd.DataFrame, forecast_df: pd.DataFrame):
    """
    Chart aktual vs prediksi sisir.
    forecast_df (baru) pakai kolom: pred_sisir
    """
    if actual_df.empty or forecast_df.empty:
        return None

    a = actual_df.copy()
    f = forecast_df.copy()

    a["tanggal"] = pd.to_datetime(a["tanggal"])
    a["nilai"] = pd.to_numeric(a["nilai"], errors="coerce")
    a = a.dropna()

    f["tanggal"] = pd.to_datetime(f["tanggal"])
    # output baru: pred_sisir
    if "pred_sisir" not in f.columns:
        return None
    f["pred_sisir"] = pd.to_numeric(f["pred_sisir"], errors="coerce")
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
            y=alt.Y("pred_sisir:Q", title="Sisir / Prediksi"),
            tooltip=[
                alt.Tooltip("tanggal:T", title="Tanggal"),
                alt.Tooltip("pred_sisir:Q", title="Prediksi (sisir)"),
            ],
        )
    )

    return (c1 + c2).properties(height=340).interactive()


def admin_page():
    st.markdown("## 🛠️ Dashboard Admin")
    st.caption("Kelola data & jalankan prediksi SARIMA (fix dari Colab)")

    tab1, tab2 = st.tabs(["📦 Data", "📈 Prediksi"])

    with tab1:
        st.markdown("### Data Historis (Excel)")
        st.write(f"File data aktif: `{DATA_PATH.as_posix()}`")

        colA, colB = st.columns([1.2, 1])
        with colA:
            uploaded = st.file_uploader(
                "Upload data Excel (kolom wajib: tanggal, nilai)",
                type=["xlsx"],
            )
            if uploaded is not None:
                _save_uploaded_file_to_repo(uploaded)
                st.success("Upload berhasil. Data disimpan sebagai data/data_umkm.xlsx")
                st.rerun()

        with colB:
            df = _load_data_from_repo()
            st.metric("Jumlah baris", 0 if df.empty else len(df))

        df = _load_data_from_repo()
        st.dataframe(df, use_container_width=True)

        chart = _chart_actual(df)
        if chart is not None:
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("Data belum ada atau format belum sesuai.")

        st.markdown("**Format kolom wajib**: `tanggal` (date) dan `nilai` (angka).")

    with tab2:
        st.markdown("### Prediksi SARIMA (jalan saat Admin klik)")
        df = _load_data_from_repo()
        if df.empty:
            st.warning("Data masih kosong. Upload dulu di tab Data.")
            st.stop()

        # INFO: param sudah dikunci
        st.info(
            f"Model dikunci sesuai Colab:\n"
            f"- order={FIX_ORDER}\n"
            f"- seasonal_order={FIX_SEASONAL_ORDER}\n"
            f"- prediksi {FIX_STEPS} bulan\n"
            f"Konversi skripsi: 1 sisir ≈ {KG_PER_SISIR} kg (1 kg ≈ 2 sisir)"
        )

        run = st.button("🚀 Jalankan SARIMA", use_container_width=True)

        if run:
            try:
                with st.spinner("Melatih model & membuat prediksi..."):
                    actual_df, forecast_df, summary_text = fit_sarima_and_forecast(
                        df=df,
                        steps=int(FIX_STEPS),
                        order=FIX_ORDER,
                        seasonal_order=FIX_SEASONAL_ORDER,
                        kg_per_sisir=float(KG_PER_SISIR),
                    )

                    _save_forecast(forecast_df)

                st.success("Prediksi berhasil dibuat & disimpan.")
                st.write(f"Hasil Excel: `{OUTPUT_PATH.as_posix()}`")
                st.write(f"Hasil CSV (dibaca UMKM): `{PRED_CSV_PATH.as_posix()}`")

                st.markdown("#### Grafik Aktual vs Prediksi (Sisir)")
                chart2 = _chart_forecast(actual_df, forecast_df)
                if chart2 is not None:
                    st.altair_chart(chart2, use_container_width=True)
                else:
                    st.info("Chart prediksi belum bisa tampil (cek kolom output forecast).")

                st.markdown("#### Tabel Prediksi (kg & sisir + min/maks)")
                st.dataframe(forecast_df, use_container_width=True)

                st.download_button(
                    "⬇️ Download hasil_prediksi.xlsx",
                    data=OUTPUT_PATH.read_bytes() if OUTPUT_PATH.exists() else b"",
                    file_name="hasil_prediksi.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

                with st.expander("📄 Ringkasan Model (summary)"):
                    st.text(summary_text)

            except Exception as e:
                st.error("❌ Gagal menjalankan SARIMA.")
                st.exception(e)

        else:
            # kalau belum klik, tapi hasil prediksi sudah ada dari sebelumnya
            if OUTPUT_PATH.exists():
                st.info("Ada hasil prediksi sebelumnya. UMKM bisa lihat dari file prediksi_sarima.csv / hasil_prediksi.xlsx.")
                try:
                    prev = pd.read_excel(OUTPUT_PATH)
                    st.dataframe(prev, use_container_width=True)
                except Exception:
                    st.warning("File hasil_prediksi.xlsx tidak bisa dibaca. Coba jalankan ulang prediksi.")
