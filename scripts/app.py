"""
Professional Executive E-commerce Dashboard (Streamlit)
Premium design with dark mode and stunning visuals for recruiters
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
    page_title="Executive E-commerce Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊"
)

# Premium Dark Theme CSS
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background */
    .main {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    /* Title Styling */
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 800 !important;
    }
    
    /* Metric Cards - Premium Design */
    [data-testid="stMetricValue"] {
        font-size: 36px !important;
        font-weight: 800 !important;
        color: #00ff87 !important;
        text-shadow: 0 0 20px rgba(0, 255, 135, 0.5);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 14px !important;
        font-weight: 600 !important;
        color: #a8b2d1 !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 14px !important;
        font-weight: 600 !important;
    }
    
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 50px rgba(102, 126, 234, 0.6);
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(26, 26, 46, 0.8);
        padding: 10px;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        color: #a8b2d1;
        font-weight: 600;
        font-size: 15px;
        padding: 0 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff !important;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Button Styling */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    }
    
    /* Download Button Special Style */
    .stDownloadButton button {
        background: linear-gradient(135deg, #00ff87 0%, #60efff 100%);
        color: #1a1a2e !important;
        font-weight: 700;
    }
    
    .stDownloadButton button:hover {
        box-shadow: 0 8px 25px rgba(0, 255, 135, 0.5);
    }
    
    /* Expander Styling */
    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    
    div[data-testid="stExpander"] summary {
        color: #ffffff !important;
        font-weight: 600;
    }
    
    /* Text and Labels */
    p, span, label {
        color: #e0e0e0 !important;
        font-size: 14px;
    }
    
    /* Slider */
    .stSlider [data-baseweb="slider"] {
        background-color: rgba(102, 126, 234, 0.3);
    }
    
    /* Selectbox and Multiselect */
    [data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.08);
        border-radius: 10px;
    }
    
    /* Date Input */
    input[type="date"] {
        background-color: rgba(255, 255, 255, 0.08);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 10px;
    }
    
    /* Dataframe Styling */
    [data-testid="stDataFrame"] {
        background-color: rgba(26, 26, 46, 0.8);
        border-radius: 15px;
        overflow: hidden;
    }
    
    /* Success/Info/Warning Messages */
    .stAlert {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        border-left: 4px solid #667eea;
    }
    
    /* Divider */
    hr {
        border-color: rgba(255, 255, 255, 0.1);
        margin: 30px 0;
    }
    
    /* Checkbox */
    [data-testid="stCheckbox"] {
        color: white !important;
    }
    
    /* Header Animation */
    @keyframes glow {
        0%, 100% { text-shadow: 0 0 20px rgba(0, 255, 135, 0.5), 0 0 40px rgba(0, 255, 135, 0.3); }
        50% { text-shadow: 0 0 30px rgba(0, 255, 135, 0.8), 0 0 60px rgba(0, 255, 135, 0.5); }
    }
    
    .glowing-title {
        animation: glow 2s ease-in-out infinite;
    }
    
    /* Card Container */
    .card-container {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin: 15px 0;
    }
    
    /* Subheader Style */
    .stMarkdown h3 {
        color: #00ff87 !important;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
        padding-left: 15px;
        border-left: 4px solid #00ff87;
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
# Premium Header with Animation
# -----------------------
st.markdown("""
    <div style='text-align:center; padding: 40px 0 30px 0;'>
        <h1 class='glowing-title' style='font-size: 52px; margin-bottom: 10px; background: linear-gradient(135deg, #00ff87 0%, #60efff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;'>
            📊 EXECUTIVE E-COMMERCE DASHBOARD
        </h1>
        <p style='font-size: 18px; color: #a8b2d1; font-weight: 500; letter-spacing: 2px;'>
            ✨ REAL-TIME BUSINESS INTELLIGENCE & ADVANCED ANALYTICS ✨
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<hr style='margin: 20px 0; border: 1px solid rgba(0, 255, 135, 0.3);'>", unsafe_allow_html=True)

