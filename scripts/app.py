# app.py
from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# =========================
# Configuración de página
# =========================
st.set_page_config(
    page_title="Executive E-commerce Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊",
)

# =========================
# Constantes y Paletas
# =========================
REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "customer_id",
    "country",
    "product_name",
    "quantity",
    "unit_price",
    "total_price",
]
NEON_COLORS = ["#00ff87", "#60efff", "#ff006e", "#ffbe0b", "#8338ec"]
DOW_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTH_ABBR = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


# =========================
# Estilos (CSS Opcional)
# =========================
def inject_css() -> None:
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    * { font-family: 'Inter', sans-serif; }
    h1, h2, h3 { font-weight: 800 !important; }
    [data-testid="stMetricValue"] {
        font-size: 32px !important; font-weight: 800 !important; color: #00ff87 !important;
        text-shadow: 0 0 12px rgba(0,255,135,0.35);
    }
    [data-testid="stMetricLabel"] {
        font-size: 12px !important; font-weight: 600 !important; color: #a8b2d1 !important;
        text-transform: uppercase; letter-spacing: 1.2px;
    }
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #2b2d42 0%, #1a1b2e 100%);
        padding: 18px; border-radius: 14px; border: 1px solid rgba(255,255,255,0.08);
    }
    .card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px; padding: 20px; backdrop-filter: blur(6px);
    }
    .hero-title {
        background: linear-gradient(135deg, #00ff87 0%, #60efff 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; margin: 0;
    }
    hr { border-color: rgba(255,255,255,0.12); margin: 18px 0; }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# =========================
# Utilidades
# =========================
def ensure_schema(df: pd.DataFrame, required_cols: List[str]) -> Tuple[bool, List[str]]:
    """Valida que el DataFrame contenga las columnas requeridas."""
    missing = [c for c in required_cols if c not in df.columns]
    return (len(missing) == 0, missing)


def format_currency(value: float, decimals: int = 2) -> str:
    return f"${value:,.{decimals}f}"


def style_fig(fig: go.Figure, title: str = "", theme: str = "dark") -> go.Figure:
    """Aplica estilo consistente a figuras Plotly con soporte dark/light."""
    template = "plotly_dark" if theme == "dark" else "plotly_white"
    txt = "#e0e0e0" if theme == "dark" else "#1f2a37"
    grid = "rgba(255,255,255,0.12)" if theme == "dark" else "rgba(0,0,0,0.08)"

    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20, color="#00ff87", family="Inter"),
            x=0.5, xanchor="center",
        ),
        font=dict(size=12, color=txt, family="Inter"),
        margin=dict(l=40, r=30, t=60, b=40),
        template=template,
        hovermode="x unified",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor=grid, zeroline=False)
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor=grid, zeroline=False)
    return fig


