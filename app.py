import math
import re
import base64
from pathlib import Path
from io import BytesIO

import pandas as pd
import streamlit as st
import altair as alt
import streamlit as st
import traceback

st.set_page_config(page_title="Prediksi Kebutuhan Pisang", page_icon="🍌", layout="wide")

try:
    st.success("✅ BOOT OK - mulai jalanin kode utama...")
    # ====== KODE APP LU YANG LAMA LANJUT DI BAWAH INI ======

except Exception:
    st.error("❌ App crash saat start. Ini errornya:")
    st.code(traceback.format_exc())
    st.stop()


# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="Prediksi Kebutuhan Pisang",
    page_icon="🍌",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).parent
ASSET_DIR = BASE_DIR / "assets"
LOGO_PATH = ASSET_DIR / "logo.png"
THEME_CSS_PATH = BASE_DIR / "theme.css"

DEFAULT_HIST_FILE = "data_umkm.xlsx"
DEFAULT_PRED_FILE = "prediksi_default.xlsx"  # backup hasil prediksi (opsional)

# =========================================================
# LOAD CSS (theme.css)
# =========================================================
def load_css():
    if THEME_CSS_PATH.exists():
        st.markdown(f"<style>{THEME_CSS_PATH.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
    else:
        # fallback minimal (kalau theme.css belum ada)
        st.markdown(
            """
            <style>
            .login-wrap{min-height:calc(100vh - 2rem);display:flex;align-items:center;justify-content:center;padding:24px 12px;}
            .login-card{width:420px;max-width:92vw;background:#fff;border-radius:24px;padding:28px 22px;box-shadow:0 18px 40px rgba(15,23,42,.08);position:relative;display:flex;flex-direction:column;align-items:center;}
            .login-badge{width:72px;height:72px;border-radius:999px;background:#fff4c4;display:flex;align-items:center;justify-content:center;position:absolute;top:-36px;left:50%;transform:translateX(-50%);}
            .login-badge img{width:40px;height:40px;object-fit:contain;}
            .login-title{margin-top:12px;font-size:1.8rem;font-weight:800;}
            .login-sub{margin-top:6px;color:#6b7280;text-align:center;}
            .hide-sidebar section[data-testid="stSidebar"]{display:none;}
            footer{visibility:hidden;}
            </style>
            """,
            unsafe_allow_html=True,
        )

load_css()

# =========================================================
# LOGO -> html img base64
# =========================================================
def img_to_base64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")

logo_html = ""
if LOGO_PATH.exists():
    logo_html = f"<img src='data:image/png;base64,{img_to_base64(LOGO_PATH)}'/>"

def render_logo_fallback():
    return logo_html if logo_html else "🍌"

# =========================================================
# USERS (st.secrets) + fallback
# =========================================================
def get_users_from_secrets():
    """
    Secrets format (Streamlit Cloud):
    [users.admin]
    password="admin123"
    role="admin"

    [users.umkm]
    password="umkm123"
    role="umkm"
    """
    try:
        return dict(st.secrets["users"])
    except Exception:
        return {
            "admin": {"password": "admin123", "role": "admin"},
            "umkm": {"password": "umkm123", "role": "umkm"},
        }

USERS = get_users_from_secrets()

# =========================================================
# SESSION STATE
# =========================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None
if "username" not in st.session_state:
    st.session_state.username = None
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# hasil prediksi terbaru (dari proses admin)
if "data_override" not in st.session_state:
    st.session_state.data_override = None

# =========================================================
# LOGIN UI
# =========================================================
def render_login_page():
    st.markdown("<div class='hide-sidebar'></div>", unsafe_allow_html=True)

    st.markdown("<div class='login-wrap'>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="login-card">
          <div class="login-badge">{render_logo_fallback()}</div>
          <div class="login-title">Login</div>
          <div class="login-sub">Masuk untuk mengakses dashboard.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.form("form_login"):
        username = st.text_input("Username", placeholder="Masukkan username")
        password = st.text_input("Password", type="password", placeholder="Masukkan password")
        submit = st.form_submit_button("MASUK", use_container_width=True)

    st.markdown(
        "<div style='text-align:center; margin-top:10px; color:#6b7280; font-size:0.92rem;'>"
        "UMKM hanya melihat hasil. Admin mengelola data dan prediksi."
        "</div>",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)
    return submit, username, password

if not st.session_state.logged_in:
    submit, username, password = render_login_page()
    if submit:
        u = (username or "").strip().lower()
        p = (password or "").strip()
        if u in USERS and USERS[u].get("password") == p:
            st.session_state.logged_in = True
            st.session_state.role = USERS[u].get("role", "umkm")
            st.session_state.username = u
            st.rerun()
        else:
            st.error("Username atau password salah.")
    st.stop()

ROLE = st.session_state.role
IS_ADMIN = ROLE == "admin"
IS_UMKM = ROLE == "umkm"

# =========================================================
# MONTH HELPERS (ID)
# =========================================================
ID_MONTHS = {
    "januari": 1, "jan": 1, "jan.": 1,
    "februari": 2, "feb": 2,
    "maret": 3, "mar": 3,
    "april": 4, "apr": 4,
    "mei": 5,
    "juni": 6, "jun": 6,
    "juli": 7, "jul": 7,
    "agustus": 8, "agu": 8, "aug": 8,
    "september": 9, "sep": 9,
    "oktober": 10, "okt": 10,
    "november": 11, "nov": 11,
    "desember": 12, "des": 12, "dec": 12,
}
ID_MONTH_NAMES = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
    5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
    9: "September", 10: "Oktober", 11: "November", 12: "Desember",
}
def month_name_id(m: int) -> str:
    return ID_MONTH_NAMES.get(int(m), str(m))

def fmt_int(v: float) -> str:
    try:
        return f"{float(v):,.0f}"
    except Exception:
        return "—"

# =========================================================
# UNIT (Kg <-> Sisir)
# =========================================================
SISIR_PER_KG = 450 / 250  # 1.8

def unit_suffix(unit_choice: str) -> str:
    return "sisir" if unit_choice == "Sisir" else "kg"

def convert_value_kg_to_unit(v_kg: float, unit_choice: str) -> float:
    if v_kg is None or (isinstance(v_kg, float) and not math.isfinite(v_kg)):
        return math.nan
    return float(v_kg) * SISIR_PER_KG if unit_choice == "Sisir" else float(v_kg)

def fmt_dual_units(v_kg: float) -> tuple[str, str]:
    v_sisir = convert_value_kg_to_unit(v_kg, "Sisir")
    return f"{fmt_int(v_kg)} kg", f"{fmt_int(v_sisir)} sisir"

# =========================================================
# UI HELPERS (simple)
# =========================================================
def card(title: str, value: str, sub: str = ""):
    st.markdown(
        f"""
        <div style="background:#fff;border-radius:22px;padding:18px 18px;box-shadow:0 14px 30px rgba(15,23,42,0.08);border:1px solid rgba(0,0,0,0.03);">
          <div style="color:#6b7280;font-size:.95rem;margin-bottom:6px;">{title}</div>
          <div style="font-size:2rem;font-weight:900;line-height:1.1;">{value}</div>
          <div style="color:#6b7280;font-size:.92rem;margin-top:6px;">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def empty_state(title="Data belum tersedia", desc="Minta Admin memperbarui data/prediksi."):
    st.markdown(
        f"""
        <div style="background:#fff;border-radius:22px;padding:18px 18px;box-shadow:0 14px 30px rgba(15,23,42,0.08);border:1px solid rgba(0,0,0,0.03);">
          <div style="color:#6b7280;font-size:.95rem;margin-bottom:6px;">{title}</div>
          <div style="color:#6b7280;font-size:.95rem;">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def to_excel_bytes(df: pd.DataFrame, sheet_name="Data"):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    return output.getvalue()

# =========================================================
# HISTORICAL EXCEL PARSER (robust)
# =========================================================
def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [re.sub(r"\s+", "_", str(c).strip()).lower() for c in df.columns]
    return df

def detect_date_column(df: pd.DataFrame):
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            if df[col].notna().sum() >= max(3, int(len(df) * 0.5)):
                return col, df[col]

    date_keywords = ["tanggal", "tgl", "date", "waktu", "period", "periode", "bulan_tahun", "bulan-tahun", "bulan_thn"]
    for col in df.columns:
        if any(k in col for k in date_keywords):
            parsed = pd.to_datetime(df[col], errors="coerce", dayfirst=True)
            if parsed.notna().sum() >= max(3, int(len(df) * 0.5)):
                return col, parsed
    return None, None

def detect_year_month(df: pd.DataFrame):
    year_col, month_col = None, None
    for col in df.columns:
        if any(k in col for k in ["tahun", "year", "thn", "th"]):
            year_col = col
        if any(k in col for k in ["bulan", "month", "bln", "mon"]):
            month_col = col
    return year_col, month_col

def parse_year_month_to_date(df: pd.DataFrame, year_col: str, month_col: str) -> pd.Series:
    y = pd.to_numeric(df[year_col], errors="coerce")
    if (y < 100).sum() > 0 and (y < 100).sum() >= len(y) * 0.5:
        y = y.apply(lambda v: 2000 + v if pd.notna(v) else v)

    months_raw = df[month_col]
    m = pd.to_numeric(months_raw, errors="coerce")

    mask = m.isna() & months_raw.notna()
    if mask.any():
        def map_month(x):
            if pd.isna(x):
                return math.nan
            s = str(x).strip().lower()
            s2 = re.sub(r"[^\w]+$", "", s)
            return ID_MONTHS.get(s2, math.nan)
        m[mask] = months_raw[mask].map(map_month)

    return pd.to_datetime({"year": y, "month": m, "day": 1}, errors="coerce")

def parse_historical_excel(file_path_or_buffer):
    df_raw = pd.read_excel(file_path_or_buffer, engine="openpyxl")
    df = normalize_columns(df_raw)

    _, date_series = detect_date_column(df)
    if date_series is None:
        year_col, month_col = detect_year_month(df)
        if year_col and month_col:
            date_series = parse_year_month_to_date(df, year_col, month_col)
        else:
            raise ValueError("Tidak bisa mengenali kolom tanggal / (bulan + tahun).")

    df["tanggal"] = pd.to_datetime(date_series, errors="coerce")
    df = df[df["tanggal"].notna()].copy()

    # cari kolom nilai (numeric)
    numeric_cols = [c for c in df.columns if c != "tanggal" and pd.api.types.is_numeric_dtype(df[c])]

    # kalau belum numeric, coba paksa
    if not numeric_cols:
        for c in df.columns:
            if c == "tanggal":
                continue
            df[c] = pd.to_numeric(df[c], errors="coerce")
        numeric_cols = [c for c in df.columns if c != "tanggal" and pd.api.types.is_numeric_dtype(df[c])]

    if not numeric_cols:
        raise ValueError("Tidak menemukan kolom angka (nilai kebutuhan/aktual).")

    prefer = ["nilai", "aktual", "realisasi", "kebutuhan", "pemakaian", "jumlah", "qty", "volume"]
    chosen = None
    for key in prefer:
        for c in numeric_cols:
            if key in c:
                chosen = c
                break
        if chosen:
            break
    if chosen is None:
        chosen = numeric_cols[0]

    out = df[["tanggal", chosen]].rename(columns={chosen: "nilai"}).copy()
    out["nilai"] = pd.to_numeric(out["nilai"], errors="coerce")
    out = out[out["nilai"].notna()].copy()

    # agregasi bulanan (MS)
    out["tanggal"] = out["tanggal"].dt.to_period("M").dt.to_timestamp()
    out = out.groupby("tanggal", as_index=False)["nilai"].sum().sort_values("tanggal")
    return out

# =========================================================
# LOAD DEFAULT PRED FILE (backup untuk UMKM)
# =========================================================
@st.cache_data(show_spinner=False)
def load_default_pred_file():
    p = BASE_DIR / DEFAULT_PRED_FILE
    if not p.exists():
        return pd.DataFrame(columns=["tanggal", "jenis", "nilai", "min", "max"])

    df = pd.read_excel(p, engine="openpyxl")
    df.columns = [str(c).strip().lower() for c in df.columns]

    # harus ada header ini
    if "tanggal" not in df.columns or "nilai" not in df.columns:
        # jangan bikin crash; anggap gak ada prediksi
        return pd.DataFrame(columns=["tanggal", "jenis", "nilai", "min", "max"])

    df["tanggal"] = pd.to_datetime(df["tanggal"], errors="coerce")
    df = df[df["tanggal"].notna()].copy()

    df["nilai"] = pd.to_numeric(df["nilai"], errors="coerce")
    df = df[df["nilai"].notna()].copy()

    if "min" not in df.columns:
        df["min"] = math.nan
    else:
        df["min"] = pd.to_numeric(df["min"], errors="coerce")

    if "max" not in df.columns:
        df["max"] = math.nan
    else:
        df["max"] = pd.to_numeric(df["max"], errors="coerce")

    df["jenis"] = "Perkiraan"
    df = df[["tanggal", "jenis", "nilai", "min", "max"]].sort_values("tanggal").reset_index(drop=True)
    return df

# =========================================================
# SARIMA (jalan hanya saat Admin klik)
# =========================================================
def build_monthly_series(df_hist: pd.DataFrame) -> pd.Series:
    s = df_hist.set_index("tanggal")["nilai"].sort_index()
    s = s.asfreq("MS")
    if s.isna().any():
        s = s.interpolate(limit_direction="both")
    return s

def run_sarima_forecast(
    series: pd.Series,
    steps: int,
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 12),
    maxiter: int = 80,
):
    from statsmodels.tsa.statespace.sarimax import SARIMAX

    model = SARIMAX(
        series,
        order=order,
        seasonal_order=seasonal_order,
        enforce_stationarity=False,
        enforce_invertibility=False,
    )
    res = model.fit(disp=False, maxiter=maxiter)

    fc = res.get_forecast(steps=steps)
    mean = fc.predicted_mean
    ci = fc.conf_int(alpha=0.05)

    df_pred = pd.DataFrame({
        "tanggal": pd.to_datetime(mean.index),
        "jenis": "Perkiraan",
        "nilai": mean.values.astype(float),
        "min": ci.iloc[:, 0].values.astype(float),
        "max": ci.iloc[:, 1].values.astype(float),
    })
    return df_pred

def build_tidy_from_hist_and_pred(df_hist: pd.DataFrame, df_pred: pd.DataFrame):
    df_act = df_hist.copy()
    df_act["jenis"] = "Aktual"
    df_act["min"] = math.nan
    df_act["max"] = math.nan
    df_act = df_act[["tanggal", "jenis", "nilai", "min", "max"]].copy()

    tidy = pd.concat([df_act, df_pred], ignore_index=True)
    tidy["tanggal"] = pd.to_datetime(tidy["tanggal"])
    tidy = tidy.sort_values(["tanggal", "jenis"]).reset_index(drop=True)

    df_actual = tidy[tidy["jenis"] == "Aktual"].copy()
    df_pred_only = tidy[tidy["jenis"] == "Perkiraan"].copy()
    return tidy, df_actual, df_pred_only

# =========================================================
# CHARTS
# =========================================================
def make_line_month_chart(df_pred_year: pd.DataFrame, unit_choice: str):
    if df_pred_year is None or df_pred_year.empty:
        return None

    u = unit_suffix(unit_choice)

    d = df_pred_year.copy()
    d["bulan"] = d["tanggal"].dt.to_period("M").dt.to_timestamp()
    agg = d.groupby("bulan", as_index=False)["nilai"].mean().sort_values("bulan")
    agg["nilai_u"] = agg["nilai"].apply(lambda x: convert_value_kg_to_unit(x, unit_choice))

    base = alt.Chart(agg).encode(
        x=alt.X("bulan:T", title="", axis=alt.Axis(format="%b %Y"))
    )

    line = base.mark_line(strokeWidth=3).encode(
        y=alt.Y("nilai_u:Q", title=u),
        color=alt.value("#FFD65A"),
        tooltip=[
            alt.Tooltip("bulan:T", title="Bulan", format="%B %Y"),
            alt.Tooltip("nilai_u:Q", title=f"Perkiraan ({u})", format=",.0f"),
        ],
    )

    nearest = alt.selection_point(on="mouseover", fields=["bulan"], nearest=True, empty=False)
    points = base.mark_point(size=80, opacity=0).add_params(nearest)
    highlight = base.mark_point(size=90).encode(y="nilai_u:Q", color=alt.value("#FFD65A")).transform_filter(nearest)
    rule = base.mark_rule(color="#cdbf9b").encode(x="bulan:T").transform_filter(nearest)
    text = base.mark_text(align="left", dx=10, dy=-10).encode(
        y="nilai_u:Q",
        text=alt.Text("nilai_u:Q", format=",.0f"),
        color=alt.value("#222222"),
    ).transform_filter(nearest)

    return (
        alt.layer(line, points, highlight, rule, text)
        .properties(height=420)
        .configure_view(stroke=None)
        .configure_axis(
            gridColor="#efe6d7",
            tickColor="#efe6d7",
            domainColor="#efe6d7",
            labelColor="#6b7280",
            titleColor="#6b7280",
        )
    )

def make_bar_month_chart(df_pred_year: pd.DataFrame, unit_choice: str):
    if df_pred_year is None or df_pred_year.empty:
        return None

    u = unit_suffix(unit_choice)

    d = df_pred_year.copy()
    d["bulan"] = d["tanggal"].dt.month
    d["bulan_nama"] = d["bulan"].apply(month_name_id)
    agg = d.groupby(["bulan", "bulan_nama"], as_index=False)["nilai"].mean().sort_values("bulan")
    agg["nilai_u"] = agg["nilai"].apply(lambda x: convert_value_kg_to_unit(x, unit_choice))

    return (
        alt.Chart(agg)
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
        .encode(
            x=alt.X("bulan_nama:N", title="", sort=list(ID_MONTH_NAMES.values())),
            y=alt.Y("nilai_u:Q", title=u),
            tooltip=[
                alt.Tooltip("bulan_nama:N", title="Bulan"),
                alt.Tooltip("nilai_u:Q", title=f"Perkiraan ({u})", format=",.0f"),
            ],
            color=alt.value("#FFD65A"),
        )
        .properties(height=360)
        .configure_view(stroke=None)
        .configure_axis(
            gridColor="#efe6d7",
            tickColor="#efe6d7",
            domainColor="#efe6d7",
            labelColor="#6b7280",
            titleColor="#6b7280",
        )
    )

def month_table(df_pred: pd.DataFrame, year: int):
    d = df_pred[df_pred["tanggal"].dt.year == year].copy()
    if d.empty:
        return d

    d["Bulan"] = d["tanggal"].dt.month.apply(month_name_id)
    out = d.groupby(["Bulan"], as_index=False).agg(
        Perkiraan_kg=("nilai", "mean"),
        Min_kg=("min", "mean"),
        Maks_kg=("max", "mean"),
    )
    if "Min_kg" in out.columns and out["Min_kg"].isna().all():
        out = out.drop(columns=["Min_kg"])
    if "Maks_kg" in out.columns and out["Maks_kg"].isna().all():
        out = out.drop(columns=["Maks_kg"])
    return out

# =========================================================
# LOAD HIST (ringan) + load pred default
# =========================================================
@st.cache_data(show_spinner=True)
def load_hist_only():
    p = BASE_DIR / DEFAULT_HIST_FILE
    if not p.exists():
        # jangan crash parah; kasih df kosong
        return pd.DataFrame(columns=["tanggal", "nilai"])
    return parse_historical_excel(p)

df_hist_default = load_hist_only()

# prioritas data:
# 1) hasil proses admin (override)
# 2) prediksi_default.xlsx (backup)
df_pred_all = pd.DataFrame(columns=["tanggal", "jenis", "nilai", "min", "max"])
df_actual_all = pd.DataFrame(columns=["tanggal", "jenis", "nilai", "min", "max"])
tidy_all = pd.DataFrame(columns=["tanggal", "jenis", "nilai", "min", "max"])

# build aktual (kalau historis ada)
if not df_hist_default.empty:
    df_actual_all = df_hist_default.copy()
    df_actual_all["jenis"] = "Aktual"
    df_actual_all["min"] = math.nan
    df_actual_all["max"] = math.nan
    df_actual_all = df_actual_all[["tanggal", "jenis", "nilai", "min", "max"]].copy()

# load pred default
df_pred_default = load_default_pred_file()

# set data awal (default)
df_pred_all = df_pred_default.copy() if not df_pred_default.empty else df_pred_all
tidy_all = pd.concat([df_actual_all, df_pred_all], ignore_index=True)

# override kalau admin sudah proses
if st.session_state.data_override is not None:
    tidy_all, df_actual_all, df_pred_all = st.session_state.data_override

# =========================================================
# SIDEBAR (ROLE LOCK)
# =========================================================
with st.sidebar:
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
          <div class="logo-circle big">{render_logo_fallback()}</div>
          <div>
            <div style="font-weight:800;color:#222;line-height:1.1;">Sale Pisang</div>
            <div style="font-weight:800;color:#222;line-height:1.1;">Bungo Family</div>
            <div class="small-muted" style="margin-top:2px;">Dashboard</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"<div class='small-muted'>Login sebagai: <b>{'Admin' if IS_ADMIN else 'UMKM'}</b></div>",
        unsafe_allow_html=True
    )
    st.markdown("<hr/>", unsafe_allow_html=True)

    def go(p):
        st.session_state.page = p
        st.rerun()

    if st.button("🏠 Beranda", use_container_width=True):
        go("Dashboard")
    if st.button("📊 Rincian Bulanan", use_container_width=True):
        go("Detail")

    if IS_ADMIN:
        st.markdown("<hr/>", unsafe_allow_html=True)
        if st.button("⬆️ Admin: Upload & Proses SARIMA", use_container_width=True):
            go("Upload")

    st.markdown("<hr/>", unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.username = None
        st.session_state.page = "Dashboard"
        st.session_state.data_override = None
        st.rerun()

page = st.session_state.page
if IS_UMKM and page == "Upload":
    st.session_state.page = "Dashboard"
    st.rerun()

# =========================================================
# HEADER
# =========================================================
st.markdown(
    f"""
    <div class="header-banana">
      <div class="header-left">
        <div class="logo-circle big">{render_logo_fallback()}</div>
        <div class="title-block">
          <h1>Berapa Pisang yang Perlu Disiapkan?</h1>
          <p>Prediksi kebutuhan pisang per bulan (SARIMA)</p>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True
)
st.write("")
st.markdown(
    """
    <div class="hint-banner">
      Pilih <b>tahun</b>, <b>bulan</b>, dan <b>satuan</b>, lalu klik <b>Tampilkan</b>.
      (Arahkan mouse ke garis kuning untuk melihat angka tiap bulan)
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# GUARD: kalau belum ada prediksi sama sekali
# =========================================================
if df_pred_all.empty:
    if IS_ADMIN:
        st.warning(
            "Belum ada hasil prediksi. "
            "Admin: buka menu 'Upload & Proses SARIMA' lalu klik Proses. "
            "Opsional: isi prediksi_default.xlsx biar UMKM langsung lihat."
        )
    else:
        st.warning("Belum ada hasil prediksi. Silakan minta Admin memproses prediksi terlebih dahulu.")
    st.stop()

# =========================================================
# FILTER
# =========================================================
years_available = sorted(df_pred_all["tanggal"].dt.year.unique()) if not df_pred_all.empty else []
if not years_available:
    st.warning("Prediksi ada, tapi format tanggal tidak terbaca. Cek kolom 'tanggal' di file prediksi.")
    st.stop()

if "filter_year" not in st.session_state:
    st.session_state.filter_year = years_available[0]
if "filter_month" not in st.session_state:
    st.session_state.filter_month = "Semua Bulan"
if "filter_unit" not in st.session_state:
    st.session_state.filter_unit = "Kg"

with st.form("form_filter"):
    c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1])
    with c1:
        year = st.selectbox("Tahun", years_available, index=years_available.index(st.session_state.filter_year))
    with c2:
        month_options = ["Semua Bulan"] + [month_name_id(m) for m in range(1, 13)]
        month = st.selectbox("Bulan", month_options, index=month_options.index(st.session_state.filter_month))
    with c3:
        unit = st.selectbox("Satuan (grafik)", ["Kg", "Sisir"], index=["Kg", "Sisir"].index(st.session_state.filter_unit))
    with c4:
        st.write("")
        submit = st.form_submit_button("Tampilkan", use_container_width=True)

