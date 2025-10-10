# scripts/app.py
"""
Advanced E-commerce Dashboard (Streamlit)
Interactive dashboard with filters, top customers/products, and revenue charts.
Improved readability with larger fonts and clearer colors.
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import subprocess

# -----------------------
# Page config
# -----------------------
st.set_page_config(page_title="E-commerce Dashboard", layout="wide")
st.title("📊 E-commerce Dashboard")
st.markdown("Interactive dashboard automatically updated from processed dataset.")

# -----------------------
# Verify required columns
# -----------------------
try:
    subprocess.run(["python", "scripts/verify_columns.py"], check=True)
except subprocess.CalledProcessError:
    st.error("❌ Dataset missing required columns. Check verify_columns.py output.")
    st.stop()

# -----------------------
# Load dataset
# -----------------------
dataset_parquet = "data/processed/ecommerce_dataset_10000_cleaned.parquet"
dataset_csv = "data/processed/ecommerce_dataset_10000_cleaned.csv"

df = None
if os.path.exists(dataset_parquet):
    df = pd.read_parquet(dataset_parquet)
    st.success(f"✅ Dataset loaded from Parquet: {len(df)} rows")
elif os.path.exists(dataset_csv):
    df = pd.read_csv(dataset_csv)
    st.success(f"✅ Dataset loaded from CSV: {len(df)} rows")

# -----------------------
# Sidebar Filters
# -----------------------
st.sidebar.header("Filters")

# Country filter
countries = sorted(df['country'].dropna().unique())
selected_countries = st.sidebar.multiselect("Select Countries", countries, default=countries)
df = df[df['country'].isin(selected_countries)]

# Date filter
df['order_date'] = pd.to_datetime(df['order_date'])
min_date = df['order_date'].min()
max_date = df['order_date'].max()
start_date, end_date = st.sidebar.date_input("Order Date Range", [min_date, max_date])
df = df[(df['order_date'] >= pd.to_datetime(start_date)) & (df['order_date'] <= pd.to_datetime(end_date))]

# Top N slider
top_n = st.sidebar.slider("Top N", min_value=5, max_value=50, value=10, step=5)

# -----------------------
# Helper for Plotly layout
# -----------------------
def style_fig(fig):
    fig.update_layout(
        title_font_size=24,
        font=dict(size=16),
        margin=dict(l=50, r=50, t=80, b=50),
        template="plotly_white"
    )
    return fig

# -----------------------
# Revenue by Country
# -----------------------
st.subheader("Revenue by Country")
country_df = df.groupby('country')['total_price'].sum().reset_index()
fig_country = px.bar(country_df, x='country', y='total_price',
                     text_auto=True, color='total_price', color_continuous_scale='Blues',
                     title="Revenue by Country")
fig_country = style_fig(fig_country)
st.plotly_chart(fig_country, use_container_width=True)

# -----------------------
# Monthly Revenue
# -----------------------
st.subheader("Monthly Revenue")
monthly = df.groupby(df['order_date'].dt.to_period('M'))['total_price'].sum().reset_index()
monthly['order_date'] = monthly['order_date'].dt.to_timestamp()
fig_monthly = px.line(monthly, x='order_date', y='total_price', markers=True,
                      title="Monthly Revenue", text='total_price')
fig_monthly = style_fig(fig_monthly)
st.plotly_chart(fig_monthly, use_container_width=True)

# -----------------------
# Top Customers
# -----------------------
st.subheader(f"Top {top_n} Customers by Revenue")
top_customers = df.groupby('customer_id')['total_price'].sum().nlargest(top_n).reset_index()
fig_customers = px.bar(top_customers, x='customer_id', y='total_price',
                       text_auto=True, color='total_price', color_continuous_scale='Viridis',
                       title=f"Top {top_n} Customers")
fig_customers = style_fig(fig_customers)
st.plotly_chart(fig_customers, use_container_width=True)

# -----------------------
# Top Products
# -----------------------
st.subheader(f"Top {top_n} Products by Quantity Sold")
top_products = df.groupby('product_name')['quantity'].sum().nlargest(top_n).reset_index()
fig_products = px.bar(top_products, x='product_name', y='quantity',
                      text_auto=True, color='quantity', color_continuous_scale='Oranges',
                      title=f"Top {top_n} Products")
fig_products = style_fig(fig_products)
st.plotly_chart(fig_products, use_container_width=True)

# -----------------------
# Unit Price Distribution
# -----------------------
st.subheader("Unit Price Distribution")
fig_price = px.histogram(df, x='unit_price', nbins=50, color_discrete_sequence=['teal'],
                         title="Unit Price Distribution")
fig_price = style_fig(fig_price)
st.plotly_chart(fig_price, use_container_width=True)
