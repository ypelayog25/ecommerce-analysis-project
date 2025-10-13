fig_forecast.add_trace(go.Scatter(
                x=hist['date'], y=hist['revenue'],
                mode='lines+markers', name='Historical',
                line=dict(color='rgb(96, 165, 250)', width=3),
                marker=dict(size=8, color='rgb(96, 165, 250)')
            ))
            
            hist = forecast_df[forecast_df['type'] == 'Historical']
            fig_forecast.add_trace(go.Scatter(
                x=hist['date'], y=hist['revenue'],
                mode='lines+markers', name='Historical',
                line=dict(color='rgb(96, 165, 250)', width=3),
                marker=dict(size=8, color='rgb(96, 165, 250)')
            ))
            
            fore = forecast_df[forecast_df['type'] == 'Forecast']
            fig_forecast.add_trace(go.Scatter(
                x=fore['date'], y=fore['revenue'],
                mode='lines+markers', name='Forecast',
                line=dict(color='rgb(251, 146, 60)', width=3, dash='dash'),
                marker=dict(size=10, symbol='diamond', color='rgb(251, 146, 60)')
            ))
            
            std_dev = monthly_data['total_price'].std()
            fig_forecast.add_trace(go.Scatter(
                x=fore['date'].tolist() + fore['date'].tolist()[::-1],
                y=(fore['revenue'] + std_dev).tolist() + (fore['revenue'] - std_dev).tolist()[::-1],
                fill='toself',
                fillcolor='rgba(251, 146, 60, 0.15)',
                line=dict(color='rgba(255,255,255,0)'),
                name='Confidence Interval'
            ))"""
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

# Page Configuration
st.set_page_config(
    page_title="Executive E-commerce Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊"
)

# Professional Dark Theme CSS
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
    
    [data-testid="stSidebar"] { 
        background: linear-gradient(180deg, rgb(31, 41, 55) 0%, rgb(17, 24, 39) 100%);
    }
    
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] div {
        color: rgb(229, 231, 235) !important;
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] div[data-testid="stExpander"] {
        background-color: rgb(55, 65, 81) !important;
        border: 1px solid rgb(75, 85, 99);
        border-radius: 8px;
    }
    
    [data-testid="stSidebar"] div[data-testid="stExpander"] > div {
        background-color: rgb(55, 65, 81) !important;
    }
    
    [data-testid="stSidebar"] div[data-testid="stExpander"] > div > div {
        background-color: rgb(55, 65, 81) !important;
        padding: 15px;
        border-radius: 8px;
    }
    
    [data-testid="stSidebar"] details[data-testid="stExpander"] {
        background-color: rgb(55, 65, 81) !important;
    }
    
    [data-testid="stSidebar"] details[data-testid="stExpander"] summary {
        background-color: rgb(55, 65, 81) !important;
        padding: 12px 15px !important;
        border-radius: 8px;
    }
    
    [data-testid="stSidebar"] details[open] {
        background-color: rgb(55, 65, 81) !important;
    }
    
    [data-testid="stSidebar"] details[open] > summary {
        background-color: rgb(55, 65, 81) !important;
        border-bottom: 1px solid rgb(75, 85, 99);
        margin-bottom: 10px;
    }
    
    [data-testid="stSidebar"] .stExpander {
        background-color: rgb(55, 65, 81) !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stExpanderDetails"] {
        background-color: rgb(55, 65, 81) !important;
    }
    
    [data-testid="stSidebar"] input[type="date"], [data-testid="stSidebar"] input[type="text"] {
        background-color: rgb(55, 65, 81) !important;
        color: rgb(243, 244, 246) !important;
        border: 1px solid rgb(75, 85, 99) !important;
        border-radius: 6px;
        padding: 10px;
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] {
        background-color: rgb(55, 65, 81) !important;
        border-radius: 6px;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: rgb(55, 65, 81) !important;
        color: rgb(243, 244, 246) !important;
        border: 1px solid rgb(75, 85, 99) !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="popover"] {
        background-color: rgb(31, 41, 55) !important;
    }
    
    [data-testid="stSidebar"] ul {
        background-color: rgb(31, 41, 55) !important;
    }
    
    [data-testid="stSidebar"] li {
        background-color: rgb(31, 41, 55) !important;
        color: rgb(229, 231, 235) !important;
    }
    
    [data-testid="stSidebar"] .stCheckbox {
        background-color: transparent !important;
    }
    
    [data-testid="stSidebar"] .stSlider {
        background-color: transparent !important;
    }
    
    [data-testid="stSidebar"] .stMultiSelect {
        background-color: rgb(55, 65, 81) !important;
    }
    
    [data-testid="stSidebar"] .stMultiSelect > div {
        background-color: rgb(55, 65, 81) !important;
    }
    
    [data-testid="stSidebar"] .stDateInput > div {
        background-color: rgb(55, 65, 81) !important;
    }
    
    [data-testid="stSidebar"] input {
        background-color: rgb(55, 65, 81) !important;
        color: rgb(243, 244, 246) !important;
    }
    
    [data-testid="stSidebar"] .row-widget {
        background-color: transparent !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        background-color: transparent !important;
    }
    
    h1 { 
        color: rgb(243, 244, 246) !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }
    
    h2 { 
        color: rgb(229, 231, 235) !important;
        font-weight: 600 !important;
        letter-spacing: -0.3px;
    }
    
    h3 { 
        color: rgb(209, 213, 219) !important;
        font-weight: 600 !important;
        letter-spacing: -0.2px;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 32px !important;
        font-weight: 700 !important;
        color: rgb(96, 165, 250) !important;
        letter-spacing: -0.5px;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 12px !important;
        font-weight: 600 !important;
        color: rgb(156, 163, 175) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 13px !important;
        font-weight: 600 !important;
    }
    
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgb(30, 58, 138) 0%, rgb(29, 78, 216) 100%);
        padding: 22px;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(59, 130, 246, 0.3);
        transition: all 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
        border-color: rgba(96, 165, 250, 0.5);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgb(31, 41, 55);
        padding: 6px;
        border-radius: 10px;
        border: 1px solid rgb(55, 65, 81);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        background-color: rgba(55, 65, 81, 0.5);
        border-radius: 8px;
        color: rgb(156, 163, 175);
        font-weight: 600;
        font-size: 13px;
        padding: 0 20px;
        border: 1px solid transparent;
        transition: all 0.2s ease;
        letter-spacing: 0.3px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgb(55, 65, 81);
        color: rgb(209, 213, 219);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgb(30, 58, 138) 0%, rgb(29, 78, 216) 100%);
        color: rgb(243, 244, 246) !important;
        border-color: rgba(59, 130, 246, 0.5);
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    }
    
    .stButton button {
        background: linear-gradient(135deg, rgb(30, 58, 138) 0%, rgb(29, 78, 216) 100%);
        color: rgb(243, 244, 246) !important;
        border: 1px solid rgba(59, 130, 246, 0.5);
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 13px;
        transition: all 0.2s ease;
        letter-spacing: 0.3px;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, rgb(37, 99, 235) 0%, rgb(59, 130, 246) 100%);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
        transform: translateY(-1px);
    }
    
    .stDownloadButton button {
        background: linear-gradient(135deg, rgb(5, 150, 105) 0%, rgb(16, 185, 129) 100%);
        color: rgb(243, 244, 246) !important;
        border: 1px solid rgba(16, 185, 129, 0.5);
        font-weight: 600;
    }
    
    .stDownloadButton button:hover {
        background: linear-gradient(135deg, rgb(16, 185, 129) 0%, rgb(52, 211, 153) 100%);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
    }
    
    p, span, label { 
        color: rgb(209, 213, 219) !important;
        font-size: 14px;
        font-weight: 400;
        line-height: 1.6;
    }
    
    .stMarkdown h3 {
        color: rgb(96, 165, 250) !important;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 16px;
        padding-left: 14px;
        border-left: 4px solid rgb(59, 130, 246);
        letter-spacing: -0.3px;
    }
    
    .stMarkdown h4 {
        color: rgb(156, 163, 175) !important;
        font-weight: 600;
        font-size: 16px;
        margin-bottom: 12px;
        letter-spacing: -0.2px;
    }
    
    [data-testid="stDataFrame"] {
        border: 1px solid rgb(55, 65, 81);
        border-radius: 8px;
    }
    
    .stAlert {
        background-color: rgba(30, 58, 138, 0.2);
        border-radius: 8px;
        border-left: 4px solid rgb(59, 130, 246);
        color: rgb(229, 231, 235) !important;
        font-weight: 500;
    }
    
    hr {
        border-color: rgb(55, 65, 81);
        margin: 30px 0;
    }
    
    /* Success, Warning, Error colors */
    .stSuccess {
        background-color: rgba(5, 150, 105, 0.15);
        border-left-color: rgb(16, 185, 129);
        color: rgb(209, 250, 229) !important;
    }
    
    .stWarning {
        background-color: rgba(217, 119, 6, 0.15);
        border-left-color: rgb(251, 146, 60);
        color: rgb(254, 243, 199) !important;
    }
    
    .stError {
        background-color: rgba(220, 38, 38, 0.15);
        border-left-color: rgb(239, 68, 68);
        color: rgb(254, 226, 226) !important;
    }
    
    .stInfo {
        background-color: rgba(30, 58, 138, 0.15);
        border-left-color: rgb(59, 130, 246);
        color: rgb(219, 234, 254) !important;
    }
    
    @media (max-width: 768px) {
        h1 { font-size: 28px !important; }
        h2 { font-size: 22px !important; }
        h3 { font-size: 18px !important; }
        [data-testid="stMetricValue"] { font-size: 24px !important; }
        div[data-testid="metric-container"] { padding: 16px; margin-bottom: 12px; }
        .stButton button { width: 100%; font-size: 13px !important; }
        p, span, label { font-size: 13px; }
    }
    </style>
""", unsafe_allow_html=True)

