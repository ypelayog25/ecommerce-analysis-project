"""
Executive E-commerce Dashboard - Power BI Style
Professional design with full responsive support for mobile devices
"""

import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# -----------------------
# Page config
# -----------------------
st.set_page_config(
    page_title="Executive Dashboard | E-commerce Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊"
)

# Power BI Style CSS - Fully Responsive
st.markdown("""
    <style>
    /* Import Professional Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700&family=Roboto:wght@400;500;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Segoe UI', 'Roboto', sans-serif;
    }
    
    /* Main Background - Power BI Style */
    .main {
        background-color: #f5f5f5;
        padding: 0.5rem;
    }
    
    /* Sidebar - Power BI Navigation Style */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2d2d2d 0%, #1f1f1f 100%);
        border-right: 3px solid #FFB600;
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    /* Power BI Header Style */
    .powerbi-header {
        background: linear-gradient(90deg, #2d2d2d 0%, #1f1f1f 100%);
        padding: 1.5rem 2rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border-left: 5px solid #FFB600;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .powerbi-title {
        color: #ffffff;
        font-size: clamp(20px, 4vw, 32px);
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
    }
    
    .powerbi-subtitle {
        color: #FFB600;
        font-size: clamp(12px, 2vw, 14px);
        font-weight: 500;
        margin: 5px 0 0 0;
        letter-spacing: 1px;
    }
    
    /* KPI Cards - Power BI Style */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #ffffff 0%, #f9f9f9 100%);
        padding: clamp(15px, 3vw, 25px);
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #0078D4;
        transition: all 0.3s ease;
        min-height: 120px;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 20px rgba(0, 120, 212, 0.2);
        border-left-color: #FFB600;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: clamp(11px, 1.8vw, 13px) !important;
        font-weight: 600 !important;
        color: #605E5C !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetricValue"] {
        font-size: clamp(24px, 4vw, 36px) !important;
        font-weight: 700 !important;
        color: #0078D4 !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: clamp(11px, 1.5vw, 13px) !important;
        font-weight: 600 !important;
    }
    
    /* Chart Container - Power BI Card Style */
    .chart-container {
        background: #ffffff;
        padding: clamp(15px, 2.5vw, 25px);
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
        border-top: 3px solid #0078D4;
    }
    
    /* Section Headers */
    .section-header {
        color: #323130;
        font-size: clamp(16px, 2.5vw, 20px);
        font-weight: 700;
        margin: 1.5rem 0 1rem 0;
        padding-left: 12px;
        border-left: 4px solid #0078D4;
    }
    
    /* Tabs - Power BI Style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: #ffffff;
        padding: 8px;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        flex-wrap: wrap;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: auto;
        min-height: 45px;
        background-color: #f3f2f1;
        border-radius: 6px;
        color: #323130;
        font-weight: 600;
        font-size: clamp(12px, 1.8vw, 14px);
        padding: 10px clamp(12px, 2vw, 20px);
        border: 2px solid transparent;
        white-space: normal;
        word-wrap: break-word;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #0078D4;
        color: #ffffff !important;
        border-color: #0078D4;
    }
    
    /* Buttons - Power BI Style */
    .stButton button {
        background-color: #0078D4;
        color: white;
        border: none;
        border-radius: 4px;
        padding: clamp(8px, 1.5vw, 12px) clamp(16px, 2.5vw, 24px);
        font-weight: 600;
        font-size: clamp(12px, 1.8vw, 14px);
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0, 120, 212, 0.2);
        width: 100%;
    }
    
    .stButton button:hover {
        background-color: #106EBE;
        box-shadow: 0 4px 8px rgba(0, 120, 212, 0.3);
    }
    
    /* Download Button - Power BI Accent */
    .stDownloadButton button {
        background-color: #FFB600;
        color: #1f1f1f !important;
        font-weight: 700;
    }
    
    .stDownloadButton button:hover {
        background-color: #FFAA00;
    }
    
    /* Expander - Power BI Card Style */
    div[data-testid="stExpander"] {
        background: #ffffff;
        border: 1px solid #e1dfdd;
        border-radius: 6px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    
    div[data-testid="stExpander"] summary {
        color: #323130 !important;
        font-weight: 600;
        font-size: clamp(13px, 2vw, 15px);
    }
    
    /* Text Colors */
    p, span, label, div {
        color: #323130 !important;
        font-size: clamp(12px, 1.8vw, 14px);
    }
    
    h1, h2, h3 {
        color: #323130 !important;
        font-weight: 700 !important;
    }
    
    /* Slider - Power BI Style */
    .stSlider [data-baseweb="slider"] {
        background-color: #e1dfdd;
    }
    
    .stSlider [role="slider"] {
        background-color: #0078D4;
    }
    
    /* Select/Multiselect */
    [data-baseweb="select"] {
        background-color: #ffffff;
        border: 1px solid #e1dfdd;
        border-radius: 4px;
    }
    
    /* Date Input */
    input[type="date"] {
        background-color: #ffffff;
        color: #323130;
        border: 1px solid #e1dfdd;
        border-radius: 4px;
        padding: clamp(8px, 1.5vw, 10px);
        font-size: clamp(12px, 1.8vw, 14px);
    }
    
    /* Dataframe - Power BI Table Style */
    [data-testid="stDataFrame"] {
        background-color: #ffffff;
        border-radius: 6px;
        overflow: hidden;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }
    
    /* Info/Warning Boxes */
    .stAlert {
        background-color: #ffffff;
        border-radius: 6px;
        border-left: 4px solid #0078D4;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }
    
    /* Divider */
    hr {
        border-color: #e1dfdd;
        margin: clamp(20px, 3vw, 30px) 0;
    }
    
    /* Stats Card */
    .stats-card {
        background: linear-gradient(135deg, #0078D4 0%, #106EBE 100%);
        padding: clamp(15px, 2.5vw, 20px);
        border-radius: 8px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 120, 212, 0.2);
        margin: 0.5rem 0;
    }
    
    .stats-value {
        font-size: clamp(20px, 3.5vw, 28px);
        font-weight: 700;
        margin: 8px 0;
    }
    
    .stats-label {
        font-size: clamp(11px, 1.8vw, 12px);
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Responsive Grid Fix */
    [data-testid="column"] {
        padding: 0 0.5rem;
    }
    
    /* Mobile Optimizations */
    @media (max-width: 768px) {
        .main {
            padding: 0.25rem;
        }
        
        .powerbi-header {
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        div[data-testid="metric-container"] {
            min-height: 100px;
            margin-bottom: 0.5rem;
        }
        
        .chart-container {
            padding: 12px;
            margin-bottom: 1rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 8px 12px;
            font-size: 12px;
        }
        
        [data-testid="column"] {
            padding: 0 0.25rem;
        }
        
        .section-header {
            font-size: 16px;
            margin: 1rem 0 0.5rem 0;
        }
    }
    
    /* Extra Small Devices */
    @media (max-width: 480px) {
        .powerbi-title {
            font-size: 18px;
        }
        
        .powerbi-subtitle {
            font-size: 11px;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 20px !important;
        }
        
        .stButton button {
            padding: 8px 12px;
            font-size: 12px;
        }
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f3f2f1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #0078D4;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #106EBE;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------
# Data Loading with Caching
# -----------------------
@st.cache_data(ttl=3600)
def load_data():
    """Load and cache dataset"""
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
# Power BI Header
# -----------------------
st.markdown("""
    <div class='powerbi-header'>
        <h1 class='powerbi-title'>📊 Executive E-commerce Dashboard</h1>
        <p class='powerbi-subtitle'>REAL-TIME BUSINESS INTELLIGENCE & ANALYTICS</p>
    </div>
""", unsafe_allow_html=True)

# -----------------------
# Sidebar - Power BI Navigation
# -----------------------
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 1.5rem 0; border-bottom: 2px solid #FFB600;'>
            <div style='font-size: 48px; margin-bottom: 10px;'>📊</div>
            <h2 style='margin: 0; font-size: 20px; color: #FFB600 !important;'>DASHBOARD</h2>
            <p style='margin: 5px 0 0 0; font-size: 11px; color: #b0b0b0 !important;'>Control Panel</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    with st.expander("📅 DATE FILTERS", expanded=True):
        min_date = df['order_date'].min().date()
        max_date = df['order_date'].max().date()
        
        start_date = st.date_input("From Date", min_date, min_value=min_date, max_value=max_date)
        end_date = st.date_input("To Date", max_date, min_value=min_date, max_value=max_date)
        
        st.markdown("**Quick Select:**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("7 Days", use_container_width=True):
                start_date = max_date - timedelta(days=7)
            if st.button("Quarter", use_container_width=True):
                start_date = max_date - timedelta(days=90)
        with col2:
            if st.button("30 Days", use_container_width=True):
                start_date = max_date - timedelta(days=30)
            if st.button("YTD", use_container_width=True):
                start_date = datetime(max_date.year, 1, 1).date()
    
    with st.expander("🌍 GEOGRAPHY", expanded=True):
        countries = sorted(df['country'].dropna().unique())
        select_all = st.checkbox("Select All", value=True)
        
        if select_all:
            selected_countries = countries
        else:
            selected_countries = st.multiselect("Countries", countries, default=countries[:3])
    
    with st.expander("⚙️ SETTINGS", expanded=False):
        top_n = st.slider("Top N Records", 5, 50, 10, 5)
        show_details = st.checkbox("Show Detailed Stats", value=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='text-align: center; padding: 1rem; background: rgba(255, 182, 0, 0.1); border-radius: 6px; border: 1px solid #FFB600;'>
            <p style='margin: 0; font-size: 11px; color: #FFB600 !important; font-weight: 600;'>LAST UPDATED</p>
            <p style='margin: 5px 0 0 0; font-size: 12px; color: #ffffff !important;'>{datetime.now().strftime('%b %d, %Y')}</p>
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
    st.warning("⚠️ No data available. Please adjust filters.")
    st.stop()

# -----------------------
# Calculate Metrics
# -----------------------
@st.cache_data
def calculate_metrics(df_current, df_all):
    """Calculate KPIs"""
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
# KPI Section
# -----------------------
st.markdown("<h3 class='section-header'>📊 Key Performance Indicators</h3>", unsafe_allow_html=True)

# Responsive KPI layout
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="💰 Total Revenue",
        value=f"${metrics['total_revenue']:,.0f}",
        delta=f"{metrics['revenue_delta']:.1f}%"
    )

with col2:
    st.metric(
        label="🛒 Orders",
        value=f"{metrics['total_orders']:,}",
        delta=f"{metrics['orders_delta']:.1f}%"
    )

with col3:
    st.metric(
        label="👥 Customers",
        value=f"{metrics['unique_customers']:,}",
        delta=f"{metrics['customers_delta']:.1f}%"
    )

with col4:
    st.metric(
        label="📦 Units Sold",
        value=f"{metrics['total_quantity']:,}"
    )

with col5:
    st.metric(
        label="💵 Avg Order",
        value=f"${metrics['avg_order_value']:.2f}"
    )

st.markdown("<hr>", unsafe_allow_html=True)

# -----------------------
# Power BI Chart Styling
# -----------------------
def style_chart(fig, title="", height=400):
    """Apply Power BI styling to charts"""
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=16, color="#323130", family="Segoe UI", weight=700),
            x=0,
            xanchor='left'
        ),
        font=dict(size=12, color="#605E5C", family="Segoe UI"),
        margin=dict(l=20, r=20, t=60, b=20),
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        hovermode='x unified',
        height=height,
        hoverlabel=dict(
            bgcolor="#ffffff",
            font_size=12,
            font_family="Segoe UI",
            bordercolor="#0078D4"
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11)
        )
    )
    fig.update_xaxes(
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='#e1dfdd',
        tickfont=dict(size=11)
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=0.5,
        gridcolor='#f3f2f1',
        showline=False,
        tickfont=dict(size=11)
    )
    return fig

# Power BI Color Palette
pbi_blue = '#0078D4'
pbi_teal = '#00BCF2'
pbi_orange = '#FFB900'
pbi_green = '#107C10'
pbi_red = '#E81123'
pbi_colors = [pbi_blue, pbi_teal, pbi_orange, pbi_green, pbi_red]

# -----------------------
# Tabs
# -----------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Revenue", 
    "👥 Customers", 
    "📦 Products", 
    "🌍 Geography"
])

# === TAB 1: Revenue ===
with tab1:
    # Revenue Trend
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    
    monthly_revenue = df_filtered.groupby(df_filtered['order_date'].dt.to_period('M'))['total_price'].sum().reset_index()
    monthly_revenue['order_date'] = monthly_revenue['order_date'].dt.to_timestamp()
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=monthly_revenue['order_date'],
        y=monthly_revenue['total_price'],
        mode='lines+markers',
        name='Revenue',
        line=dict(color=pbi_blue, width=3),
        marker=dict(size=8, color=pbi_blue),
        fill='tozeroy',
        fillcolor='rgba(0, 120, 212, 0.1)',
        hovertemplate='<b>%{x|%b %Y}</b><br>$%{y:,.0f}<extra></extra>'
    ))
    
    # Trend line
    if len(monthly_revenue) > 1:
        z = np.polyfit(range(len(monthly_revenue)), monthly_revenue['total_price'], 1)
        p = np.poly1d(z)
        fig_trend.add_trace(go.Scatter(
            x=monthly_revenue['order_date'],
            y=p(range(len(monthly_revenue))),
            mode='lines',
            name='Trend',
            line=dict(color=pbi_red, width=2, dash='dash'),
            hovertemplate='<b>Trend</b><br>$%{y:,.0f}<extra></extra>'
        ))
    
    st.plotly_chart(style_chart(fig_trend, "📊 Monthly Revenue Trend"), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Two column layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        
        # Revenue by Day of Week
        dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_revenue = df_filtered.groupby('day_of_week')['total_price'].sum().reindex(dow_order).reset_index()
        
        fig_dow = go.Figure(data=[
            go.Bar(
                x=dow_revenue['day_of_week'],
                y=dow_revenue['total_price'],
                marker=dict(color=pbi_blue),
                text=[f"${val:,.0f}" for val in dow_revenue['total_price']],
                textposition='outside',
                textfont=dict(size=10),
                hovertemplate='<b>%{x}</b><br>$%{y:,.0f}<extra></extra>'
            )
        ])
        
        st.plotly_chart(style_chart(fig_dow, "📅 Revenue by Day of Week", height=350), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        
        # Top Countries Pie
        country_revenue = df_filtered.groupby('country')['total_price'].sum().nlargest(5).reset_index()
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=country_revenue['country'],
            values=country_revenue['total_price'],
            hole=0.4,
            marker=dict(colors=pbi_colors),
            textinfo='label+percent',
            textfont=dict(size=11),
            hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>'
        )])
        
        st.plotly_chart(style_chart(fig_pie, "🌍 Top 5 Countries", height=350), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# === TAB 2: Customers ===
with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        
        # Top Customers
        top_customers = df_filtered.groupby('customer_id').agg({
            'total_price': 'sum',
            'order_id': 'nunique'
        }).nlargest(top_n, 'total_price').reset_index()
        top_customers.columns = ['customer_id', 'revenue', 'orders']
        
        fig_customers = go.Figure(data=[
            go.Bar(
                y=top_customers['customer_id'],
                x=top_customers['revenue'],
                orientation='h',
                marker=dict(color=pbi_teal),
                text=[f"${val:,.0f}" for val in top_customers['revenue']],
                textposition='outside',
                textfont=dict(size=10),
                hovertemplate='<b>%{y}</b><br>Revenue: $%{x:,.0f}<extra></extra>'
            )
        ])
        
        st.plotly_chart(style_chart(fig_customers, f"🌟 Top {top_n} Customers", height=400), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        
        # Order Frequency
        order_freq = df_filtered.groupby('customer_id')['order_id'].nunique().value_counts().sort_index().reset_index()
        order_freq.columns = ['orders', 'customers']
        
        fig_freq = go.Figure(data=[
            go.Bar(
                x=order_freq['orders'],
                y=order_freq['customers'],
                marker=dict(color=pbi_orange),
                text=order_freq['customers'],
                textposition='outside',
                textfont=dict(size=10),
                hovertemplate='<b>%{x} Orders</b><br>%{y} Customers<extra></extra>'
            )
        ])
        
        st.plotly_chart(style_chart(fig_freq, "🔄 Order Frequency", height=400), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Customer Segmentation
    if show_details:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("#### 🎯 Customer Segmentation (RFM Analysis)")
        
        snapshot_date = df_filtered['order_date'].max() + timedelta(days=1)
        rfm = df_filtered.groupby('customer_id').agg({
            'order_date': lambda x: (snapshot_date - x.max()).days,
            'order_id': 'nunique',
            'total_price': 'sum'
        }).reset_index()
        rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']
        
        rfm['segment'] = 'Regular'
        rfm.loc[(rfm['frequency'] >= rfm['frequency'].quantile(0.75)) & 
                (rfm['monetary'] >= rfm['monetary'].quantile(0.75)), 'segment'] = 'VIP'
        rfm.loc[(rfm['recency'] <= rfm['recency'].quantile(0.25)) & 
                (rfm['frequency'] >= rfm['frequency'].quantile(0.5)), 'segment'] = 'Active'
        rfm.loc[rfm['recency'] >= rfm['recency'].quantile(0.75), 'segment'] = 'At Risk'
        
        segment_summary = rfm.groupby('segment').agg({
            'customer_id': 'count',
            'monetary': 'sum'
        }).reset_index()
        segment_summary.columns = ['segment', 'customers', 'revenue']
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_seg_count = go.Figure(data=[
                go.Bar(
                    x=segment_summary['segment'],
                    y=segment_summary['customers'],
                    marker=dict(color=pbi_colors[:len(segment_summary)]),
                    text=segment_summary['customers'],
                    textposition='outside',
                    textfont=dict(size=11),
                    hovertemplate='<b>%{x}</b><br>%{y} Customers<extra></extra>'
                )
            ])
            st.plotly_chart(style_chart(fig_seg_count, "👥 Customers by Segment", height=300), use_container_width=True)
        
        with col2:
            fig_seg_rev = go.Figure(data=[
                go.Bar(
                    x=segment_summary['segment'],
                    y=segment_summary['revenue'],
                    marker=dict(color=pbi_colors[:len(segment_summary)]),
                    text=[f"${val:,.0f}" for val in segment_summary['revenue']],
                    textposition='outside',
                    textfont=dict(size=11),
                    hovertemplate='<b>%{x}</b><br>$%{y:,.0f}<extra></extra>'
                )
            ])
            st.plotly_chart(style_chart(fig_seg_rev, "💰 Revenue by Segment", height=300), use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# === TAB 3: Products ===
with tab3:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        
        # Top Products by Revenue
        top_products = df_filtered.groupby('product_name').agg({
            'total_price': 'sum',
            'quantity': 'sum'
        }).nlargest(top_n, 'total_price').reset_index()
        
        fig_products = go.Figure(data=[
            go.Bar(
                y=top_products['product_name'],
                x=top_products['total_price'],
                orientation='h',
                marker=dict(color=pbi_green),
                text=[f"${val:,.0f}" for val in top_products['total_price']],
                textposition='outside',
                textfont=dict(size=10),
                hovertemplate='<b>%{y}</b><br>Revenue: $%{x:,.0f}<extra></extra>'
            )
        ])
        
        st.plotly_chart(style_chart(fig_products, f"🎯 Top {top_n} Products by Revenue", height=450), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        
        # Top Products by Quantity
        top_qty = df_filtered.groupby('product_name')['quantity'].sum().nlargest(top_n).reset_index()
        
        fig_qty = go.Figure(data=[
            go.Bar(
                y=top_qty['product_name'],
                x=top_qty['quantity'],
                orientation='h',
                marker=dict(color=pbi_orange),
                text=top_qty['quantity'],
                textposition='outside',
                textfont=dict(size=10),
                hovertemplate='<b>%{y}</b><br>Units: %{x:,}<extra></extra>'
            )
        ])
        
        st.plotly_chart(style_chart(fig_qty, f"📦 Top {top_n} by Quantity", height=450), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Price Distribution
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        fig_price = go.Figure()
        
        fig_price.add_trace(go.Histogram(
            x=df_filtered['unit_price'],
            nbinsx=40,
            marker=dict(color=pbi_blue, line=dict(color='white', width=1)),
            opacity=0.8,
            name='Distribution',
            hovertemplate='Price: $%{x:.2f}<br>Count: %{y}<extra></extra>'
        ))
        
        st.plotly_chart(style_chart(fig_price, "💲 Unit Price Distribution", height=350), use_container_width=True)
    
    with col2:
        price_stats = df_filtered['unit_price'].describe()
        
        st.markdown("""
            <div style='background: linear-gradient(135deg, #0078D4 0%, #106EBE 100%); 
                        padding: 15px; border-radius: 6px; color: white; margin-top: 60px;'>
                <p style='margin: 0; font-size: 11px; opacity: 0.9;'>PRICE STATS</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.metric("Mean", f"${price_stats['mean']:.2f}")
        st.metric("Median", f"${price_stats['50%']:.2f}")
        st.metric("Max", f"${price_stats['max']:.2f}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# === TAB 4: Geography ===
with tab4:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    
    # Country Analysis
    country_data = df_filtered.groupby('country').agg({
        'total_price': 'sum',
        'order_id': 'nunique',
        'customer_id': 'nunique'
    }).reset_index().sort_values('total_price', ascending=False)
    country_data.columns = ['country', 'revenue', 'orders', 'customers']
    
    fig_country = go.Figure(data=[
        go.Bar(
            x=country_data['country'],
            y=country_data['revenue'],
            marker=dict(
                color=country_data['revenue'],
                colorscale='Blues',
                showscale=True,
                colorbar=dict(title="Revenue", tickprefix="$", len=0.7)
            ),
            text=[f"${val:,.0f}" for val in country_data['revenue']],
            textposition='outside',
            textfont=dict(size=11),
            hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>'
        )
    ])
    
    st.plotly_chart(style_chart(fig_country, "🌍 Revenue by Country", height=400), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Country Performance Table
    if show_details:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("#### 📋 Country Performance Details")
        
        country_data['avg_order_value'] = country_data['revenue'] / country_data['orders']
        country_data['revenue_formatted'] = country_data['revenue'].apply(lambda x: f"${x:,.0f}")
        country_data['aov_formatted'] = country_data['avg_order_value'].apply(lambda x: f"${x:.2f}")
        
        display_data = country_data[['country', 'revenue_formatted', 'orders', 'customers', 'aov_formatted']]
        display_data.columns = ['Country', 'Total Revenue', 'Orders', 'Customers', 'Avg Order Value']
        
        st.dataframe(
            display_data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Country": st.column_config.TextColumn("🌍 Country", width="medium"),
                "Total Revenue": st.column_config.TextColumn("💰 Revenue", width="medium"),
                "Orders": st.column_config.NumberColumn("🛒 Orders", format="%d"),
                "Customers": st.column_config.NumberColumn("👥 Customers", format="%d"),
                "Avg Order Value": st.column_config.TextColumn("💵 AOV", width="small")
            }
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Geographic Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        
        fig_country_pie = go.Figure(data=[go.Pie(
            labels=country_data['country'][:8],
            values=country_data['revenue'][:8],
            hole=0.4,
            marker=dict(colors=px.colors.qualitative.Set3),
            textinfo='label+percent',
            textfont=dict(size=10),
            hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>'
        )])
        
        st.plotly_chart(style_chart(fig_country_pie, "🌎 Revenue Distribution", height=350), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        
        # Orders by Country
        fig_orders = go.Figure(data=[
            go.Bar(
                x=country_data['country'][:8],
                y=country_data['orders'][:8],
                marker=dict(color=pbi_teal),
                text=country_data['orders'][:8],
                textposition='outside',
                textfont=dict(size=10),
                hovertemplate='<b>%{x}</b><br>%{y} Orders<extra></extra>'
            )
        ])
        
        st.plotly_chart(style_chart(fig_orders, "📊 Orders by Country", height=350), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------
# Advanced Analytics Section
# -----------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h3 class='section-header'>🔬 Advanced Analytics</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    
    # Growth Rate Analysis
    monthly_revenue = df_filtered.groupby(df_filtered['order_date'].dt.to_period('M'))['total_price'].sum().reset_index()
    monthly_revenue['order_date'] = monthly_revenue['order_date'].dt.to_timestamp()
    monthly_revenue['growth_rate'] = monthly_revenue['total_price'].pct_change() * 100
    
    fig_growth = go.Figure()
    
    colors = [pbi_green if x >= 0 else pbi_red for x in monthly_revenue['growth_rate']]
    
    fig_growth.add_trace(go.Bar(
        x=monthly_revenue['order_date'],
        y=monthly_revenue['growth_rate'],
        marker=dict(color=colors),
        text=[f"{val:.1f}%" if not pd.isna(val) else "" for val in monthly_revenue['growth_rate']],
        textposition='outside',
        textfont=dict(size=10),
        hovertemplate='<b>%{x|%b %Y}</b><br>Growth: %{y:.1f}%<extra></extra>'
    ))
    
    fig_growth.add_hline(y=0, line_dash="solid", line_color="#e1dfdd", line_width=2)
    
    st.plotly_chart(style_chart(fig_growth, "📈 Month-over-Month Growth Rate", height=350), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    
    # Pareto Analysis
    product_revenue = df_filtered.groupby('product_name')['total_price'].sum().sort_values(ascending=False).reset_index()
    product_revenue['cumulative_pct'] = (product_revenue['total_price'].cumsum() / product_revenue['total_price'].sum()) * 100
    
    fig_pareto = go.Figure()
    
    fig_pareto.add_trace(go.Bar(
        x=product_revenue.index[:15],
        y=product_revenue['total_price'][:15],
        name='Revenue',
        marker=dict(color=pbi_blue),
        yaxis='y',
        hovertemplate='Rank %{x}<br>$%{y:,.0f}<extra></extra>'
    ))
    
    fig_pareto.add_trace(go.Scatter(
        x=product_revenue.index[:15],
        y=product_revenue['cumulative_pct'][:15],
        name='Cumulative %',
        mode='lines+markers',
        marker=dict(color=pbi_orange, size=6),
        line=dict(color=pbi_orange, width=2),
        yaxis='y2',
        hovertemplate='%{y:.1f}%<extra></extra>'
    ))
    
    fig_pareto.update_layout(
        yaxis=dict(title='Revenue ($)', side='left'),
        yaxis2=dict(title='Cumulative %', overlaying='y', side='right', range=[0, 100])
    )
    
    st.plotly_chart(style_chart(fig_pareto, "📊 Pareto Analysis (80/20 Rule)", height=350), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------
# Executive Summary Cards
# -----------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h3 class='section-header'>🎯 Executive Summary</h3>", unsafe_allow_html=True)

sum_col1, sum_col2, sum_col3, sum_col4 = st.columns(4)

with sum_col1:
    top_country = country_data.iloc[0]
    st.markdown(f"""
        <div class='stats-card'>
            <div class='stats-label'>TOP MARKET</div>
            <div class='stats-value'>{top_country['country']}</div>
            <div style='font-size: 16px; margin-top: 5px;'>${top_country['revenue']:,.0f}</div>
        </div>
    """, unsafe_allow_html=True)

with sum_col2:
    best_product = top_products.iloc[0]
    product_name_short = best_product['product_name'][:20] + "..." if len(best_product['product_name']) > 20 else best_product['product_name']
    st.markdown(f"""
        <div class='stats-card' style='background: linear-gradient(135deg, #107C10 0%, #0B5A08 100%);'>
            <div class='stats-label'>BEST PRODUCT</div>
            <div class='stats-value' style='font-size: clamp(14px, 2.5vw, 18px);'>{product_name_short}</div>
            <div style='font-size: 16px; margin-top: 5px;'>${best_product['total_price']:,.0f}</div>
        </div>
    """, unsafe_allow_html=True)

with sum_col3:
    avg_growth = monthly_revenue['growth_rate'].mean()
    growth_color = "#107C10" if avg_growth >= 0 else "#E81123"
    st.markdown(f"""
        <div class='stats-card' style='background: linear-gradient(135deg, {growth_color} 0%, {growth_color}DD 100%);'>
            <div class='stats-label'>AVG GROWTH RATE</div>
            <div class='stats-value'>{avg_growth:.1f}%</div>
            <div style='font-size: 14px; margin-top: 5px;'>Month-over-Month</div>
        </div>
    """, unsafe_allow_html=True)

with sum_col4:
    if 'segment' in rfm.columns:
        vip_count = rfm[rfm['segment'] == 'VIP'].shape[0]
        vip_revenue = rfm[rfm['segment'] == 'VIP']['monetary'].sum()
    else:
        vip_count = 0
        vip_revenue = 0
    
    st.markdown(f"""
        <div class='stats-card' style='background: linear-gradient(135deg, #FFB900 0%, #FF8C00 100%);'>
            <div class='stats-label'>VIP CUSTOMERS</div>
            <div class='stats-value'>{vip_count}</div>
            <div style='font-size: 14px; margin-top: 5px;'>${vip_revenue:,.0f} Revenue</div>
        </div>
    """, unsafe_allow_html=True)

# -----------------------
# Export Section
# -----------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h3 class='section-header'>📥 Export Data</h3>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.download_button(
        "📊 Filtered Dataset",
        df_filtered.to_csv(index=False).encode('utf-8'),
        file_name=f"data_export_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with col2:
    st.download_button(
        "👥 Top Customers",
        top_customers.to_csv(index=False).encode('utf-8'),
        file_name=f"customers_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with col3:
    st.download_button(
        "📦 Top Products",
        top_products.to_csv(index=False).encode('utf-8'),
        file_name=f"products_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with col4:
    st.download_button(
        "🌍 Country Report",
        country_data.to_csv(index=False).encode('utf-8'),
        file_name=f"countries_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# -----------------------
# Footer - Power BI Style
# -----------------------
st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(f"""
    <div style='text-align: center; padding: 2rem 1rem; background: linear-gradient(90deg, #2d2d2d 0%, #1f1f1f 100%); 
                border-radius: 8px; border-left: 5px solid #FFB600;'>
        <h3 style='color: #FFB600 !important; margin: 0 0 10px 0; font-size: clamp(16px, 2.5vw, 20px);'>
            📊 EXECUTIVE E-COMMERCE DASHBOARD
        </h3>
        <p style='color: #ffffff !important; margin: 5px 0; font-size: clamp(12px, 1.8vw, 14px);'>
            Built with Streamlit & Plotly | Power BI Style Design
        </p>
        <p style='color: #b0b0b0 !important; margin: 5px 0; font-size: clamp(11px, 1.5vw, 12px);'>
            📅 Last Updated: {datetime.now().strftime('%B %d, %Y at %H:%M')}
        </p>
        <div style='margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255, 182, 0, 0.3);'>
            <p style='color: #b0b0b0 !important; margin: 0; font-size: clamp(10px, 1.5vw, 11px);'>
                💼 Data Analytics Portfolio Project | Business Intelligence
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)
