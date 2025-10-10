# scripts/app_debug.py
"""
Debug E-commerce Dashboard (Streamlit)
Checks dataset and renders basic charts for troubleshooting.
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import subprocess

# -----------------------
# Page config
# -----------------------
st.set_page_config(page_title="E-commerce Debug Dashboard", layout="wide")
st.title("🛠️ E-commerce Debug Dashboard")
st.markdown("Check dataset, filters, and basic charts.")

# -----------------------
# Verify required columns
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

# Show first rows
st.subheader("Dataset Preview")
st.dataframe(df.head())

# -----------------------
# Sidebar Filters
# -----------------------
st.sidebar.header("Filters")
countries = sorted(df['country'].dropna().unique())
selected_countries = st.sidebar.multiselect("Select Countries", countries, default=countries)
df = df[df['country'].isin(selected_countries)]

df['order_date'] = pd.to_datetime(df['order_date'])
min_date = df['order_date'].min()
max_date = df['order_date'].max()
start_date, end_date = st.sidebar.date_input("Order Date Range", [min_date, max_date])
df = df[(df['order_date'] >= pd.to_datetime(start_date)) & (df['order_date'] <= pd.to_datetime(end_date))]

top_n = st.sidebar.slider("Top N", min_value=5, max_value=50, value=10, step=5)

# -----------------------
# Helper for Plotly layout
# -----------------------
def style_fig(fig):
    fig.update_layout(
        title_font_size=20,
        font=dict(size=12),
        margin=dict(l=30, r=30, t=50, b=30),
        template="plotly_white"
    )
    return fig

# -----------------------
# Revenue by Country
# -----------------------
st.subheader("Revenue by Country")
if 'country' in df.columns and 'total_price' in df.columns and not df.empty:
    country_df = df.groupby('country')['total_price'].sum().reset_index()
    fig_country = px.bar(country_df, x='country', y='total_price', text_auto=True, title="Revenue by Country")
    st.plotly_chart(style_fig(fig_country), use_container_width=True)
else:
    st.warning("❌ Missing columns for 'Revenue by Country' chart.")

# -----------------------
# Monthly Revenue
# -----------------------
st.subheader("Monthly Revenue")
if 'order_date' in df.columns and 'total_price' in df.columns and not df.empty:
    monthly = df.groupby(df['order_date'].dt.to_period('M'))['total_price'].sum().reset_index()
    monthly['order_date'] = monthly['order_date'].dt.to_timestamp()
    fig_monthly = px.bar(monthly, x='order_date', y='total_price', text_auto=True, title="Monthly Revenue")
    st.plotly_chart(style_fig(fig_monthly), use_container_width=True)
else:
    st.warning("❌ Missing columns for 'Monthly Revenue' chart.")

# -----------------------
# Top Customers
# -----------------------
st.subheader(f"Top {top_n} Customers by Revenue")
if 'customer_id' in df.columns and 'total_price' in df.columns and not df.empty:
    top_customers = df.groupby('customer_id')['total_price'].sum().nlargest(top_n).reset_index()
    fig_customers = px.bar(top_customers, x='customer_id', y='total_price', text_auto=True, title=f"Top {top_n} Customers")
    st.plotly_chart(style_fig(fig_customers), use_container_width=True)
else:
    st.warning("❌ Missing columns for Top Customers chart.")

# -----------------------
# Top Products
# -----------------------
st.subheader(f"Top {top_n} Products by Quantity Sold")
if 'product_name' in df.columns and 'quantity' in df.columns and not df.empty:
    top_products = df.groupby('product_name')['quantity'].sum().nlargest(top_n).reset_index()
    fig_products = px.bar(top_products, x='product_name', y='quantity', text_auto=True, title=f"Top {top_n} Products")
    st.plotly_chart(style_fig(fig_products), use_container_width=True)
else:
    st.warning("❌ Missing columns for Top Products chart.")

# -----------------------
# Unit Price Distribution
# -----------------------
st.subheader("Unit Price Distribution")
if 'unit_price' in df.columns and not df.empty:
    fig_price = px.histogram(df, x='unit_price', nbins=50, title="Unit Price Distribution")
    st.plotly_chart(style_fig(fig_price), use_container_width=True)
else:
    st.warning("❌ Missing column 'unit_price' for Price Distribution chart.")
