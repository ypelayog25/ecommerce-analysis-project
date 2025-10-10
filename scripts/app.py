# scripts/app.py
"""
Premium E-commerce Dashboard (Streamlit)
Cards for KPIs, professional charts, responsive layout.
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import subprocess

# -----------------------
# Page config
# -----------------------
st.set_page_config(page_title="E-commerce Dashboard", layout="wide", initial_sidebar_state="expanded")
st.markdown("<h1 style='text-align:center'>📊 E-commerce Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center'>Interactive dashboard with professional KPIs and visuals</p>", unsafe_allow_html=True)

# -----------------------
# Theme toggle
# -----------------------
theme = st.sidebar.radio("Theme", ["Light", "Dark"], index=0)

# -----------------------
# Verify required columns (non-blocking)
# -----------------------
try:
    subprocess.run(["python", "scripts/verify_columns.py"], check=True)
except subprocess.CalledProcessError:
    st.warning("⚠ Dataset may be missing required columns.")

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

# -----------------------
# Sidebar Filters
# -----------------------
with st.sidebar.expander("Filters", expanded=True):
    countries = sorted(df['country'].dropna().unique())
    selected_countries = st.multiselect("Select Countries", countries, default=countries)
    df = df[df['country'].isin(selected_countries)]

    df['order_date'] = pd.to_datetime(df['order_date'])
    start_date, end_date = st.date_input("Order Date Range", [df['order_date'].min(), df['order_date'].max()])
    df = df[(df['order_date'] >= pd.to_datetime(start_date)) & (df['order_date'] <= pd.to_datetime(end_date))]

    top_n = st.slider("Top N", min_value=5, max_value=50, value=10, step=5)

# -----------------------
# KPIs cards
# -----------------------
st.markdown("### Key Performance Indicators")
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

kpi_style = """
<div style='
    background-color:#f5f5f5; padding:20px; border-radius:10px;
    text-align:center; font-size:20px; font-weight:bold; box-shadow: 2px 2px 5px #aaaaaa;
'>
    {title}<br><span style='font-size:24px; color:#2E86C1'>{value}</span>
</div>
"""

kpi_col1.markdown(kpi_style.format(title="💰 Total Revenue", value=f"${df['total_price'].sum():,.0f}"), unsafe_allow_html=True)
kpi_col2.markdown(kpi_style.format(title="🛒 Total Orders", value=f"{df['order_id'].nunique()}"), unsafe_allow_html=True)
kpi_col3.markdown(kpi_style.format(title="👤 Unique Customers", value=f"{df['customer_id'].nunique()}"), unsafe_allow_html=True)
kpi_col4.markdown(kpi_style.format(title="📦 Total Products Sold", value=f"{df['quantity'].sum():,.0f}"), unsafe_allow_html=True)

# -----------------------
# Helper for Plotly layout
# -----------------------
def style_fig(fig, title_font=28, axis_font=16):
    fig.update_layout(
        title_font_size=title_font,
        font=dict(size=axis_font, color="#111111" if theme=="Light" else "#FFFFFF"),
        margin=dict(l=50, r=50, t=80, b=50),
        template="plotly_dark" if theme=="Dark" else "plotly_white"
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor="lightgrey")
    return fig

# -----------------------
# Tabs for charts
# -----------------------
tab1, tab2, tab3, tab4 = st.tabs(["Revenue Overview", "Top Customers", "Top Products", "Price Distribution"])

# Revenue Overview Tab
with tab1:
    st.subheader("Revenue by Country")
    country_df = df.groupby('country')['total_price'].sum().reset_index()
    fig_country = px.bar(country_df, x='country', y='total_price', text_auto='.2s',
                         color='total_price', color_continuous_scale=px.colors.sequential.Blues,
                         title="Revenue by Country", hover_data={"total_price":':,.2f'})
    st.plotly_chart(style_fig(fig_country), use_container_width=True)

    st.subheader("Monthly Revenue Trend")
    monthly = df.groupby(df['order_date'].dt.to_period('M'))['total_price'].sum().reset_index()
    monthly['order_date'] = monthly['order_date'].dt.to_timestamp()
    fig_monthly = px.bar(monthly, x='order_date', y='total_price', text='total_price', color='total_price',
                         color_continuous_scale='Blues', title="Monthly Revenue")
    fig_line = px.line(monthly, x='order_date', y='total_price', markers=True, title="Revenue Trend")
    for trace in fig_line.data:
        fig_monthly.add_trace(trace)
    st.plotly_chart(style_fig(fig_monthly), use_container_width=True)

# Top Customers Tab
with tab2:
    st.subheader(f"Top {top_n} Customers by Revenue")
    top_customers = df.groupby('customer_id')['total_price'].sum().nlargest(top_n).reset_index()
    fig_customers = px.bar(top_customers, x='customer_id', y='total_price', text_auto='.2s',
                           color='total_price', color_continuous_scale=px.colors.sequential.Viridis,
                           title=f"Top {top_n} Customers", hover_data={"total_price":':,.2f'})
    st.plotly_chart(style_fig(fig_customers), use_container_width=True)

# Top Products Tab
with tab3:
    st.subheader(f"Top {top_n} Products by Quantity Sold")
    top_products = df.groupby('product_name')['quantity'].sum().nlargest(top_n).reset_index()
    fig_products = px.bar(top_products, x='product_name', y='quantity', text_auto='.2s',
                          color='quantity', color_continuous_scale=px.colors.sequential.Oranges,
                          title=f"Top {top_n} Products", hover_data={"quantity":True})
    st.plotly_chart(style_fig(fig_products), use_container_width=True)

# Price Distribution Tab
with tab4:
    st.subheader("Unit Price Distribution")
    fig_price = px.histogram(df, x='unit_price', nbins=50, color_discrete_sequence=['#00CC96'],
                             title="Unit Price Distribution", marginal="box")
    st.plotly_chart(style_fig(fig_price), use_container_width=True)

# -----------------------
# Download button
# -----------------------
st.download_button(
    "📥 Download Filtered Dataset (CSV)",
    df.to_csv(index=False),
    file_name="filtered_dataset.csv"
)
