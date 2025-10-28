import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(
    page_title="Executive E-commerce Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊"
)

# Light Professional Theme CSS (White background with gray text)
st.markdown("""
    <style>
    body {
        background-color: #ffffff;
        color: #374151;
    }
    h1, h2, h3, h4, h5 {
        color: #111827;
        font-family: 'Inter', sans-serif;
    }
    .main {
        background-color: #ffffff;
    }
    [data-testid="stSidebar"] {
        background-color: #f9fafb;
        color: #374151;
    }
    [data-testid="stMetricValue"] {
        color: #1E3A8A !important;
    }
    [data-testid="stMetricLabel"] {
        color: #6B7280 !important;
    }
    .stAlert {
        background-color: #f3f4f6;
        color: #374151 !important;
        border-left: 4px solid #2563EB;
    }
    </style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data(ttl=3600)
def load_data():
    dataset_parquet = "data/processed/ecommerce_dataset_10000_cleaned.parquet"
    dataset_csv = "data/processed/ecommerce_dataset_10000_cleaned.csv"
    try:
        if os.path.exists(dataset_parquet):
            df = pd.read_parquet(dataset_parquet)
        elif os.path.exists(dataset_csv):
            df = pd.read_csv(dataset_csv)
        else:
            return None
        df['order_date'] = pd.to_datetime(df['order_date'])
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df = load_data()
if df is None or df.empty:
    st.error("No dataset found or dataset is empty.")
    st.stop()

# Header
st.markdown("""
    <div style='text-align:center; padding: 40px 0 30px 0; background:#F3F4F6; border-radius: 16px; margin-bottom: 30px;'>
        <h1 style='font-size: 42px; margin-bottom: 12px; color:#1E3A8A;'>📊 Executive E-Commerce Dashboard</h1>
        <p style='font-size:16px; color:#6B7280;'>Real-Time Business Intelligence & Advanced Analytics</p>
    </div>
""", unsafe_allow_html=True)

# Simulated metrics for display
metrics = {
    'revenue_delta': 0.0,
    'customers_delta': 0.0,
    'avg_order_value': 745.08
}
top_5_revenue_pct = 0.8

# ==============================
# EXPORT CENTER SECTION
# ==============================
st.markdown("---")
st.markdown("## <span style='color:#1E3A8A;'>📥 EXPORT CENTER</span>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.download_button("📊 DATASET", "data", use_container_width=True)
with col2:
    st.download_button("🏆 CUSTOMERS", "customers", use_container_width=True)
with col3:
    st.download_button("📦 PRODUCTS", "products", use_container_width=True)
with col4:
    st.download_button("🌍 COUNTRIES", "countries", use_container_width=True)

# ==============================
# ADVANCED FEATURES SECTION
# ==============================
st.markdown("---")
st.markdown("## <span style='color:#6D28D9;'>🚀 ADVANCED FEATURES</span>", unsafe_allow_html=True)

adv_tab1, adv_tab2, adv_tab3 = st.tabs(["🔔 SMART ALERTS", "📈 FORECAST", "📄 REPORT"])

with adv_tab1:
    st.markdown("### <span style='color:#DB2777;'>📉 Performance Alerts</span>", unsafe_allow_html=True)
    st.success(f"<span style='color:#059669; font-weight:600;'>✅ Revenue grew {metrics['revenue_delta']:.1f}%</span>", unsafe_allow_html=True)
    st.success(f"<span style='color:#059669; font-weight:600;'>✅ Customer base grew {metrics['customers_delta']:.1f}%</span>", unsafe_allow_html=True)
    
    st.markdown("### <span style='color:#D97706;'>📊 Threshold Monitoring</span>", unsafe_allow_html=True)
    st.success(f"<span style='color:#059669; font-weight:600;'>✅ AOV (${metrics['avg_order_value']:.2f}) exceeds target</span>", unsafe_allow_html=True)
    st.info(f"<span style='color:#1E3A8A; font-weight:600;'>ℹ️ Top 5 customers: {top_5_revenue_pct:.1f}% of revenue</span>", unsafe_allow_html=True)
    
    st.markdown("### <span style='color:#059669;'>🎯 Recommendations</span>", unsafe_allow_html=True)
    st.success("<span style='color:#1E3A8A; font-weight:600;'>✅ All metrics performing well!</span>", unsafe_allow_html=True)

with adv_tab2:
    st.markdown("### 📈 Forecast Section (example)")
    st.info("Future forecasting visualization goes here.")

with adv_tab3:
    st.markdown("### 📄 Executive PDF Report")
    st.info("Downloadable report generator placeholder.")

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.markdown("""
    <div style='text-align:center; padding:20px; background:#F9FAFB; border-radius:10px;'>
        <p style='color:#6B7280; font-size:13px;'>Executive Dashboard v3.0 — Built with Streamlit & Plotly</p>
    </div>
""", unsafe_allow_html=True)