# =========================
# Carga y preparación de datos
# =========================
@st.cache_data(ttl=3600)
def load_data(dataset_parquet: str, dataset_csv: str) -> Optional[pd.DataFrame]:
    """Carga el dataset con fallback parquet/csv y preprocesa columnas de fecha."""
    try:
        if os.path.exists(dataset_parquet):
            df = pd.read_parquet(dataset_parquet)
        elif os.path.exists(dataset_csv):
            df = pd.read_csv(dataset_csv)
        else:
            return None

        ok, missing = ensure_schema(df, REQUIRED_COLUMNS)
        if not ok:
            st.error(f"Faltan columnas requeridas: {missing}. Revisa el esquema del dataset.")
            return None

        # Tipos y columnas temporales
        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
        df = df.dropna(subset=["order_date"])
        df["year_month"] = df["order_date"].dt.to_period("M")
        df["year"] = df["order_date"].dt.year
        df["month"] = df["order_date"].dt.month
        df["day_of_week"] = df["order_date"].dt.day_name()

        # Asegurar numéricos
        for col in ["quantity", "unit_price", "total_price"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        # Normalizar strings
        for col in ["country", "product_name"]:
            df[col] = df[col].astype(str).str.strip()

        return df
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return None


@st.cache_data(show_spinner=False)
def filter_data(
    df: pd.DataFrame,
    start_dt: pd.Timestamp,
    end_dt: pd.Timestamp,
    countries: List[str],
) -> pd.DataFrame:
    """Filtra datos por rango de fechas y países."""
    mask = (
        (df["order_date"] >= start_dt)
        & (df["order_date"] <= end_dt)
        & (df["country"].isin(countries))
    )
    return df.loc[mask].copy()


@st.cache_data(show_spinner=False)
def calculate_metrics(df_current: pd.DataFrame, df_all: pd.DataFrame) -> Dict[str, float]:
    """Calcula KPIs y deltas period-over-period."""
    total_revenue = df_current["total_price"].sum()
    total_orders = df_current["order_id"].nunique()
    unique_customers = df_current["customer_id"].nunique()
    total_quantity = df_current["quantity"].sum()
    avg_order_value = float(total_revenue / total_orders) if total_orders > 0 else 0.0

    if df_current.empty:
        return {
            "total_revenue": 0.0,
            "total_orders": 0,
            "unique_customers": 0,
            "total_quantity": 0,
            "avg_order_value": 0.0,
            "revenue_delta": 0.0,
            "orders_delta": 0.0,
            "customers_delta": 0.0,
        }

    date_diff = (df_current["order_date"].max() - df_current["order_date"].min()).days
    date_diff = max(date_diff, 1)  # evitar 0
    prev_start = df_current["order_date"].min() - timedelta(days=date_diff)
    prev_end = df_current["order_date"].min()

    df_prev = df_all[(df_all["order_date"] >= prev_start) & (df_all["order_date"] < prev_end)]

    prev_revenue = df_prev["total_price"].sum()
    prev_orders = df_prev["order_id"].nunique()
    prev_customers = df_prev["customer_id"].nunique()

    def pct_delta(curr: float, prev: float) -> float:
        return float(((curr - prev) / prev) * 100) if prev > 0 else 0.0

    return {
        "total_revenue": float(total_revenue),
        "total_orders": int(total_orders),
        "unique_customers": int(unique_customers),
        "total_quantity": int(total_quantity),
        "avg_order_value": float(avg_order_value),
        "revenue_delta": pct_delta(total_revenue, prev_revenue),
        "orders_delta": pct_delta(total_orders, prev_orders),
        "customers_delta": pct_delta(unique_customers, prev_customers),
    }


# =========================
# Gráficos
# =========================
def plot_revenue_trend(df_filtered: pd.DataFrame, theme: str) -> go.Figure:
    monthly = (
        df_filtered.groupby(df_filtered["order_date"].dt.to_period("M"))["total_price"]
        .sum()
        .reset_index()
    )
    monthly["order_date"] = monthly["order_date"].dt.to_timestamp()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=monthly["order_date"],
            y=monthly["total_price"],
            mode="lines+markers",
            name="Revenue",
            line=dict(color="#00ff87", width=3),
            marker=dict(size=8, color="#00ff87"),
            fill="tozeroy",
            fillcolor="rgba(0,255,135,0.18)",
        )
    )
    # Tendencia lineal simple
    if len(monthly) >= 2:
        z = np.polyfit(np.arange(len(monthly)), monthly["total_price"].values, 1)
        p = np.poly1d(z)
        fig.add_trace(
            go.Scatter(
                x=monthly["order_date"],
                y=p(np.arange(len(monthly))),
                mode="lines",
                name="Trend",
                line=dict(color="#ff006e", width=2, dash="dash"),
            )
        )
    return style_fig(fig, "Monthly Revenue Performance", theme)


