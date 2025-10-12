"""
Professional Executive E-commerce Dashboard (Streamlit)
Premium responsive design with advanced features:
- PDF Export, Smart Alerts, ML Predictions, YoY Comparison, Save Configs
"""

import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# -----------------------
# Page Configuration
# -----------------------
st.set_page_config(
    page_title="Executive E-commerce Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊"
)

# -----------------------
# Professional Dark Theme CSS with Mobile Responsive
# -----------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, rgb(15, 12, 41) 0%, rgb(48, 43, 99) 50%, rgb(36, 36, 62) 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgb(26, 26, 46) 0%, rgb(22, 33, 62) 100%);
    }
    
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {
        color: rgb(232, 234, 246) !important;
    }
    
    [data-testid="stSidebar"] div[data-testid="stExpander"] {
        background-color: rgb(45, 45, 68) !important;
        border: 1px solid rgba(79, 195, 247, 0.3);
    }
    
    [data-testid="stSidebar"] div[data-testid="stExpander"] > div > div {
        background-color: rgb(58, 58, 82) !important;
        padding: 15px;
        border-radius: 8px;
    }
    
    [data-testid="stSidebar"] details[data-testid="stExpander"] summary {
        background-color: rgb(45, 45, 68) !important;
        padding: 12px 15px !important;
        border-radius: 8px;
    }
    
    [data-testid="stSidebar"] details[open] > summary {
        background-color: rgb(58, 58, 82) !important;
        border-bottom: 1px solid rgba(79, 195, 247, 0.2);
        margin-bottom: 10px;
    }
    
    [data-testid="stSidebar"] input[type="date"],
    [data-testid="stSidebar"] input[type="text"] {
        background-color: rgb(45, 45, 68) !important;
        color: rgb(255, 255, 255) !important;
        border: 1px solid rgba(79, 195, 247, 0.3) !important;
        border-radius: 8px;
        padding: 10px;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] {
        background-color: rgb(45, 45, 68) !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: rgb(45, 45, 68) !important;
        color: rgb(255, 255, 255) !important;
    }
    
    h1 {
        color: rgb(255, 255, 255) !important;
        font-weight: 800 !important;
    }
    
    h2 {
        color: rgb(224, 224, 224) !important;
        font-weight: 700 !important;
    }
    
    h3 {
        color: rgb(176, 176, 176) !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 32px !important;
        font-weight: 800 !important;
        color: rgb(79, 195, 247) !important;
        text-shadow: 0 2px 8px rgba(79, 195, 247, 0.3);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 13px !important;
        font-weight: 600 !important;
        color: rgb(197, 202, 233) !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 13px !important;
        font-weight: 600 !important;
    }
    
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgb(94, 53, 177) 0%, rgb(81, 45, 168) 100%);
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.08);
        transition: all 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 32px rgba(94, 53, 177, 0.5);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: rgba(26, 26, 46, 0.7);
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: rgba(255, 255, 255, 0.04);
        border-radius: 8px;
        color: rgb(176, 190, 197);
        font-weight: 600;
        font-size: 14px;
        padding: 0 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        white-space: nowrap;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgb(94, 53, 177) 0%, rgb(81, 45, 168) 100%);
        color: rgb(255, 255, 255) !important;
        box-shadow: 0 4px 16px rgba(94, 53, 177, 0.4);
    }
    
    .stButton button {
        background: linear-gradient(135deg, rgb(94, 53, 177) 0%, rgb(81, 45, 168) 100%);
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 13px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(94, 53, 177, 0.3);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(94, 53, 177, 0.5);
    }
    
    .stDownloadButton button {
        background: linear-gradient(135deg, rgb(38, 198, 218) 0%, rgb(0, 172, 193) 100%);
        color: rgb(255, 255, 255) !important;
        font-weight: 700;
    }
    
    .stDownloadButton button:hover {
        box-shadow: 0 6px 20px rgba(38, 198, 218, 0.5);
    }
    
    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }
    
    div[data-testid="stExpander"] summary {
        color: rgb(224, 224, 224) !important;
        font-weight: 600;
    }
    
    div[data-testid="stExpander"] p,
    div[data-testid="stExpander"] label {
        color: rgb(197, 202, 233) !important;
    }
    
    p, span, label {
        color: rgb(176, 190, 197) !important;
        font-size: 14px;
    }
    
    .stSlider [data-baseweb="slider"] {
        background-color: rgba(94, 53, 177, 0.3);
    }
    
    [data-baseweb="select"] {
        background-color: rgba(45, 45, 68, 0.8);
        border-radius: 8px;
    }
    
    [data-baseweb="select"] > div {
        color: rgb(224, 224, 224) !important;
    }
    
    [data-testid="stDataFrame"] {
        background-color: rgba(26, 26, 46, 0.7);
        border-radius: 12px;
        overflow: hidden;
    }
    
    [data-testid="stDataFrame"] * {
        color: rgb(224, 224, 224) !important;
    }
    
    .stAlert {
        background-color: rgba(94, 53, 177, 0.15);
        border-radius: 12px;
        border-left: 4px solid rgb(94, 53, 177);
        color: rgb(224, 224, 224) !important;
    }
    
    hr {
        border-color: rgba(255, 255, 255, 0.1);
        margin: 25px 0;
    }
    
    [data-testid="stCheckbox"] label {
        color: rgb(224, 224, 224) !important;
    }
    
    @keyframes glow {
        0%, 100% { 
            text-shadow: 0 0 15px rgba(79, 195, 247, 0.4), 0 0 30px rgba(79, 195, 247, 0.2); 
        }
        50% { 
            text-shadow: 0 0 25px rgba(79, 195, 247, 0.6), 0 0 50px rgba(79, 195, 247, 0.3); 
        }
    }
    
    .glowing-title {
        animation: glow 2s ease-in-out infinite;
    }
    
    .card-container {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.3);
        margin: 12px 0;
    }
    
    .stMarkdown h3 {
        color: rgb(79, 195, 247) !important;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 12px;
        padding-left: 12px;
        border-left: 3px solid rgb(79, 195, 247);
    }
    
    @media (max-width: 768px) {
        h1 {
            font-size: 28px !important;
        }
        
        h2 {
            font-size: 22px !important;
        }
        
        h3 {
            font-size: 18px !important;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 24px !important;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 11px !important;
        }
        
        div[data-testid="metric-container"] {
            padding: 15px;
            margin-bottom: 10px;
        }
        
        .stTabs [data-baseweb="tab"] {
            font-size: 12px !important;
            padding: 0 12px;
            height: 40px;
        }
        
        .stButton button,
        .stDownloadButton button {
            width: 100%;
            font-size: 12px !important;
            padding: 12px 16px;
        }
        
        .card-container {
            padding: 15px;
            margin: 10px 0;
        }
        
        [data-testid="stSidebar"] {
            width: 100% !important;
        }
    }
    
    @media (min-width: 769px) and (max-width: 1024px) {
        [data-testid="stMetricValue"] {
            font-size: 28px !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            font-size: 13px !important;
            padding: 0 16px;
        }
    }
    
    .element-container {
        color: rgb(224, 224, 224) !important;
    }
    
    .js-plotly-plot .plotly {
        color: rgb(224, 224, 224) !important;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------
# Data Loading with Caching
# -----------------------
@st.cache_data(ttl=3600)
def load_data():
    """Load and cache dataset with error handling"""
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
        df['year_month'] = df['order_date'].dt.to_period('M')
        df['year'] = df['order_date'].dt.year
        df['month'] = df['order_date'].dt.month
        df['day_of_week'] = df['order_date'].dt.day_name()
        
        return df
    except Exception as e:
        st.error(f"⚠️ Error loading data: {e}")
        return None

df = load_data()

if df is None or df.empty:
    st.error("❌ No dataset found or dataset is empty.")
    st.stop()

# -----------------------
# Professional Header with Better Visibility
# -----------------------
st.markdown("""
    <div style='text-align:center; padding: 35px 0 25px 0; background: rgba(26, 26, 46, 0.4); border-radius: 20px; margin-bottom: 20px; border: 1px solid rgba(79, 195, 247, 0.2);'>
        <h1 style='font-size: 46px; margin-bottom: 10px; color: rgb(255, 255, 255); font-weight: 800; text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5);'>
            📊 EXECUTIVE E-COMMERCE DASHBOARD
        </h1>
        <p style='font-size: 17px; color: rgb(197, 202, 233); font-weight: 500; letter-spacing: 2px; text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.3);'>
            Real-Time Business Intelligence & Advanced Analytics
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<hr style='margin: 15px 0; border: 1px solid rgba(79, 195, 247, 0.3);'>", unsafe_allow_html=True)

# -----------------------
# Professional Sidebar
# -----------------------
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 15px 0;'>
            <div style='font-size: 48px; margin-bottom: 8px;'>⚡</div>
            <h2 style='margin: 0; font-size: 22px; color: rgb(79, 195, 247);'>
                CONTROL CENTER
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border-color: rgba(79, 195, 247, 0.3);'>", unsafe_allow_html=True)
    
    with st.expander("📅 DATE RANGE FILTER", expanded=True):
        date_col1, date_col2 = st.columns(2)
        
        min_date = df['order_date'].min().date()
        max_date = df['order_date'].max().date()
        
        with date_col1:
            st.markdown("<p style='color: rgb(224, 224, 224); font-size: 12px; margin-bottom: 5px;'>From Date</p>", unsafe_allow_html=True)
            start_date = st.date_input("From", min_date, min_value=min_date, max_value=max_date, label_visibility="collapsed")
        with date_col2:
            st.markdown("<p style='color: rgb(224, 224, 224); font-size: 12px; margin-bottom: 5px;'>To Date</p>", unsafe_allow_html=True)
            end_date = st.date_input("To", max_date, min_value=min_date, max_value=max_date, label_visibility="collapsed")
        
        st.markdown("<p style='color: rgb(197, 202, 233); font-weight: 600; margin-top: 15px; margin-bottom: 8px;'>⚡ Quick Filters</p>", unsafe_allow_html=True)
        col_q1, col_q2 = st.columns(2)
        with col_q1:
            if st.button("Last 30D", use_container_width=True):
                start_date = max_date - timedelta(days=30)
            if st.button("Quarter", use_container_width=True):
                start_date = max_date - timedelta(days=90)
        with col_q2:
            if st.button("Last 7D", use_container_width=True):
                start_date = max_date - timedelta(days=7)
            if st.button("YTD", use_container_width=True):
                start_date = datetime(max_date.year, 1, 1).date()
    
    with st.expander("🌍 GEOGRAPHIC FILTER", expanded=True):
        countries = sorted(df['country'].dropna().unique())
        select_all = st.checkbox("✅ Select All Countries", value=True)
        
        if select_all:
            selected_countries = countries
        else:
            selected_countries = st.multiselect("Choose Countries", countries, default=countries[:3])
    
    with st.expander("⚙️ DISPLAY SETTINGS", expanded=False):
        top_n = st.slider("Top N Items", 5, 50, 10, 5)
        chart_theme = st.selectbox("Chart Theme", ["plotly_dark", "plotly_white", "seaborn", "ggplot2"], key="theme_selector")
        
        if 'selected_theme' not in st.session_state:
            st.session_state.selected_theme = chart_theme
        else:
            st.session_state.selected_theme = chart_theme
    
    st.markdown("<hr style='border-color: rgba(79, 195, 247, 0.2); margin: 25px 0;'>", unsafe_allow_html=True)
    
    st.markdown("<p style='color: rgb(197, 202, 233); font-weight: 600; margin-bottom: 10px;'>💾 PREFERENCES</p>", unsafe_allow_html=True)
    
    if st.button("💾 Save Current Filters", use_container_width=True):
        st.session_state.saved_filters = {
            'start_date': start_date,
            'end_date': end_date,
            'countries': selected_countries,
            'top_n': top_n
        }
        st.success("✅ Filters saved!")
    
    if 'saved_filters' in st.session_state:
        if st.button("🔄 Load Saved Filters", use_container_width=True):
            saved = st.session_state.saved_filters
            st.info(f"📌 Saved: {saved['start_date']} to {saved['end_date']}")
    
    st.markdown("<hr style='border-color: rgba(79, 195, 247, 0.2); margin: 25px 0;'>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='text-align: center; padding: 15px; background: rgba(79, 195, 247, 0.1); border-radius: 12px; border: 1px solid rgba(79, 195, 247, 0.3);'>
            <p style='margin: 0; font-size: 11px; color: rgb(79, 195, 247); font-weight: 600;'>💼 PORTFOLIO PROJECT</p>
            <p style='margin: 5px 0 0 0; font-size: 10px; color: rgb(176, 190, 197);'>Built with Streamlit & Plotly</p>
        </div>
    """, unsafe_allow_html=True)

# Filter data
start_date_dt = pd.to_datetime(start_date)
end_date_dt = pd.to_datetime(end_date)
df_filtered = df[
    (df['country'].isin(selected_countries)) &
    (df['order_date'] >= start_date_dt) &
    (df['order_date'] <= end_date_dt)
].copy()

if df_filtered.empty:
    st.warning("⚠️ No data available for selected filters. Please adjust your filters.")
    st.stop()

# -----------------------
# Calculate Metrics
# -----------------------
@st.cache_data
def calculate_metrics(df_current, df_all):
    """Calculate KPIs with period-over-period comparison"""
    total_revenue = df_current['total_price'].sum()
    total_orders = df_current['order_id'].nunique()
    unique_customers = df_current['customer_id'].nunique()
    total_quantity = df_current['quantity'].sum()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    
    date_diff = (df_current['order_date'].max() - df_current['order_date'].min()).days
    prev_start = df_current['order_date'].min() - timedelta(days=date_diff)
    prev_end = df_current['order_date'].min()
    
    df_prev = df_all[
        (df_all['order_date'] >= prev_start) &
        (df_all['order_date'] < prev_end)
    ]
    
    prev_revenue = df_prev['total_price'].sum()
    prev_orders = df_prev['order_id'].nunique()
    prev_customers = df_prev['customer_id'].nunique()
    
    revenue_delta = ((total_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
    orders_delta = ((total_orders - prev_orders) / prev_orders * 100) if prev_orders > 0 else 0
    customers_delta = ((unique_customers - prev_customers) / prev_customers * 100) if prev_customers > 0 else 0
    
    return {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'unique_customers': unique_customers,
        'total_quantity': total_quantity,
        'avg_order_value': avg_order_value,
        'revenue_delta': revenue_delta,
        'orders_delta': orders_delta,
        'customers_delta': customers_delta
    }

metrics = calculate_metrics(df_filtered, df)

# -----------------------
# Professional KPI Cards
# -----------------------
st.markdown("<h3 style='color: rgb(79, 195, 247); margin-bottom: 15px;'>🎯 KEY PERFORMANCE INDICATORS</h3>", unsafe_allow_html=True)
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.metric(
        label="💰 REVENUE",
        value=f"${metrics['total_revenue']:,.0f}",
        delta=f"{metrics['revenue_delta']:.1f}%"
    )

with kpi2:
    st.metric(
        label="🛒 ORDERS",
        value=f"{metrics['total_orders']:,}",
        delta=f"{metrics['orders_delta']:.1f}%"
    )

with kpi3:
    st.metric(
        label="👥 CUSTOMERS",
        value=f"{metrics['unique_customers']:,}",
        delta=f"{metrics['customers_delta']:.1f}%"
    )

with kpi4:
    st.metric(
        label="📦 UNITS",
        value=f"{metrics['total_quantity']:,}"
    )

with kpi5:
    st.metric(
        label="💵 AVG ORDER",
        value=f"${metrics['avg_order_value']:.2f}"
    )

st.markdown("<hr style='margin: 25px 0; border: 1px solid rgba(79, 195, 247, 0.2);'>", unsafe_allow_html=True)

# -----------------------
# Helper for Plotly Styling
# -----------------------
def style_fig(fig, title="", title_font=20, axis_font=12):
    """Apply professional dark theme styling to Plotly figures"""
    theme_to_use = st.session_state.get('selected_theme', 'plotly_dark')
    
    fig.update_layout(
        title=dict(
            text=title, 
            font=dict(size=title_font, color="rgb(79, 195, 247)", family="Inter"),
            x=0.5,
            xanchor='center'
        ),
        font=dict(size=axis_font, color="rgb(176, 190, 197)", family="Inter"),
        margin=dict(l=50, r=50, t=70, b=50),
        template=theme_to_use,
        hovermode='x unified',
        plot_bgcolor='rgba(26, 26, 46, 0.5)' if theme_to_use == 'plotly_dark' else 'rgba(255, 255, 255, 0.9)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        hoverlabel=dict(
            bgcolor="rgba(94, 53, 177, 0.9)",
            font_size=12,
            font_family="Inter",
            font_color="rgb(255, 255, 255)"
        )
    )
    
    if theme_to_use in ['plotly_white', 'seaborn', 'ggplot2']:
        fig.update_xaxes(
            showgrid=True, 
            gridwidth=0.4, 
            gridcolor='rgba(0, 0, 0, 0.1)',
            showline=True, 
            linewidth=1, 
            linecolor='rgba(0, 0, 0, 0.2)',
            title_font=dict(color="rgb(44, 62, 80)")
        )
        fig.update_yaxes(
            showgrid=True, 
            gridwidth=0.4, 
            gridcolor='rgba(0, 0, 0, 0.1)',
            title_font=dict(color="rgb(44, 62, 80)")
        )
    else:
        fig.update_xaxes(
            showgrid=True, 
            gridwidth=0.4, 
            gridcolor='rgba(255, 255, 255, 0.08)',
            showline=True, 
            linewidth=1, 
            linecolor='rgba(255, 255, 255, 0.15)',
            title_font=dict(color="rgb(197, 202, 233)")
        )
        fig.update_yaxes(
            showgrid=True, 
            gridwidth=0.4, 
            gridcolor='rgba(255, 255, 255, 0.08)',
            title_font=dict(color="rgb(197, 202, 233)")
        )
    
    return fig

professional_colors = ['rgb(79, 195, 247)', 'rgb(126, 87, 194)', 'rgb(236, 64, 122)', 'rgb(255, 112, 67)', 'rgb(38, 198, 218)']

# -----------------------
# Dashboard Tabs
# -----------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 REVENUE", 
    "👥 CUSTOMERS", 
    "📦 PRODUCTS", 
    "🌍 GEOGRAPHY",
    "🔬 ADVANCED"
])

