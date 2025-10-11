# scripts/app.py
"""
Executive E-commerce Dashboard — Premium theme (clean, professional, mobile-friendly)
Replace the previous app file with this one. Keeps same data flow but updates visual theme.
"""

from __future__ import annotations
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# -----------------------
# Page config
# -----------------------
st.set_page_config(
    page_title="Executive E-commerce Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊",
)

# -----------------------
# Premium palette (corporate / fintech look)
# -----------------------
PALETTE = {
    "bg_grad_start": "#111218",   # deep graphite
    "bg_grad_end": "#223046",     # muted blue/graphite
    "panel": "#FFFFFF",           # white panels on light mode fallback
    "text_light": "#E9EEF3",      # light text (dark mode)
    "text_dim": "#9AA6B2",
    "accent": "#2ECC71",          # emerald (positive)
    "accent_alt": "#1E90FF",      # blue petrol (buttons/links)
    "gold": "#F1C40F",            # highlight
    "muted": "#7B8A99",           # muted gray text
    "card_border": "rgba(255,255,255,0.06)"
}

# -----------------------
# Inject improved CSS (responsive + mobile)
# -----------------------
def inject_css() -> None:
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {{
        font-family: 'Inter', sans-serif;
    }}

    /* Page background gradient (dark) */
    .stApp {{
        background: linear-gradient(180deg, {PALETTE['bg_grad_start']} 0%, {PALETTE['bg_grad_end']} 100%);
        color: {PALETTE['text_light']};
    }}

    /* Header */
    .dashboard-title {{
        font-size: 28px;
        font-weight: 800;
        letter-spacing: 0.6px;
        margin: 0;
        color: {PALETTE['text_light']};
    }}
    .dashboard-subtitle {{
        font-size: 13px;
        color: {PALETTE['text_dim']};
        margin-top: 4px;
        margin-bottom: 8px;
    }}

    /* Metric cards */
    .kpi-card {{
        border-radius: 12px;
        padding: 14px;
        transition: transform 0.18s ease, box-shadow 0.18s ease;
        background: rgba(255,255,255,0.02);
        border: 1px solid {PALETTE['card_border']};
        box-shadow: 0 6px 20px rgba(2,6,23,0.35);
        min-height: 88px;
    }}
    .kpi-card:hover {{
        transform: translateY(-6px);
        box-shadow: 0 12px 30px rgba(2,6,23,0.45);
    }}
    .kpi-title {{ font-size:12px; color:{PALETTE['muted']}; font-weight:700; letter-spacing:0.6px; }}
    .kpi-value {{ font-size:26px; font-weight:800; margin-top:6px; color:{PALETTE['text_light']}; }}
    .kpi-delta {{ font-size:13px; margin-top:6px; font-weight:700; }}

    /* Card container for summaries */
    .card-container {{
        border-radius: 12px;
        padding: 16px;
        background: rgba(255,255,255,0.015);
        border: 1px solid {PALETTE['card_border']};
        box-shadow: 0 6px 24px rgba(2,6,23,0.35);
    }}

    /* Sidebar tweaks */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, rgba(34,48,70,0.95) 0%, rgba(17,18,24,0.95) 100%);
        color: {PALETTE['text_light']} !important;
    }}
    [data-testid="stSidebar"] .stButton>button {{
        background: linear-gradient(90deg, {PALETTE['accent_alt']}, {PALETTE['accent']});
        color: #fff;
        border-radius: 8px;
    }}

    /* Tabs styling */
    .stTabs [role="tablist"] > button {{
        border-radius: 10px;
        background: rgba(255,255,255,0.02);
        color: {PALETTE['text_dim']};
        border: 1px solid rgba(255,255,255,0.03);
        padding: 8px 14px;
        font-weight:700;
    }}
    .stTabs [role="tablist"] > button[aria-selected="true"] {{
        background: linear-gradient(90deg, rgba(46,204,113,0.12), rgba(30,144,255,0.08));
        color: {PALETTE['text_light']};
        box-shadow: 0 8px 24px rgba(2,6,23,0.45);
    }}

    /* Dataframe */
    [data-testid="stDataFrame"] {{
        border-radius: 10px;
        overflow: hidden;
    }}

    /* Small responsive tweaks */
    @media (max-width: 640px) {{
        .dashboard-title {{ font-size: 20px; }}
        .kpi-value {{ font-size:20px; }}
        .kpi-card {{ padding: 10px; min-height:72px; }}
    }}

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


inject_css()

