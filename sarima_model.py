# sarima_model.py
import warnings
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Patokan skripsi: 1 kg ≈ 2 sisir => 1 sisir ≈ 0.5 kg
DEFAULT_KG_PER_SISIR = 0.5

# Param fix dari colab kamu
DEFAULT_ORDER = (0, 0, 0)
DEFAULT_SEASONAL_ORDER = (0, 1, 0, 12)

def fit_sarima_and_forecast(
    df: pd.DataFrame,
    date_col: str = "tanggal",
    value_col: str = "nilai",
    steps: int = 12,
    order=DEFAULT_ORDER,
    seasonal_order=DEFAULT_SEASONAL_ORDER,
    kg_per_sisir: float = DEFAULT_KG_PER_SISIR,
):
    """
    Input df harus punya kolom tanggal & nilai (nilai = sisir/bulan).
    Output:
      - df_ts: data historis (tanggal, nilai) bulanan (MS)
      - forecast_df: prediksi ke depan (tanggal, pred_sisir, low_sisir, up_sisir, pred_kg, low_kg, up_kg)
      - model_summary: ringkasan model (string)
    """
    if date_col not in df.columns or value_col not in df.columns:
        raise ValueError(f"Kolom harus ada: '{date_col}' dan '{value_col}'")

    df2 = df[[date_col, value_col]].copy()
    df2[date_col] = pd.to_datetime(df2[date_col], errors="coerce")
    df2 = df2.dropna(subset=[date_col, value_col])

    df2[value_col] = pd.to_numeric(df2[value_col], errors="coerce")
    df2 = df2.dropna(subset=[value_col])

    df2 = df2.sort_values(date_col).set_index(date_col)
    df2 = df2.asfreq("MS")  # Month Start

    if df2[value_col].isna().any():
        df2[value_col] = df2[value_col].interpolate(method="time")

    y = df2[value_col]

    warnings.filterwarnings("ignore")

    model = SARIMAX(
        y,
        order=order,
        seasonal_order=seasonal_order,
        enforce_stationarity=False,
        enforce_invertibility=False,
    )
    res = model.fit(disp=False)

    fc = res.get_forecast(steps=steps)
    mean = fc.predicted_mean
    ci = fc.conf_int()

    # index forecast mengikuti mean index (paling aman)
    idx_forecast = mean.index

    forecast_df = pd.DataFrame({
        "tanggal": idx_forecast,
        "pred_sisir": mean.values,
        "low_sisir": ci.iloc[:, 0].values,
        "up_sisir":  ci.iloc[:, 1].values,
    })

    forecast_df["pred_kg"] = forecast_df["pred_sisir"] * kg_per_sisir
    forecast_df["low_kg"]  = forecast_df["low_sisir"]  * kg_per_sisir
    forecast_df["up_kg"]   = forecast_df["up_sisir"]   * kg_per_sisir

    df_ts = df2.reset_index().rename(columns={value_col: "nilai"})

    return df_ts, forecast_df, str(res.summary())
