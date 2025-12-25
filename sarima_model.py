import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

def fit_sarima_and_forecast(
    df: pd.DataFrame,
    date_col: str = "tanggal",
    value_col: str = "nilai",
    steps: int = 12,
    order=(0, 0, 0),
    seasonal_order=(0, 1, 0, 12),
    kg_per_sisir: float = 0.5,
    freq: str = "MS",
):
    df = df.copy()

    if date_col not in df.columns or value_col not in df.columns:
        raise ValueError(f"Kolom wajib ada: '{date_col}' dan '{value_col}'")

    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")
    df = df.dropna(subset=[date_col, value_col]).sort_values(date_col)

    if len(df) < 24:
        raise ValueError(f"Data terlalu sedikit untuk seasonal 12. Minimal ~24 baris, sekarang {len(df)}.")

    # normalisasi tanggal ke awal bulan supaya asfreq MS gak bikin bolong parah
    df[date_col] = df[date_col].dt.to_period("M").dt.to_timestamp("MS")

    ts = df.set_index(date_col)[value_col].asfreq(freq)
    ts = ts.interpolate(limit_direction="both")

    model = SARIMAX(
        ts,
        order=order,
        seasonal_order=seasonal_order,
        enforce_stationarity=False,
        enforce_invertibility=False,
    )

    # penting: batasi iterasi + pakai method yang "selesai"
    res = model.fit(disp=False, maxiter=80, method="powell")

    fc = res.get_forecast(steps=steps)
    pred = fc.predicted_mean

    forecast_df = pred.reset_index()
    forecast_df.columns = [date_col, "prediksi_sisir"]
    forecast_df["prediksi_kg"] = forecast_df["prediksi_sisir"] * float(kg_per_sisir)

    actual_df = ts.reset_index()
    actual_df.columns = [date_col, "aktual_sisir"]
    actual_df["aktual_kg"] = actual_df["aktual_sisir"] * float(kg_per_sisir)

    summary_text = str(res.summary())

    return actual_df, forecast_df, summary_text