if submit:
    st.session_state.filter_year = year
    st.session_state.filter_month = month
    st.session_state.filter_unit = unit

year = st.session_state.filter_year
month_name = st.session_state.filter_month
unit_choice = st.session_state.filter_unit

df_pred_year = df_pred_all[df_pred_all["tanggal"].dt.year == int(year)].copy()

# =========================================================
# PAGE: DASHBOARD
# =========================================================
if page == "Dashboard":
    st.subheader("Jawaban cepat")

    if month_name == "Semua Bulan":
        card("Perkiraan pisang yang perlu disiapkan", "Pilih bulan", f"Tahun {year}")
    else:
        month_num = [k for k, v in ID_MONTH_NAMES.items() if v == month_name][0]
        df_month = df_pred_year[df_pred_year["tanggal"].dt.month == int(month_num)].copy()

        if df_month.empty:
            card("Perkiraan pisang yang perlu disiapkan", "Data belum ada", f"{month_name} {year}")
        else:
            v_kg = float(df_month["nilai"].mean())
            text_kg, text_sisir = fmt_dual_units(v_kg)
            card(
                "Perkiraan pisang yang perlu disiapkan",
                f"± {text_kg} (≈ {text_sisir})",
                f"Bulan {month_name} {year}",
            )

    st.write("")
    st.subheader("Perkiraan kebutuhan pisang per bulan")
    chart = make_line_month_chart(df_pred_year, unit_choice)
    if chart is None:
        empty_state("Grafik belum tersedia", "Data prediksi untuk tahun ini belum ada.")
    else:
        st.altair_chart(chart, use_container_width=True)