# TAB 1: Revenue Analysis
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<h3 style='color: rgb(79, 195, 247);'>📈 REVENUE TREND</h3>", unsafe_allow_html=True)
        
        monthly_revenue = df_filtered.groupby(df_filtered['order_date'].dt.to_period('M'))['total_price'].sum().reset_index()
        monthly_revenue['order_date'] = monthly_revenue['order_date'].dt.to_timestamp()
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=monthly_revenue['order_date'],
            y=monthly_revenue['total_price'],
            mode='lines+markers',
            name='Revenue',
            line=dict(color='rgb(79, 195, 247)', width=3),
            marker=dict(size=8, color='rgb(79, 195, 247)', line=dict(color='rgb(255, 255, 255)', width=1.5)),
            fill='tozeroy',
            fillcolor='rgba(79, 195, 247, 0.15)'
        ))
        
        z = np.polyfit(range(len(monthly_revenue)), monthly_revenue['total_price'], 1)
        p = np.poly1d(z)
        fig_trend.add_trace(go.Scatter(
            x=monthly_revenue['order_date'],
            y=p(range(len(monthly_revenue))),
            mode='lines',
            name='Trend',
            line=dict(color='rgb(236, 64, 122)', width=2.5, dash='dash')
        ))
        
        st.plotly_chart(style_fig(fig_trend, "Monthly Performance"), use_container_width=True)
    
    with col2:
        st.markdown("<h3 style='color: rgb(79, 195, 247);'>🏆 TOP COUNTRIES</h3>", unsafe_allow_html=True)
        country_revenue = df_filtered.groupby('country')['total_price'].sum().nlargest(5).reset_index()
        
        fig_pie = px.pie(
            country_revenue,
            values='total_price',
            names='country',
            hole=0.45,
            color_discrete_sequence=professional_colors
        )
        fig_pie.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            textfont=dict(size=13, family="Inter", color="white"),
            marker=dict(line=dict(color='rgb(255, 255, 255)', width=1.5))
        )
        fig_pie.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='rgb(176, 190, 197)', family="Inter"),
            showlegend=True,
            legend=dict(font=dict(color='rgb(197, 202, 233)', size=11))
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("<h3 style='color: rgb(79, 195, 247); margin-top: 25px;'>📅 WEEKLY PATTERN</h3>", unsafe_allow_html=True)
    dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_revenue = df_filtered.groupby('day_of_week')['total_price'].sum().reindex(dow_order).reset_index()
    
    fig_dow = go.Figure(data=[
        go.Bar(
            x=dow_revenue['day_of_week'],
            y=dow_revenue['total_price'],
            marker=dict(
                color=dow_revenue['total_price'],
                colorscale='Viridis',
                showscale=False,
                line=dict(color='rgba(255, 255, 255, 0.2)', width=1.5)
            ),
            text=[f"${val:,.0f}" for val in dow_revenue['total_price']],
            textposition='outside',
            textfont=dict(size=11, color='rgb(79, 195, 247)')
        )
    ])
    st.plotly_chart(style_fig(fig_dow, "Revenue by Day of Week"), use_container_width=True)