# -----------------------
# Premium Sidebar
# -----------------------
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <div style='font-size: 60px; margin-bottom: 10px;'>⚡</div>
            <h2 style='margin: 0; font-size: 24px; background: linear-gradient(135deg, #00ff87 0%, #60efff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                CONTROL CENTER
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border-color: rgba(255, 255, 255, 0.2);'>", unsafe_allow_html=True)
    
    with st.expander("📅 DATE RANGE FILTER", expanded=True):
        date_col1, date_col2 = st.columns(2)
        
        min_date = df['order_date'].min().date()
        max_date = df['order_date'].max().date()
        
        with date_col1:
            start_date = st.date_input("📍 From", min_date, min_value=min_date, max_value=max_date)
        with date_col2:
            end_date = st.date_input("📍 To", max_date, min_value=min_date, max_value=max_date)
        
        st.markdown("**⚡ Quick Filters:**")
        col_q1, col_q2 = st.columns(2)
        with col_q1:
            if st.button("📅 Last 30 Days", use_container_width=True):
                start_date = max_date - timedelta(days=30)
            if st.button("📊 Last Quarter", use_container_width=True):
                start_date = max_date - timedelta(days=90)
        with col_q2:
            if st.button("⚡ Last 7 Days", use_container_width=True):
                start_date = max_date - timedelta(days=7)
            if st.button("📈 Year to Date", use_container_width=True):
                start_date = datetime(max_date.year, 1, 1).date()
    
    with st.expander("🌍 GEOGRAPHIC FILTER", expanded=True):
        countries = sorted(df['country'].dropna().unique())
        select_all = st.checkbox("✅ Select All Countries", value=True)
        
        if select_all:
            selected_countries = countries
        else:
            selected_countries = st.multiselect("🌎 Choose Countries", countries, default=countries[:3])
    
    with st.expander("⚙️ DISPLAY SETTINGS", expanded=False):
        top_n = st.slider("🔢 Top N Items", 5, 50, 10, 5)
        chart_theme = st.selectbox("🎨 Chart Theme", ["plotly_dark", "plotly_white", "seaborn", "ggplot2"])
    
    st.markdown("<hr style='border-color: rgba(255, 255, 255, 0.2); margin: 30px 0;'>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='text-align: center; padding: 20px; background: rgba(0, 255, 135, 0.1); border-radius: 15px; border: 1px solid rgba(0, 255, 135, 0.3);'>
            <p style='margin: 0; font-size: 12px; color: #00ff87; font-weight: 600;'>💼 PORTFOLIO DASHBOARD</p>
            <p style='margin: 5px 0 0 0; font-size: 11px; color: #a8b2d1;'>Built with Streamlit & Plotly</p>
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
# Premium KPI Cards
# -----------------------
st.markdown("### 🎯 KEY PERFORMANCE INDICATORS")
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.metric(
        label="💰 TOTAL REVENUE",
        value=f"${metrics['total_revenue']:,.0f}",
        delta=f"{metrics['revenue_delta']:.1f}% vs prev"
    )

with kpi2:
    st.metric(
        label="🛒 TOTAL ORDERS",
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
        label="📦 UNITS SOLD",
        value=f"{metrics['total_quantity']:,}"
    )

with kpi5:
    st.metric(
        label="💵 AVG ORDER",
        value=f"${metrics['avg_order_value']:.2f}"
    )

st.markdown("<hr style='margin: 30px 0; border: 1px solid rgba(0, 255, 135, 0.2);'>", unsafe_allow_html=True)

# -----------------------
# Helper for Plotly Styling (Dark Theme)
# -----------------------
def style_fig(fig, title="", title_font=22, axis_font=12):
    """Apply premium dark theme styling to Plotly figures"""
    fig.update_layout(
        title=dict(
            text=title, 
            font=dict(size=title_font, color="#00ff87", family="Inter"),
            x=0.5,
            xanchor='center'
        ),
        font=dict(size=axis_font, color="#e0e0e0", family="Inter"),
        margin=dict(l=60, r=60, t=80, b=60),
        template="plotly_dark",
        hovermode='x unified',
        plot_bgcolor='rgba(26, 26, 46, 0.6)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        hoverlabel=dict(
            bgcolor="rgba(102, 126, 234, 0.9)",
            font_size=13,
            font_family="Inter"
        )
    )
    fig.update_xaxes(
        showgrid=True, 
        gridwidth=0.5, 
        gridcolor='rgba(255, 255, 255, 0.1)',
        showline=True, 
        linewidth=1, 
        linecolor='rgba(255, 255, 255, 0.2)'
    )
    fig.update_yaxes(
        showgrid=True, 
        gridwidth=0.5, 
        gridcolor='rgba(255, 255, 255, 0.1)'
    )
    return fig

