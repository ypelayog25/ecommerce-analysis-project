# scripts/app.py
"""
Power-BI style Executive E-commerce Dashboard (Streamlit)
Clean, professional, white theme, KPI cards with sparklines and delta indicators.
"""

from __future__ import annotations
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# -----------------------
# Page config
# -----------------------
st.set_page_config(
    page_title="Executive E-commerce Dashboard (Power BI style)",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊",
)

# -----------------------
# Constants & Colors (Power BI-ish)
# -----------------------
REQUIRED_COLUMNS = [
    "order_date",
    "customer_id",
    "country",
    "product_name",
    "quantity",
    "unit_price",
    "total_price",
]
ACCENT = "#0078D4"  # Power BI blue-ish accent
ACCENT_DARK = "#005A9E"
POS_GREEN = "#1E8E3E"
NEG_RED = "#D9534F"
CARD_BG = "#ffffff"
TEXT = "#111827"

# -----------------------
# Helpers
# -----------------------
def format_currency(v: float, decimals: int = 0) -> str:
    return f"${v:,.{decimals}f}"

def pct_change_display(curr: float, prev: float) -> Tuple[str, str]:
    """Return (formatted_delta, color)"""
    if prev == 0:
        return ("—", TEXT)
    delta = (curr - prev) / prev * 100.0
    color = POS_GREEN if delta >= 0 else NEG_RED
    sign = "+" if delta >= 0 else ""
    return (f"{sign}{delta:.1f}%", color)

def safe_head_record(df: pd.DataFrame, idx: int = 0) -> dict:
    return df.iloc[idx].to_dict() if not df.empty else {}

# -----------------------
# Data loading & preprocessing
# -----------------------
@st.cache_data(ttl=3600)
def load_data(parquet_path: str, csv_path: str) -> Optional[pd.DataFrame]:
    if os.path.exists(parquet_path):
        df = pd.read_parquet(parquet_path)
    elif os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        return None

    # Ensure minimal schema: if missing critical columns, warning upstream, but proceed gracefully
    present = [c for c in REQUIRED_COLUMNS if c in df.columns]
    if len(present) < len(REQUIRED_COLUMNS):
        # don't crash: fill missing numeric with zeros / strings with "N/A"
        for c in REQUIRED_COLUMNS:
            if c not in df.columns:
                if c in ("quantity", "unit_price", "total_price"):
                    df[c] = 0
                else:
                    df[c] = "N/A"

    # Parse order_date
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df = df.dropna(subset=["order_date"])
    # Ensure numeric
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce").fillna(0.0)
    df["total_price"] = pd.to_numeric(df["total_price"], errors="coerce").fillna(df["unit_price"] * df["quantity"])
    # Normalize strings
    for s in ["country", "product_name", "customer_id"]:
        if s in df.columns:
            df[s] = df[s].astype(str).str.strip()
    # Derived
    df["year_month"] = df["order_date"].dt.to_period("M").dt.to_timestamp()
    df["day_name"] = df["order_date"].dt.day_name()
    return df

# -----------------------
# Filter function
# -----------------------
@st.cache_data
def filter_df(df: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp, countries: List[str]) -> pd.DataFrame:
    mask = (df["order_date"] >= start) & (df["order_date"] <= end)
    if countries:
        mask &= df["country"].isin(countries)
    return df.loc[mask].copy()