# TAB 2: Customer Intelligence
with tab2:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"<h3 style='color: rgb(79, 195, 247);'>🌟 TOP {top_n} CUSTOMERS</h3>", unsafe_allow_html=True)
        top_customers = df_filtered.groupby('customer_id').agg({
            'total_price': 'sum',
            'order_id': 'nunique'
        }).nlargest(top_n, 'total_price').reset_index()
        top_customers.columns = ['customer_id', 'total_revenue', 'order_count']
        
        fig_customers = go.Figure(data=[
            go.Bar(
                x=top_customers['total_revenue'],
                y=top_customers['customer_id'],
                orientation='h',
                marker=dict(
                    color=top_customers['total_revenue'],
                    colorscale='Plasma',
                    showscale=False,
                    line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
                ),
                text=[f"${val:,.0f}" for val in top_customers['total_revenue']],
                textposition='outside',
                textfont=dict(color='rgb(79, 195, 247)', size=10)
            )
        ])
        st.plotly_chart(style_fig(fig_customers, "Revenue Champions"), use_container_width=True)
    
    with col2:
        st.markdown("<h3 style='color: rgb(79, 195, 247);'>🔄 RETENTION</h3>", unsafe_allow_html=True)
        
        order_frequency = df_filtered.groupby('customer_id')['order_id'].nunique().value_counts().sort_index().reset_index()
        order_frequency.columns = ['orders', 'customer_count']
        
        fig_freq = go.Figure(data=[
            go.Bar(
                x=order_frequency['orders'],
                y=order_frequency['customer_count'],
                marker=dict(
                    color=order_frequency['customer_count'],
                    colorscale='Turbo',
                    showscale=False,
                    line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
                ),
                text=order_frequency['customer_count'],
                textposition='outside',
                textfont=dict(color='rgb(79, 195, 247)', size=10)
            )
        ])
        st.plotly_chart(style_fig(fig_freq, "Order Frequency"), use_container_width=True)
    
    st.markdown("<h3 style='color: rgb(79, 195, 247); margin-top: 25px;'>🎯 CUSTOMER SEGMENTATION</h3>", unsafe_allow_html=True)
    
    snapshot_date = df_filtered['order_date'].max() + timedelta(days=1)
    rfm = df_filtered.groupby('customer_id').agg({
        'order_date': lambda x: (snapshot_date - x.max()).days,
        'order_id': 'nunique',
        'total_price': 'sum'
    }).reset_index()
    rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']
    
    rfm['segment'] = 'Regular'
    rfm.loc[(rfm['frequency'] >= rfm['frequency'].quantile(0.75)) & 
            (rfm['monetary'] >= rfm['monetary'].quantile(0.75)), 'segment'] = '💎 VIP'
    rfm.loc[(rfm['recency'] <= rfm['recency'].quantile(0.25)) & 
            (rfm['frequency'] >= rfm['frequency'].quantile(0.5)), 'segment'] = '⚡ Active'
    rfm.loc[rfm['recency'] >= rfm['recency'].quantile(0.75), 'segment'] = '⚠️ At Risk'
    
    segment_summary = rfm.groupby('segment').agg({
        'customer_id': 'count',
        'monetary': 'sum'
    }).reset_index()
    segment_summary.columns = ['segment', 'customer_count', 'total_revenue']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📉 Performance Alerts")
        
        if metrics['revenue_delta'] < -10:
            st.error(f"🚨 **CRITICAL:** Revenue dropped {abs(metrics['revenue_delta']):.1f}% vs previous period!")
        elif metrics['revenue_delta'] < 0:
            st.warning(f"⚠️ **WARNING:** Revenue declined {abs(metrics['revenue_delta']):.1f}%")
        else:
            st.success(f"✅ **HEALTHY:** Revenue grew {metrics['revenue_delta']:.1f}%")
        
        if metrics['customers_delta'] < -5:
            st.error(f"🚨 **ATTENTION:** Lost {abs(metrics['customers_delta']):.1f}% of customers!")
        elif metrics['customers_delta'] < 0:
            st.warning(f"⚠️ Customer count decreased by {abs(metrics['customers_delta']):.1f}%")
        else:
            st.success(f"✅ Customer base grew {metrics['customers_delta']:.1f}%")
    
    with col2:
        st.markdown("#### 📊 Threshold Monitoring")
        
        aov_threshold = 100
        if metrics['avg_order_value'] < aov_threshold:
            st.warning(f"⚠️ Avg Order Value (${metrics['avg_order_value']:.2f}) below target (${aov_threshold})")
        else:
            st.success(f"✅ Avg Order Value (${metrics['avg_order_value']:.2f}) exceeds target")
        
        if top_5_revenue_pct > 50:
            st.warning(f"⚠️ Top 5 customers represent {top_5_revenue_pct:.1f}% of revenue - High concentration risk!")
        else:
            st.info(f"ℹ️ Top 5 customers: {top_5_revenue_pct:.1f}% of revenue")
    
    st.markdown("#### 🎯 Key Recommendations")
    recommendations = []
    
    if metrics['revenue_delta'] < 0:
        recommendations.append("💡 Focus on customer retention campaigns")
    if metrics['avg_order_value'] < aov_threshold:
        recommendations.append("💡 Implement upselling strategies to increase AOV")
    if top_5_revenue_pct > 50:
        recommendations.append("💡 Diversify customer base to reduce concentration risk")
    if metrics['customers_delta'] > 10:
        recommendations.append("💡 Capitalize on growth momentum with loyalty programs")
    
    if recommendations:
        for rec in recommendations:
            st.markdown(f"""
                <div style='background: rgba(79, 195, 247, 0.1); padding: 12px; border-radius: 8px; margin: 8px 0; border-left: 3px solid rgb(79, 195, 247);'>
                    <p style='margin: 0; color: rgb(197, 202, 233);'>{rec}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ All metrics are performing well! Keep up the great work.")

# ML PREDICTIONS TAB
with adv_tab2:
    st.markdown("<h3 style='color: rgb(79, 195, 247);'>📈 REVENUE FORECASTING</h3>", unsafe_allow_html=True)
    
    monthly_rev_data = df_filtered.groupby(df_filtered['order_date'].dt.to_period('M'))['total_price'].sum().reset_index()
    monthly_rev_data['order_date'] = monthly_rev_data['order_date'].dt.to_timestamp()
    monthly_rev_data['month_num'] = range(len(monthly_rev_data))
    
    if len(monthly_rev_data) >= 3:
        z = np.polyfit(monthly_rev_data['month_num'], monthly_rev_data['total_price'], 2)
        p = np.poly1d(z)
        
        future_months = 3
        last_month_num = monthly_rev_data['month_num'].max()
        future_month_nums = range(last_month_num + 1, last_month_num + future_months + 1)
        future_predictions = [p(x) for x in future_month_nums]
        
        last_date = monthly_rev_data['order_date'].max()
        future_dates = [last_date + timedelta(days=30 * (i+1)) for i in range(future_months)]
        
        forecast_df = pd.DataFrame({
            'date': list(monthly_rev_data['order_date']) + future_dates,
            'revenue': list(monthly_rev_data['total_price']) + future_predictions,
            'type': ['Historical'] * len(monthly_rev_data) + ['Forecast'] * future_months
        })
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig_forecast = go.Figure()
            
            historical = forecast_df[forecast_df['type'] == 'Historical']
            fig_forecast.add_trace(go.Scatter(
                x=historical['date'],
                y=historical['revenue'],
                mode='lines+markers',
                name='Historical',
                line=dict(color='rgb(79, 195, 247)', width=3),
                marker=dict(size=8)
            ))
            
            forecast = forecast_df[forecast_df['type'] == 'Forecast']
            fig_forecast.add_trace(go.Scatter(
                x=forecast['date'],
                y=forecast['revenue'],
                mode='lines+markers',
                name='Forecast',
                line=dict(color='rgb(236, 64, 122)', width=3, dash='dash'),
                marker=dict(size=10, symbol='diamond')
            ))
            
            std_dev = monthly_rev_data['total_price'].std()
            fig_forecast.add_trace(go.Scatter(
                x=forecast['date'].tolist() + forecast['date'].tolist()[::-1],
                y=(forecast['revenue'] + std_dev).tolist() + (forecast['revenue'] - std_dev).tolist()[::-1],
                fill='toself',
                fillcolor='rgba(236, 64, 122, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='Confidence Interval',
                showlegend=True
            ))
            
            st.plotly_chart(style_fig(fig_forecast, "Revenue Forecast - Next 3 Months"), use_container_width=True)
        
        with col2:
            st.markdown("#### 🎯 Forecast Summary")
            for i, (date, pred) in enumerate(zip(future_dates, future_predictions), 1):
                st.metric(
                    f"Month +{i}",
                    f"${pred:,.0f}",
                    delta=f"{((pred - monthly_rev_data['total_price'].iloc[-1]) / monthly_rev_data['total_price'].iloc[-1] * 100):.1f}%"
                )
            
            st.markdown("#### 📊 Model Info")
            st.info(f"""
                **Method:** Polynomial Regression (Degree 2)
                
                **Training Data:** {len(monthly_rev_data)} months
                
                **Confidence:** ±${std_dev:,.0f}
            """)
    else:
        st.warning("⚠️ Need at least 3 months of data for forecasting")

# YoY COMPARISON TAB
with adv_tab3:
    st.markdown("<h3 style='color: rgb(79, 195, 247);'>📊 YEAR-OVER-YEAR ANALYSIS</h3>", unsafe_allow_html=True)
    
    years_available = sorted(df['order_date'].dt.year.unique())
    
    if len(years_available) >= 2:
        col1, col2 = st.columns(2)
        with col1:
            year1 = st.selectbox("Compare Year", years_available[:-1] if len(years_available) > 1 else years_available, index=0)
        with col2:
            year2 = st.selectbox("With Year", [y for y in years_available if y > year1], index=0)
        
        df_year1 = df[df['order_date'].dt.year == year1]
        df_year2 = df[df['order_date'].dt.year == year2]
        
        monthly_y1 = df_year1.groupby(df_year1['order_date'].dt.month)['total_price'].sum().reset_index()
        monthly_y2 = df_year2.groupby(df_year2['order_date'].dt.month)['total_price'].sum().reset_index()
        monthly_y1.columns = ['month', 'revenue']
        monthly_y2.columns = ['month', 'revenue']
        
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly_y1['month_name'] = monthly_y1['month'].apply(lambda x: month_names[x-1])
        monthly_y2['month_name'] = monthly_y2['month'].apply(lambda x: month_names[x-1])
        
        fig_yoy = go.Figure()
        
        fig_yoy.add_trace(go.Bar(
            x=monthly_y1['month_name'],
            y=monthly_y1['revenue'],
            name=str(year1),
            marker=dict(color='rgb(79, 195, 247)'),
            text=[f"${val:,.0f}" for val in monthly_y1['revenue']],
            textposition='outside'
        ))
        
        fig_yoy.add_trace(go.Bar(
            x=monthly_y2['month_name'],
            y=monthly_y2['revenue'],
            name=str(year2),
            marker=dict(color='rgb(126, 87, 194)'),
            text=[f"${val:,.0f}" for val in monthly_y2['revenue']],
            textposition='outside'
        ))
        
        st.plotly_chart(style_fig(fig_yoy, f"Monthly Revenue: {year1} vs {year2}"), use_container_width=True)
        
        st.markdown("#### 📈 Year-over-Year Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        y1_revenue = df_year1['total_price'].sum()
        y2_revenue = df_year2['total_price'].sum()
        yoy_revenue_growth = ((y2_revenue - y1_revenue) / y1_revenue * 100) if y1_revenue > 0 else 0
        
        y1_orders = df_year1['order_id'].nunique()
        y2_orders = df_year2['order_id'].nunique()
        yoy_orders_growth = ((y2_orders - y1_orders) / y1_orders * 100) if y1_orders > 0 else 0
        
        y1_customers = df_year1['customer_id'].nunique()
        y2_customers = df_year2['customer_id'].nunique()
        yoy_customers_growth = ((y2_customers - y1_customers) / y1_customers * 100) if y1_customers > 0 else 0
        
        y1_aov = y1_revenue / y1_orders if y1_orders > 0 else 0
        y2_aov = y2_revenue / y2_orders if y2_orders > 0 else 0
        yoy_aov_growth = ((y2_aov - y1_aov) / y1_aov * 100) if y1_aov > 0 else 0
        
        with col1:
            st.metric(f"Revenue {year2}", f"${y2_revenue:,.0f}", f"{yoy_revenue_growth:+.1f}%")
        with col2:
            st.metric(f"Orders {year2}", f"{y2_orders:,}", f"{yoy_orders_growth:+.1f}%")
        with col3:
            st.metric(f"Customers {year2}", f"{y2_customers:,}", f"{yoy_customers_growth:+.1f}%")
        with col4:
            st.metric(f"AOV {year2}", f"${y2_aov:.2f}", f"{yoy_aov_growth:+.1f}%")
        
    else:
        st.info("ℹ️ Year-over-year comparison requires data from at least 2 different years")

# PDF REPORT TAB
with adv_tab4:
    st.markdown("<h3 style='color: rgb(79, 195, 247);'>📄 EXECUTIVE PDF REPORT</h3>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: rgba(79, 195, 247, 0.1); padding: 20px; border-radius: 12px; border: 1px solid rgba(79, 195, 247, 0.3);'>
            <h4 style='color: rgb(79, 195, 247); margin-top: 0;'>📋 Report Contents</h4>
            <ul style='color: rgb(197, 202, 233);'>
                <li>✅ Executive Summary with Key Metrics</li>
                <li>✅ Performance Trends & Growth Analysis</li>
                <li>✅ Top Customers & Products Tables</li>
                <li>✅ Geographic Distribution</li>
                <li>✅ Customer Segmentation (RFM)</li>
                <li>✅ Smart Alerts & Recommendations</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("🔄 GENERATE PDF REPORT", use_container_width=True, type="primary"):
            with st.spinner("Generating comprehensive PDF report..."):
                html_content = f"""
                <html>
                <head>
                    <style>
                        body {{ font-family: 'Arial', sans-serif; margin: 40px; background: rgb(245, 245, 245); }}
                        .header {{ background: linear-gradient(135deg, rgb(94, 53, 177) 0%, rgb(81, 45, 168) 100%); color: white; padding: 30px; border-radius: 10px; text-align: center; }}
                        .metric-card {{ background: white; padding: 20px; margin: 15px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                        .metric-value {{ font-size: 32px; color: rgb(79, 195, 247); font-weight: bold; }}
                        .metric-label {{ font-size: 14px; color: rgb(102, 102, 102); text-transform: uppercase; }}
                        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; background: white; }}
                        th {{ background: rgb(94, 53, 177); color: white; padding: 12px; text-align: left; }}
                        td {{ padding: 10px; border-bottom: 1px solid rgb(221, 221, 221); }}
                        h2 {{ color: rgb(94, 53, 177); border-bottom: 2px solid rgb(79, 195, 247); padding-bottom: 10px; }}
                    </style>
                </head>
                <body>
                    <div class="header">
                        <h1>📊 EXECUTIVE E-COMMERCE DASHBOARD</h1>
                        <p>Period: {start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}</p>
                        <p>Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}</p>
                    </div>
                    
                    <h2>📈 Executive Summary</h2>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;">
                        <div class="metric-card">
                            <div class="metric-label">Total Revenue</div>
                            <div class="metric-value">${metrics['total_revenue']:,.0f}</div>
                            <div style="color: {'green' if metrics['revenue_delta'] > 0 else 'red'};">
                                {metrics['revenue_delta']:+.1f}% vs previous period
                            </div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">Total Orders</div>
                            <div class="metric-value">{metrics['total_orders']:,}</div>
                            <div style="color: {'green' if metrics['orders_delta'] > 0 else 'red'};">
                                {metrics['orders_delta']:+.1f}%
                            </div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">Unique Customers</div>
                            <div class="metric-value">{metrics['unique_customers']:,}</div>
                            <div style="color: {'green' if metrics['customers_delta'] > 0 else 'red'};">
                                {metrics['customers_delta']:+.1f}%
                            </div>
                        </div>
                    </div>
                    
                    <h2>🏆 Top 10 Customers</h2>
                    <table>
                        <tr>
                            <th>Customer ID</th>
                            <th>Total Revenue</th>
                            <th>Order Count</th>
                        </tr>
                        {''.join([f"<tr><td>{row['customer_id']}</td><td>${row['total_revenue']:,.0f}</td><td>{row['order_count']}</td></tr>" 
                                  for _, row in top_customers.head(10).iterrows()])}
                    </table>
                    
                    <h2>📦 Top 10 Products</h2>
                    <table>
                        <tr>
                            <th>Product Name</th>
                            <th>Revenue</th>
                            <th>Quantity Sold</th>
                        </tr>
                        {''.join([f"<tr><td>{row['product_name']}</td><td>${row['total_price']:,.0f}</td><td>{row['quantity']}</td></tr>" 
                                  for _, row in top_products_rev.head(10).iterrows()])}
                    </table>
                    
                    <h2>🌍 Geographic Distribution</h2>
                    <table>
                        <tr>
                            <th>Country</th>
                            <th>Revenue</th>
                            <th>Orders</th>
                            <th>Customers</th>
                        </tr>
                        {''.join([f"<tr><td>{row['country']}</td><td>${row['revenue']:,.0f}</td><td>{row['orders']}</td><td>{row['customers']}</td></tr>" 
                                  for _, row in country_analysis.head(10).iterrows()])}
                    </table>
                    
                    <h2>🎯 Customer Segmentation</h2>
                    <table>
                        <tr>
                            <th>Segment</th>
                            <th>Customer Count</th>
                            <th>Total Revenue</th>
                        </tr>
                        {''.join([f"<tr><td>{row['segment']}</td><td>{row['customer_count']}</td><td>${row['total_revenue']:,.0f}</td></tr>" 
                                  for _, row in segment_summary.iterrows()])}
                    </table>
                    
                    <h2>💡 Key Recommendations</h2>
                    <div class="metric-card">
                """
                
                if metrics['revenue_delta'] < 0:
                    html_content += "<p>🔴 Revenue declined - Focus on customer retention campaigns</p>"
                if metrics['avg_order_value'] < 100:
                    html_content += "<p>🟡 Average order value below target - Implement upselling strategies</p>"
                if top_5_revenue_pct > 50:
                    html_content += "<p>🟡 High customer concentration - Diversify customer base</p>"
                if metrics['customers_delta'] > 10:
                    html_content += "<p>🟢 Strong customer growth - Implement loyalty programs</p>"
                
                html_content += """
                    </div>
                    
                    <div style="margin-top: 40px; text-align: center; color: rgb(102, 102, 102); font-size: 12px; border-top: 1px solid rgb(221, 221, 221); padding-top: 20px;">
                        <p>This is an automated report generated by the Executive E-commerce Dashboard</p>
                        <p>© 2025 - Confidential Business Intelligence Report</p>
                    </div>
                </body>
                </html>
                """
                
                st.download_button(
                    label="📥 DOWNLOAD HTML REPORT",
                    data=html_content,
                    file_name=f"executive_report_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
                    mime="text/html",
                    use_container_width=True
                )
                
                st.success("✅ Report generated successfully! Click the button above to download.")
                st.info("💡 **Tip:** Open the HTML file in any browser and use 'Print to PDF' for a professional PDF report.")
    
    st.markdown("---")
    st.markdown("""
        <div style='background: rgba(126, 87, 194, 0.1); padding: 15px; border-radius: 8px; border-left: 3px solid rgb(126, 87, 194);'>
            <p style='margin: 0; color: rgb(197, 202, 233); font-size: 13px;'>
                💡 <strong>Pro Tip:</strong> The HTML report can be opened in Chrome/Edge and saved as PDF using Ctrl+P (Print → Save as PDF)
            </p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<hr style='margin: 35px 0; border: 1px solid rgba(79, 195, 247, 0.2);'>", unsafe_allow_html=True)