# -----------------------
# Premium Color Palettes
# -----------------------
neon_colors = ['#00ff87', '#60efff', '#ff006e', '#ffbe0b', '#8338ec']
gradient_colors = px.colors.sequential.Viridis

# -----------------------
# Dashboard Tabs with Premium Icons
# -----------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 REVENUE ANALYSIS", 
    "👥 CUSTOMER INTEL", 
    "📦 PRODUCT PERF", 
    "🌍 GEO INSIGHTS",
    "🔬 ADVANCED"
])

# === TAB 1: Revenue Analysis ===
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📈 REVENUE TREND OVER TIME")
        
        monthly_revenue = df_filtered.groupby(df_filtered['order_date'].dt.to_period('M'))['total_price'].sum().reset_index()
        monthly_revenue['order_date'] = monthly_revenue['order_date'].dt.to_timestamp()
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=monthly_revenue['order_date'],
            y=monthly_revenue['total_price'],
            mode='lines+markers',
            name='Revenue',
            line=dict(color='#00ff87', width=4),
            marker=dict(size=10, color='#00ff87', line=dict(color='#ffffff', width=2)),
            fill='tozeroy',
            fillcolor='rgba(0, 255, 135, 0.2)'
        ))
        
        z = np.polyfit(range(len(monthly_revenue)), monthly_revenue['total_price'], 1)
        p = np.poly1d(z)
        fig_trend.add_trace(go.Scatter(
            x=monthly_revenue['order_date'],
            y=p(range(len(monthly_revenue))),
            mode='lines',
            name='Trend Line',
            line=dict(color='#ff006e', width=3, dash='dash')
        ))
        
        st.plotly_chart(style_fig(fig_trend, "📊 Monthly Revenue Performance"), use_container_width=True)
    
    with col2:
        st.markdown("### 🏆 TOP COUNTRIES")
        country_revenue = df_filtered.groupby('country')['total_price'].sum().nlargest(5).reset_index()
        
        fig_pie = px.pie(
            country_revenue,
            values='total_price',
            names='country',
            hole=0.5,
            color_discrete_sequence=neon_colors
        )
        fig_pie.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            textfont=dict(size=14, family="Inter", color="white")
        )
        fig_pie.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='#e0e0e0', family="Inter"),
            showlegend=True,
            legend=dict(font=dict(color='#e0e0e0'))
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("### 📅 REVENUE BY DAY OF WEEK")
    dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_revenue = df_filtered.groupby('day_of_week')['total_price'].sum().reindex(dow_order).reset_index()
    
    fig_dow = go.Figure(data=[
        go.Bar(
            x=dow_revenue['day_of_week'],
            y=dow_revenue['total_price'],
            marker=dict(
                color=dow_revenue['total_price'],
                colorscale='Viridis',
                showscale=True,
                line=dict(color='rgba(255, 255, 255, 0.3)', width=2)
            ),
            text=[f"${val:,.0f}" for val in dow_revenue['total_price']],
            textposition='outside',
            textfont=dict(size=12, color='#00ff87')
        )
    ])
    st.plotly_chart(style_fig(fig_dow, "🔥 Weekly Revenue Pattern"), use_container_width=True)

# === TAB 2: Customer Intelligence ===
with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### 🌟 TOP {top_n} CUSTOMERS")
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
                    line=dict(color='rgba(255, 255, 255, 0.3)', width=1)
                ),
                text=[f"${val:,.0f}" for val in top_customers['total_revenue']],
                textposition='outside',
                textfont=dict(color='#60efff')
            )
        ])
        st.plotly_chart(style_fig(fig_customers, "💎 Revenue Champions"), use_container_width=True)
    
    with col2:
        st.markdown("### 🔄 CUSTOMER RETENTION")
        
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
                    line=dict(color='rgba(255, 255, 255, 0.3)', width=1)
                ),
                text=order_frequency['customer_count'],
                textposition='outside',
                textfont=dict(color='#00ff87')
            )
        ])
        st.plotly_chart(style_fig(fig_freq, "📊 Order Frequency Distribution"), use_container_width=True)
    
    st.markdown("### 🎯 CUSTOMER SEGMENTATION (RFM)")
    
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
        fig_seg_count = go.Figure(data=[
            go.Bar(
                x=segment_summary['segment'],
                y=segment_summary['customer_count'],
                marker=dict(color=neon_colors[:len(segment_summary)]),
                text=segment_summary['customer_count'],
                textposition='outside',
                textfont=dict(size=14, color='#00ff87')
            )
        ])
        st.plotly_chart(style_fig(fig_seg_count, "👥 Customers by Segment"), use_container_width=True)
    
    with col2:
        fig_seg_rev = go.Figure(data=[
            go.Bar(
                x=segment_summary['segment'],
                y=segment_summary['total_revenue'],
                marker=dict(color=neon_colors[:len(segment_summary)]),
                text=[f"${val:,.0f}" for val in segment_summary['total_revenue']],
                textposition='outside',
                textfont=dict(size=14, color='#60efff')
            )
        ])
        st.plotly_chart(style_fig(fig_seg_rev, "💰 Revenue by Segment"), use_container_width=True)

