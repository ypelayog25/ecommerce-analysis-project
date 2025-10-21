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

# Enhanced Professional Dark Theme CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Roboto:wght@300;400;500;700&display=swap');
    
    * { 
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    .main { 
        background: linear-gradient(135deg, rgb(17, 24, 39) 0%, rgb(31, 41, 55) 50%, rgb(17, 24, 39) 100%);
    }
    
    /* ENHANCED TEXT VISIBILITY - HIGH CONTRAST */
    h1, h2, h3, h4, .stMarkdown h3 {
        color: rgb(243, 244, 246) !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
        font-weight: 700 !important;
        letter-spacing: -0.3px;
    }
    
    h1 { 
        font-size: 42px !important;
        background: linear-gradient(135deg, rgb(96, 165, 250) 0%, rgb(147, 197, 253) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px !important;
    }
    
    h2 { 
        font-size: 28px !important;
        color: rgb(229, 231, 235) !important;
        border-left: 4px solid rgb(59, 130, 246);
        padding-left: 12px;
        margin: 25px 0 15px 0 !important;
    }
    
    h3 { 
        font-size: 22px !important;
        color: rgb(209, 213, 219) !important;
        margin: 20px 0 12px 0 !important;
    }
    
    /* ENHANCED KPI CARDS TEXT VISIBILITY */
    [data-testid="stMetricValue"] {
        font-size: 32px !important;
        font-weight: 800 !important;
        color: rgb(96, 165, 250) !important;
        letter-spacing: -0.5px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 13px !important;
        font-weight: 700 !important;
        color: rgb(243, 244, 246) !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        background: rgba(59, 130, 246, 0.2);
        padding: 6px 12px;
        border-radius: 6px;
        display: inline-block;
        margin-bottom: 8px;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 14px !important;
        font-weight: 700 !important;
        color: rgb(243, 244, 246) !important;
    }
    
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(30, 58, 138, 0.9) 0%, rgba(29, 78, 216, 0.9) 100%);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(96, 165, 250, 0.4);
        backdrop-filter: blur(10px);
    }
    
    /* ENHANCED TAB TEXT VISIBILITY */
    .stTabs [data-baseweb="tab"] {
        color: rgb(229, 231, 235) !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgb(37, 99, 235) 0%, rgb(59, 130, 246) 100%);
        color: rgb(255, 255, 255) !important;
        font-weight: 800 !important;
    }
    
    /* ENHANCED ALERT TEXT VISIBILITY */
    .stAlert {
        background: rgba(30, 58, 138, 0.25) !important;
        border-left: 5px solid rgb(59, 130, 246) !important;
        color: rgb(243, 244, 246) !important;
        font-weight: 600 !important;
        border-radius: 10px;
        padding: 15px;
        backdrop-filter: blur(5px);
    }
    
    .stSuccess {
        background: rgba(5, 150, 105, 0.25) !important;
        border-left: 5px solid rgb(16, 185, 129) !important;
        color: rgb(243, 244, 246) !important;
        font-weight: 600 !important;
    }
    
    .stWarning {
        background: rgba(217, 119, 6, 0.25) !important;
        border-left: 5px solid rgb(251, 146, 60) !important;
        color: rgb(243, 244, 246) !important;
        font-weight: 600 !important;
    }
    
    .stError {
        background: rgba(220, 38, 38, 0.25) !important;
        border-left: 5px solid rgb(239, 68, 68) !important;
        color: rgb(243, 244, 246) !important;
        font-weight: 600 !important;
    }
    
    .stInfo {
        background: rgba(30, 58, 138, 0.25) !important;
        border-left: 5px solid rgb(59, 130, 246) !important;
        color: rgb(243, 244, 246) !important;
        font-weight: 600 !important;
    }
    
    /* ENHANCED EXPANDER TEXT */
    [data-testid="stExpander"] details summary {
        color: rgb(243, 244, 246) !important;
        font-weight: 700 !important;
        font-size: 16px !important;
    }
    
    /* ENHANCED BUTTON TEXT */
    .stButton button {
        color: rgb(243, 244, 246) !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }
    
    /* ENHANCED DATA FRAME TEXT */
    [data-testid="stDataFrame"] th {
        color: rgb(243, 244, 246) !important;
        font-weight: 700 !important;
        background: rgb(30, 58, 138) !important;
    }
    
    [data-testid="stDataFrame"] td {
        color: rgb(229, 231, 235) !important;
        font-weight: 500 !important;
    }
    
    /* ENHANCED SIDEBAR TEXT */
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] div:not(.stCheckbox) {
        color: rgb(243, 244, 246) !important;
        font-weight: 600 !important;
    }
    
    /* MOBILE OPTIMIZATIONS */
    @media (max-width: 768px) {
        h1 { font-size: 32px !important; }
        h2 { font-size: 24px !important; }
        h3 { font-size: 20px !important; }
        [data-testid="stMetricValue"] { font-size: 28px !important; }
        [data-testid="stMetricLabel"] { font-size: 12px !important; }
    }
    </style>