# -----------------------
# Metrics calculation
# -----------------------
def compute_metrics(df_filtered: pd.DataFrame, df_all: pd.DataFrame) -> Dict[str, float]:
    total_revenue = float(df_filtered["total_price"].sum())
    total_orders = int(df_filtered.shape[0])  # assume each row is an order line; if order_id present, change logic
    unique_customers = int(df_filtered["customer_id"].nunique())
    total_quantity = int(df_filtered["quantity"].sum())
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0.0

    # previous period: same length immediately before start
    if df_filtered.empty:
        prev_revenue = prev_orders = prev_customers = 0.0
    else:
        period_days = (df_filtered["order_date"].max() - df_filtered["order_date"].min()).days or 1
        prev_start = df_filtered["order_date"].min() - pd.Timedelta(days=period_days)
        prev_end = df_filtered["order_date"].min() - pd.Timedelta(seconds=1)
        prev = df_all[(df_all["order_date"] >= prev_start) & (df_all["order_date"] <= prev_end)]
        prev_revenue = float(prev["total_price"].sum())
        prev_orders = int(prev.shape[0])
        prev_customers = int(prev["customer_id"].nunique())

    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "unique_customers": unique_customers,
        "total_quantity": total_quantity,
        "avg_order_value": avg_order_value,
        "prev_revenue": prev_revenue,
        "prev_orders": prev_orders,
        "prev_customers": prev_customers,
    }

# -----------------------
# Plot helpers (Power BI style)
# -----------------------
def style_chart(fig: go.Figure, title: str) -> go.Figure:
    fig.update_layout(
        title=dict(text=title, x=0.5, xanchor="center", font=dict(size=18, color=TEXT)),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=TEXT),
        margin=dict(l=40, r=20, t=60, b=40),
        hovermode="x unified",
    )
    fig.update_xaxes(showgrid=True, gridcolor="#f3f4f6")
    fig.update_yaxes(showgrid=True, gridcolor="#f3f4f6")
    return fig

def sparkline(values: List[float], color: str = ACCENT) -> go.Figure:
    fig = go.Figure(go.Scatter(x=list(range(len(values))), y=values, mode="lines", line=dict(color=color, width=2), fill="tozeroy", fillcolor=color, marker=dict(size=0)))
    fig.update_layout(margin=dict(l=0,r=0,t=0,b=0), height=48, xaxis_visible=False, yaxis_visible=False, plot_bgcolor="white", paper_bgcolor="white")
    return fig