# === TAB 3: Product Performance ===
with tab3:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown(f"### 🎯 TOP {top_n} PRODUCTS BY REVENUE")
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
                    line=dict(color='rgba(255, 255, 255, 0.3)', width=1)
                ),
                text=[f"${val:,.0f}" for val in top_products_rev['total_price']],
                textposition='outside',
                textfont=dict(color='#00ff87', size=11)
            )
        ])
        st.plotly_chart(style_fig(fig_prod_rev, "💰 Revenue Leaders"), use_container_width=True)
    
    with col2:
        st.markdown("### 📦 BY QUANTITY SOLD")
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
                    line=dict(color='rgba(255, 255, 255, 0.3)', width=1)
                ),
                text=top_products_qty['quantity'],
                textposition='outside',
                textfont=dict(color='#60efff', size=11)
            )
        ])
        st.plotly_chart(style_fig(fig_prod_qty, "📊 Volume Champions"), use_container_width=True)
    
    st.markdown("### 💲 PRICE DISTRIBUTION ANALYSIS")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_price = go.Figure()
        fig_price.add_trace(go.Histogram(
            x=df_filtered['unit_price'],
            nbinsx=50,
            marker=dict(
                color='#9b59b6',
                line=dict(color='rgba(255, 255, 255, 0.3)', width=1)
            ),
            opacity=0.8
        ))
        fig_price.add_trace(go.Box(
            x=df_filtered['unit_price'],
            marker=dict(color='#00ff87'),
            name='Distribution',
            yaxis='y2'
        ))
        fig_price.update_layout(yaxis2=dict(overlaying='y', side='right'))
        st.plotly_chart(style_fig(fig_price, "📊 Unit Price Distribution"), use_container_width=True)
    
    with col2:
        price_stats = df_filtered['unit_price'].describe()
        st.markdown("""
            <div class='card-container'>
                <h4 style='color: #00ff87; margin-bottom: 15px;'>📈 PRICE STATISTICS</h4>
        """, unsafe_allow_html=True)
        st.metric("Mean Price", f"${price_stats['mean']:.2f}")
        st.metric("Median Price", f"${price_stats['50%']:.2f}")
        st.metric("Std Dev", f"${price_stats['std']:.2f}")
        st.metric("Max Price", f"${price_stats['max']:.2f}")
        st.markdown("</div>", unsafe_allow_html=True)

# === TAB 4: Geographic Insights ===
with tab4:
    st.markdown("### 🌍 REVENUE BY COUNTRY")
    
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
                colorbar=dict(title="Revenue", tickprefix="$"),
                line=dict(color='rgba(255, 255, 255, 0.3)', width=2)
            ),
            text=[f"${val:,.0f}" for val in country_analysis['revenue']],
            textposition='outside',
            textfont=dict(color='#00ff87', size=13),
            hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>'
        )
    ])
    st.plotly_chart(style_fig(fig_country, "🌎 Global Revenue Distribution"), use_container_width=True)
    
    st.markdown("### 📋 COUNTRY PERFORMANCE DETAILS")
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
            "revenue": st.column_config.TextColumn("💰 Total Revenue", width="medium"),
            "orders": st.column_config.NumberColumn("🛒 Orders", format="%d"),
            "customers": st.column_config.NumberColumn("👥 Customers", format="%d"),
            "avg_order_value": st.column_config.TextColumn("💵 Avg Order Value", width="medium")
        }
    )