# -----------------------
# Utility: Plotly theme function
# -----------------------
def apply_plotly_theme(fig: go.Figure, title: str = "") -> go.Figure:
    fig.update_layout(
        title=dict(text=title, x=0.5, xanchor="center", font=dict(size=18, color=PALETTE["text_light"])),
        font=dict(color=PALETTE["text_light"], family="Inter"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=30, t=60, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.04)", tickfont=dict(color=PALETTE["text_light"]))
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.04)", tickfont=dict(color=PALETTE["text_light"]))
    return fig

# -----------------------
# Data loading with fallback
# -----------------------
@st.cache_data(ttl=3600)
def load_data(parquet_path: str = "data/processed/ecommerce_dataset_10000_cleaned.parquet",
              csv_path: str = "data/processed/ecommerce_dataset_10000_cleaned.csv") -> Optional[pd.DataFrame]:
    if os.path.exists(parquet_path):
        df = pd.read_parquet(parquet_path)
    elif os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        return None

    # Normalize & safe defaults
    for col in ["country", "order_date", "customer_id", "product_name", "quantity", "unit_price", "total_price"]:
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
    # if total_price missing, compute it
    df["total_price"] = pd.to_numeric(df.get("total_price", df["unit_price"] * df["quantity"]), errors="coerce")
    df["country"] = df["country"].astype(str).str.strip()
    df["customer_id"] = df["customer_id"].astype(str).str.strip()
    df["product_name"] = df["product_name"].astype(str).str.strip()
    df["year_month"] = df["order_date"].dt.to_period("M").dt.to_timestamp()
    df["day_of_week"] = df["order_date"].dt.day_name()
    return df

df = load_data()
if df is None or df.empty:
    st.error("❌ Dataset not found or dataset is empty. Place the processed parquet/csv in data/processed/")
    st.stop()

# -----------------------
# Sidebar controls (theme toggle kept implicit)
# -----------------------
with st.sidebar:
    st.header("Controls")
    min_date = df["order_date"].min().date()
    max_date = df["order_date"].max().date()
    start_date = st.date_input("From", min_value=min_date, value=min_date, max_value=max_date)
    end_date = st.date_input("To", min_value=min_date, value=max_date, max_value=max_date)
    countries = sorted(df["country"].dropna().unique().tolist())
    selected = st.multiselect("Countries", options=countries, default=countries[:6] if len(countries) > 6 else countries)
    top_n = st.slider("Top N", min_value=5, max_value=50, value=10, step=5)
    st.markdown("---")
    st.markdown("**Export / debug**")
    if st.button("Download sample CSV"):
        st.download_button("Download sample", df.head(100).to_csv(index=False).encode("utf-8"), file_name="sample.csv")

# -----------------------
# Filter data safely
# -----------------------
start_ts = pd.to_datetime(start_date)
end_ts = pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

if not selected:
    st.warning("Select at least one country.")
    st.stop()

df_filtered = df[
    (df["order_date"] >= start_ts)
    & (df["order_date"] <= end_ts)
    & (df["country"].isin(selected))
].copy()

if df_filtered.empty:
    st.warning("No data for selected filters. Try expanding the date range or countries.")
    st.stop()

# -----------------------
# Metrics calculation
# -----------------------
def safe_order_count(d: pd.DataFrame) -> int:
    return int(d["order_id"].nunique()) if "order_id" in d.columns else int(len(d))

def compute_metrics(curr: pd.DataFrame, all_df: pd.DataFrame) -> Dict[str, float]:
    total_revenue = float(curr["total_price"].sum())
    total_orders = safe_order_count(curr)
    unique_customers = int(curr["customer_id"].nunique())
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0.0
    countries_active = int(curr["country"].nunique())
    total_quantity = int(curr["quantity"].sum())

    # previous period (same number of days)
    period_days = max(1, (curr["order_date"].max() - curr["order_date"].min()).days)
    prev_start = curr["order_date"].min() - pd.Timedelta(days=period_days)
    prev_end = curr["order_date"].min() - pd.Timedelta(seconds=1)
    prev_df = all_df[(all_df["order_date"] >= prev_start) & (all_df["order_date"] <= prev_end)]

    prev_revenue = float(prev_df["total_price"].sum()) if not prev_df.empty else 0.0
    prev_orders = safe_order_count(prev_df) if not prev_df.empty else 0
    prev_customers = int(prev_df["customer_id"].nunique()) if not prev_df.empty else 0

    def pct(curr_v, prev_v):
        return (curr_v - prev_v) / prev_v * 100.0 if prev_v and prev_v != 0 else 0.0

    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "unique_customers": unique_customers,
        "avg_order_value": avg_order_value,
        "countries_active": countries_active,
        "total_quantity": total_quantity,
        "prev_revenue": prev_revenue,
        "revenue_delta_pct": pct(total_revenue, prev_revenue),
        "orders_delta_pct": pct(total_orders, prev_orders),
        "customers_delta_pct": pct(unique_customers, prev_customers),
    }

