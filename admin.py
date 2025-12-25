# admin.py (FINAL - BUTTON TRUE, NO on_click/session_flag)
from pathlib import Path
import os
import pandas as pd
import streamlit as st
import altair as alt

from sarima_model import fit_sarima_and_forecast

DATA_PATH = Path("data") / "data_umkm.xlsx"
OUTPUT_PATH = Path("data") / "hasil_prediksi.xlsx"
PRED_CSV_PATH = Path("data") / "prediksi_sarima.csv"

FIX_STEPS = 12
FIX_ORDER = (0, 0, 0)
FIX_SEASONAL_ORDER = (0, 1, 0, 12)
KG_PER_SISIR = 0.5


def _load_data_from_repo() -> pd.DataFrame:
    if not DATA_PATH.exists():
        return pd.DataFrame(columns=["tanggal", "nilai"])
    try:
        return pd.read_excel(DATA_PATH)
    except Exception as e:
        st.error("❌ Gagal baca Excel (cek openpyxl / file corrupt).")
        st.exception(e)
        return pd.DataFrame(columns=["tanggal", "nilai"])


def _save_uploaded_file_to_repo(uploaded_file) -> None:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_PATH, "wb") as f:
        f.write(uploaded_file.getbuffer())


def _save_forecast(forecast_df: pd.DataFrame) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    forecast_df.to_excel(OUTPUT_PATH, index=False)
    forecast_df.to_csv(PRED_CSV_PATH, index=False)


def _chart_actual(df: pd.DataFrame):
    if df.empty:
        return None
    df2 = df.copy()
    df2["tanggal"] = pd.to_datetime(df2["tanggal"], errors="coerce")
    df2["nilai"] = pd.to_numeric(df2["nilai"], errors="coerce")
    df2 = df2.dropna()

    return (
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


def admin_page():
    st.markdown("## 🛠️ Dashboard Admin")
    tab1, tab2 = st.tabs(["📦 Data", "📈 Prediksi"])

    # ---------------- TAB DATA ----------------
    with tab1:
        st.markdown("### Data Historis (Excel)")
        st.write(f"File data aktif: `{DATA_PATH.as_posix()}`")

        uploaded = st.file_uploader("Upload data Excel (kolom: tanggal, nilai)", type=["xlsx"])
        if uploaded is not None:
            _save_uploaded_file_to_repo(uploaded)
            st.success("✅ Upload berhasil & disimpan.")
            st.rerun()

        df = _load_data_from_repo()
        st.metric("Jumlah baris", 0 if df.empty else len(df))
        st.dataframe(df, use_container_width=True)

        chart = _chart_actual(df)
        if chart is not None:
            st.altair_chart(chart, use_container_width=True)

        st.divider()
        st.markdown("#### DEBUG: isi folder `data/`")
        Path("data").mkdir(parents=True, exist_ok=True)
        st.code("\n".join(sorted(os.listdir("data"))) if os.path.exists("data") else "(folder data tidak ada)")

    # ---------------- TAB PREDIKSI ----------------
    with tab2:
        st.markdown("### Prediksi SARIMA")
        st.info(
            f"order={FIX_ORDER}, seasonal_order={FIX_SEASONAL_ORDER}, steps={FIX_STEPS}\n"
            f"Konversi: 1 sisir ≈ {KG_PER_SISIR} kg"
        )

        # dependency check
        try:
            import statsmodels  # noqa
            st.success("✅ statsmodels OK")
        except Exception as e:
            st.error("❌ statsmodels ERROR")
            st.exception(e)
            st.stop()

        try:
            import openpyxl  # noqa
            st.success("✅ openpyxl OK")
        except Exception as e:
            st.error("❌ openpyxl ERROR")
            st.exception(e)
            st.stop()

        df = _load_data_from_repo()
        if df.empty:
            st.warning("Data masih kosong. Upload dulu di tab Data.")
            st.stop()

        st.markdown("#### DEBUG: cek kolom & tipe data")
        st.write("Kolom:", list(df.columns))
        if "tanggal" not in df.columns or "nilai" not in df.columns:
            st.error("❌ Excel wajib punya kolom persis: 'tanggal' dan 'nilai'")
            st.stop()

        st.caption(
            f"Status file prediksi_sarima.csv: "
            f"{'ADA ✅' if PRED_CSV_PATH.exists() else 'BELUM ❌'}"
        )

        # =====================
        # 1) TEST KLIK (HARUS TRUE)
        # =====================
        st.markdown("### 🧪 Test Klik")
        test_clicked = st.button("🧪 TEST KLIK (harus muncul sukses)", key="test_click_btn")
        st.write("DEBUG test_clicked =", test_clicked)
        if test_clicked:
            st.success("✅ KLIK MASUK KE PYTHON (berarti tombol berfungsi)")

        st.divider()

        # =====================
        # 2) RUN SARIMA (PAKAI TRUE DARI st.button)
        # =====================
        run_clicked = st.button("🚀 Jalankan SARIMA", key="run_sarima_btn")
        st.write("DEBUG run_clicked =", run_clicked)

        if run_clicked:
            st.warning("🔔 Tombol kepencet. Mulai proses...")

            try:
                with st.spinner("Melatih model & membuat prediksi..."):
                    actual_df, forecast_df, summary_text = fit_sarima_and_forecast(
                        df=df,
                        date_col="tanggal",
                        value_col="nilai",
                        steps=int(FIX_STEPS),
                        order=FIX_ORDER,
                        seasonal_order=FIX_SEASONAL_ORDER,
                        kg_per_sisir=float(KG_PER_SISIR),
                    )
                    _save_forecast(forecast_df)

                st.success("✅ SARIMA selesai & file tersimpan!")
                st.dataframe(forecast_df, use_container_width=True)

                # download buttons (biar gampang)
                if PRED_CSV_PATH.exists():
                    st.download_button(
                        "⬇️ Download prediksi_sarima.csv",
                        data=PRED_CSV_PATH.read_bytes(),
                        file_name="prediksi_sarima.csv",
                        mime="text/csv",
                    )
                if OUTPUT_PATH.exists():
                    st.download_button(
                        "⬇️ Download hasil_prediksi.xlsx",
                        data=OUTPUT_PATH.read_bytes(),
                        file_name="hasil_prediksi.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )

                with st.expander("Summary model"):
                    st.text(summary_text)

            except Exception as e:
                st.error("❌ SARIMA gagal. Ini error aslinya:")
                st.exception(e)

            st.markdown("#### DEBUG: isi folder `data/` setelah run")
            st.code("\n".join(sorted(os.listdir("data"))) if os.path.exists("data") else "(folder data tidak ada)")