# === TAB 5: Advanced Analytics ===
with tab5:
    st.markdown("### 🔬 ADVANCED ANALYTICS & INSIGHTS")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💹 REVENUE GROWTH RATE")
        monthly_revenue = df_filtered.groupby(df_filtered['order_date'].dt.to_period('M'))['total_price'].sum().reset_index()
        monthly_revenue['order_date'] = monthly_revenue['order_date'].dt.to_timestamp()
        growth_data = monthly_revenue.copy()
        growth_data['growth_rate'] = growth_data['total_price'].pct_change() * 100
        
        fig_growth = go.Figure()
        
        colors = ['#00ff87' if x >= 0 else '#ff006e' for x in growth_data['growth_rate']]
        
        fig_growth.add_trace(go.Bar(
            x=growth_data['order_date'],
            y=growth_data['growth_rate'],
            marker=dict(color=colors, line=dict(color='rgba(255, 255, 255, 0.3)', width=1)),
            text=[f"{val:.1f}%" if not pd.isna(val) else "" for val in growth_data['growth_rate']],
            textposition='outside',
            textfont=dict(size=11)
        ))
        
        fig_growth.add_hline(y=0, line_dash="solid", line_color="rgba(255, 255, 255, 0.5)", line_width=2)
        st.plotly_chart(style_fig(fig_growth, "📊 Month-over-Month Growth %"), use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 REVENUE CONCENTRATION")
        
        # Pareto analysis
        product_revenue = df_filtered.groupby('product_name')['total_price'].sum().sort_values(ascending=False).reset_index()
        product_revenue['cumulative_pct'] = (product_revenue['total_price'].cumsum() / product_revenue['total_price'].sum()) * 100
        
        fig_pareto = go.Figure()
        
        fig_pareto.add_trace(go.Bar(
            x=product_revenue.index[:20],
            y=product_revenue['total_price'][:20],
            name='Revenue',
            marker=dict(color='#667eea'),
            yaxis='y'
        ))
        
        fig_pareto.add_trace(go.Scatter(
            x=product_revenue.index[:20],
            y=product_revenue['cumulative_pct'][:20],
            name='Cumulative %',
            mode='lines+markers',
            marker=dict(color='#00ff87', size=8),
            line=dict(color='#00ff87', width=3),
            yaxis='y2'
        ))
        
        fig_pareto.update_layout(
            yaxis=dict(title='Revenue'),
            yaxis2=dict(title='Cumulative %', overlaying='y', side='right', range=[0, 100]),
            showlegend=True,
            legend=dict(font=dict(color='#e0e0e0'))
        )
        
        st.plotly_chart(style_fig(fig_pareto, "📈 Pareto Analysis (80/20 Rule)"), use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔗 QUANTITY VS PRICE CORRELATION")
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
                colorbar=dict(title="Total Price"),
                line=dict(color='rgba(255, 255, 255, 0.3)', width=1),
                opacity=0.7
            ),
            text=[f"Total: ${val:,.0f}" for val in sample_df['total_price']],
            hovertemplate='<b>Qty:</b> %{x}<br><b>Price:</b> $%{y:.2f}<br>%{text}<extra></extra>'
        ))
        st.plotly_chart(style_fig(fig_scatter, "🔍 Price vs Quantity Analysis"), use_container_width=True)
    
    with col2:
        st.markdown("#### ⏰ SALES BY HOUR (if available)")
        
        # Mock hourly data for visualization
        if 'order_hour' not in df_filtered.columns:
            st.info("💡 Hourly data not available. Add 'order_hour' column for time-of-day analysis.")
        
        # Alternative: Show monthly comparison
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
                    line=dict(color='rgba(255, 255, 255, 0.3)', width=1)
                ),
                text=[f"${val:,.0f}" for val in yearly_comp['revenue']],
                textposition='outside',
                textfont=dict(color='#00ff87', size=11)
            )
        ])
        st.plotly_chart(style_fig(fig_monthly, "📅 Seasonal Revenue Patterns"), use_container_width=True)
    
    # Performance Summary Card
    st.markdown("""
        <div class='card-container' style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%); border: 2px solid rgba(0, 255, 135, 0.3);'>
            <h3 style='color: #00ff87; text-align: center; margin-bottom: 20px;'>🎯 EXECUTIVE SUMMARY</h3>
    """, unsafe_allow_html=True)
    
    sum_col1, sum_col2, sum_col3, sum_col4 = st.columns(4)
    
    with sum_col1:
        top_country = country_analysis.iloc[0]
        st.markdown(f"""
            <div style='text-align: center;'>
                <p style='color: #a8b2d1; font-size: 12px; margin: 0;'>TOP COUNTRY</p>
                <p style='color: #00ff87; font-size: 24px; font-weight: 700; margin: 5px 0;'>{top_country['country']}</p>
                <p style='color: #60efff; font-size: 14px; margin: 0;'>${top_country['revenue']:,.0f}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with sum_col2:
        best_product = top_products_rev.iloc[0]
        st.markdown(f"""
            <div style='text-align: center;'>
                <p style='color: #a8b2d1; font-size: 12px; margin: 0;'>BEST PRODUCT</p>
                <p style='color: #00ff87; font-size: 18px; font-weight: 700; margin: 5px 0;'>{best_product['product_name'][:15]}...</p>
                <p style='color: #60efff; font-size: 14px; margin: 0;'>${best_product['total_price']:,.0f}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with sum_col3:
        vip_customers = rfm[rfm['segment'] == '💎 VIP'].shape[0]
        st.markdown(f"""
            <div style='text-align: center;'>
                <p style='color: #a8b2d1; font-size: 12px; margin: 0;'>VIP CUSTOMERS</p>
                <p style='color: #00ff87; font-size: 24px; font-weight: 700; margin: 5px 0;'>{vip_customers}</p>
                <p style='color: #60efff; font-size: 14px; margin: 0;'>Top Tier</p>
            </div>
        """, unsafe_allow_html=True)
    
    with sum_col4:
        growth_avg = growth_data['growth_rate'].mean()
        st.markdown(f"""
            <div style='text-align: center;'>
                <p style='color: #a8b2d1; font-size: 12px; margin: 0;'>AVG GROWTH</p>
                <p style='color: #00ff87; font-size: 24px; font-weight: 700; margin: 5px 0;'>{growth_avg:.1f}%</p>
                <p style='color: #60efff; font-size: 14px; margin: 0;'>MoM</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------
# Premium Export Section
# -----------------------
st.markdown("<hr style='margin: 40px 0; border: 1px solid rgba(0, 255, 135, 0.3);'>", unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: center; margin-bottom: 20px;'>
        <h2 style='color: #00ff87; font-size: 32px;'>📥 EXPORT DATA CENTER</h2>
        <p style='color: #a8b2d1; font-size: 14px;'>Download filtered datasets and reports</p>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.download_button(
        "📊 FILTERED DATASET",
        df_filtered.to_csv(index=False).encode('utf-8'),
        file_name=f"filtered_data_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with col2:
    st.download_button(
        "🏆 TOP CUSTOMERS",
        top_customers.to_csv(index=False).encode('utf-8'),
        file_name=f"top_customers_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with col3:
    st.download_button(
        "📦 TOP PRODUCTS",
        top_products_rev.to_csv(index=False).encode('utf-8'),
        file_name=f"top_products_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with col4:
    st.download_button(
        "🌍 COUNTRY REPORT",
        display_df.to_csv(index=False).encode('utf-8'),
        file_name=f"country_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# -----------------------
# Premium Footer
# -----------------------
st.markdown("<hr style='margin: 40px 0; border: 1px solid rgba(0, 255, 135, 0.2);'>", unsafe_allow_html=True)

st.markdown(f"""
    <div style='text-align: center; padding: 30px; background: rgba(255, 255, 255, 0.03); border-radius: 20px; border: 1px solid rgba(0, 255, 135, 0.2);'>
        <div style='font-size: 48px; margin-bottom: 15px;'>⚡</div>
        <h3 style='color: #00ff87; margin: 10px 0;'>EXECUTIVE E-COMMERCE DASHBOARD v2.0</h3>
        <p style='color: #a8b2d1; font-size: 14px; margin: 10px 0;'>
            Built with <span style='color: #ff006e;'>❤️</span> using Streamlit & Plotly
        </p>
        <p style='color: #60efff; font-size: 12px; margin: 5px 0;'>
            📅 Last Updated: {datetime.now().strftime('%B %d, %Y at %H:%M')}
        </p>
        <div style='margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(255, 255, 255, 0.1);'>
            <p style='color: #a8b2d1; font-size: 11px; margin: 0;'>
                💼 Portfolio Project | Data Analytics & Business Intelligence
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)
