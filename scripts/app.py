# scripts/app.py
"""
Power BI Dark — Executive E-commerce Dashboard (Streamlit)
Clean, corporate dark theme using Power BI-like palette (blue/yellow).
Safe with missing columns, sparkline KPIs, responsive charts.
"""

from __future__ import annotations
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -----------------------
# Page config
# -----------------------
st.set_page_config(
    page_title="Executive E-commerce Dashboard — Power BI Dark",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊",
)

# -----------------------
# Power BI-ish palette (dark)
# -----------------------
BG = "#0b0f14"            # main background (dark)
PANEL = "#0f1720"         # panels/cards
TEXT = "#E6E6E6"          # main text
SUBTEXT = "#A0A0A0"       # secondary text
ACCENT_BLUE = "#118DFF"   # primary accent (Power BI-like blue)
ACCENT_YELLOW = "#FFB900" # secondary accent (Power BI yellow)
ACCENT_RED = "#D13438"    # negative / alert
BORDER = "rgba(255,255,255,0.06)"

# -----------------------
# Inject polished CSS (dark + clean)
# -----------------------
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [data-testid="stAppViewContainer"] {{
        background: {BG};
        color: {TEXT};
        font-family: 'Inter', sans-serif;
    }}
    .stApp {{
        background: {BG};
    }}
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {PANEL}, #071019);
        color: {TEXT};
        border-right: 1px solid rgba(255,255,255,0.02);
    }}
    .css-1d391kg {{ padding-top: 0.5rem; }} /* small tweak to header spacing */
    h1, h2, h3 {{ color: {TEXT}; font-weight:700; }}
    p, label, span {{ color: {SUBTEXT}; }}

    /* Metric containers (cards) */
    div[data-testid="metric-container"] {{
        background: linear-gradient(90deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        border: 1px solid {BORDER};
        padding: 14px;
        border-radius: 12px;
        box-shadow: 0 6px 24px rgba(0,0,0,0.6);
    }}
    [data-testid="stMetricValue"] {{
        font-size: 28px !important;
        font-weight: 700 !important;
        color: {ACCENT_BLUE} !important;
    }}
    [data-testid="stMetricLabel"] {{
        font-size: 12px !important;
        color: {SUBTEXT} !important;
        letter-spacing: 1px;
    }}
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{ gap: 8px; }}
    .stTabs [data-baseweb="tab"] {{
        background: rgba(255,255,255,0.02); color: {SUBTEXT}; border-radius: 8px;
        padding: 6px 18px; font-weight:600;
    }}
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(90deg, {ACCENT_BLUE}, {ACCENT_YELLOW});
        color: #0b0f14 !important;
        box-shadow: 0 6px 20px rgba(17, 100, 255, 0.12);
    }}
    /* Buttons */
    .stButton button {{
        background: linear-gradient(90deg, {ACCENT_BLUE}, {ACCENT_YELLOW});
        color: #0b0f14;
        border-radius: 10px;
        padding: 8px 14px;
        font-weight:600;
    }}
    .stDownloadButton button {{
        background: linear-gradient(90deg, {ACCENT_YELLOW}, {ACCENT_BLUE});
        color: #0b0f14;
        font-weight:700;
    }}
    /* Dataframe */
    [data-testid="stDataFrame"] {{
        background: rgba(255,255,255,0.02); border-radius: 10px;
    }}
    /* Minor inputs */
    input[type="date"], .css-1hwfws3 {{ background: rgba(255,255,255,0.02); color:{TEXT}; border-radius:8px; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------
# Data loading
# -----------------------
@st.cache_data(ttl=3600)
def load_data(parquet_path: str = "data/processed/ecommerce_dataset_10000_cleaned.parquet",
              csv_path: str = "data/processed/ecommerce_dataset_10000_cleaned.csv") -> Optional[pd.DataFrame]:
    """Load dataset with safe defaults and minimal preprocessing."""
    if os.path.exists(parquet_path):
        df = pd.read_parquet(parquet_path)
    elif os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        return None

    # Ensure expected columns exist (provide fallbacks)
    expected = ["country", "order_date", "customer_id", "product_name", "quantity", "unit_price", "total_price"]
    for col in expected:
        if col not in df.columns:
            # create safe fallback
            if col in ("quantity",):
                df[col] = 0
            elif col in ("unit_price", "total_price"):
                df[col] = 0.0
            else:
                df[col] = "N/A"

    # datetime
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df = df.dropna(subset=["order_date"]).copy()

    # numeric conversions
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce").fillna(0.0)
    df["total_price"] = pd.to_numeric(df["total_price"], errors="coerce")
    # if total_price missing but unit_price*quantity available, fallback
    df["total_price"] = df["total_price"].fillna(df["unit_price"] * df["quantity"])

    # tidy strings
    df["country"] = df["country"].astype(str).str.strip()
    df["product_name"] = df["product_name"].astype(str).str.strip()
    df["customer_id"] = df["customer_id"].astype(str).str.strip()

    # derived
    df["year_month"] = df["order_date"].dt.to_period("M").dt.to_timestamp()
    df["day_of_week"] = df["order_date"].dt.day_name()
    return df

df = load_data()
if df is None or df.empty:
    st.error("❌ Dataset not found or is empty. Place your processed Parquet/CSV in data/processed/")
    st.stop()

# -----------------------
# Sidebar controls (compact)
# -----------------------
with st.sidebar:
    st.markdown("<div style='text-align:center;padding:8px 0'>"
                f"<h2 style='margin:0;color:{TEXT}'>Control Center</h2></div>", unsafe_allow_html=True)

    min_date = df["order_date"].min().date()
    max_date = df["order_date"].max().date()
    start_date = st.date_input("From", min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.date_input("To", min_value=min_date, max_value=max_date, value=max_date)

    # make inclusive timestamps
    start_ts = pd.to_datetime(start_date)
    end_ts = pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

    countries = sorted(df["country"].dropna().unique())
    select_all = st.checkbox("Select all countries", value=True)
    if select_all:
        selected_countries = countries
    else:
        selected_countries = st.multiselect("Countries", options=countries, default=countries[:3])

    top_n = st.slider("Top N", min_value=5, max_value=50, value=10, step=5)
    chart_theme = st.selectbox("Plotly theme (visual)", ["plotly_dark", "plotly_white"], index=0)

# -----------------------
# Filter data safely
# -----------------------
df_filtered = df[
    (df["order_date"] >= start_ts)
    & (df["order_date"] <= end_ts)
    & (df["country"].isin(selected_countries))
].copy()

if df_filtered.empty:
    st.warning("⚠️ No data for selected filters — try expanding the date range or countries.")
    st.stop()

# -----------------------
# Utilities & metrics
# -----------------------
def safe_count_orders(df_in: pd.DataFrame) -> int:
    # if order_id exists use unique order id, else fallback to number of rows
    if "order_id" in df_in.columns:
        try:
            return int(df_in["order_id"].nunique())
        except Exception:
            return int(len(df_in))
    return int(len(df_in))

def compute_metrics(curr: pd.DataFrame, all_df: pd.DataFrame) -> Dict[str, float]:
    total_revenue = float(curr["total_price"].sum())
    total_orders = safe_count_orders(curr)
    unique_customers = int(curr["customer_id"].nunique())
    total_quantity = int(curr["quantity"].sum())
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0.0

    # previous period (same duration immediately before)
    period_days = max(1, (curr["order_date"].max() - curr["order_date"].min()).days)
    prev_start = curr["order_date"].min() - pd.Timedelta(days=period_days)
    prev_end = curr["order_date"].min() - pd.Timedelta(seconds=1)
    prev_df = all_df[(all_df["order_date"] >= prev_start) & (all_df["order_date"] <= prev_end)]

    prev_revenue = float(prev_df["total_price"].sum()) if not prev_df.empty else 0.0
    prev_orders = safe_count_orders(prev_df) if not prev_df.empty else 0
    prev_customers = int(prev_df["customer_id"].nunique()) if not prev_df.empty else 0

    def pct(curr_v, prev_v):
        if prev_v == 0:
            return 0.0
        return (curr_v - prev_v) / prev_v * 100.0

    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "unique_customers": unique_customers,
        "total_quantity": total_quantity,
        "avg_order_value": avg_order_value,
        "prev_revenue": prev_revenue,
        "prev_orders": prev_orders,
        "prev_customers": prev_customers,
        "revenue_delta_pct": pct(total_revenue, prev_revenue),
        "orders_delta_pct": pct(total_orders, prev_orders),
        "customers_delta_pct": pct(unique_customers, prev_customers),
    }

metrics = compute_metrics(df_filtered, df)

# -----------------------
# Styling function for Plotly
# -----------------------
def style_plotly(fig: go.Figure, title: str = "") -> go.Figure:
    fig.update_layout(
        title=dict(text=title, x=0.5, xanchor="center", font=dict(size=18, color=TEXT)),
        font=dict(color=TEXT),
        margin=dict(l=40, r=30, t=60, b=40),
        template=chart_theme,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.03)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.03)")
    return fig

# -----------------------
# Top-level header
# -----------------------
st.markdown(
    f"""
    <div style="padding: 18px 0 6px 0; text-align:center">
        <h1 style="margin:0;color:{TEXT};font-size:34px;font-weight:800;">📊 Executive E-commerce Dashboard</h1>
        <p style="margin:6px 0 0 0;color:{SUBTEXT};">Power BI style • Dark theme • Clean & professional</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr style='border-color: rgba(255,255,255,0.04); margin: 14px 0 22px 0;'>", unsafe_allow_html=True)

# -----------------------
# KPI cards row
# -----------------------
st.markdown("### Key Performance Indicators")
c1, c2, c3, c4, c5 = st.columns([2,1,1,1,1])

# Sparkline data (monthly revenue)
monthly_rev = (
    df_filtered.groupby(df_filtered["order_date"].dt.to_period("M"))["total_price"]
    .sum()
    .reset_index()
)
monthly_rev["order_date"] = monthly_rev["order_date"].dt.to_timestamp()
spark_vals = monthly_rev["total_price"].fillna(0).tolist() if not monthly_rev.empty else [0]

with c1:
    # big revenue card
    rev = metrics["total_revenue"]
    rev_delta = metrics["revenue_delta_pct"]
    rev_color = ACCENT_BLUE if rev_delta >= 0 else ACCENT_RED
    st.metric(label="💰 Total Revenue", value=f"{rev:,.0f}", delta=f"{rev_delta:.1f}%")
    # tiny sparkline
    fig_s = go.Figure(go.Scatter(x=list(range(len(spark_vals))), y=spark_vals, mode="lines", line=dict(color=ACCENT_BLUE, width=2), fill="tozeroy", fillcolor="rgba(17,141,255,0.12)"))
    fig_s.update_layout(margin=dict(l=0,r=0,t=0,b=0), height=48, xaxis_visible=False, yaxis_visible=False, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_s, use_container_width=True)

with c2:
    ords = metrics["total_orders"]
    ord_delta = metrics["orders_delta_pct"]
    st.metric(label="🛒 Orders", value=f"{ords:,}", delta=f"{ord_delta:.1f}%")

with c3:
    custs = metrics["unique_customers"]
    cust_delta = metrics["customers_delta_pct"]
    st.metric(label="👥 Customers", value=f"{custs:,}", delta=f"{cust_delta:.1f}%")

with c4:
    st.metric(label="📦 Units Sold", value=f"{metrics['total_quantity']:,}")

with c5:
    st.metric(label="💵 Avg Order", value=f"${metrics['avg_order_value']:.2f}")

st.markdown("<hr style='border-color: rgba(255,255,255,0.04); margin: 18px 0 20px 0;'>", unsafe_allow_html=True)

# -----------------------
# Tabs layout
# -----------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Revenue", "Customers", "Products", "Geo", "Advanced"])

# --- TAB: Revenue
with tab1:
    left, right = st.columns([2,1])
    with left:
        st.subheader("Monthly Revenue")
        monthly = monthly_rev.copy()
        fig = go.Figure()
        fig.add_trace(go.Bar(x=monthly["order_date"], y=monthly["total_price"], marker_color=ACCENT_BLUE, name="Revenue"))
        # 3-month moving average
        fig.add_trace(go.Scatter(x=monthly["order_date"], y=monthly["total_price"].rolling(3, min_periods=1).mean(), mode="lines", line=dict(color=ACCENT_YELLOW, width=3), name="3-mo MA"))
        st.plotly_chart(style_plotly(fig, "Monthly Revenue"), use_container_width=True)
    with right:
        st.subheader("Top Countries by Revenue")
        country_rev = df_filtered.groupby("country")["total_price"].sum().reset_index().sort_values("total_price", ascending=False)
        figc = go.Figure(go.Bar(x=country_rev["country"].head(top_n), y=country_rev["total_price"].head(top_n), marker_color=px.colors.sequential.Blues))
        st.plotly_chart(style_plotly(figc, "Top Countries"), use_container_width=True)

    st.subheader("Revenue by Day of Week")
    dow_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    dow = df_filtered.groupby("day_of_week")["total_price"].sum().reindex(dow_order).reset_index()
    fig_dow = go.Figure(go.Bar(x=dow["day_of_week"], y=dow["total_price"], marker_color=ACCENT_BLUE, text=[f"{v:,.0f}" for v in dow["total_price"]], textposition="outside"))
    st.plotly_chart(style_plotly(fig_dow, "Weekly Revenue Pattern"), use_container_width=True)

# --- TAB: Customers
with tab2:
    st.subheader(f"Top {top_n} Customers by Revenue")
    top_customers = df_filtered.groupby("customer_id").agg(total_revenue=("total_price","sum")).reset_index().nlargest(top_n, "total_revenue")
    fig_tc = go.Figure(go.Bar(x=top_customers["total_revenue"], y=top_customers["customer_id"], orientation="h", marker_color=px.colors.sequential.Plasma))
    st.plotly_chart(style_plotly(fig_tc, "Top Customers"), use_container_width=True)

    st.markdown("Customer Frequency Distribution")
    freq = df_filtered.groupby("customer_id")["order_date"].nunique().value_counts().sort_index().reset_index()
    freq.columns = ["orders","customers"]
    fig_freq = go.Figure(go.Bar(x=freq["orders"], y=freq["customers"], marker_color=ACCENT_BLUE))
    st.plotly_chart(style_plotly(fig_freq, "Order Frequency Distribution"), use_container_width=True)

# --- TAB: Products
with tab3:
    st.subheader(f"Top {top_n} Products by Revenue")
    top_products_rev = df_filtered.groupby("product_name").agg(total_price=("total_price","sum"), quantity=("quantity","sum")).reset_index().nlargest(top_n, "total_price")
    fig_pr = go.Figure(go.Bar(x=top_products_rev["total_price"], y=top_products_rev["product_name"], orientation="h", marker_color=px.colors.sequential.Teal))
    st.plotly_chart(style_plotly(fig_pr, "Top Products by Revenue"), use_container_width=True)

    st.subheader("Price Distribution")
    fig_price = go.Figure()
    fig_price.add_trace(go.Histogram(x=df_filtered["unit_price"], nbinsx=50, marker_color="#9b59b6"))
    fig_price.add_trace(go.Box(x=df_filtered["unit_price"], name="Distribution", marker_color=ACCENT_BLUE))
    fig_price.update_layout(yaxis2=dict(overlaying="y", side="right"))
    st.plotly_chart(style_plotly(fig_price, "Unit Price Distribution"), use_container_width=True)

# --- TAB: Geo
with tab4:
    st.subheader("Revenue by Country")
    country_analysis = df_filtered.groupby("country").agg(revenue=("total_price","sum"), orders=("order_date","count"), customers=("customer_id","nunique")).reset_index().sort_values("revenue", ascending=False)
    fig_geo = go.Figure(go.Bar(x=country_analysis["country"], y=country_analysis["revenue"], marker_color=px.colors.sequential.Blues))
    st.plotly_chart(style_plotly(fig_geo, "Global Revenue Distribution"), use_container_width=True)

    st.markdown("Country details")
    display_df = country_analysis.copy()
    display_df["revenue"] = display_df["revenue"].apply(lambda x: f"${x:,.0f}")
    display_df["avg_order_value"] = (country_analysis["revenue"] / country_analysis["orders"]).fillna(0).apply(lambda x: f"${x:,.2f}")
    st.dataframe(display_df, use_container_width=True)

# --- TAB: Advanced
with tab5:
    st.subheader("Growth & Pareto")
    # Growth
    monthly_g = df_filtered.groupby(df_filtered["order_date"].dt.to_period("M"))["total_price"].sum().reset_index()
    monthly_g["order_date"] = monthly_g["order_date"].dt.to_timestamp()
    monthly_g["growth_pct"] = monthly_g["total_price"].pct_change() * 100
    fig_g = go.Figure(go.Bar(x=monthly_g["order_date"], y=monthly_g["growth_pct"], marker_color=[ACCENT_BLUE if (not pd.isna(v) and v>=0) else ACCENT_RED for v in monthly_g["growth_pct"]]))
    fig_g.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.06)")
    st.plotly_chart(style_plotly(fig_g, "Month-over-Month Growth %"), use_container_width=True)

    # Pareto
    pr = df_filtered.groupby("product_name")["total_price"].sum().sort_values(ascending=False).reset_index()
    pr["cum_pct"] = pr["total_price"].cumsum() / pr["total_price"].sum() * 100
    top20 = pr.head(20)
    fig_p = go.Figure()
    fig_p.add_trace(go.Bar(x=list(range(len(top20))), y=top20["total_price"], name="Revenue", marker_color=ACCENT_BLUE))
    fig_p.add_trace(go.Scatter(x=list(range(len(top20))), y=top20["cum_pct"], name="Cumulative %", yaxis="y2", line=dict(color=ACCENT_YELLOW, width=3)))
    fig_p.update_layout(yaxis2=dict(overlaying="y", side="right", range=[0,100]))
    st.plotly_chart(style_plotly(fig_p, "Pareto (Top 20 Products)"), use_container_width=True)

# -----------------------
# Executive summary (safe)
# -----------------------
st.markdown("---")
st.subheader("Executive Summary")
country_analysis = country_analysis if "country_analysis" in locals() else df_filtered.groupby("country").agg(revenue=("total_price","sum")).reset_index().sort_values("revenue", ascending=False)
top_country = country_analysis.iloc[0].to_dict() if not country_analysis.empty else {"country":"N/A", "revenue":0}
best_product = top_products_rev.iloc[0].to_dict() if "top_products_rev" in locals() and not top_products_rev.empty else {"product_name":"N/A", "total_price":0}

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Top Country", top_country.get("country","N/A"), f"${top_country.get('revenue',0):,.0f}")
with col2:
    name = best_product.get("product_name","N/A")
    st.metric("Best Product", name if len(name)<=24 else name[:21]+"…", f"${best_product.get('total_price',0):,.0f}")
with col3:
    # vip estimate (top 5% customers by revenue)
    cust_rev = df_filtered.groupby("customer_id")["total_price"].sum().reset_index().sort_values("total_price", ascending=False)
    vip_count = int(max(0, round(len(cust_rev) * 0.05)))
    st.metric("Est. VIPs (top 5%)", f"{vip_count}")
with col4:
    avg_mom = monthly_g["growth_pct"].mean() if "monthly_g" in locals() and not monthly_g.empty else 0.0
    st.metric("Avg MoM Growth", f"{avg_mom:.1f}%")

# -----------------------
# Export buttons
# -----------------------
st.markdown("<hr style='border-color: rgba(255,255,255,0.04); margin: 16px 0;'>", unsafe_allow_html=True)
e1, e2, e3, e4 = st.columns(4)
now = datetime.now().strftime("%Y%m%d_%H%M")
with e1:
    st.download_button("📥 Download filtered dataset", df_filtered.to_csv(index=False).encode("utf-8"), file_name=f"filtered_{now}.csv", mime="text/csv")
with e2:
    if not top_customers.empty:
        st.download_button("🏆 Download top customers", top_customers.to_csv(index=False).encode("utf-8"), file_name=f"top_customers_{now}.csv", mime="text/csv")
with e3:
    if 'top_products_rev' in locals() and not top_products_rev.empty:
        st.download_button("📦 Download top products", top_products_rev.to_csv(index=False).encode("utf-8"), file_name=f"top_products_{now}.csv", mime="text/csv")
with e4:
    st.download_button("🌍 Download country report", country_analysis.to_csv(index=False).encode("utf-8"), file_name=f"country_report_{now}.csv", mime="text/csv")

# Footer
st.markdown("<hr style='border-color: rgba(255,255,255,0.04); margin: 18px 0;'>", unsafe_allow_html=True)
st.caption("Built with Streamlit • Power BI style dark theme • Clean & professional")

# End
