# scripts/app.py
"""
Advanced E-commerce Dashboard (Streamlit)
Interactive dashboard with filters, top customers/products, and revenue charts.
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------
# Page config
# -----------------------
st.set_page_config(page_title="E-commerce Dashboard", layout="wide")
st.title("📊 E-commerce Dashboard")
st.markdown("Interactive dashboard updated automatically from processed dataset.")

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
else:
    st.error("❌ Processed dataset not found. Run feature engineering first.")

# -----------------------
# Proceed if dataset loaded
# -----------------------
if df is not None:

    # -----------------------
    # Filters: Country & Date
    # -----------------------
    st.sidebar.header("Filters")
    
    # Country filter
    if 'country' in df.columns:
        countries = sorted(df['country'].dropna().unique())
        selected_countries = st.sidebar.multiselect("Select Countries", countries, default=countries)
        df = df[df['country'].isin(selected_countries)]
    
    # Date filter
    if 'order_date' in df.columns:
        df['order_date'] = pd.to_datetime(df['order_date'])
        min_date = df['order_date'].min()
        max_date = df['order_date'].max()
        start_date, end_date = st.sidebar.date_input("Order Date Range", [min_date, max_date])
        df = df[(df['order_date'] >= pd.to_datetime(start_date)) & (df['order_date'] <= pd.to_datetime(end_date))]

    # Top N filter
    top_n = st.sidebar.slider("Top N", min_value=5, max_value=50, value=10, step=5)

    # -----------------------
    # Revenue by Country
    # -----------------------
    if {'country', 'total_price'}.issubset(df.columns):
        st.subheader("Revenue by Country")
        country_df = df.groupby('country')['total_price'].sum().reset_index()
        fig_country = px.bar(country_df, x='country', y='total_price',
                             title="Revenue by Country", text_auto=True)
        st.plotly_chart(fig_country, use_container_width=True)
    else:
        st.warning("Missing columns for 'Revenue by Country' chart")

    # -----------------------
    # Monthly Revenue
    # -----------------------
    if {'order_date', 'total_price'}.issubset(df.columns):
        st.subheader("Monthly Revenue")
        monthly = df.groupby(df['order_date'].dt.to_period('M'))['total_price'].sum().reset_index()
        monthly['order_date'] = monthly['order_date'].dt.to_timestamp()
        fig_monthly = px.line(monthly, x='order_date', y='total_price', markers=True,
                              title="Monthly Revenue")
        st.plotly_chart(fig_monthly, use_container_width=True)
    else:
        st.warning("Missing columns for 'Monthly Revenue' chart")

    # -----------------------
    # Top Customers
    # -----------------------
    if {'customer_id', 'total_price'}.issubset(df.columns):
        st.subheader(f"Top {top_n} Customers by Revenue")
        top_customers = df.groupby('customer_id')['total_price'].sum().nlargest(top_n).reset_index()
        fig_customers = px.bar(top_customers, x='customer_id', y='total_price',
                               title=f"Top {top_n} Customers", text_auto=True)
        st.plotly_chart(fig_customers, use_container_width=True)
    else:
        st.warning("Missing columns for Top Customers chart")

    # -----------------------
    # Top Products
    # -----------------------
    if {'product_name', 'quantity'}.issubset(df.columns):
        st.subheader(f"Top {top_n} Products by Quantity Sold")
        top_products = df.groupby('product_name')['quantity'].sum().nlargest(top_n).reset_index()
        fig_products = px.bar(top_products, x='product_name', y='quantity',
                              title=f"Top {top_n} Products", text_auto=True)
        st.plotly_chart(fig_products, use_container_width=True)
    else:
        st.warning("Missing columns for Top Products chart")

    # -----------------------
    # Unit Price Distribution
    # -----------------------
    if 'unit_price' in df.columns:
        st.subheader("Unit Price Distribution")
        fig_price = px.histogram(df, x='unit_price', nbins=50,
                                 title="Unit Price Distribution")
        st.plotly_chart(fig_price, use_container_width=True)
    else:
        st.warning("Missing 'unit_price' column for distribution chart")
