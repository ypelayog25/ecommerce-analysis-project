import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ==============================
# 🔧 PAGE CONFIGURATION
# ==============================
st.set_page_config(
    page_title="E-commerce Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==============================
# 🎨 GLOBAL STYLE (CSS)
# ==============================
st.markdown("""
<style>
/* ----------- GENERAL ----------- */
* {
    font-family: 'Inter', sans-serif;
    box-sizing: border-box;
}

.stApp {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    color: #E5E7EB;
}

/* ----------- TITLES ----------- */
h1, h2, h3 {
    font-weight: 800;
    letter-spacing: -0.02em;
}

h1 {
    color: #FFFFFF !important;
}

h2, h3 {
    color: rgb(240, 245, 255) !important; /* bright text for contrast */
}

h4 {
    color: rgb(212, 225, 255) !important; /* softer blue for subheaders */
    font-weight: 600 !important;
}

/* ----------- KPI METRICS ----------- */
[data-testid="stMetricLabel"] {
    color: #E0E7FF !important;
    font-weight: 600 !important;
}
[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-weight: 800 !important;
}
[data-testid="stMetricDelta"] {
    color: #F9FAFB !important;
    font-weight: 700 !important;
}

/* ----------- ALERTS / BLUE CARDS ----------- */
.stAlert, .stSuccess, .stWarning, .stInfo, .stError {
    color: rgb(255, 255, 255) !important;
    font-weight: 600 !important;
    letter-spacing: 0.2px;
}

/* ----------- PLOTLY AXIS / LEGENDS ----------- */
.plotly .xtick text,
.plotly .ytick text,
.plotly .legend text,
.plotly .axis-title {
    fill: #F8FAFC !important;
    font-weight: 600 !important;
}

/* ----------- BUTTONS ----------- */
.stButton>button {
    background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
    color: #FFFFFF !important;
    font-weight: 600;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1.2rem;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
    box-shadow: 0 0 10px rgba(59,130,246,0.5);
}

/* ----------- TABLES ----------- */
.dataframe thead tr th {
    background: #1E293B !important;
    color: #FFFFFF !important;
}
.dataframe tbody tr {
    background: #334155 !important;
    color: #FFFFFF !important;
}
.dataframe tbody tr:hover {
    background: #475569 !important;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# 📦 LOAD DATA
# ==============================
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/ypelayog25/ecommerce-analysis-project/main/data/processed/ecommerce_dataset_10000_cleaned.csv"
    df = pd.read_csv(url)
    
    # ✅ Create TotalPrice safely regardless of column naming
    if "TotalPrice" not in df.columns:
        quantity_col = next((c for c in df.columns if "quantity" in c.lower()), None)
        price_col = next((c for c in df.columns if "unit" in c.lower() or "price" in c.lower()), None)
        
        if quantity_col and price_col:
            df["TotalPrice"] = df[quantity_col] * df[price_col]
        else:
            st.error("❌ Could not find Quantity or Unit Price columns in dataset.")
            st.stop()
    return df

df = load_data()

# ==============================
# 🧭 DASHBOARD HEADER
# ==============================
st.markdown("### 🛒 E-COMMERCE DASHBOARD")
st.markdown("#### Comprehensive analytics on revenue, orders, and customer insights.")

# ==============================
# 📈 KPI SECTION
# ==============================
st.markdown("## KEY PERFORMANCE INDICATORS")

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
    avg_quantity = df[quantity_col].mean() if "quantity_col" in locals() else np.nan
    st.metric(label="Avg. Quantity per Order", value=f"{avg_quantity:.2f}")

# ==============================
# 💰 REVENUE TREND
# ==============================
st.markdown("## REVENUE TREND")

if "InvoiceDate" in df.columns:
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)
    monthly_revenue = df.groupby("Month")["TotalPrice"].sum().reset_index()

    fig_revenue = px.line(
        monthly_revenue,
        x="Month",
        y="TotalPrice",
        title="Monthly Revenue Trend",
        template="plotly_dark",
        markers=True,
    )
    fig_revenue.update_traces(line_color="#60A5FA", line_width=3)
    fig_revenue.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue (USD)",
        font=dict(color="#F8FAFC", size=12),
        title_font=dict(size=18, color="#FFFFFF", family="Inter")
    )
    st.plotly_chart(fig_revenue, use_container_width=True)

# ==============================
# 🌍 TOP COUNTRIES
# ==============================
st.markdown("## TOP COUNTRIES BY REVENUE")

if "Country" in df.columns:
    country_revenue = (
        df.groupby("Country")["TotalPrice"]
        .sum()
        .reset_index()
        .sort_values("TotalPrice", ascending=False)
        .head(5)
    )

    fig_country = px.bar(
        country_revenue,
        x="Country",
        y="TotalPrice",
        color="TotalPrice",
        color_continuous_scale=["#3B82F6", "#60A5FA"],
        title="Top 5 Countries by Revenue",
        template="plotly_dark",
    )
    fig_country.update_layout(
        xaxis_title="Country",
        yaxis_title="Revenue (USD)",
        font=dict(color="#F8FAFC", size=12),
        title_font=dict(size=18, color="#FFFFFF", family="Inter"),
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_country, use_container_width=True)

# ==============================
# 🛍️ TOP PRODUCTS
# ==============================
st.markdown("## TOP PRODUCTS")

if "Description" in df.columns:
    top_products = (
        df.groupby("Description")["TotalPrice"]
        .sum()
        .reset_index()
        .sort_values("TotalPrice", ascending=False)
        .head(10)
    )

    fig_products = px.bar(
        top_products,
        x="TotalPrice",
        y="Description",
        orientation="h",
        color="TotalPrice",
        color_continuous_scale=["#1E3A8A", "#3B82F6"],
        title="Top 10 Products by Revenue",
        template="plotly_dark",
    )
    fig_products.update_layout(
        xaxis_title="Revenue (USD)",
        yaxis_title="Product Description",
        font=dict(color="#F8FAFC", size=12),
        title_font=dict(size=18, color="#FFFFFF", family="Inter"),
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_products, use_container_width=True)

# ==============================
# 👥 CUSTOMER INSIGHTS
# ==============================
st.markdown("## CUSTOMER INSIGHTS")

if "CustomerID" in df.columns:
    customer_spending = (
        df.groupby("CustomerID")["TotalPrice"]
        .sum()
        .reset_index()
        .sort_values("TotalPrice", ascending=False)
        .head(10)
    )

    fig_customers = px.bar(
        customer_spending,
        x="CustomerID",
        y="TotalPrice",
        color="TotalPrice",
        color_continuous_scale=["#0EA5E9", "#60A5FA"],
        title="Top 10 Customers by Spending",
        template="plotly_dark",
    )
    fig_customers.update_layout(
        xaxis_title="Customer ID",
        yaxis_title="Total Spending (USD)",
        font=dict(color="#F8FAFC", size=12),
        title_font=dict(size=18, color="#FFFFFF", family="Inter"),
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_customers, use_container_width=True)

# ==============================
# 🔚 FOOTER
# ==============================
st.markdown("""
<hr style="border: 1px solid rgba(59,130,246,0.2); margin-top: 2rem; margin-bottom: 1rem;">
<div style="text-align: center; color: #94A3B8; font-size: 0.9rem;">
© 2025 Yenismara Pelayo — E-commerce Analytics Dashboard
</div>
""", unsafe_allow_html=True)