metrics = compute_metrics(df_filtered, df)

# -----------------------
# Header (clean)
# -----------------------
st.markdown(
    f"""
    <div style='display:flex;flex-direction:column;align-items:center;gap:6px;margin-bottom:8px;'>
        <div class="dashboard-title">📊 Executive E-commerce Dashboard</div>
        <div class="dashboard-subtitle">Clean, legible & mobile-friendly — designed for recruiters</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------
# KPI cards (Power-BI style, responsive)
# -----------------------
st.markdown("### Key Performance Indicators")
cols = st.columns([2, 1, 1, 1, 1], gap="large")

# Card helper
def kpi_card(col, title: str, value_html: str, delta_html: str = ""):
    with col:
        st.markdown(f"<div class='kpi-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='kpi-title'>{title}</div>", unsafe_allow_html=True)
        st.markdown(value_html, unsafe_allow_html=True)
        if delta_html:
            st.markdown(delta_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Metrics HTML
rev = metrics["total_revenue"]
rev_delta = metrics["revenue_delta_pct"]
rev_delta_col = PALETTE["accent"] if rev_delta >= 0 else "#FF6B6B"

kpi_card(
    cols[0],
    "TOTAL REVENUE",
    f"<div class='kpi-value' style='color:{PALETTE['accent']};'>${rev:,.0f}</div>",
    f"<div class='kpi-delta' style='color:{rev_delta_col};'>{rev_delta:+.1f}% vs prev</div>"
)

orders = metrics["total_orders"]
orders_delta = metrics["orders_delta_pct"]
ord_col = PALETTE["accent"] if orders_delta >= 0 else "#FF6B6B"
kpi_card(
    cols[1],
    "TOTAL ORDERS",
    f"<div class='kpi-value'>{orders:,}</div>",
    f"<div class='kpi-delta' style='color:{ord_col};'>{orders_delta:+.1f}%</div>"
)

kpi_card(cols[2], "AVG ORDER VALUE", f"<div class='kpi-value'>${metrics['avg_order_value']:,.2f}</div>")
kpi_card(cols[3], "UNIQUE CUSTOMERS", f"<div class='kpi-value'>{metrics['unique_customers']:,}</div>")
kpi_card(cols[4], "COUNTRIES ACTIVE", f"<div class='kpi-value'>{metrics['countries_active']:,}</div>")

st.markdown("---")

# -----------------------
# TAB layout for charts
# -----------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Revenue", "Customers", "Products", "Geography", "Advanced"
])

# TAB: Revenue
with tab1:
    left, right = st.columns([2, 1])
    with left:
        st.subheader("Monthly Revenue")
        monthly = df_filtered.groupby(df_filtered["order_date"].dt.to_period("M"))["total_price"].sum().reset_index()
        monthly["order_date"] = monthly["order_date"].dt.to_timestamp()
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=monthly["order_date"],
            y=monthly["total_price"],
            marker_color=PALETTE["accent_alt"],
            text=[f"${v:,.0f}" for v in monthly["total_price"]],
            textposition="outside",
            hovertemplate="%{x|%b %Y}<br>Revenue: %{y:$,.0f}<extra></extra>"
        ))
        apply_plotly_theme(fig, "Monthly Revenue")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Top Countries by Revenue")
        ctop = df_filtered.groupby("country")["total_price"].sum().nlargest(6).reset_index()
        figc = px.pie(ctop, values="total_price", names="country", hole=0.45,
                      color_discrete_sequence=[PALETTE["accent"], PALETTE["accent_alt"], PALETTE["gold"], "#8E44AD", "#3498DB", "#95A5A6"])
        figc.update_traces(textinfo="percent+label", textposition="inside")
        apply_plotly_theme(figc, "Top Countries")
        st.plotly_chart(figc, use_container_width=True)

# TAB: Customers
with tab2:
    st.subheader(f"Top {top_n} Customers by Revenue")
    top_cust = df_filtered.groupby("customer_id").agg(total_revenue=("total_price", "sum")).nlargest(top_n, "total_revenue").reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=top_cust["total_revenue"],
        y=top_cust["customer_id"],
        orientation="h",
        marker_color=PALETTE["accent"],
        text=[f"${v:,.0f}" for v in top_cust["total_revenue"]],
        textposition="outside",
        hovertemplate="%{y}<br>Revenue: %{x:$,.0f}<extra></extra>"
    ))
    apply_plotly_theme(fig, f"Top {top_n} Customers")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Customer Segmentation (RFM sample)")
    snapshot = df_filtered["order_date"].max() + timedelta(days=1)
    rfm = df_filtered.groupby("customer_id").agg(
        recency=("order_date", lambda x: (snapshot - x.max()).days),
        frequency=("order_id", "nunique") if "order_id" in df_filtered.columns else ("order_id", lambda x: len(x)),
        monetary=("total_price", "sum")
    ).reset_index()
    # safe rename if needed
    if rfm.shape[1] == 4:
        rfm.columns = ["customer_id", "recency", "frequency", "monetary"]
    rfm_sample = rfm.sort_values("monetary", ascending=False).head(10)
    st.dataframe(rfm_sample, use_container_width=True)

# TAB: Products
with tab3:
    st.subheader(f"Top {top_n} Products by Revenue")
    top_prod = df_filtered.groupby("product_name").agg(total_revenue=("total_price", "sum"), qty=("quantity", "sum")).nlargest(top_n, "total_revenue").reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=top_prod["total_revenue"],
        y=top_prod["product_name"],
        orientation="h",
        marker_color=PALETTE["accent_alt"],
        text=[f"${v:,.0f}" for v in top_prod["total_revenue"]],
        textposition="outside",
        hovertemplate="%{y}<br>Revenue: %{x:$,.0f}<extra></extra>"
    ))
    apply_plotly_theme(fig, "Product Revenue Leaders")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Price Distribution")
    figp = go.Figure()
    figp.add_trace(go.Histogram(x=df_filtered["unit_price"], nbinsx=40, marker_color=PALETTE["gold"], opacity=0.9))
    apply_plotly_theme(figp, "Unit Price Distribution")
    st.plotly_chart(figp, use_container_width=True)

# TAB: Geography
with tab4:
    st.subheader("Revenue by Country (detailed)")
    country_df = df_filtered.groupby("country").agg(revenue=("total_price", "sum"), orders=("order_id", "nunique") if "order_id" in df_filtered.columns else ("order_id", "size"), customers=("customer_id", "nunique")).reset_index()
    country_df = country_df.sort_values("revenue", ascending=False)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=country_df["country"],
        y=country_df["revenue"],
        marker=dict(color=country_df["revenue"], colorscale="Blues"),
        text=[f"${v:,.0f}" for v in country_df["revenue"]],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Revenue: %{y:$,.0f}<extra></extra>"
    ))
    apply_plotly_theme(fig, "Global Revenue Distribution")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(country_df, use_container_width=True)

# TAB: Advanced
with tab5:
    st.subheader("Advanced Analytics")
    # Pareto: top products cumulative
    prod_rev = df_filtered.groupby("product_name")["total_price"].sum().reset_index().sort_values("total_price", ascending=False)
    prod_rev["cum_pct"] = prod_rev["total_price"].cumsum() / prod_rev["total_price"].sum() * 100
    pareto = prod_rev.head(20)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=list(range(len(pareto))), y=pareto["total_price"], name="Revenue", marker_color=PALETTE["accent_alt"]))
    fig.add_trace(go.Scatter(x=list(range(len(pareto))), y=pareto["cum_pct"], name="Cumulative %", yaxis="y2", marker_color=PALETTE["accent"]))
    fig.update_layout(yaxis2=dict(overlaying="y", side="right", range=[0, 100]))
    apply_plotly_theme(fig, "Pareto: Revenue Concentration (Top 20)")
    st.plotly_chart(fig, use_container_width=True)

# -----------------------
# Export / footer
# -----------------------
st.markdown("---")
cols = st.columns(4)
with cols[0]:
    st.download_button("Download filtered CSV", df_filtered.to_csv(index=False).encode("utf-8"), file_name=f"filtered_{datetime.now().strftime('%Y%m%d_%H%M')}.csv")
with cols[1]:
    st.download_button("Top customers CSV", top_cust.to_csv(index=False).encode("utf-8"), file_name="top_customers.csv")
with cols[2]:
    st.download_button("Top products CSV", top_prod.to_csv(index=False).encode("utf-8"), file_name="top_products.csv")
with cols[3]:
    st.write("")  # placeholder

st.markdown(
    f"<div style='text-align:center;color:{PALETTE['muted']};font-size:12px;margin-top:8px;'>Dashboard · Built with Streamlit · Last updated: {datetime.now().strftime('%b %d, %Y %H:%M')}</div>",
    unsafe_allow_html=True
)
