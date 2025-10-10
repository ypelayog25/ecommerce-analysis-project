# scripts/app.py
"""
Executive E-commerce Dashboard (Streamlit)
Professional KPIs with sparklines, growth indicators, and responsive charts.
"""

import os
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# -----------------------
# Page config
# -----------------------
st.set_page_config(
    page_title="Executive E-commerce Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("<h1 style='text-align:center'>📊 Executive E-commerce Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center'>Interactive KPIs and professional charts</p>", unsafe_allow_html=True)

# -----------------------
# Load dataset
# -----------------------
dataset_parquet = "data/processed/ecommerce_dataset_10000_cleaned.parquet"
dataset_csv = "data/processed/ecommerce_dataset_10000_cleaned.csv"

df = None
if os.path.exists(dataset_parquet):
    df = pd.read_parquet(dataset_parquet)
elif os.path.exists(dataset_csv):
    df = pd.read_csv(dataset_csv)

if df is None or df.empty:
    st.error("❌ No dataset found or dataset is empty.")
    st.stop()

df['order_date'] = pd.to_datetime(df['order_date'])

# -----------------------
# Sidebar Filters
# -----------------------
with st.sidebar.expander("Filters", expanded=True):
    theme = st.radio("Theme", ["Light", "Dark"], index=0)

    countries = sorted(df['country'].dropna().unique())
    selected_countries = st.multiselect("Select Countries", countries, default=countries)
    df = df[df['country'].isin(selected_countries)]

    start_date, end_date = st.date_input(
        "Order Date Range",
        [df['order_date'].min(), df['order_date'].max()]
    )
    df = df[(df['order_date'] >= start_date) & (df['order_date'] <= end_date)]

    top_n = st.slider("Top N", 5, 50, 10, 5)

# -----------------------
# KPI Cards with Sparklines
# -----------------------
st.markdown("### Key Performance Indicators")
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

# Monthly revenue for sparkline
monthly_total = df.groupby(df['order_date'].dt.to_period('M'))['total_price'].sum().reset_index()
monthly_total['order_date'] = monthly_total['order_date'].dt.to_timestamp()

prev_month_revenue = monthly_total['total_price'].iloc[-2] if len(monthly_total) > 1 else 0
revenue_growth = ((monthly_total['total_price'].iloc[-1] - prev_month_revenue) / max(prev_month_revenue,1)) * 100

sparkline = go.Figure(go.Scatter(
    x=monthly_total['order_date'],
    y=monthly_total['total_price'],
    mode='lines',
    line=dict(color="#2E86C1", width=2),
    fill='tozeroy'
))
sparkline.update_layout(margin=dict(l=0,r=0,t=0,b=0), height=50, xaxis_visible=False, yaxis_visible=False)

kpi_col1.plotly_chart(sparkline, use_container_width=True)
kpi_col1.markdown(f"<div style='text-align:center; font-weight:bold;'>💰 Total Revenue<br><span style='font-size:26px; color:#2E86C1'>${df['total_price'].sum():,.0f}</span><br>Growth: {revenue_growth:.1f}%</div>", unsafe_allow_html=True)

kpi_col2.markdown(f"<div style='background:#f0f2f6; padding:15px; border-radius:12px; text-align:center;'>🛒 Total Orders<br><span style='font-size:26px; color:#2E86C1'>{len(df)}</span></div>", unsafe_allow_html=True)
kpi_col3.markdown(f"<div style='background:#f0f2f6; padding:15px; border-radius:12px; text-align:center;'>👤 Unique Customers<br><span style='font-size:26px; color:#2E86C1'>{df['customer_id'].nunique()}</span></div>", unsafe_allow_html=True)
kpi_col4.markdown(f"<div style='background:#f0f2f6; padding:15px; border-radius:12px; text-align:center;'>📦 Total Products Sold<br><span style='font-size:26px; color:#2E86C1'>{df['quantity'].sum():,.0f}</span></div>", unsafe_allow_html=True)

# -----------------------
# Helper function for Plotly styling
# -----------------------
def style_fig(fig):
    fig.update_layout(
        title_font_size=24,
        font=dict(size=14, color="#111111" if theme=="Light" else "#FFFFFF"),
        margin=dict(l=50,r=50,t=50,b=50),
        template="plotly_white" if theme=="Light" else "plotly_dark"
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor="lightgrey")
    return fig

# -----------------------
# Tabs for charts
# -----------------------
tab1, tab2, tab3, tab4 = st.tabs(["Revenue Overview", "Top Customers", "Top Products", "Price Distribution"])

# Revenue Overview
with tab1:
    st.subheader("Revenue by Country")
    country_df = df.groupby('country')['total_price'].sum().reset_index().sort_values('total_price', ascending=False)
    fig_country = px.bar(country_df, x='country', y='total_price', text_auto='.2s',
                         color='total_price', color_continuous_scale=px.colors.sequential.Blues)
    st.plotly_chart(style_fig(fig_country), use_container_width=True)

    st.subheader("Monthly Revenue Trend")
    fig_monthly = px.line(monthly_total, x='order_date', y='total_price', markers=True, title="Monthly Revenue Trend")
    st.plotly_chart(style_fig(fig_monthly), use_container_width=True)

# Top Customers
with tab2:
    st.subheader(f"Top {top_n} Customers by Revenue")
    top_customers = df.groupby('customer_id')['total_price'].sum().nlargest(top_n).reset_index()
    fig_customers = px.bar(top_customers, x='total_price', y='customer_id', orientation='h', text_auto='.2s',
                           color='total_price', color_continuous_scale=px.colors.sequential.Viridis)
    st.plotly_chart(style_fig(fig_customers), use_container_width=True)

# Top Products
with tab3:
    st.subheader(f"Top {top_n} Products by Quantity Sold")
    top_products = df.groupby('product_name')['quantity'].sum().nlargest(top_n).reset_index()
    fig_products = px.bar(top_products, x='quantity', y='product_name', orientation='h', text_auto='.2s',
                          color='quantity', color_continuous_scale=px.colors.sequential.Oranges)
    st.plotly_chart(style_fig(fig_products), use_container_width=True)

# Price Distribution
with tab4:
    st.subheader("Unit Price Distribution")
    fig_price = px.histogram(df, x='unit_price', nbins=50, color_discrete_sequence=['#00CC96'], marginal="box")
    st.plotly_chart(style_fig(fig_price), use_container_width=True)

# -----------------------
# Download Filtered Dataset
# -----------------------
st.download_button(
    "📥 Download Filtered Dataset (CSV)",
    df.to_csv(index=False),
    file_name="filtered_dataset.csv"
)