def plot_top_countries_pie(df_filtered: pd.DataFrame, theme: str, top: int = 5) -> go.Figure:
    country_rev = (
        df_filtered.groupby("country")["total_price"].sum().nlargest(top).reset_index()
    )
    fig = px.pie(
        country_rev,
        values="total_price",
        names="country",
        hole=0.5,
        color_discrete_sequence=NEON_COLORS,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return style_fig(fig, "Top Countries by Revenue", theme)


def plot_dow_revenue(df_filtered: pd.DataFrame, theme: str) -> go.Figure:
    dow = (
        df_filtered.groupby("day_of_week")["total_price"].sum().reindex(DOW_ORDER).reset_index()
    )
    fig = go.Figure(
        data=[
            go.Bar(
                x=dow["day_of_week"],
                y=dow["total_price"],
                marker=dict(
                    color=dow["total_price"],
                    colorscale="Viridis",
                    showscale=True,
                    line=dict(color="rgba(255,255,255,0.25)", width=1),
                ),
                text=[format_currency(v, 0) for v in dow["total_price"]],
                textposition="outside",
            )
        ]
    )
    return style_fig(fig, "Weekly Revenue Pattern", theme)


def plot_top_customers(df_filtered: pd.DataFrame, theme: str, top_n: int) -> go.Figure:
    top_customers = (
        df_filtered.groupby("customer_id")
        .agg(total_revenue=("total_price", "sum"), order_count=("order_id", "nunique"))
        .nlargest(top_n, "total_revenue")
        .reset_index()
    )
    fig = go.Figure(
        data=[
            go.Bar(
                x=top_customers["total_revenue"],
                y=top_customers["customer_id"],
                orientation="h",
                marker=dict(
                    color=top_customers["total_revenue"], colorscale="Plasma", showscale=False
                ),
                text=[format_currency(v, 0) for v in top_customers["total_revenue"]],
                textposition="outside",
            )
        ]
    )
    return style_fig(fig, f"Top {top_n} Customers by Revenue", theme)


def compute_rfm(df_filtered: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    snapshot_date = df_filtered["order_date"].max() + timedelta(days=1)
    rfm = (
        df_filtered.groupby("customer_id")
        .agg(
            recency=("order_date", lambda x: (snapshot_date - x.max()).days),
            frequency=("order_id", "nunique"),
            monetary=("total_price", "sum"),
        )
        .reset_index()
    )

    rfm["segment"] = "Regular"
    q = rfm.quantile([0.25, 0.5, 0.75])
    rfm.loc[
        (rfm["frequency"] >= q.loc[0.75, "frequency"])
        & (rfm["monetary"] >= q.loc[0.75, "monetary"]),
        "segment",
    ] = "💎 VIP"
    rfm.loc[
        (rfm["recency"] <= q.loc[0.25, "recency"])
        & (rfm["frequency"] >= q.loc[0.50, "frequency"]),
        "segment",
    ] = "⚡ Active"
    rfm.loc[rfm["recency"] >= q.loc[0.75, "recency"], "segment"] = "⚠️ At Risk"

    summary = (
        rfm.groupby("segment")
        .agg(customer_count=("customer_id", "count"), total_revenue=("monetary", "sum"))
        .reset_index()
    )
    return rfm, summary


def plot_price_distribution(df_filtered: pd.DataFrame, theme: str) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Histogram(
            x=df_filtered["unit_price"], nbinsx=50,
            marker=dict(color="#9b59b6", line=dict(color="rgba(255,255,255,0.25)", width=1)),
            opacity=0.85, name="Unit Price"
        )
    )
    fig.add_trace(
        go.Box(
            x=df_filtered["unit_price"], name="Distribution",
            marker=dict(color="#00ff87"), yaxis="y2"
        )
    )
    fig.update_layout(yaxis2=dict(overlaying="y", side="right"))
    return style_fig(fig, "Unit Price Distribution", theme)


def plot_pareto(df_filtered: pd.DataFrame, theme: str, head: int = 20) -> go.Figure:
    product_rev = (
        df_filtered.groupby("product_name")["total_price"]
        .sum().sort_values(ascending=False).reset_index()
    )
    product_rev["cumulative_pct"] = product_rev["total_price"].cumsum() / product_rev["total_price"].sum() * 100

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=list(range(min(head, len(product_rev)))),
            y=product_rev["total_price"][:head],
            name="Revenue",
            marker=dict(color="#667eea"),
            yaxis="y",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=list(range(min(head, len(product_rev)))),
            y=product_rev["cumulative_pct"][:head],
            name="Cumulative %",
            mode="lines+markers",
            marker=dict(color="#00ff87", size=7),
            line=dict(color="#00ff87", width=2),
            yaxis="y2",
        )
    )
    fig.update_layout(
        yaxis=dict(title="Revenue"),
        yaxis2=dict(title="Cumulative %", overlaying="y", side="right", range=[0, 100]),
        showlegend=True,
    )
    return style_fig(fig, "Pareto Analysis (80/20)", theme)