# =========================================================
# PAGE: DETAIL
# =========================================================
elif page == "Detail":
    st.subheader("Rincian kebutuhan pisang per bulan")

    if df_pred_year.empty:
        empty_state("Data tahun ini belum ada", "Coba pilih tahun lain.")
        st.stop()

    st.markdown("#### Grafik ringkas")
    bar = make_bar_month_chart(df_pred_year, unit_choice)
    if bar is not None:
        st.altair_chart(bar, use_container_width=True)

    st.markdown("#### Tabel (kg & sisir)")
    tbl = month_table(df_pred_all, int(year))
    if tbl.empty:
        st.caption("Belum ada data prediksi.")
    else:
        tbl_show = tbl.copy()
        for col in ["Perkiraan_kg", "Min_kg", "Maks_kg"]:
            if col in tbl_show.columns:
                tbl_show[col.replace("_kg", "_sisir")] = tbl_show[col].apply(
                    lambda x: convert_value_kg_to_unit(x, "Sisir")
                )

        tbl_show = tbl_show.rename(columns={
            "Perkiraan_kg": "Perkiraan (kg)",
            "Min_kg": "Min (kg)",
            "Maks_kg": "Maks (kg)",
            "Perkiraan_sisir": "Perkiraan (sisir)",
            "Min_sisir": "Min (sisir)",
            "Maks_sisir": "Maks (sisir)",
        })
        st.dataframe(tbl_show, use_container_width=True, hide_index=True)

        xlsx_bytes = to_excel_bytes(tbl_show, sheet_name=f"Rincian_{year}")
        st.download_button(
            "⬇️ Unduh tabel rincian",
            data=xlsx_bytes,
            file_name=f"rincian_kebutuhan_{year}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

# =========================================================
# PAGE: UPLOAD (ADMIN ONLY)
# =========================================================
elif page == "Upload":
    if not IS_ADMIN:
        empty_state("Akses ditolak", "Menu ini hanya untuk Admin.")
        st.stop()

    st.subheader("Admin: Upload Data Historis & Proses SARIMA")
    st.caption("Alur: Upload historis → klik Proses SARIMA → hasil langsung masuk dashboard (UMKM tinggal lihat).")

    uploaded = st.file_uploader("Upload file historis (.xlsx)", type=["xlsx", "xls"])
    steps = st.number_input("Prediksi berapa bulan ke depan?", min_value=3, max_value=36, value=24, step=1)

    order = (1, 1, 1)
    seasonal_order = (1, 1, 1, 12)

    with st.expander("⚙️ Advanced (opsional): Pengaturan SARIMA", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            p = st.number_input("p", 0, 5, order[0])
            d = st.number_input("d", 0, 2, order[1])
            q = st.number_input("q", 0, 5, order[2])
        with c2:
            P = st.number_input("P", 0, 5, seasonal_order[0])
            D = st.number_input("D", 0, 2, seasonal_order[1])
            Q = st.number_input("Q", 0, 5, seasonal_order[2])
            s = st.number_input("s (musiman)", 1, 24, seasonal_order[3])

        order = (int(p), int(d), int(q))
        seasonal_order = (int(P), int(D), int(Q), int(s))

    st.markdown("### Preview historis")
    if uploaded is None:
        st.info("Upload file historis untuk diproses.")
        st.stop()

    try:
        df_hist = parse_historical_excel(uploaded)
        st.dataframe(df_hist.head(12), use_container_width=True)
    except Exception as e:
        st.error(f"Gagal baca historis: {e}")
        st.stop()

    if st.button("⚙️ Proses Prediksi & Terapkan", use_container_width=True):
        try:
            with st.spinner("Sedang memproses SARIMA (mode aman)..."):
                series = build_monthly_series(df_hist)

                # limiter biar ringan (5 tahun terakhir)
                if len(series) > 60:
                    series = series.iloc[-60:]

                df_pred = run_sarima_forecast(
                    series,
                    steps=int(steps),
                    order=order,
                    seasonal_order=seasonal_order,
                    maxiter=80,
                )

                tidy_new, act_new, pred_new = build_tidy_from_hist_and_pred(df_hist, df_pred)
                st.session_state.data_override = (tidy_new, act_new, pred_new)

            st.success("Berhasil! Prediksi terbaru sudah diterapkan ke dashboard.")

            # kasih download untuk dijadikan prediksi_default.xlsx
            st.download_button(
                "⬇️ Unduh prediksi terbaru (jadikan prediksi_default.xlsx)",
                data=to_excel_bytes(df_pred, sheet_name="Prediksi"),
                file_name="prediksi_default.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

            st.session_state.page = "Dashboard"
            st.rerun()

        except Exception as e:
            st.error(f"Gagal memproses SARIMA: {e}")


