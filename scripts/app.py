import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Executive E-commerce Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊"
)

# ==============================
# CUSTOM LIGHT THEME (WHITE BACKGROUND)
# ==============================
st.markdown("""
<style>
body { background-color: #ffffff; color: #374151; }
h1, h2, h3, h4, h5 { color: #111827; font-family: 'Inter', sans-serif; }
.main { background-color: #ffffff; }
[data-testid="stSidebar"] { background-color: #f9fafb; color: #374151; }
hr { border-color: #e5e7eb; }
.markdown-box {
    padding: 14px 18px;
    border-radius: 8px;
    margin: 6px 0;
    font-weight: 600;
    font-size: 15px;
}
.green { background: #ecfdf5; color: #065f46; border-left: 4px solid #059669; }
.orange { background: #fff7ed; color: #92400e; border-left: 4px solid #d97706; }
.blue { background: #eff6ff; color: #1e3a8a; border-left: 4px solid #3b82f6; }
.purple { background: #f5f3ff; color: #5b21b6; border-left: 4px solid #6d28d9; }
.pink { background: #fdf2f8; color: #9d174d; border-left: 4px solid #db2777; }
</style>
""", unsafe_allow_html=True)

# ==============================
# HEADER
# ==============================
st.markdown("""
<div style='text-align:center; padding:40px 0 30px 0; background:#f3f4f6; border-radius:16px; margin-bottom:30px;'>
    <h1 style='font-size:42px; margin-bottom:12px; color:#1E3A8A;'>📊 Executive E-Commerce Dashboard</h1>
    <p style='font-size:16px; color:#6B7280;'>Real-Time Business Intelligence & Advanced Analytics</p>
</div>
""", unsafe_allow_html=True)

# ==============================
# SIMULATED METRICS (for design)
# ==============================
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

tab1, tab2, tab3 = st.tabs(["🔔 SMART ALERTS", "📈 FORECAST", "📄 REPORT"])

# --- TAB 1: SMART ALERTS ---
with tab1:
    st.markdown("### <span style='color:#DB2777;'>📉 Performance Alerts</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='markdown-box green'>✅ Revenue grew {metrics['revenue_delta']:.1f}%</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='markdown-box green'>✅ Customer base grew {metrics['customers_delta']:.1f}%</div>", unsafe_allow_html=True)

    st.markdown("### <span style='color:#D97706;'>📊 Threshold Monitoring</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='markdown-box green'>✅ AOV (${metrics['avg_order_value']:.2f}) exceeds target</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='markdown-box blue'>ℹ️ Top 5 customers: {top_5_revenue_pct:.1f}% of revenue</div>", unsafe_allow_html=True)

    st.markdown("### <span style='color:#059669;'>🎯 Recommendations</span>", unsafe_allow_html=True)
    st.markdown("<div class='markdown-box blue'>✅ All metrics performing well!</div>", unsafe_allow_html=True)

# --- TAB 2: FORECAST ---
with tab2:
    st.markdown("### 📈 Forecast (Example)")
    st.markdown("<div class='markdown-box purple'>📊 Future trend forecast visualization will appear here.</div>", unsafe_allow_html=True)

# --- TAB 3: REPORT ---
with tab3:
    st.markdown("### 📄 Executive PDF Report")
    st.markdown("<div class='markdown-box orange'>📋 Downloadable report generator placeholder.</div>", unsafe_allow_html=True)

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.markdown("""
<div style='text-align:center; padding:20px; background:#f9fafb; border-radius:10px;'>
    <p style='color:#6B7280; font-size:13px;'>Executive Dashboard v3.0 — Built with Streamlit & Plotly</p>
</div>
""", unsafe_allow_html=True)