def plot_growth_rate(df_filtered: pd.DataFrame, theme: str) -> go.Figure:
    monthly = (
        df_filtered.groupby(df_filtered["order_date"].dt.to_period("M"))["total_price"]
        .sum()
        .reset_index()
    )
    monthly["order_date"] = monthly["order_date"].dt.to_timestamp()
    monthly["growth_rate"] = monthly["total_price"].pct_change() * 100

    colors = ["#00ff87" if (not pd.isna(x) and x >= 0) else "#ff006e" for x in monthly["growth_rate"]]
    fig = go.Figure(
        data=[
            go.Bar(
                x=monthly["order_date"],
                y=monthly["growth_rate"],
                marker=dict(color=colors, line=dict(color="rgba(255,255,255,0.25)", width=1)),
                text=[f"{v:.1f}%" if pd.notna(v) else "" for v in monthly["growth_rate"]],
                textposition="outside",
            )
        ]
    )
    fig.add_hline(y=0, line_dash="solid", line_color="rgba(200,200,200,0.6)", line_width=2)
    return style_fig(fig, "Month-over-Month Growth %", theme)


# =========================
# App
# =========================
def main():
    inject_css()

    # Header
    st.markdown(
        """
        <div style="text-align:center; padding: 24px 0 8px;">
            <h1 class="hero-title" style="font-size:44px;">📊 Executive E-commerce Dashboard</h1>
            <p style="color:#a8b2d1; font-size:14px; margin-top:6px;">
                Real-time business intelligence & advanced analytics
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<hr/>", unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Control Center")

        # Tema de gráficos (no cambia el CSS global para mantener consistencia)
        theme = st.radio("Theme", options=["dark", "light"], index=0, horizontal=True)

        # Carga de datos
        with st.expander("📁 Data Source", expanded=True):
            parquet_path = st.text_input("Parquet path", "data/processed/ecommerce_dataset_10000_cleaned.parquet")
            csv_path = st.text_input("CSV path (fallback)", "data/processed/ecommerce_dataset_10000_cleaned.csv")

        df = load_data(parquet_path, csv_path)
        if df is None or df.empty:
            st.error("No se encontró dataset o está vacío. Revisa rutas y esquema.")
            st.stop()

        # Filtros
        with st.expander("📅 Date Range", expanded=True):
            min_date = df["order_date"].min().date()
            max_date = df["order_date"].max().date()

            c1, c2 = st.columns(2)
            with c1:
                start_date = st.date_input("From", min_date, min_value=min_date, max_value=max_date, key="from_date")
            with c2:
                end_date = st.date_input("To", max_date, min_value=min_date, max_value=max_date, key="to_date")

            # Quick filters
            q1, q2, q3, q4 = st.columns(4)
            if q1.button("Last 7 days", use_container_width=True):
                st.session_state.from_date = max_date - timedelta(days=7)
                st.session_state.to_date = max_date
                st.rerun()
            if q2.button("Last 30 days", use_container_width=True):
                st.session_state.from_date = max_date - timedelta(days=30)
                st.session_state.to_date = max_date
                st.rerun()
            if q3.button("Last Quarter", use_container_width=True):
                st.session_state.from_date = max_date - timedelta(days=90)
                st.session_state.to_date = max_date
                st.rerun()
            if q4.button("Year to Date", use_container_width=True):
                st.session_state.from_date = datetime(max_date.year, 1, 1).date()
                st.session_state.to_date = max_date
                st.rerun()

        with st.expander("🌍 Geographic Filter", expanded=True):
            countries = sorted(df["country"].dropna().unique().tolist())
            select_all = st.checkbox("Select all", value=True)
            if select_all:
                selected_countries = countries
            else:
                selected_countries = st.multiselect("Countries", countries, default=countries[:5])

        with st.expander("📊 Display", expanded=False):
            top_n = st.slider("Top N", min_value=5, max_value=50, value=10, step=5)
            show_data_table = st.toggle("Show country details table", value=True)

    # Filtrado
    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)  # inclusive end
    df_filtered = filter_data(df, start_dt, end_dt, selected_countries)
    if df_filtered.empty:
        st.warning("No hay datos para los filtros seleccionados. Ajusta el rango o países.")
        st.stop()

    # Métricas
    metrics = calculate_metrics(df_filtered, df)

    # KPI Cards
    st.subheader("🎯 Key Performance Indicators")
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.metric("Total Revenue", format_currency(metrics["total_revenue"], 0), f"{metrics['revenue_delta']:.1f}% vs prev")
    with k2:
        st.metric("Total Orders", f"{metrics['total_orders']:,}", f"{metrics['orders_delta']:.1f}%")
    with k3:
        st.metric("Customers", f"{metrics['unique_customers']:,}", f"{metrics['customers_delta']:.1f}%")
    with k4:
        st.metric("Units Sold", f"{metrics['total_quantity']:,}")
    with k5:
        st.metric("Avg Order Value", format_currency(metrics["avg_order_value"]))

    st.markdown("<hr/>", unsafe_allow_html=True)

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📊 Revenue", "👥 Customer Intel", "📦 Product Perf", "🌍 Geo Insights", "🔬 Advanced"]
    )

    with tab1:
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown("### 📈 Revenue Trend Over Time")
            st.plotly_chart(plot_revenue_trend(df_filtered, theme), use_container_width=True)
        with c2:
            st.markdown("### 🏆 Top Countries")
            st.plotly_chart(plot_top_countries_pie(df_filtered, theme), use_container_width=True)

        st.markdown("### 📅 Revenue by Day of Week")
        st.plotly_chart(plot_dow_revenue(df_filtered, theme), use_container_width=True)

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"### 🌟 Top {top_n} Customers")
            st.plotly_chart(plot_top_customers(df_filtered, theme, top_n), use_container_width=True)
        with c2:
            st.markdown("### 🔄 Customer Retention (Order Frequency)")
            order_freq = (
                df_filtered.groupby("customer_id")["order_id"].nunique().value_counts().sort_index().reset_index()
            )
            order_freq.columns = ["orders", "customer_count"]
            fig = go.Figure(
                data=[
                    go.Bar(
                        x=order_freq["orders"],
                        y=order_freq["customer_count"],
                        marker=dict(color=order_freq["customer_count"], colorscale="Turbo"),
                        text=order_freq["customer_count"], textposition="outside",
                    )
                ]
            )
            st.plotly_chart(style_fig(fig, "Order Frequency Distribution", theme), use_container_width=True)

        st.markdown("### 🎯 Customer Segmentation (RFM)")
        rfm, seg_summary = compute_rfm(df_filtered)
        c1, c2 = st.columns(2)
        with c1:
            fig_seg_cnt = go.Figure(
                data=[
                    go.Bar(
                        x=seg_summary["segment"],
                        y=seg_summary["customer_count"],
                        marker=dict(color=NEON_COLORS[: len(seg_summary)]),
                        text=seg_summary["customer_count"],
                        textposition="outside",
                    )
                ]
            )
            st.plotly_chart(style_fig(fig_seg_cnt, "Customers by Segment", theme), use_container_width=True)
        with c2:
            fig_seg_rev = go.Figure(
                data=[
                    go.Bar(
                        x=seg_summary["segment"],
                        y=seg_summary["total_revenue"],
                        marker=dict(color=NEON_COLORS[: len(seg_summary)]),
                        text=[format_currency(v, 0) for v in seg_summary["total_revenue"]],
                        textposition="outside",
                    )
                ]
            )
            st.plotly_chart(style_fig(fig_seg_rev, "Revenue by Segment", theme), use_container_width=True)

    with tab3:
        c1, c2 = st.columns([3, 2])
        with c1:
            st.markdown(f"### 🎯 Top {top_n} Products by Revenue")
            top_products_rev = (
                df_filtered.groupby("product_name")
                .agg(total_price=("total_price", "sum"), quantity=("quantity", "sum"))
                .nlargest(top_n, "total_price")
                .reset_index()
            )
            fig_prod_rev = go.Figure(
                data=[
                    go.Bar(
                        x=top_products_rev["total_price"],
                        y=top_products_rev["product_name"],
                        orientation="h",
                        marker=dict(color=top_products_rev["total_price"], colorscale="Rainbow"),
                        text=[format_currency(v, 0) for v in top_products_rev["total_price"]],
                        textposition="outside",
                    )
                ]
            )
            st.plotly_chart(style_fig(fig_prod_rev, "Revenue Leaders", theme), use_container_width=True)

        with c2:
            st.markdown("### 📦 By Quantity Sold")
            top_products_qty = (
                df_filtered.groupby("product_name")["quantity"].sum().nlargest(top_n).reset_index()
            )
            fig_prod_qty = go.Figure(
                data=[
                    go.Bar(
                        x=top_products_qty["quantity"],
                        y=top_products_qty["product_name"],
                        orientation="h",
                        marker=dict(color=top_products_qty["quantity"], colorscale="Teal"),
                        text=top_products_qty["quantity"],
                        textposition="outside",
                    )
                ]
            )
            st.plotly_chart(style_fig(fig_prod_qty, "Volume Champions", theme), use_container_width=True)

        st.markdown("### 💲 Price Distribution Analysis")
        c3, c4 = st.columns([2, 1])
        with c3:
            st.plotly_chart(plot_price_distribution(df_filtered, theme), use_container_width=True)
        with c4:
            price_stats = df_filtered["unit_price"].describe()
            with st.container(border=True):
                st.markdown("#### 📈 Price Statistics")
                st.metric("Mean", format_currency(price_stats["mean"]))
                st.metric("Median", format_currency(price_stats["50%"]))
                st.metric("Std Dev", format_currency(price_stats["std"]))
                st.metric("Max", format_currency(price_stats["max"]))

    with tab4:
        st.markdown("### 🌍 Revenue by Country")
        country_analysis = (
            df_filtered.groupby("country")
            .agg(revenue=("total_price", "sum"), orders=("order_id", "nunique"), customers=("customer_id", "nunique"))
            .reset_index()
            .sort_values("revenue", ascending=False)
        )
        fig_country = go.Figure(
            data=[
                go.Bar(
                    x=country_analysis["country"],
                    y=country_analysis["revenue"],
                    marker=dict(
                        color=country_analysis["revenue"],
                        colorscale="Viridis",
                        showscale=True,
                        colorbar=dict(title="Revenue", tickprefix="$"),
                    ),
                    text=[format_currency(v, 0) for v in country_analysis["revenue"]],
                    textposition="outside",
                    hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>",
                )
            ]
        )
        st.plotly_chart(style_fig(fig_country, "Global Revenue Distribution", theme), use_container_width=True)

        if st.toggle("Show details table", value=True if show_data_table else False):
            country_analysis["avg_order_value"] = (
                country_analysis["revenue"] / country_analysis["orders"].replace(0, np.nan)
            ).fillna(0)
            display_df = country_analysis.copy()
            display_df["revenue"] = display_df["revenue"].apply(lambda x: format_currency(x, 0))
            display_df["avg_order_value"] = display_df["avg_order_value"].apply(lambda x: format_currency(x, 2))
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "country": st.column_config.TextColumn("🌍 Country", width="medium"),
                    "revenue": st.column_config.TextColumn("💰 Total Revenue", width="medium"),
                    "orders": st.column_config.NumberColumn("🛒 Orders", format="%d"),
                    "customers": st.column_config.NumberColumn("👥 Customers", format="%d"),
                    "avg_order_value": st.column_config.TextColumn("💵 Avg Order Value", width="medium"),
                },
            )

    with tab5:
        st.markdown("### 🔬 Advanced Analytics & Insights")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 💹 Revenue Growth Rate")
            st.plotly_chart(plot_growth_rate(df_filtered, theme), use_container_width=True)
        with c2:
            st.markdown("#### 📊 Revenue Concentration (Pareto)")
            st.plotly_chart(plot_pareto(df_filtered, theme), use_container_width=True)

        c3, c4 = st.columns(2)
        with c3:
            st.markdown("#### 🔗 Quantity vs Price Correlation")
            sample_df = df_filtered.sample(min(1000, len(df_filtered)), random_state=42)
            fig_scatter = go.Figure(
                data=go.Scatter(
                    x=sample_df["quantity"],
                    y=sample_df["unit_price"],
                    mode="markers",
                    marker=dict(
                        size=np.clip(sample_df["total_price"] / 100, 4, 30),
                        color=sample_df["total_price"],
                        colorscale="Plasma",
                        showscale=True,
                        colorbar=dict(title="Total Price"),
                        opacity=0.75,
                    ),
                    text=[f"Total: {format_currency(v, 0)}" for v in sample_df["total_price"]],
                    hovertemplate="<b>Qty:</b> %{x}<br><b>Price:</b> $%{y:.2f}<br>%{text}<extra></extra>",
                )
            )
            st.plotly_chart(style_fig(fig_scatter, "Price vs Quantity", theme), use_container_width=True)
        with c4:
            st.markdown("#### ⏰ Seasonal Revenue Patterns")
            monthly_rev = (
                df_filtered.groupby(df_filtered["order_date"].dt.month)["total_price"].sum().reset_index()
            )
            monthly_rev.columns = ["month", "revenue"]
            monthly_rev["month_name"] = monthly_rev["month"].apply(lambda x: MONTH_ABBR[x - 1] if 1 <= x <= 12 else str(x))
            fig_monthly = go.Figure(
                data=[
                    go.Bar(
                        x=monthly_rev["month_name"],
                        y=monthly_rev["revenue"],
                        marker=dict(color=monthly_rev["revenue"], colorscale="Turbo"),
                        text=[format_currency(v, 0) for v in monthly_rev["revenue"]],
                        textposition="outside",
                    )
                ]
            )
            st.plotly_chart(style_fig(fig_monthly, "Seasonal Revenue Patterns", theme), use_container_width=True)

        # Executive Summary
        st.markdown("----")
        st.markdown("### 🎯 Executive Summary")
        country_analysis = (
            df_filtered.groupby("country")
            .agg(revenue=("total_price", "sum"))
            .reset_index()
            .sort_values("revenue", ascending=False)
        )
        top_country = country_analysis.iloc,[object Object], if not country_analysis.empty else {"country": "N/A", "revenue": 0}
        best_product = (
            df_filtered.groupby("product_name")["total_price"].sum().sort_values(ascending=False).reset_index()
        )
        best_product = best_product.iloc,[object Object], if not best_product.empty else {"product_name": "N/A", "total_price": 0}
        rfm_df, _ = compute_rfm(df_filtered)
        vip_count = int((rfm_df["segment"] == "💎 VIP").sum()) if not rfm_df.empty else 0
        monthly = (
            df_filtered.groupby(df_filtered["order_date"].dt.to_period("M"))["total_price"].sum().reset_index()
        )
        monthly["order_date"] = monthly["order_date"].dt.to_timestamp()
        monthly["growth_rate"] = monthly["total_price"].pct_change() * 100
        growth_avg = float(monthly["growth_rate"].mean()) if len(monthly) > 1 else 0.0

        g1, g2, g3, g4 = st.columns(4)
        with g1:
            st.metric("Top Country", str(top_country["country"]), format_currency(float(top_country["revenue"]), 0))
        with g2:
            name = str(best_product["product_name"])
            name_short = name if len(name) <= 18 else name[:18] + "…"
            st.metric("Best Product", name_short, format_currency(float(best_product["total_price"]), 0))
        with g3:
            st.metric("VIP Customers", f"{vip_count}")
        with g4:
            st.metric("Avg MoM Growth", f"{growth_avg:.1f}%")

    # Export Center
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("## 📥 Export Data Center")
    c1, c2, c3, c4 = st.columns(4)

    # Reusar dataframes calculados (guardamos en variables locales para export)
    # Nota: recalculamos top_dfs rápidamente para garantizar coherencia con filtros.
    top_customers_df = (
        df_filtered.groupby("customer_id")
        .agg(total_revenue=("total_price", "sum"), order_count=("order_id", "nunique"))
        .nlargest(top_n, "total_revenue")
        .reset_index()
    )
    top_products_rev_df = (
        df_filtered.groupby("product_name")
        .agg(total_price=("total_price", "sum"), quantity=("quantity", "sum"))
        .nlargest(top_n, "total_price")
        .reset_index()
    )
    country_analysis_df = (
        df_filtered.groupby("country")
        .agg(revenue=("total_price", "sum"), orders=("order_id", "nunique"), customers=("customer_id", "nunique"))
        .reset_index()
        .sort_values("revenue", ascending=False)
    )

    now_str = datetime.now().strftime("%Y%m%d_%H%M")
    with c1:
        st.download_button(
            "📊 Filtered dataset",
            df_filtered.to_csv(index=False).encode("utf-8"),
            file_name=f"filtered_data_{now_str}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with c2:
        st.download_button(
            "🏆 Top customers",
            top_customers_df.to_csv(index=False).encode("utf-8"),
            file_name=f"top_customers_{now_str}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with c3:
        st.download_button(
            "📦 Top products",
            top_products_rev_df.to_csv(index=False).encode("utf-8"),
            file_name=f"top_products_{now_str}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with c4:
        st.download_button(
            "🌍 Country report",
            country_analysis_df.to_csv(index=False).encode("utf-8"),
            file_name=f"country_analysis_{now_str}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # Footer
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="text-align:center; padding: 18px; border-radius: 12px;">
            <h3 class="hero-title" style="font-size:22px; margin-bottom:4px;">Executive E-commerce Dashboard v2.1</h3>
            <p style="color:#a8b2d1; font-size:12px; margin: 2px 0;">Built with ❤️ using Streamlit & Plotly</p>
            <p style="color:#60efff; font-size:11px; margin: 0;">Last Updated: {datetime.now().strftime('%B %d, %Y at %H:%M')}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