""", unsafe_allow_html=True)

# Data Loading (unchanged)
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

# Enhanced Header with better text visibility
st.markdown("""
    <div style='text-align:center; padding: 40px 0 30px 0; background: linear-gradient(135deg, rgba(31, 41, 55, 0.9) 0%, rgba(17, 24, 39, 0.95) 100%); border-radius: 16px; margin-bottom: 30px; border: 1px solid rgb(55, 65, 81);'>
        <h1>📊 Executive E-Commerce Dashboard</h1>
        <p style='font-size: 18px; color: rgb(209, 213, 219); font-weight: 500; letter-spacing: 1px; margin-top: 10px;'>
            Real-Time Business Intelligence & Advanced Analytics
        </p>
    </div>
""", unsafe_allow_html=True)

# Sidebar (unchanged, but with enhanced text visibility from CSS above)
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 20px 0 15px 0;'>
            <div style='font-size: 44px; margin-bottom: 10px;'>⚡</div>
            <h2 style='margin: 0; font-size: 22px; color: rgb(96, 165, 250); font-weight: 700;'>
                Control Center
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📅 DATE RANGE FILTER", expanded=True):
        min_date = df['order_date'].min().date()
        max_date = df['order_date'].max().date()
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("From", min_date, min_value=min_date, max_value=max_date)
        with col2:
            end_date = st.date_input("To", max_date, min_value=min_date, max_value=max_date)
        
        st.markdown("**⚡ Quick Filters**")
        qcol1, qcol2 = st.columns(2)
        with qcol1:
            if st.button("Last 30D", use_container_width=True):
                start_date = max_date - timedelta(days=30)
            if st.button("Quarter", use_container_width=True):
                start_date = max_date - timedelta(days=90)
        with qcol2:
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
        chart_theme = st.selectbox("Chart Theme", ["plotly_dark", "plotly_white", "seaborn", "ggplot2"])
        
        if 'selected_theme' not in st.session_state:
            st.session_state.selected_theme = chart_theme
        else:
            st.session_state.selected_theme = chart_theme
    
    st.markdown("---")
    st.markdown("**💾 PREFERENCES**")
    
    if st.button("💾 Save Filters", use_container_width=True):
        st.session_state.saved_filters = {
            'start_date': start_date,
            'end_date': end_date,
            'countries': selected_countries,
            'top_n': top_n
        }
        st.success("✅ Filters saved!")
    
    if 'saved_filters' in st.session_state:
        if st.button("🔄 Load Filters", use_container_width=True):
            saved = st.session_state.saved_filters
            st.info(f"📌 Saved: {saved['start_date']} to {saved['end_date']}")

# Filter data
start_date_dt = pd.to_datetime(start_date)
end_date_dt = pd.to_datetime(end_date)
df_filtered = df[
    (df['country'].isin(selected_countries)) &
    (df['order_date'] >= start_date_dt) &
    (df['order_date'] <= end_date_dt)
].copy()

if df_filtered.empty:
    st.warning("⚠️ No data available for selected filters.")
    st.stop()

# Calculate Metrics (unchanged)
@st.cache_data
def calculate_metrics(df_current, df_all):
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

# ENHANCED KPI CARDS with better text visibility
st.markdown("### 🎯 KEY PERFORMANCE INDICATORS")
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.metric("💰 REVENUE", f"${metrics['total_revenue']:,.0f}", f"{metrics['revenue_delta']:.1f}%")
with kpi2:
    st.metric("🛒 ORDERS", f"{metrics['total_orders']:,}", f"{metrics['orders_delta']:.1f}%")
with kpi3:
    st.metric("👥 CUSTOMERS", f"{metrics['unique_customers']:,}", f"{metrics['customers_delta']:.1f}%")
with kpi4:
    st.metric("📦 UNITS", f"{metrics['total_quantity']:,}")
with kpi5:
    st.metric("💵 AVG ORDER", f"${metrics['avg_order_value']:.2f}")

st.markdown("---")

# ENHANCED Plotly Helper with better text contrast
def style_fig(fig, title=""):
    theme = st.session_state.get('selected_theme', 'plotly_dark')
    
    # Enhanced color settings for maximum visibility
    is_light_theme = theme in ['plotly_white', 'seaborn', 'ggplot2']
    
    title_color = "rgb(31, 41, 55)" if is_light_theme else "rgb(243, 244, 246)"  # Enhanced contrast
    text_color = "rgb(55, 65, 81)" if is_light_theme else "rgb(229, 231, 235)"   # Enhanced contrast
    grid_color = "rgba(0, 0, 0, 0.15)" if is_light_theme else "rgba(156, 163, 175, 0.4)"  # Enhanced grid
    paper_bg = "rgba(255, 255, 255, 0.95)" if is_light_theme else "rgba(17, 24, 39, 0.1)"
    plot_bg = "rgba(249, 250, 251, 1)" if is_light_theme else "rgba(31, 41, 55, 0.5)"
    
    fig.update_layout(
        title=dict(
            text=title, 
            font=dict(size=22, color=title_color, family="Inter", weight=700),  # Enhanced title
            x=0.5, 
            xanchor='center',
            y=0.95
        ),
        font=dict(size=14, color=text_color, family="Inter", weight=600),  # Enhanced font
        margin=dict(l=60, r=60, t=80, b=60),  # Enhanced margins
        template=theme,
        hovermode='x unified',
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        hoverlabel=dict(
            bgcolor="rgb(31, 41, 55)" if not is_light_theme else "white",
            font_size=13,
            font_family="Inter",
            font_color="white" if not is_light_theme else "rgb(31, 41, 55)",
            font_weight=600  # Enhanced hover
        )
    )
    
    # Enhanced axis configuration
    axis_config = dict(
        showgrid=True, 
        gridcolor=grid_color,
        gridwidth=1,
        title_font=dict(color=text_color, size=14, weight=700),  # Enhanced axis titles
        tickfont=dict(color=text_color, size=12, weight=600),    # Enhanced axis labels
        linecolor=grid_color,
        linewidth=1
    )
    
    fig.update_xaxes(**axis_config)
    fig.update_yaxes(**axis_config)
    
    # Enhanced text in traces
    for trace in fig.data:
        if hasattr(trace, 'textfont'):
            trace.textfont.color = text_color
            trace.textfont.size = 12
            trace.textfont.weight = 600
        if hasattr(trace, 'marker'):
            if hasattr(trace.marker, 'line'):
                trace.marker.line.width = 1
    
    return fig

# Enhanced colors for better visibility
colors = ['rgb(96, 165, 250)', 'rgb(129, 140, 248)', 'rgb(167, 139, 250)', 'rgb(236, 72, 153)', 'rgb(251, 146, 60)']

# Enhanced text color function
def get_text_color():
    theme = st.session_state.get('selected_theme', 'plotly_dark')
    return "rgb(31, 41, 55)" if theme in ['plotly_white', 'seaborn', 'ggplot2'] else "rgb(243, 244, 246)"  # Enhanced contrast

# Dashboard Tabs (rest of the code remains the same but with enhanced text visibility from CSS)
# ... [Rest of your existing code remains exactly the same] ...

# The rest of your existing code (tab1, tab2, tab3, tab4, tab5) remains unchanged
# The CSS enhancements will automatically improve text visibility throughout the dashboard
