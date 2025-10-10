# scripts/app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="E-commerce Dashboard", layout="wide")

# Load dataset
dataset_file = "data/processed/ecommerce_dataset_10000_cleaned.parquet"

if os.path.exists(dataset_file):
    df = pd.read_parquet(dataset_file)
    st.success(f"Dataset loaded: {len(df)} rows")
else:
    st.error("Dataset not found. Run the workflow first.")

# Revenue by Country
if 'country' in df.columns and 'total_price' in df.columns:
    st.subheader("Revenue by Country")
    fig_country = px.bar(df.groupby('country')['total_price'].sum().reset_index(),
                         x='country', y='total_price')
    st.plotly_chart(fig_country, use_container_width=True)

# Monthly Revenue
if 'order_date' in df.columns and 'total_price' in df.columns:
    st.subheader("Monthly Revenue")
    df['order_date'] = pd.to_datetime(df['order_date'])
    monthly = df.groupby(df['order_date'].dt.to_period('M'))['total_price'].sum().reset_index()
    monthly['order_date'] = monthly['order_date'].dt.to_timestamp()
    fig_monthly = px.line(monthly, x='order_date', y='total_price')
    st.plotly_chart(fig_monthly, use_container_width=True)

# Add more plots as needed...
