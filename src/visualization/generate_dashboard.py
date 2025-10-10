import pandas as pd
import plotly.express as px
import streamlit as st

# Load cleaned dataset
df = pd.read_parquet("data/processed/ecommerce_dataset_10000_cleaned.parquet")

# --- Dashboard Title ---
st.title("E-commerce Sales Dashboard")

# --- Key Performance Indicators (KPIs) ---
total_revenue = df['Revenue'].sum()
total_orders = len(df)
top_customer = df.groupby('CustomerID')['Revenue'].sum().idxmax()

# Display KPIs in columns
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Orders", total_orders)
col3.metric("Top Customer", top_customer)

# --- Monthly Revenue Line Chart ---
monthly = df.groupby('OrderMonth')['Revenue'].sum().reset_index()
fig_monthly = px.line(monthly, x='OrderMonth', y='Revenue', title="Revenue Over Time")
st.plotly_chart(fig_monthly)

# --- Top 10 Products Bar Chart ---
top_products = df.groupby('ProductName')['Revenue'].sum().sort_values(ascending=False).head(10).reset_index()
fig_products = px.bar(top_products, x='Revenue', y='ProductName', orientation='h', title="Top 10 Products")
st.plotly_chart(fig_products)

# --- Revenue by Country Choropleth Map ---
country_revenue = df.groupby('Country')['Revenue'].sum().reset_index()
fig_map = px.choropleth(
    country_revenue,
    locations='Country',
    locationmode='country names',
    color='Revenue',
    title="Revenue by Country"
)
st.plotly_chart(fig_map)