st.markdown(f"""
    <div style='text-align: center; padding: 25px; background: rgba(255, 255, 255, 0.03); border-radius: 16px; border: 1px solid rgba(79, 195, 247, 0.2);'>
        <div style='font-size: 40px; margin-bottom: 12px;'>⚡</div>
        <h3 style='color: rgb(79, 195, 247); margin: 8px 0; font-size: 22px;'>EXECUTIVE DASHBOARD v3.0</h3>
        <p style='color: rgb(176, 190, 197); font-size: 13px; margin: 8px 0;'>
            Built with Streamlit, Plotly & Advanced ML
        </p>
        <div style='display: flex; justify-content: center; gap: 15px; margin: 15px 0; flex-wrap: wrap;'>
            <span style='background: rgba(79, 195, 247, 0.2); padding: 6px 12px; border-radius: 20px; font-size: 11px; color: rgb(79, 195, 247);'>🔔 Smart Alerts</span>
            <span style='background: rgba(126, 87, 194, 0.2); padding: 6px 12px; border-radius: 20px; font-size: 11px; color: rgb(126, 87, 194);'>📈 ML Forecasting</span>
            <span style='background: rgba(236, 64, 122, 0.2); padding: 6px 12px; border-radius: 20px; font-size: 11px; color: rgb(236, 64, 122);'>📊 YoY Analysis</span>
            <span style='background: rgba(38, 198, 218, 0.2); padding: 6px 12px; border-radius: 20px; font-size: 11px; color: rgb(38, 198, 218);'>📄 PDF Reports</span>
            <span style='background: rgba(255, 190, 11, 0.2); padding: 6px 12px; border-radius: 20px; font-size: 11px; color: rgb(255, 190, 11);'>💾 Save Configs</span>
        </div>
        <p style='color: rgb(126, 87, 194); font-size: 11px; margin: 5px 0;'>
            📅 Updated: {datetime.now().strftime('%B %d, %Y - %H:%M')}
        </p>
        <div style='margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255, 255, 255, 0.08);'>
            <p style='color: rgb(176, 190, 197); font-size: 10px; margin: 0;'>
                💼 Data Analytics & Business Intelligence Portfolio
            </p>
            <p style='color: rgb(126, 87, 194); font-size: 9px; margin: 5px 0 0 0;'>
                🎯 Featuring: RFM Segmentation • Pareto Analysis • Predictive Analytics • Interactive Visualizations
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)
    with col1:
        fig_seg_count = go.Figure(data=[
            go.Bar(
                x=segment_summary['segment'],
                y=segment_summary['customer_count'],
                marker=dict(color=professional_colors[:len(segment_summary)]),
                text=segment_summary['customer_count'],
                textposition='outside',
                textfont=dict(size=13, color='rgb(79, 195, 247)')
            )
        ])
        st.plotly_chart(style_fig(fig_seg_count, "Customers by Segment"), use_container_width=True)
    
    with col2:
        fig_seg_rev = go.Figure(data=[
            go.Bar(
                x=segment_summary['segment'],
                y=segment_summary['total_revenue'],
                marker=dict(color=professional_colors[:len(segment_summary)]),
                text=[f"${val:,.0f}" for val in segment_summary['total_revenue']],
                textposition='outside',
                textfont=dict(size=13, color='rgb(79, 195, 247)')
            )
        ])
        st.plotly_chart(style_fig(fig_seg_rev, "Revenue by Segment"), use_container_width=True)

# TAB 3: Product Performance
with tab3:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown(f"<h3 style='color: rgb(79, 195, 247);'>🎯 TOP {top_n} PRODUCTS - REVENUE</h3>", unsafe_allow_html=True)
        top_products_rev = df_filtered.groupby('product_name').agg({
            'total_price': 'sum',
            'quantity': 'sum'
        }).nlargest(top_n, 'total_price').reset_index()
        
        fig_prod_rev = go.Figure(data=[
            go.Bar(
                x=top_products_rev['total_price'],
                y=top_products_rev['product_name'],
                orientation='h',
                marker=dict(
                    color=top_products_rev['total_price'],
                    colorscale='Rainbow',
                    showscale=False,
                    line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
                ),
                text=[f"${val:,.0f}" for val in top_products_rev['total_price']],
                textposition='outside',
                textfont=dict(color='rgb(79, 195, 247)', size=10)
            )
        ])
        st.plotly_chart(style_fig(fig_prod_rev, "Revenue Leaders"), use_container_width=True)
    
    with col2:
        st.markdown("<h3 style='color: rgb(79, 195, 247);'>📦 BY QUANTITY</h3>", unsafe_allow_html=True)
        top_products_qty = df_filtered.groupby('product_name')['quantity'].sum().nlargest(top_n).reset_index()
        
        fig_prod_qty = go.Figure(data=[
            go.Bar(
                x=top_products_qty['quantity'],
                y=top_products_qty['product_name'],
                orientation='h',
                marker=dict(
                    color=top_products_qty['quantity'],
                    colorscale='Teal',
                    showscale=False,
                    line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
                ),
                text=top_products_qty['quantity'],
                textposition='outside',
                textfont=dict(color='rgb(79, 195, 247)', size=10)
            )
        ])
        st.plotly_chart(style_fig(fig_prod_qty, "Volume Champions"), use_container_width=True)
    
    st.markdown("<h3 style='color: rgb(79, 195, 247); margin-top: 25px;'>💲 PRICE DISTRIBUTION</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_price = go.Figure()
        fig_price.add_trace(go.Histogram(
            x=df_filtered['unit_price'],
            nbinsx=50,
            marker=dict(
                color='rgb(126, 87, 194)',
                line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
            ),
            opacity=0.8,
            name='Distribution'
        ))
        fig_price.add_trace(go.Box(
            x=df_filtered['unit_price'],
            marker=dict(color='rgb(79, 195, 247)'),
            name='Box Plot',
            yaxis='y2'
        ))
        fig_price.update_layout(
            yaxis2=dict(overlaying='y', side='right'),
            showlegend=True,
            legend=dict(font=dict(color='rgb(197, 202, 233)'))
        )
        st.plotly_chart(style_fig(fig_price, "Unit Price Analysis"), use_container_width=True)
    
    with col2:
        price_stats = df_filtered['unit_price'].describe()
        st.markdown("""
            <div class='card-container'>
                <h4 style='color: rgb(79, 195, 247); margin-bottom: 12px; text-align: center;'>📈 STATISTICS</h4>
        """, unsafe_allow_html=True)
        st.metric("Mean", f"${price_stats['mean']:.2f}")
        st.metric("Median", f"${price_stats['50%']:.2f}")
        st.metric("Std Dev", f"${price_stats['std']:.2f}")
        st.metric("Max", f"${price_stats['max']:.2f}")
        st.markdown("</div>", unsafe_allow_html=True)

# TAB 4: Geographic Insights
with tab4:
    st.markdown("<h3 style='color: rgb(79, 195, 247);'>🌍 REVENUE BY COUNTRY</h3>", unsafe_allow_html=True)
    
    country_analysis = df_filtered.groupby('country').agg({
        'total_price': 'sum',
        'order_id': 'nunique',
        'customer_id': 'nunique'
    }).reset_index()
    country_analysis.columns = ['country', 'revenue', 'orders', 'customers']
    country_analysis = country_analysis.sort_values('revenue', ascending=False)
    
    fig_country = go.Figure(data=[
        go.Bar(
            x=country_analysis['country'],
            y=country_analysis['revenue'],
            marker=dict(
                color=country_analysis['revenue'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Revenue", tickprefix="$", title_font=dict(color="rgb(197, 202, 233)"), tickfont=dict(color="rgb(176, 190, 197)")),
                line=dict(color='rgba(255, 255, 255, 0.2)', width=1.5)
            ),
            text=[f"${val:,.0f}" for val in country_analysis['revenue']],
            textposition='outside',
            textfont=dict(color='rgb(79, 195, 247)', size=12),
            hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>'
        )
    ])
    st.plotly_chart(style_fig(fig_country, "Global Distribution"), use_container_width=True)
    
    st.markdown("<h3 style='color: rgb(79, 195, 247); margin-top: 25px;'>📋 DETAILED PERFORMANCE</h3>", unsafe_allow_html=True)
    country_analysis['avg_order_value'] = country_analysis['revenue'] / country_analysis['orders']
    
    display_df = country_analysis.copy()
    display_df['revenue'] = display_df['revenue'].apply(lambda x: f"${x:,.0f}")
    display_df['avg_order_value'] = display_df['avg_order_value'].apply(lambda x: f"${x:.2f}")
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "country": st.column_config.TextColumn("🌍 Country", width="medium"),
            "revenue": st.column_config.TextColumn("💰 Revenue", width="medium"),
            "orders": st.column_config.NumberColumn("🛒 Orders", format="%d"),
            "customers": st.column_config.NumberColumn("👥 Customers", format="%d"),
            "avg_order_value": st.column_config.TextColumn("💵 Avg Order", width="medium")
        }
    )

# TAB 5: Advanced Analytics
with tab5:
    st.markdown("<h3 style='color: rgb(79, 195, 247);'>🔬 ADVANCED ANALYTICS</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h4 style='color: rgb(197, 202, 233);'>💹 GROWTH RATE</h4>", unsafe_allow_html=True)
        growth_data = monthly_revenue.copy()
        growth_data['growth_rate'] = growth_data['total_price'].pct_change() * 100
        
        fig_growth = go.Figure()
        
        colors = ['rgb(79, 195, 247)' if x >= 0 else 'rgb(236, 64, 122)' for x in growth_data['growth_rate']]
        
        fig_growth.add_trace(go.Bar(
            x=growth_data['order_date'],
            y=growth_data['growth_rate'],
            marker=dict(color=colors, line=dict(color='rgba(255, 255, 255, 0.2)', width=1)),
            text=[f"{val:.1f}%" if not pd.isna(val) else "" for val in growth_data['growth_rate']],
            textposition='outside',
            textfont=dict(size=10, color='rgb(197, 202, 233)')
        ))
        
        fig_growth.add_hline(y=0, line_dash="solid", line_color="rgba(255, 255, 255, 0.4)", line_width=1.5)
        st.plotly_chart(style_fig(fig_growth, "Month-over-Month Growth %"), use_container_width=True)
    
    with col2:
        st.markdown("<h4 style='color: rgb(197, 202, 233);'>📊 PARETO ANALYSIS</h4>", unsafe_allow_html=True)
        
        product_revenue = df_filtered.groupby('product_name')['total_price'].sum().sort_values(ascending=False).reset_index()
        product_revenue['cumulative_pct'] = (product_revenue['total_price'].cumsum() / product_revenue['total_price'].sum()) * 100
        
        fig_pareto = go.Figure()
        
        fig_pareto.add_trace(go.Bar(
            x=product_revenue.index[:20],
            y=product_revenue['total_price'][:20],
            name='Revenue',
            marker=dict(color='rgb(126, 87, 194)'),
            yaxis='y'
        ))
        
        fig_pareto.add_trace(go.Scatter(
            x=product_revenue.index[:20],
            y=product_revenue['cumulative_pct'][:20],
            name='Cumulative %',
            mode='lines+markers',
            marker=dict(color='rgb(79, 195, 247)', size=6),
            line=dict(color='rgb(79, 195, 247)', width=2.5),
            yaxis='y2'
        ))
        
        fig_pareto.update_layout(
            yaxis=dict(title='Revenue', title_font=dict(color="rgb(197, 202, 233)")),
            yaxis2=dict(title='Cumulative %', overlaying='y', side='right', range=[0, 100], title_font=dict(color="rgb(197, 202, 233)")),
            showlegend=True,
            legend=dict(font=dict(color='rgb(197, 202, 233)'))
        )
        
        st.plotly_chart(style_fig(fig_pareto, "80/20 Rule"), use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h4 style='color: rgb(197, 202, 233);'>🔗 CORRELATION ANALYSIS</h4>", unsafe_allow_html=True)
        sample_df = df_filtered.sample(min(1000, len(df_filtered)))
        
        fig_scatter = go.Figure(data=go.Scatter(
            x=sample_df['quantity'],
            y=sample_df['unit_price'],
            mode='markers',
            marker=dict(
                size=sample_df['total_price']/100,
                color=sample_df['total_price'],
                colorscale='Plasma',
                showscale=True,
                colorbar=dict(title="Total", title_font=dict(color="rgb(197, 202, 233)"), tickfont=dict(color="rgb(176, 190, 197)")),
                line=dict(color='rgba(255, 255, 255, 0.2)', width=1),
                opacity=0.7
            ),
            text=[f"${val:,.0f}" for val in sample_df['total_price']],
            hovertemplate='<b>Qty:</b> %{x}<br><b>Price:</b> $%{y:.2f}<br><b>Total:</b> %{text}<extra></extra>'
        ))
        st.plotly_chart(style_fig(fig_scatter, "Quantity vs Price"), use_container_width=True)
    
    with col2:
        st.markdown("<h4 style='color: rgb(197, 202, 233);'>📅 SEASONAL PATTERNS</h4>", unsafe_allow_html=True)
        
        yearly_comp = df_filtered.groupby(df_filtered['order_date'].dt.month)['total_price'].sum().reset_index()
        yearly_comp.columns = ['month', 'revenue']
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        yearly_comp['month_name'] = yearly_comp['month'].apply(lambda x: month_names[x-1] if x <= 12 else str(x))
        
        fig_monthly = go.Figure(data=[
            go.Bar(
                x=yearly_comp['month_name'],
                y=yearly_comp['revenue'],
                marker=dict(
                    color=yearly_comp['revenue'],
                    colorscale='Turbo',
                    showscale=False,
                    line=dict(color='rgba(255, 255, 255, 0.2)', width=1)
                ),
                text=[f"${val:,.0f}" for val in yearly_comp['revenue']],
                textposition='outside',
                textfont=dict(color='rgb(79, 195, 247)', size=10)
            )
        ])
        st.plotly_chart(style_fig(fig_monthly, "Monthly Revenue"), use_container_width=True)
    
    top_5_revenue_pct = (top_customers['total_revenue'].head(5).sum() / metrics['total_revenue']) * 100
    
    st.markdown("""
        <div class='card-container' style='background: linear-gradient(135deg, rgba(94, 53, 177, 0.15) 0%, rgba(79, 195, 247, 0.15) 100%); border: 2px solid rgba(79, 195, 247, 0.3); margin-top: 25px;'>
            <h3 style='color: rgb(79, 195, 247); text-align: center; margin-bottom: 20px;'>🎯 EXECUTIVE SUMMARY</h3>
    """, unsafe_allow_html=True)
    
    sum_col1, sum_col2, sum_col3, sum_col4 = st.columns(4)
    
    with sum_col1:
        top_country = country_analysis.iloc[0]
        st.markdown(f"""
            <div style='text-align: center;'>
                <p style='color: rgb(176, 190, 197); font-size: 11px; margin: 0;'>TOP COUNTRY</p>
                <p style='color: rgb(79, 195, 247); font-size: 22px; font-weight: 700; margin: 5px 0;'>{top_country['country']}</p>
                <p style='color: rgb(197, 202, 233); font-size: 13px; margin: 0;'>${top_country['revenue']:,.0f}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with sum_col2:
        best_product = top_products_rev.iloc[0]
        st.markdown(f"""
            <div style='text-align: center;'>
                <p style='color: rgb(176, 190, 197); font-size: 11px; margin: 0;'>BEST PRODUCT</p>
                <p style='color: rgb(79, 195, 247); font-size: 16px; font-weight: 700; margin: 5px 0;'>{best_product['product_name'][:15]}...</p>
                <p style='color: rgb(197, 202, 233); font-size: 13px; margin: 0;'>${best_product['total_price']:,.0f}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with sum_col3:
        vip_customers = rfm[rfm['segment'] == '💎 VIP'].shape[0]
        st.markdown(f"""
            <div style='text-align: center;'>
                <p style='color: rgb(176, 190, 197); font-size: 11px; margin: 0;'>VIP CUSTOMERS</p>
                <p style='color: rgb(79, 195, 247); font-size: 22px; font-weight: 700; margin: 5px 0;'>{vip_customers}</p>
                <p style='color: rgb(197, 202, 233); font-size: 13px; margin: 0;'>Top Tier</p>
            </div>
        """, unsafe_allow_html=True)
    
    with sum_col4:
        growth_avg = growth_data['growth_rate'].mean()
        st.markdown(f"""
            <div style='text-align: center;'>
                <p style='color: rgb(176, 190, 197); font-size: 11px; margin: 0;'>AVG GROWTH</p>
                <p style='color: rgb(79, 195, 247); font-size: 22px; font-weight: 700; margin: 5px 0;'>{growth_avg:.1f}%</p>
                <p style='color: rgb(197, 202, 233); font-size: 13px; margin: 0;'>MoM</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Export Section
st.markdown("<hr style='margin: 35px 0; border: 1px solid rgba(79, 195, 247, 0.3);'>", unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: center; margin-bottom: 20px;'>
        <h2 style='color: rgb(79, 195, 247); font-size: 28px;'>📥 EXPORT CENTER</h2>
        <p style='color: rgb(176, 190, 197); font-size: 13px;'>Download reports and datasets</p>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.download_button(
        "📊 DATASET",
        df_filtered.to_csv(index=False).encode('utf-8'),
        file_name=f"data_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with col2:
    st.download_button(
        "🏆 CUSTOMERS",
        top_customers.to_csv(index=False).encode('utf-8'),
        file_name=f"customers_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with col3:
    st.download_button(
        "📦 PRODUCTS",
        top_products_rev.to_csv(index=False).encode('utf-8'),
        file_name=f"products_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with col4:
    st.download_button(
        "🌍 COUNTRIES",
        display_df.to_csv(index=False).encode('utf-8'),
        file_name=f"countries_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# Advanced Features Section
st.markdown("<hr style='margin: 40px 0; border: 1px solid rgba(79, 195, 247, 0.3);'>", unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: center; margin-bottom: 25px;'>
        <h2 style='color: rgb(79, 195, 247); font-size: 32px;'>🚀 ADVANCED FEATURES</h2>
        <p style='color: rgb(176, 190, 197); font-size: 14px;'>AI-Powered Insights & Smart Analytics</p>
    </div>
""", unsafe_allow_html=True)

adv_tab1, adv_tab2, adv_tab3, adv_tab4 = st.tabs([
    "🔔 SMART ALERTS",
    "📈 ML PREDICTIONS", 
    "📊 YoY COMPARISON",
    "📄 PDF REPORT"
])

# SMART ALERTS TAB
with adv_tab1:
    st.markdown("<h3 style='color: rgb(79, 195, 247);'>🔔 INTELLIGENT ALERTS</h3>", unsafe_allow_html=True)
