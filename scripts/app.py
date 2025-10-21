import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from components import style  # Import the global dark theme

# =========================
# Apply the custom theme
# =========================
style.apply_theme()
plotly_template = style.get_plotly_template()

# =========================
# Page Configuration
# =========================
st.set_page_config(
    page_title="E-commerce Dashboard",
    page_icon="🛒",
    layout="wide"
)

# =========================
# Load Data
# =========================
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/ypelayog25/ecommerce-analysis-project/main/data/processed/ecommerce_dataset_10000_cleaned.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

# =========================
# Header
# =========================
style.create_header(
    title="E-COMMERCE DASHBOARD",
    subtitle="Comprehensive analytics on revenue, orders, and customer insights.",
    breadcrumb="Home / Analytics / Dashboard"
)

# =========================
# KPI Section
# =========================
style.create_section_header("KEY PERFORMANCE INDICATORS")

col1, col2, col3, col4 = st.columns(4)
with col1:
    total_revenue = df["TotalPrice"].sum()
    st.metric(label="Total Revenue", value=f"${total_revenue:,.0f}")

with col2:
    avg_order = df["TotalPrice"].mean()
    st.metric(label="Average Order Value", value=f"${avg_order:,.2f}")

with col3:
    unique_customers = df["CustomerID"].nunique()
    st.metric(label="Unique Customers", value=f"{unique_customers:,}")

with col4:
    avg_quantity = df["Quantity"].mean()
    st.metric(label="Avg. Quantity per Order", value=f"{avg_quantity:.2f}")

# =========================
# Revenue Trend
# =========================
style.create_section_header("REVENUE TREND")

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["Month"] = df["InvoiceDate"].dt.to_period("M")
monthly_revenue = df.groupby("Month")["TotalPrice"].sum().reset_index()
monthly_revenue["Month"] = monthly_revenue["Month"].astype(str)

fig_revenue = px.line(
    monthly_revenue,
    x="Month",
    y="TotalPrice",
    title="Monthly Revenue Trend",
    template=plotly_template,
    markers=True
)
fig_revenue.update_traces(line_color=style.COLORS["primary"], line_width=3)
fig_revenue.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue (USD)",
    title_font=dict(size=18, color="#FFFFFF", family="Inter"),
    font=dict(color="#F8FAFC", size=12)
)
st.plotly_chart(fig_revenue, use_container_width=True)

# =========================
# Top 5 Countries by Revenue
# =========================
style.create_section_header("TOP COUNTRIES BY REVENUE")

country_revenue = df.groupby("Country")["TotalPrice"].sum().reset_index().sort_values(by="TotalPrice", ascending=False).head(5)
fig_country = px.bar(
    country_revenue,
    x="Country",
    y="TotalPrice",
    title="Top 5 Countries by Revenue",
    template=plotly_template,
    color="TotalPrice",
    color_continuous_scale=["#3B82F6", "#60A5FA"]
)
fig_country.update_layout(
    xaxis_title="Country",
    yaxis_title="Revenue (USD)",
    title_font=dict(size=18, color="#FFFFFF", family="Inter"),
    font=dict(color="#F8FAFC", size=12),
    coloraxis_showscale=False
)
st.plotly_chart(fig_country, use_container_width=True)

# =========================
# Product Performance
# =========================
style.create_section_header("TOP PRODUCTS")

top_products = (
    df.groupby("Description")["TotalPrice"]
    .sum()
    .reset_index()
    .sort_values(by="TotalPrice", ascending=False)
    .head(10)
)

fig_products = px.bar(
    top_products,
    x="TotalPrice",
    y="Description",
    orientation="h",
    title="Top 10 Products by Revenue",
    template=plotly_template,
    color="TotalPrice",
    color_continuous_scale=["#1E3A8A", "#3B82F6"]
)
fig_products.update_layout(
    xaxis_title="Revenue (USD)",
    yaxis_title="Product Description",
    title_font=dict(size=18, color="#FFFFFF", family="Inter"),
    font=dict(color="#F8FAFC", size=12),
    coloraxis_showscale=False
)
st.plotly_chart(fig_products, use_container_width=True)

# =========================
# Customer Insights
# =========================
style.create_section_header("CUSTOMER INSIGHTS")

customer_spending = (
    df.groupby("CustomerID")["TotalPrice"]
    .sum()
    .reset_index()
    .sort_values(by="TotalPrice", ascending=False)
    .head(10)
)

fig_customers = px.bar(
    customer_spending,
    x="CustomerID",
    y="TotalPrice",
    title="Top 10 Customers by Spending",
    template=plotly_template,
    color="TotalPrice",
    color_continuous_scale=["#0EA5E9", "#60A5FA"]
)
fig_customers.update_layout(
    xaxis_title="Customer ID",
    yaxis_title="Total Spending (USD)",
    title_font=dict(size=18, color="#FFFFFF", family="Inter"),
    font=dict(color="#F8FAFC", size=12),
    coloraxis_showscale=False
)
st.plotly_chart(fig_customers, use_container_width=True)

# =========================
# Footer
# =========================
st.markdown(
    """
    <hr style="border: 1px solid rgba(59,130,246,0.2); margin-top: 2rem; margin-bottom: 1rem;">
    <div style="text-align: center; color: #94A3B8; font-size: 0.9rem;">
        © 2025 Yenismara Pelayo — E-commerce Analytics Dashboard
    </div>
    """,
    unsafe_allow_html=True
)
