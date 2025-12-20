# sarima_model.py
import warnings
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

def fit_sarima_and_forecast(
    df: pd.DataFrame,
    date_col: str = "tanggal",
    value_col: str = "nilai",
    seasonal_periods: int = 12,
    steps: int = 6,
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 12),
):
    """
    Input df harus punya kolom tanggal & nilai.
    Output:
      - df_ts: data historis dengan index datetime (MS)
      - forecast_df: prediksi ke depan (tanggal, prediksi)
      - model_summary: ringkasan model (string)
    """
    if date_col not in df.columns or value_col not in df.columns:
        raise ValueError(f"Kolom harus ada: '{date_col}' dan '{value_col}'")

    df2 = df[[date_col, value_col]].copy()
    df2[date_col] = pd.to_datetime(df2[date_col], errors="coerce")
    df2 = df2.dropna(subset=[date_col, value_col])

    # pastikan numeric
    df2[value_col] = pd.to_numeric(df2[value_col], errors="coerce")
    df2 = df2.dropna(subset=[value_col])

    # index time series (awal bulan)
    df2 = df2.sort_values(date_col)
    df2 = df2.set_index(date_col)

    # set frekuensi bulanan (MS = Month Start)
    df2 = df2.asfreq("MS")

    # kalau ada missing value di tengah, isi interpolasi
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

    pred = res.get_forecast(steps=steps)
    pred_mean = pred.predicted_mean

    # bikin tanggal prediksi (lanjut dari bulan terakhir)
    start_next = (df2.index.max() + pd.offsets.MonthBegin(1)).normalize()
    idx_forecast = pd.date_range(start=start_next, periods=steps, freq="MS")

    forecast_df = pd.DataFrame(
        {
            "tanggal": idx_forecast,
            "prediksi": pred_mean.values,
        }
    )

    return df2.reset_index().rename(columns={value_col: "nilai"}), forecast_df, str(res.summary())