# Data Loading
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

# Header
st.markdown("""
    <div style='text-align:center; padding: 40px 0 30px 0; background: linear-gradient(135deg, rgba(31, 41, 55, 0.8) 0%, rgba(17, 24, 39, 0.9) 100%); border-radius: 16px; margin-bottom: 30px; border: 1px solid rgb(55, 65, 81);'>
        <h1 style='font-size: 42px; margin-bottom: 12px; color: rgb(243, 244, 246); font-weight: 700; letter-spacing: -1px;'>
            📊 Executive E-Commerce Dashboard
        </h1>
        <p style='font-size: 16px; color: rgb(156, 163, 175); font-weight: 500; letter-spacing: 1px;'>
            Real-Time Business Intelligence & Advanced Analytics
        </p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 20px 0 15px 0;'>
            <div style='font-size: 44px; margin-bottom: 10px;'>⚡</div>
            <h2 style='margin: 0; font-size: 20px; color: rgb(96, 165, 250); font-weight: 700; letter-spacing: 0.5px;'>
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

# Calculate Metrics
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

# KPI Cards
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

# Plotly Helper
def style_fig(fig, title=""):
    theme = st.session_state.get('selected_theme', 'plotly_dark')
    
    fig.update_layout(
        title=dict(
            text=title, 
            font=dict(size=20, color="rgb(229, 231, 235)", family="Inter"),
            x=0.5, 
            xanchor='center'
        ),
        font=dict(size=12, color="rgb(209, 213, 219)", family="Inter"),
        margin=dict(l=50, r=50, t=70, b=50),
        template=theme,
        hovermode='x unified',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(31, 41, 55, 0.3)' if theme == 'plotly_dark' else 'rgba(255, 255, 255, 0.9)'
    )
    
    if theme in ['plotly_white', 'seaborn', 'ggplot2']:
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.08)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.08)')
    else:
        fig.update_xaxes(showgrid=True, gridcolor='rgba(75, 85, 99, 0.3)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(75, 85, 99, 0.3)')
    
    return fig

colors = ['rgb(96, 165, 250)', 'rgb(129, 140, 248)', 'rgb(167, 139, 250)', 'rgb(236, 72, 153)', 'rgb(251, 146, 60)']

# Dashboard Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 REVENUE", "👥 CUSTOMERS", "📦 PRODUCTS", "🌍 GEOGRAPHY", "🔬 ADVANCED"])

# TAB 1: Revenue
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📈 REVENUE TREND")
        monthly_revenue = df_filtered.groupby(df_filtered['order_date'].dt.to_period('M'))['total_price'].sum().reset_index()
        monthly_revenue['order_date'] = monthly_revenue['order_date'].dt.to_timestamp()
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=monthly_revenue['order_date'], y=monthly_revenue['total_price'],
            mode='lines+markers', name='Revenue',
            line=dict(color='rgb(96, 165, 250)', width=3),
            marker=dict(size=8, color='rgb(96, 165, 250)'),
            fill='tozeroy', fillcolor='rgba(96, 165, 250, 0.1)'
        ))
        
        z = np.polyfit(range(len(monthly_revenue)), monthly_revenue['total_price'], 1)
        p = np.poly1d(z)
        fig_trend.add_trace(go.Scatter(
            x=monthly_revenue['order_date'], y=p(range(len(monthly_revenue))),
            mode='lines', name='Trend',
            line=dict(color='rgb(251, 146, 60)', width=2.5, dash='dash')
        ))
        
        st.plotly_chart(style_fig(fig_trend, "Monthly Performance"), use_container_width=True)
    
    with col2:
        st.markdown("### 🏆 TOP COUNTRIES")
        country_revenue = df_filtered.groupby('country')['total_price'].sum().nlargest(5).reset_index()
        
        fig_pie = px.pie(country_revenue, values='total_price', names='country', hole=0.45, color_discrete_sequence=colors)
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)', showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("### 📅 WEEKLY PATTERN")
    dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_revenue = df_filtered.groupby('day_of_week')['total_price'].sum().reindex(dow_order).reset_index()
    
    fig_dow = go.Figure(data=[go.Bar(
        x=dow_revenue['day_of_week'], y=dow_revenue['total_price'],
        marker=dict(color=dow_revenue['total_price'], colorscale='Viridis'),
        text=[f"${val:,.0f}" for val in dow_revenue['total_price']], textposition='outside'
    )])
    st.plotly_chart(style_fig(fig_dow, "Revenue by Day"), use_container_width=True)

# TAB 2: Customers
with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### 🌟 TOP {top_n} CUSTOMERS")
        top_customers = df_filtered.groupby('customer_id').agg({
            'total_price': 'sum', 'order_id': 'nunique'
        }).nlargest(top_n, 'total_price').reset_index()
        top_customers.columns = ['customer_id', 'total_revenue', 'order_count']
        
        fig_cust = go.Figure(data=[go.Bar(
            x=top_customers['total_revenue'], y=top_customers['customer_id'], orientation='h',
            marker=dict(color=top_customers['total_revenue'], colorscale='Plasma'),
            text=[f"${val:,.0f}" for val in top_customers['total_revenue']], textposition='outside'
        )])
        st.plotly_chart(style_fig(fig_cust, "Revenue Champions"), use_container_width=True)
    
    with col2:
        st.markdown("### 🔄 RETENTION")
        order_freq = df_filtered.groupby('customer_id')['order_id'].nunique().value_counts().sort_index().reset_index()
        order_freq.columns = ['orders', 'customer_count']
        
        fig_freq = go.Figure(data=[go.Bar(
            x=order_freq['orders'], y=order_freq['customer_count'],
            marker=dict(color=order_freq['customer_count'], colorscale='Turbo'),
            text=order_freq['customer_count'], textposition='outside'
        )])
        st.plotly_chart(style_fig(fig_freq, "Order Frequency"), use_container_width=True)
    
    st.markdown("### 🎯 CUSTOMER SEGMENTATION")
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
        'customer_id': 'count', 'monetary': 'sum'
    }).reset_index()
    segment_summary.columns = ['segment', 'customer_count', 'total_revenue']
    
    sc1, sc2 = st.columns(2)
    with sc1:
        fig_seg = go.Figure(data=[go.Bar(
            x=segment_summary['segment'], y=segment_summary['customer_count'],
            marker=dict(color=colors[:len(segment_summary)]),
            text=segment_summary['customer_count'], textposition='outside'
        )])
        st.plotly_chart(style_fig(fig_seg, "Customers by Segment"), use_container_width=True)
    
    with sc2:
        fig_segrev = go.Figure(data=[go.Bar(
            x=segment_summary['segment'], y=segment_summary['total_revenue'],
            marker=dict(color=colors[:len(segment_summary)]),
            text=[f"${val:,.0f}" for val in segment_summary['total_revenue']], textposition='outside'
        )])
        st.plotly_chart(style_fig(fig_segrev, "Revenue by Segment"), use_container_width=True)

# TAB 3: Products
with tab3:
    pc1, pc2 = st.columns([3, 2])
    
    with pc1:
        st.markdown(f"### 🎯 TOP {top_n} PRODUCTS")
        top_prod = df_filtered.groupby('product_name').agg({
            'total_price': 'sum', 'quantity': 'sum'
        }).nlargest(top_n, 'total_price').reset_index()
        
        fig_prod = go.Figure(data=[go.Bar(
            x=top_prod['total_price'], y=top_prod['product_name'], orientation='h',
            marker=dict(color=top_prod['total_price'], colorscale='Rainbow'),
            text=[f"${val:,.0f}" for val in top_prod['total_price']], textposition='outside'
        )])
        st.plotly_chart(style_fig(fig_prod, "Revenue Leaders"), use_container_width=True)
    
    with pc2:
        st.markdown("### 📦 BY QUANTITY")
        top_qty = df_filtered.groupby('product_name')['quantity'].sum().nlargest(top_n).reset_index()
        
        fig_qty = go.Figure(data=[go.Bar(
            x=top_qty['quantity'], y=top_qty['product_name'], orientation='h',
            marker=dict(color=top_qty['quantity'], colorscale='Teal'),
            text=top_qty['quantity'], textposition='outside'
        )])
        st.plotly_chart(style_fig(fig_qty, "Volume Champions"), use_container_width=True)
    
    st.markdown("### 💲 PRICE DISTRIBUTION")
    prc1, prc2 = st.columns([2, 1])
    
    with prc1:
        fig_price = go.Figure()
        fig_price.add_trace(go.Histogram(
            x=df_filtered['unit_price'], nbinsx=50,
            marker=dict(color='rgb(126, 87, 194)'), name='Distribution'
        ))
        st.plotly_chart(style_fig(fig_price, "Unit Price Analysis"), use_container_width=True)
    
    with prc2:
        price_stats = df_filtered['unit_price'].describe()
        st.markdown("**📈 STATISTICS**")
        st.metric("Mean", f"${price_stats['mean']:.2f}")
        st.metric("Median", f"${price_stats['50%']:.2f}")
        st.metric("Std Dev", f"${price_stats['std']:.2f}")
        st.metric("Max", f"${price_stats['max']:.2f}")

# TAB 4: Geography
with tab4:
    st.markdown("### 🌍 REVENUE BY COUNTRY")
    
    country_analysis = df_filtered.groupby('country').agg({
        'total_price': 'sum', 'order_id': 'nunique', 'customer_id': 'nunique'
    }).reset_index()
    country_analysis.columns = ['country', 'revenue', 'orders', 'customers']
    country_analysis = country_analysis.sort_values('revenue', ascending=False)
    
    fig_country = go.Figure(data=[go.Bar(
        x=country_analysis['country'], y=country_analysis['revenue'],
        marker=dict(color=country_analysis['revenue'], colorscale='Viridis', showscale=True),
        text=[f"${val:,.0f}" for val in country_analysis['revenue']], textposition='outside'
    )])
    st.plotly_chart(style_fig(fig_country, "Global Distribution"), use_container_width=True)
    
    st.markdown("### 📋 DETAILED PERFORMANCE")
    country_analysis['avg_order_value'] = country_analysis['revenue'] / country_analysis['orders']
    display_df = country_analysis.copy()
    display_df['revenue'] = display_df['revenue'].apply(lambda x: f"${x:,.0f}")
    display_df['avg_order_value'] = display_df['avg_order_value'].apply(lambda x: f"${x:.2f}")
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# TAB 5: Advanced
with tab5:
    st.markdown("### 🔬 ADVANCED ANALYTICS")
    
    adv1, adv2 = st.columns(2)
    
    with adv1:
        st.markdown("#### 💹 GROWTH RATE")
        growth_data = monthly_revenue.copy()
        growth_data['growth_rate'] = growth_data['total_price'].pct_change() * 100
        
        fig_growth = go.Figure()
        colors_growth = ['rgb(16, 185, 129)' if x >= 0 else 'rgb(239, 68, 68)' for x in growth_data['growth_rate']]
        fig_growth.add_trace(go.Bar(
            x=growth_data['order_date'], y=growth_data['growth_rate'],
            marker=dict(color=colors_growth),
            text=[f"{val:.1f}%" if not pd.isna(val) else "" for val in growth_data['growth_rate']],
            textposition='outside'
        ))
        fig_growth.add_hline(y=0, line_dash="solid", line_color="rgba(255, 255, 255, 0.4)")
        st.plotly_chart(style_fig(fig_growth, "MoM Growth %"), use_container_width=True)
    
    with adv2:
        st.markdown("#### 📊 PARETO ANALYSIS")
        prod_rev = df_filtered.groupby('product_name')['total_price'].sum().sort_values(ascending=False).reset_index()
        prod_rev['cumulative_pct'] = (prod_rev['total_price'].cumsum() / prod_rev['total_price'].sum()) * 100
        
        fig_pareto = go.Figure()
        fig_pareto.add_trace(go.Bar(
            x=prod_rev.index[:20], y=prod_rev['total_price'][:20],
            name='Revenue', marker=dict(color='rgb(129, 140, 248)')
        ))
        fig_pareto.add_trace(go.Scatter(
            x=prod_rev.index[:20], y=prod_rev['cumulative_pct'][:20],
            name='Cumulative %', mode='lines+markers',
            marker=dict(color='rgb(96, 165, 250)', size=6),
            line=dict(color='rgb(96, 165, 250)', width=2.5),
            yaxis='y2'
        ))
        fig_pareto.update_layout(yaxis2=dict(overlaying='y', side='right', range=[0, 100]))
        st.plotly_chart(style_fig(fig_pareto, "80/20 Rule"), use_container_width=True)
    
    top_5_revenue_pct = (top_customers['total_revenue'].head(5).sum() / metrics['total_revenue']) * 100
    
    st.markdown("### 🎯 EXECUTIVE SUMMARY")
    sum1, sum2, sum3, sum4 = st.columns(4)
    
    with sum1:
        top_country = country_analysis.iloc[0]
        st.markdown(f"**TOP COUNTRY**")
        st.metric("", top_country['country'], f"${top_country['revenue']:,.0f}")
    
    with sum2:
        best_prod = top_prod.iloc[0]
        st.markdown(f"**BEST PRODUCT**")
        st.metric("", best_prod['product_name'][:15], f"${best_prod['total_price']:,.0f}")
    
    with sum3:
        vip_count = rfm[rfm['segment'] == '💎 VIP'].shape[0]
        st.markdown(f"**VIP CUSTOMERS**")
        st.metric("", vip_count, "Top Tier")
    
    with sum4:
        growth_avg = growth_data['growth_rate'].mean()
        st.markdown(f"**AVG GROWTH**")
        st.metric("", f"{growth_avg:.1f}%", "MoM")

# Export Section
st.markdown("---")
st.markdown("## 📥 EXPORT CENTER")

exp1, exp2, exp3, exp4 = st.columns(4)

with exp1:
    st.download_button(
        "📊 DATASET",
        df_filtered.to_csv(index=False).encode('utf-8'),
        file_name=f"data_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with exp2:
    st.download_button(
        "🏆 CUSTOMERS",
        top_customers.to_csv(index=False).encode('utf-8'),
        file_name=f"customers_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with exp3:
    st.download_button(
        "📦 PRODUCTS",
        top_prod.to_csv(index=False).encode('utf-8'),
        file_name=f"products_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with exp4:
    st.download_button(
        "🌍 COUNTRIES",
        display_df.to_csv(index=False).encode('utf-8'),
        file_name=f"countries_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# Advanced Features
st.markdown("---")
st.markdown("## 🚀 ADVANCED FEATURES")

adv_tab1, adv_tab2, adv_tab3, adv_tab4 = st.tabs([
    "🔔 SMART ALERTS", "📈 ML PREDICTIONS", "📊 YoY COMPARISON", "📄 PDF REPORT"
])

# SMART ALERTS
with adv_tab1:
    st.markdown("### 🔔 INTELLIGENT ALERTS")
    
    alert1, alert2 = st.columns(2)
    
    with alert1:
        st.markdown("#### 📉 Performance Alerts")
        
        if metrics['revenue_delta'] < -10:
            st.error(f"🚨 Revenue dropped {abs(metrics['revenue_delta']):.1f}%")
        elif metrics['revenue_delta'] < 0:
            st.warning(f"⚠️ Revenue declined {abs(metrics['revenue_delta']):.1f}%")
        else:
            st.success(f"✅ Revenue grew {metrics['revenue_delta']:.1f}%")
        
        if metrics['customers_delta'] < -5:
            st.error(f"🚨 Lost {abs(metrics['customers_delta']):.1f}% of customers")
        elif metrics['customers_delta'] < 0:
            st.warning(f"⚠️ Customer count decreased {abs(metrics['customers_delta']):.1f}%")
        else:
            st.success(f"✅ Customer base grew {metrics['customers_delta']:.1f}%")
    
    with alert2:
        st.markdown("#### 📊 Threshold Monitoring")
        
        aov_threshold = 100
        if metrics['avg_order_value'] < aov_threshold:
            st.warning(f"⚠️ AOV (${metrics['avg_order_value']:.2f}) below target (${aov_threshold})")
        else:
            st.success(f"✅ AOV (${metrics['avg_order_value']:.2f}) exceeds target")
        
        if top_5_revenue_pct > 50:
            st.warning(f"⚠️ Top 5 customers: {top_5_revenue_pct:.1f}% - High risk")
        else:
            st.info(f"ℹ️ Top 5 customers: {top_5_revenue_pct:.1f}% of revenue")
    
    st.markdown("#### 🎯 Recommendations")
    
    recs = []
    if metrics['revenue_delta'] < 0:
        recs.append("💡 Focus on customer retention campaigns")
    if metrics['avg_order_value'] < aov_threshold:
        recs.append("💡 Implement upselling strategies")
    if top_5_revenue_pct > 50:
        recs.append("💡 Diversify customer base")
    if metrics['customers_delta'] > 10:
        recs.append("💡 Launch loyalty programs")
    
    if recs:
        for rec in recs:
            st.info(rec)
    else:
        st.success("✅ All metrics performing well!")

# ML PREDICTIONS
with adv_tab2:
    st.markdown("### 📈 REVENUE FORECASTING")
    
    monthly_data = df_filtered.groupby(df_filtered['order_date'].dt.to_period('M'))['total_price'].sum().reset_index()
    monthly_data['order_date'] = monthly_data['order_date'].dt.to_timestamp()
    monthly_data['month_num'] = range(len(monthly_data))
    
    if len(monthly_data) >= 3:
        z = np.polyfit(monthly_data['month_num'], monthly_data['total_price'], 2)
        p = np.poly1d(z)
        
        future_months = 3
        last_num = monthly_data['month_num'].max()
        future_nums = range(last_num + 1, last_num + future_months + 1)
        future_preds = [p(x) for x in future_nums]
        
        last_date = monthly_data['order_date'].max()
        future_dates = [last_date + timedelta(days=30 * (i+1)) for i in range(future_months)]
        
        forecast_df = pd.DataFrame({
            'date': list(monthly_data['order_date']) + future_dates,
            'revenue': list(monthly_data['total_price']) + future_preds,
            'type': ['Historical'] * len(monthly_data) + ['Forecast'] * future_months
        })
        
        fc1, fc2 = st.columns([2, 1])
        
        with fc1:
            fig_forecast = go.Figure()
            
            hist = forecast_df[forecast_df['type'] == 'Historical']
            fig_forecast.add_trace(go.Scatter(
                x=hist['date'], y=hist['revenue'],
                mode='lines+markers', name='Historical',
                line=dict(color='rgb(79, 195, 247)', width=3)
            ))
            
            fore = forecast_df[forecast_df['type'] == 'Forecast']
            fig_forecast.add_trace(go.Scatter(
                x=fore['date'], y=fore['revenue'],
                mode='lines+markers', name='Forecast',
                line=dict(color='rgb(236, 64, 122)', width=3, dash='dash')
            ))
            
            std_dev = monthly_data['total_price'].std()
            fig_forecast.add_trace(go.Scatter(
                x=fore['date'].tolist() + fore['date'].tolist()[::-1],
                y=(fore['revenue'] + std_dev).tolist() + (fore['revenue'] - std_dev).tolist()[::-1],
                fill='toself',
                fillcolor='rgba(236, 64, 122, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='Confidence Interval'
            ))
            
            st.plotly_chart(style_fig(fig_forecast, "3-Month Forecast"), use_container_width=True)
        
        with fc2:
            st.markdown("#### 🎯 Forecast")
            for i, (date, pred) in enumerate(zip(future_dates, future_preds), 1):
                delta = ((pred - monthly_data['total_price'].iloc[-1]) / monthly_data['total_price'].iloc[-1] * 100)
                st.metric(f"Month +{i}", f"${pred:,.0f}", f"{delta:.1f}%")
            
            st.markdown("#### 📊 Model Info")
            st.info(f"Method: Polynomial Regression\n\nData: {len(monthly_data)} months\n\nConfidence: ±${std_dev:,.0f}")
    else:
        st.warning("⚠️ Need at least 3 months of data")

# YoY COMPARISON
with adv_tab3:
    st.markdown("### 📊 YEAR-OVER-YEAR ANALYSIS")
    
    years = sorted(df['order_date'].dt.year.unique())
    
    if len(years) >= 2:
        yoy1, yoy2 = st.columns(2)
        with yoy1:
            year1 = st.selectbox("Compare Year", years[:-1], index=0)
        with yoy2:
            year2 = st.selectbox("With Year", [y for y in years if y > year1], index=0)
        
        df_y1 = df[df['order_date'].dt.year == year1]
        df_y2 = df[df['order_date'].dt.year == year2]
        
        m_y1 = df_y1.groupby(df_y1['order_date'].dt.month)['total_price'].sum().reset_index()
        m_y2 = df_y2.groupby(df_y2['order_date'].dt.month)['total_price'].sum().reset_index()
        m_y1.columns = ['month', 'revenue']
        m_y2.columns = ['month', 'revenue']
        
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        m_y1['month_name'] = m_y1['month'].apply(lambda x: months[x-1])
        m_y2['month_name'] = m_y2['month'].apply(lambda x: months[x-1])
        
        fig_yoy = go.Figure()
        fig_yoy.add_trace(go.Bar(
            x=m_y1['month_name'], y=m_y1['revenue'], name=str(year1),
            marker=dict(color='rgb(96, 165, 250)'),
            text=[f"${v:,.0f}" for v in m_y1['revenue']], textposition='outside',
            textfont=dict(color='rgb(209, 213, 219)')
        ))
        fig_yoy.add_trace(go.Bar(
            x=m_y2['month_name'], y=m_y2['revenue'], name=str(year2),
            marker=dict(color='rgb(129, 140, 248)'),
            text=[f"${v:,.0f}" for v in m_y2['revenue']], textposition='outside',
            textfont=dict(color='rgb(209, 213, 219)')
        ))
        
        st.plotly_chart(style_fig(fig_yoy, f"{year1} vs {year2}"), use_container_width=True)
        
        st.markdown("#### 📈 YoY Metrics")
        ym1, ym2, ym3, ym4 = st.columns(4)
        
        y1_rev = df_y1['total_price'].sum()
        y2_rev = df_y2['total_price'].sum()
        yoy_rev = ((y2_rev - y1_rev) / y1_rev * 100) if y1_rev > 0 else 0
        
        y1_ord = df_y1['order_id'].nunique()
        y2_ord = df_y2['order_id'].nunique()
        yoy_ord = ((y2_ord - y1_ord) / y1_ord * 100) if y1_ord > 0 else 0
        
        y1_cust = df_y1['customer_id'].nunique()
        y2_cust = df_y2['customer_id'].nunique()
        yoy_cust = ((y2_cust - y1_cust) / y1_cust * 100) if y1_cust > 0 else 0
        
        y1_aov = y1_rev / y1_ord if y1_ord > 0 else 0
        y2_aov = y2_rev / y2_ord if y2_ord > 0 else 0
        yoy_aov = ((y2_aov - y1_aov) / y1_aov * 100) if y1_aov > 0 else 0
        
        with ym1:
            st.metric(f"Revenue {year2}", f"${y2_rev:,.0f}", f"{yoy_rev:+.1f}%")
        with ym2:
            st.metric(f"Orders {year2}", f"{y2_ord:,}", f"{yoy_ord:+.1f}%")
        with ym3:
            st.metric(f"Customers {year2}", f"{y2_cust:,}", f"{yoy_cust:+.1f}%")
        with ym4:
            st.metric(f"AOV {year2}", f"${y2_aov:.2f}", f"{yoy_aov:+.1f}%")
    else:
        st.info("ℹ️ Need data from at least 2 years")

# PDF REPORT
with adv_tab4:
    st.markdown("### 📄 EXECUTIVE PDF REPORT")
    
    st.info("""
    **📋 Report Contents:**
    - Executive Summary with Key Metrics
    - Performance Trends & Growth Analysis
    - Top Customers & Products Tables
    - Geographic Distribution
    - Customer Segmentation (RFM)
    - Smart Alerts & Recommendations
    """)
    
    if st.button("🔄 GENERATE REPORT", use_container_width=True, type="primary"):
        with st.spinner("Generating report..."):
            html = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial; margin: 40px; background: rgb(245, 245, 245); }}
                    .header {{ background: linear-gradient(135deg, rgb(94, 53, 177), rgb(81, 45, 168)); color: white; padding: 30px; border-radius: 10px; text-align: center; }}
                    .metric-card {{ background: white; padding: 20px; margin: 15px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                    table {{ width: 100%; border-collapse: collapse; margin: 20px 0; background: white; }}
                    th {{ background: rgb(94, 53, 177); color: white; padding: 12px; }}
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
                <div class="metric-card">
                    <p><strong>Total Revenue:</strong> ${metrics['total_revenue']:,.0f} ({metrics['revenue_delta']:+.1f}%)</p>
                    <p><strong>Total Orders:</strong> {metrics['total_orders']:,} ({metrics['orders_delta']:+.1f}%)</p>
                    <p><strong>Unique Customers:</strong> {metrics['unique_customers']:,} ({metrics['customers_delta']:+.1f}%)</p>
                </div>
                
                <h2>🏆 Top 10 Customers</h2>
                <table>
                    <tr><th>Customer ID</th><th>Revenue</th><th>Orders</th></tr>
                    {''.join([f"<tr><td>{r['customer_id']}</td><td>${r['total_revenue']:,.0f}</td><td>{r['order_count']}</td></tr>" for _, r in top_customers.head(10).iterrows()])}
                </table>
                
                <h2>📦 Top 10 Products</h2>
                <table>
                    <tr><th>Product</th><th>Revenue</th><th>Quantity</th></tr>
                    {''.join([f"<tr><td>{r['product_name']}</td><td>${r['total_price']:,.0f}</td><td>{r['quantity']}</td></tr>" for _, r in top_prod.head(10).iterrows()])}
                </table>
                
                <h2>🌍 Geographic Distribution</h2>
                <table>
                    <tr><th>Country</th><th>Revenue</th><th>Orders</th><th>Customers</th></tr>
                    {''.join([f"<tr><td>{r['country']}</td><td>${r['revenue']:,.0f}</td><td>{r['orders']}</td><td>{r['customers']}</td></tr>" for _, r in country_analysis.head(10).iterrows()])}
                </table>
                
                <div style="margin-top: 40px; text-align: center; color: rgb(102, 102, 102); border-top: 1px solid rgb(221, 221, 221); padding-top: 20px;">
                    <p>Automated report - Executive E-commerce Dashboard</p>
                    <p>© 2025 - Confidential Business Intelligence Report</p>
                </div>
            </body>
            </html>
            """
            
            st.download_button(
                "📥 DOWNLOAD REPORT",
                html,
                file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
                mime="text/html",
                use_container_width=True
            )
            
            st.success("✅ Report generated! Download above.")
            st.info("💡 Open HTML in browser, then Print → Save as PDF")

# Footer
st.markdown("---")
st.markdown(f"""
    <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, rgba(31, 41, 55, 0.6) 0%, rgba(17, 24, 39, 0.8) 100%); border-radius: 12px; border: 1px solid rgb(55, 65, 81);'>
        <div style='font-size: 36px; margin-bottom: 12px;'>⚡</div>
        <h3 style='color: rgb(243, 244, 246); margin: 10px 0; font-size: 22px; font-weight: 700; letter-spacing: -0.5px;'>Executive Dashboard v3.0</h3>
        <p style='color: rgb(156, 163, 175); font-size: 13px; margin: 10px 0; font-weight: 500;'>Built with Streamlit, Plotly & Machine Learning</p>
        <div style='display: flex; justify-content: center; gap: 12px; margin: 20px 0; flex-wrap: wrap;'>
            <span style='background: rgba(96, 165, 250, 0.2); padding: 6px 14px; border-radius: 20px; font-size: 11px; color: rgb(147, 197, 253); font-weight: 600; border: 1px solid rgba(96, 165, 250, 0.3);'>🔔 Smart Alerts</span>
            <span style='background: rgba(129, 140, 248, 0.2); padding: 6px 14px; border-radius: 20px; font-size: 11px; color: rgb(165, 180, 252); font-weight: 600; border: 1px solid rgba(129, 140, 248, 0.3);'>📈 ML Forecasting</span>
            <span style='background: rgba(251, 146, 60, 0.2); padding: 6px 14px; border-radius: 20px; font-size: 11px; color: rgb(253, 186, 116); font-weight: 600; border: 1px solid rgba(251, 146, 60, 0.3);'>📊 YoY Analysis</span>
            <span style='background: rgba(16, 185, 129, 0.2); padding: 6px 14px; border-radius: 20px; font-size: 11px; color: rgb(110, 231, 183); font-weight: 600; border: 1px solid rgba(16, 185, 129, 0.3);'>📄 PDF Reports</span>
            <span style='background: rgba(236, 72, 153, 0.2); padding: 6px 14px; border-radius: 20px; font-size: 11px; color: rgb(244, 114, 182); font-weight: 600; border: 1px solid rgba(236, 72, 153, 0.3);'>💾 Save Configs</span>
        </div>
        <p style='color: rgb(107, 114, 128); font-size: 11px; margin: 12px 0; font-weight: 500;'>📅 Last Updated: {datetime.now().strftime('%B %d, %Y - %H:%M')}</p>
        <div style='margin-top: 18px; padding-top: 18px; border-top: 1px solid rgb(55, 65, 81);'>
            <p style='color: rgb(156, 163, 175); font-size: 10px; margin: 0; font-weight: 500;'>💼 Data Analytics & Business Intelligence Portfolio</p>
            <p style='color: rgb(107, 114, 128); font-size: 9px; margin: 8px 0 0 0; font-weight: 400;'>🎯 RFM Segmentation • Pareto Analysis • Predictive Analytics • Interactive Visualizations</p>
        </div>
    </div>
""", unsafe_allow_html=True)
