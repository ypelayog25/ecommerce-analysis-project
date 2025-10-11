# scripts/app.py
"""
Executive E-commerce Dashboard — Power BI inspired (refined)
- Light/Dark theme toggle
- Animated KPI cards with tooltips
- Adaptive Plotly charts
- Loading splash + elegant footer with personal branding
- Clean separators (no stray <div>)
"""

from __future__ import annotations
import os, time
from datetime import datetime, timedelta
from typing import Optional, Dict, List

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# -----------------------
# Page config & fast splash
# -----------------------
st.set_page_config(
    page_title="Executive E-commerce Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊",
)

# Small splash while caching loads
with st.spinner("Loading dashboard assets and dataset…"):
    time.sleep(0.2)  # tiny pause to show spinner briefly (feel free to remove)

# -----------------------
# Theme palettes (light + dark)
# -----------------------
PALETTES = {
    "light": {
        "app_bg": "#F4F6F8",
        "panel": "#FFFFFF",
        "text": "#2B2B2B",
        "subtext": "#5B6366",
        "accent": "#0F62FE",   # clean blue
        "accent_dark": "#0057B8",
        "warn": "#FFB900",
        "neg": "#D13438",
        "border": "rgba(16,24,32,0.06)"
    },
    "dark": {
        "app_bg": "#0F1720",
        "panel": "#0B1116",
        "text": "#E6EEF3",
        "subtext": "#9AA6B2",
        "accent": "#4EA8FF",   # brighter for dark
        "accent_dark": "#118DFF",
        "warn": "#FFB900",
        "neg": "#FF6B6B",
        "border": "rgba(255,255,255,0.06)"
    }
}