# -----------------------
# Main app
# -----------------------
def main():
    st.title("📊 Executive E-commerce Dashboard — Power BI style")
    st.markdown("**Clean visuals • white background • crisp typography • actionable KPIs**")

    # Sidebar controls
    with st.sidebar:
        st.header("Controls")
        parquet_path = st.text_input("Parquet path", "data/processed/ecommerce_dataset_10000_cleaned.parquet")
        csv_path = st.text_input("CSV fallback", "data/processed/ecommerce_dataset_10000_cleaned.csv")
        df_all = load_data(parquet_path, csv_path)
        if df_all is None or df_all.empty:
            st.error("No data found (check paths).")
            st.stop()

        # Date range
        min_date = df_all["order_date"].min().date()
        max_date = df_all["order_date"].max().date()
        start_date = st.date_input("From", min_date, min_value=min_date, max_value=max_date)
        end_date = st.date_input("To", max_date, min_value=min_date, max_value=max_date)
        # convert to timestamps (inclusive)
        start_ts = pd.to_datetime(start_date)
        end_ts = pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

        # Country filter
        countries = sorted(df_all["country"].dropna().unique())
        selected_countries = st.multiselect("Countries", countries, default=countries)

        # Top N
        top_n = st.slider("Top N", min_value=5, max_value=50, value=10)

        # Toggle options
        show_table = st.checkbox("Show country details table", value=False)
        st.markdown("---")

    # Filter data
    df = filter_df(df_all, start_ts, end_ts, selected_countries)
    if df.empty:
        st.warning("No data for selected filters.")
        st.stop()

    # Metrics
    metrics = compute_metrics(df, df_all)
    rev_delta_text, rev_color = pct_change_display(metrics["total_revenue"], metrics["prev_revenue"])
    ord_delta_text, ord_color = pct_change_display(metrics["total_orders"], metrics["prev_orders"])
    cust_delta_text, cust_color = pct_change_display(metrics["unique_customers"], metrics["prev_customers"])

    # KPI row (cards)
    c1, c2, c3, c4, c5 = st.columns([2,1,1,1,1])
    # Sparkline data for revenue last months
    monthly_rev = df.groupby(df["year_month"])["total_price"].sum().sort_index()
    spark_vals = monthly_rev.tail(12).fillna(0).tolist() if not monthly_rev.empty else [0]

    with c1:
        # big card with sparkline and delta
        st.markdown(f"""
        <div style="background:{CARD_BG}; padding:14px; border-radius:12px; box-shadow: 0 2px 6px rgba(17,24,39,0.06);">
            <div style="font-size:13px; color:#6b7280; font-weight:600;">Total Revenue</div>
            <div style="font-size:28px; color:{ACCENT}; font-weight:700;">{format_currency(metrics['total_revenue'],0)}</div>
            <div style="font-size:13px; margin-top:6px; color:{rev_color}; font-weight:600;">{rev_delta_text} vs prev</div>
        </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(sparkline(spark_vals, ACCENT), use_container_width=True)

    with c2:
        st.metric("Orders", f"{metrics['total_orders']:,}", ord_delta_text)

    with c3:
        st.metric("Customers", f"{metrics['unique_customers']:,}", cust_delta_text)

    with c4:
        st.metric("Units Sold", f"{metrics['total_quantity']:,}")

    with c5:
        st.metric("Avg Order Value", format_currency(metrics["avg_order_value"],0))

    st.markdown("---")

    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Revenue", "Customers", "Products", "Geo"])

    with tab1:
        # Revenue trend and growth
        left, right = st.columns([2,1])
        with left:
            st.subheader("Revenue Trend")
            # Plot revenue trend
            monthly = df.groupby(df["year_month"])["total_price"].sum().reset_index()
            monthly["year_month"] = monthly["year_month"].dt.to_timestamp()
            fig = go.Figure()
            fig.add_trace(go.Bar(x=monthly["year_month"], y=monthly["total_price"], marker_color=ACCENT, name="Revenue"))
            fig.add_trace(go.Scatter(x=monthly["year_month"], y=monthly["total_price"].rolling(3, min_periods=1).mean(), mode="lines", line=dict(color=ACCENT_DARK, width=3), name="3-mo MA"))
            fig = style_chart(fig, "Monthly Revenue")
            st.plotly_chart(fig, use_container_width=True)
        with right:
            st.subheader("Top Countries (by revenue)")
            country_rev = df.groupby("country")["total_price"].sum().sort_values(ascending=False).reset_index()
            top_c = country_rev.head(top_n)
            fig_c = go.Figure(go.Bar(x=top_c["total_price"], y=top_c["country"], orientation="h", marker_color=px.colors.sequential.Blues[:len(top_c)]))
            fig_c = style_chart(fig_c, "Top Countries")
            st.plotly_chart(fig_c, use_container_width=True)

        st.subheader("Day-of-week Revenue Pattern")
        dow = df.groupby("day_name")["total_price"].sum().reindex(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]).reset_index()
        fig_dow = go.Figure(go.Bar(x=dow["day_name"], y=dow["total_price"], marker_color=ACCENT))
        fig_dow = style_chart(fig_dow, "Revenue by Day of Week")
        st.plotly_chart(fig_dow, use_container_width=True)

    with tab2:
        st.subheader(f"Top {top_n} Customers by Revenue")
        top_customers = df.groupby("customer_id")["total_price"].sum().nlargest(top_n).reset_index()
        fig_tc = go.Figure(go.Bar(x=top_customers["total_price"], y=top_customers["customer_id"], orientation="h", marker_color=px.colors.sequential.Plasma))
        fig_tc = style_chart(fig_tc, "Top Customers")
        st.plotly_chart(fig_tc, use_container_width=True)

        st.markdown("Customer Frequency Distribution")
        freq = df.groupby("customer_id")["order_date"].nunique().value_counts().sort_index().reset_index()
        freq.columns = ["orders", "customers"]
        fig_freq = go.Figure(go.Bar(x=freq["orders"], y=freq["customers"], marker_color=ACCENT))
        fig_freq = style_chart(fig_freq, "Order Frequency")
        st.plotly_chart(fig_freq, use_container_width=True)

    with tab3:
        st.subheader(f"Top {top_n} Products (Revenue & Volume)")
        prod_rev = df.groupby("product_name").agg(total_price=("total_price","sum"), quantity=("quantity","sum")).reset_index()
        top_prod = prod_rev.sort_values("total_price", ascending=False).head(top_n)
        fig_pr = go.Figure(go.Bar(x=top_prod["total_price"], y=top_prod["product_name"], orientation="h", marker_color=px.colors.sequential.Teal))
        fig_pr = style_chart(fig_pr, "Top Products by Revenue")
        st.plotly_chart(fig_pr, use_container_width=True)

        st.subheader("Price distribution")
        fig_price = go.Figure()
        fig_price.add_trace(go.Histogram(x=df["unit_price"], nbinsx=50, marker_color=ACCENT))
        fig_price = style_chart(fig_price, "Unit Price Distribution")
        st.plotly_chart(fig_price, use_container_width=True)

    with tab4:
        st.subheader("Geo Insights")
        country_analysis = df.groupby("country").agg(revenue=("total_price","sum"), orders=("order_date","count")).reset_index().sort_values("revenue", ascending=False)
        fig_geo = go.Figure(go.Bar(x=country_analysis["country"], y=country_analysis["revenue"], marker_color=ACCENT))
        fig_geo = style_chart(fig_geo, "Revenue by Country")
        st.plotly_chart(fig_geo, use_container_width=True)

        if show_table:
            display = country_analysis.copy()
            display["revenue"] = display["revenue"].apply(lambda x: format_currency(x,0))
            st.dataframe(display, use_container_width=True)

    # Executive summary (safe extraction of top country & best product)
    st.markdown("---")
    st.subheader("Executive Summary")
    country_analysis = df.groupby("country").agg(revenue=("total_price","sum")).reset_index().sort_values("revenue", ascending=False)
    top_country = country_analysis.iloc[0].to_dict() if not country_analysis.empty else {"country":"N/A","revenue":0}
    product_analysis = df.groupby("product_name").agg(revenue=("total_price","sum")).reset_index().sort_values("revenue", ascending=False)
    best_product = product_analysis.iloc[0].to_dict() if not product_analysis.empty else {"product_name":"N/A","revenue":0}

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Top Country", top_country.get("country","N/A"), format_currency(top_country.get("revenue",0),0))
    with c2:
        name = best_product.get("product_name","N/A")
        st.metric("Best Product", name if len(name)<=24 else name[:21]+"…", format_currency(best_product.get("revenue",0),0))
    with c3:
        # VIP estimate using top 5% customers by revenue
        cust_rev = df.groupby("customer_id")["total_price"].sum().reset_index().sort_values("total_price", ascending=False)
        vip_count = int(max(0, round(len(cust_rev) * 0.05)))
        st.metric("Est. VIPs (top 5%)", f"{vip_count}")
    with c4:
        # avg monthly growth
        monthly = df.groupby(df["year_month"])["total_price"].sum().reset_index()
        if len(monthly) > 1:
            monthly["pct"] = monthly["total_price"].pct_change() * 100
            avg_growth = monthly["pct"].mean()
        else:
            avg_growth = 0.0
        st.metric("Avg MoM Growth", f"{avg_growth:.1f}%")

    # Export
    st.markdown("---")
    st.subheader("Export data")
    now = datetime.now().strftime("%Y%m%d_%H%M")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("Download filtered CSV", df.to_csv(index=False).encode("utf-8"), file_name=f"filtered_{now}.csv")
    with c2:
        top_customers_csv = df.groupby("customer_id").agg(total_revenue=("total_price","sum")).sort_values("total_revenue", ascending=False).head(top_n).reset_index()
        st.download_button("Download top customers CSV", top_customers_csv.to_csv(index=False).encode("utf-8"), file_name=f"top_customers_{now}.csv")

    # Footer
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.caption("Built with Streamlit • Design inspired by Power BI — Clean & Corporate")

if __name__ == "__main__":
    main()