# -----------------------
# Inject CSS for cards & responsiveness (clean)
# -----------------------
def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
        html, body, [data-testid="stAppViewContainer"] { font-family: 'Inter', sans-serif; }
        .kpi-card {
            border-radius: 10px;
            padding: 12px;
            transition: transform .18s ease, box-shadow .18s ease;
        }
        .kpi-card:hover { transform: translateY(-6px); }
        .kpi-title { font-size:12px; font-weight:600; letter-spacing:0.6px; margin-bottom:6px; color:inherit }
        .kpi-value { font-size:26px; font-weight:800; margin:0; color:inherit }
        .kpi-delta { font-size:13px; font-weight:700; margin-top:6px; color:inherit }
        .tiny-note { font-size:12px; color:inherit; }
        @media (max-width: 640px) {
            .kpi-title { font-size:11px; }
            .kpi-value { font-size:20px; }
        }
        /* subtle divider style we will reuse */
        .thin-divider { height:1px; background: rgba(0,0,0,0.06); margin:12px 0; border-radius:1px; }
        </style>
        """,
        unsafe_allow_html=True,
    )

inject_css()

# -----------------------
# Data loading (safe)
# -----------------------
@st.cache_data(ttl=600)
def load_data(parquet: str = "data/processed/ecommerce_dataset_10000_cleaned.parquet",
              csvf: str = "data/processed/ecommerce_dataset_10000_cleaned.csv") -> Optional[pd.DataFrame]:
    if os.path.exists(parquet):
        df = pd.read_parquet(parquet)
    elif os.path.exists(csvf):
        df = pd.read_csv(csvf)
    else:
        return None

    # Ensure minimal schema, fill safe defaults
    expected = ["country", "order_date", "customer_id", "product_name", "quantity", "unit_price", "total_price"]
    for col in expected:
        if col not in df.columns:
            if col in ("quantity",):
                df[col] = 0
            elif col in ("unit_price", "total_price"):
                df[col] = 0.0
            else:
                df[col] = "N/A"

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df = df.dropna(subset=["order_date"]).copy()
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce").fillna(0.0)
    df["total_price"] = pd.to_numeric(df["total_price"], errors="coerce").fillna(df["unit_price"] * df["quantity"])
    df["country"] = df["country"].astype(str).str.strip()
    df["customer_id"] = df["customer_id"].astype(str).str.strip()
    df["product_name"] = df["product_name"].astype(str).str.strip()
    df["year_month"] = df["order_date"].dt.to_period("M").dt.to_timestamp()
    df["day_name"] = df["order_date"].dt.day_name()
    return df

df = load_data()
if df is None or df.empty:
    st.error("Dataset not found or empty. Put processed Parquet/CSV into data/processed/")
    st.stop()

# -----------------------
# Sidebar: theme toggle & filters
# -----------------------
with st.sidebar:
    st.markdown("## Controls")
    dark_mode = st.checkbox("🌙 Dark mode", value=False)
    theme = "dark" if dark_mode else "light"
    pal = PALETTES[theme]

    # Date range
    min_date = df["order_date"].min().date()
    max_date = df["order_date"].max().date()
    start_date = st.date_input("From", value=min_date, min_value=min_date, max_value=max_date)
    end_date = st.date_input("To", value=max_date, min_value=min_date, max_value=max_date)
    start_ts = pd.to_datetime(start_date)
    end_ts = pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

    # Countries
    countries = sorted(df["country"].dropna().unique().tolist())
    select_all = st.checkbox("Select all countries", value=True)
    selected_countries = countries if select_all else st.multiselect("Countries", options=countries, default=countries[:4])

    # Top N
    top_n = st.slider("Top N", min_value=5, max_value=50, value=10, step=5)

# Apply some background styling depending on theme (best-effort)
st.markdown(
    f"""
    <style>
    .reportview-container .main {{ background: {pal['app_bg']}; }}
    .stApp {{ background: {pal['app_bg']}; color: {pal['text']}; }}
    .kpi-card {{ color: {pal['text']}; background: {pal['panel']}; border:1px solid {pal['border']}; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------
# Filtered data
# -----------------------
df_filtered = df[
    (df["order_date"] >= start_ts) &
    (df["order_date"] <= end_ts) &
    (df["country"].isin(selected_countries))
].copy()

if df_filtered.empty:
    st.warning("No data for the selected filters. Expand range or countries.")
    st.stop()

# -----------------------
# Metrics computation
# -----------------------
def safe_order_count(d: pd.DataFrame) -> int:
    if "order_id" in d.columns:
        return int(d["order_id"].nunique())
    return int(len(d))

def compute_metrics(curr: pd.DataFrame, all_df: pd.DataFrame) -> Dict[str, float]:
    total_revenue = float(curr["total_price"].sum())
    total_orders = safe_order_count(curr)
    unique_customers = int(curr["customer_id"].nunique())
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0.0
    countries_active = int(curr["country"].nunique())
    total_quantity = int(curr["quantity"].sum())

    # previous period (same length immediately before)
    period_days = max(1, (curr["order_date"].max() - curr["order_date"].min()).days)
    prev_start = curr["order_date"].min() - pd.Timedelta(days=period_days)
    prev_end = curr["order_date"].min() - pd.Timedelta(seconds=1)
    prev_df = all_df[(all_df["order_date"] >= prev_start) & (all_df["order_date"] <= prev_end)]

    prev_revenue = float(prev_df["total_price"].sum()) if not prev_df.empty else 0.0
    prev_orders = safe_order_count(prev_df) if not prev_df.empty else 0
    prev_customers = int(prev_df["customer_id"].nunique()) if not prev_df.empty else 0

    def pct(curr_v, prev_v):
        if prev_v == 0:
            return 0.0
        return (curr_v - prev_v) / prev_v * 100.0

    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "unique_customers": unique_customers,
        "avg_order_value": avg_order_value,
        "countries_active": countries_active,
        "total_quantity": total_quantity,
        "prev_revenue": prev_revenue,
        "prev_orders": prev_orders,
        "prev_customers": prev_customers,
        "revenue_delta_pct": pct(total_revenue, prev_revenue),
        "orders_delta_pct": pct(total_orders, prev_orders),
        "customers_delta_pct": pct(unique_customers, prev_customers),
    }

metrics = compute_metrics(df_filtered, df)

# -----------------------
# Animated KPI helper (keeps final value stable across reruns using session_state)
# -----------------------
def animate_number(value: float, fmt: str = "{:,.0f}", seconds: float = 0.9, key: str = ""):
    placeholder = st.empty()
    # If already animated in this session for this key, show static final value
    animated_key = f"_animated_{key}"
    if key and st.session_state.get(animated_key, False):
        try:
            placeholder.markdown(f"<div class='kpi-value' style='color:{pal['accent']};'>{fmt.format(value)}</div>", unsafe_allow_html=True)
        except Exception:
            placeholder.markdown(f"<div class='kpi-value' style='color:{pal['accent']};'>{int(value):,}</div>", unsafe_allow_html=True)
        return
    # animate once
    steps = int(max(8, min(48, seconds * 30)))
    start = 0.0
    for i in range(1, steps + 1):
        frac = i / steps
        current = start + (value - start) * (frac ** 0.85)
        try:
            placeholder.markdown(f"<div class='kpi-value' style='color:{pal['accent']};'>{fmt.format(current)}</div>", unsafe_allow_html=True)
        except Exception:
            placeholder.markdown(f"<div class='kpi-value' style='color:{pal['accent']};'>{int(current):,}</div>", unsafe_allow_html=True)
        time.sleep(seconds / steps)
    # final
    placeholder.markdown(f"<div class='kpi-value' style='color:{pal['accent']};'>{fmt.format(value)}</div>", unsafe_allow_html=True)
    if key:
        st.session_state[animated_key] = True

# -----------------------
# KPI Cards (Power BI-style) - responsive
# -----------------------
st.markdown("")  # small spacer
st.markdown("### Key Performance Indicators")

cols = st.columns([2,1,1,1,1], gap="large")

# Card 1: Total Revenue (big) with tooltip (abbr)
with cols[0]:
    card_style = f"background:{pal['panel']}; border:1px solid {pal['border']};"
    st.markdown(f"<div class='kpi-card' style='{card_style}' title='Total revenue within the selected filters (currency).'>", unsafe_allow_html=True)
    st.markdown(f"<div class='kpi-title'>{'<abbr title=\"Total revenue in selected period\">💰 TOTAL REVENUE</abbr>'}</div>", unsafe_allow_html=True)
    animate_number(metrics["total_revenue"], fmt="${:,.0f}", seconds=0.9, key="rev")
    # delta
    delta = metrics["revenue_delta_pct"]
    delta_color = pal["accent"] if delta >= 0 else pal["neg"]
    st.markdown(f"<div class='kpi-delta' style='color:{delta_color};'>{delta:+.1f}% vs prev period</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Card 2: Total Orders
with cols[1]:
    card_style = f"background:{pal['panel']}; border:1px solid {pal['border']};"
    st.markdown(f"<div class='kpi-card' style='{card_style}' title='Unique orders (if order_id exists) or rows in filtered selection.'>", unsafe_allow_html=True)
    st.markdown(f"<div class='kpi-title'>{'<abbr title=\"Count of unique orders\">🛒 TOTAL ORDERS</abbr>'}</div>", unsafe_allow_html=True)
    animate_number(metrics["total_orders"], fmt="{:,.0f}", seconds=0.7, key="orders")
    delta_o = metrics["orders_delta_pct"]
    dc = pal["accent"] if delta_o >= 0 else pal["neg"]
    st.markdown(f"<div class='kpi-delta' style='color:{dc};'>{delta_o:+.1f}% vs prev</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Card 3: Avg Order Value
with cols[2]:
    card_style = f"background:{pal['panel']}; border:1px solid {pal['border']};"
    st.markdown(f"<div class='kpi-card' style='{card_style}' title='Average order value = Total revenue / Orders.'>", unsafe_allow_html=True)
    st.markdown(f"<div class='kpi-title'>{'<abbr title=\"Average order value (AOV)\">📊 AVG ORDER VALUE</abbr>'}</div>", unsafe_allow_html=True)
    animate_number(metrics["avg_order_value"], fmt="${:,.2f}", seconds=0.7, key="aov")
    st.markdown("</div>", unsafe_allow_html=True)

# Card 4: Unique Customers
with cols[3]:
    card_style = f"background:{pal['panel']}; border:1px solid {pal['border']};"
    st.markdown(f"<div class='kpi-card' style='{card_style}' title='Unique customers in the filtered set.'>", unsafe_allow_html=True)
    st.markdown(f"<div class='kpi-title'>{'<abbr title=\"Number of unique customers\">👥 UNIQUE CUSTOMERS</abbr>'}</div>", unsafe_allow_html=True)
    animate_number(metrics["unique_customers"], fmt="{:,.0f}", seconds=0.7, key="customers")
    st.markdown("</div>", unsafe_allow_html=True)

# Card 5: Countries Active
with cols[4]:
    card_style = f"background:{pal['panel']}; border:1px solid {pal['border']};"
    st.markdown(f"<div class='kpi-card' style='{card_style}' title='Number of distinct countries with sales.'>", unsafe_allow_html=True)
    st.markdown(f"<div class='kpi-title'>{'<abbr title=\"Active countries in filters\">🌍 COUNTRIES ACTIVE</abbr>'}</div>", unsafe_allow_html=True)
    animate_number(metrics["countries_active"], fmt="{:,.0f}", seconds=0.7, key="countries")
    st.markdown("</div>", unsafe_allow_html=True)

# Elegant thin divider (instead of raw div spacer)
st.markdown("<div class='thin-divider' style='opacity:0.6'></div>", unsafe_allow_html=True)

# -----------------------
# Small example chart to show adaptive Plotly colors (vertical bars + values on top)
# -----------------------
def plot_monthly_revenue_adaptive(df_in: pd.DataFrame, palette: dict):
    monthly = df_in.groupby(df_in["order_date"].dt.to_period("M"))["total_price"].sum().reset_index()
    monthly["order_date"] = monthly["order_date"].dt.to_timestamp()
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=monthly["order_date"],
        y=monthly["total_price"],
        marker_color=palette["accent"],
        hovertemplate="%{x|%b %Y}<br>Revenue: %{y:$,.0f}<extra></extra>",
        text=[f"${v:,.0f}" for v in monthly["total_price"]],
        textposition="outside"
    ))
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        title=dict(text="Monthly Revenue", x=0.5, xanchor="center", font=dict(color=palette["text"], size=16)),
        font=dict(color=palette["text"]),
        yaxis=dict(gridcolor="rgba(0,0,0,0.04)", tickformat=","),
        xaxis=dict(tickangle=-45, tickfont=dict(size=11))
    )
    # make bars readable on small screens (reduce margins)
    fig.update_layout(margin=dict(l=40, r=20, t=60, b=80))
    return fig

st.plotly_chart(plot_monthly_revenue_adaptive(df_filtered, pal), use_container_width=True)

# -----------------------
# Footer (elegant, right aligned, personal branding)
# -----------------------
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)  # slight space before footer
footer_html = f"""
<div style='width:100%; display:flex; justify-content:flex-end;'>
  <div style='text-align:right; color:{pal['subtext']}; font-size:12px;'>
    Executive Dashboard • Powered by <b>Python</b> & <b>Streamlit</b> • Designed by <b>Yenismara Pelayo</b>
  </div>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
