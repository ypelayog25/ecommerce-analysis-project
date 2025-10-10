"""
Professional Executive E-commerce Dashboard (Streamlit)
Enhanced version with advanced analytics, caching, and modern UX
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

# Custom CSS for modern look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 14px;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-delta {
        font-size: 14px;
        margin-top: 8px;
    }
    div[data-testid="stExpander"] {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
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
        st.error(f"Error loading data: {e}")
        return None

df = load_data()

if df is None or df.empty:
    st.error("❌ No dataset found or dataset is empty.")
    st.stop()

# -----------------------
# Header
# -----------------------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
        <h1 style='text-align:center; color:#2c3e50; font-size: 42px; margin-bottom: 5px;'>
            📊 Executive E-commerce Dashboard
        </h1>
        <p style='text-align:center; color:#7f8c8d; font-size: 16px;'>
            Real-time Business Intelligence & Analytics
        </p>
    """, unsafe_allow_html=True)

st.markdown("---")

# -----------------------
# Sidebar Filters
# -----------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/bar-chart.png", width=80)
    st.title("🎛️ Control Panel")
    
    with st.expander("📅 Date Range", expanded=True):
        date_col1, date_col2 = st.columns(2)
        
        min_date = df['order_date'].min().date()
        max_date = df['order_date'].max().date()
        
        with date_col1:
            start_date = st.date_input("From", min_date, min_value=min_date, max_value=max_date)
        with date_col2:
            end_date = st.date_input("To", max_date, min_value=min_date, max_value=max_date)
        
        # Quick date filters
        st.markdown("**Quick Filters:**")
        col_q1, col_q2 = st.columns(2)
        with col_q1:
            if st.button("Last 30 Days", use_container_width=True):
                start_date = max_date - timedelta(days=30)
            if st.button("Last Quarter", use_container_width=True):
                start_date = max_date - timedelta(days=90)
        with col_q2:
            if st.button("Last 7 Days", use_container_width=True):
                start_date = max_date - timedelta(days=7)
            if st.button("Year to Date", use_container_width=True):
                start_date = datetime(max_date.year, 1, 1).date()
    
    with st.expander("🌍 Geography", expanded=True):
        countries = sorted(df['country'].dropna().unique())
        select_all = st.checkbox("Select All Countries", value=True)
        
        if select_all:
            selected_countries = countries
        else:
            selected_countries = st.multiselect("Select Countries", countries, default=countries[:3])
    
    with st.expander("⚙️ Display Options", expanded=False):
        top_n = st.slider("Top N Items", 5, 50, 10, 5)
        show_annotations = st.checkbox("Show Chart Annotations", value=True)
        chart_theme = st.selectbox("Chart Theme", ["plotly_white", "plotly_dark", "seaborn", "ggplot2"])

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
    # Current period metrics
    total_revenue = df_current['total_price'].sum()
    total_orders = df_current['order_id'].nunique()
    unique_customers = df_current['customer_id'].nunique()
    total_quantity = df_current['quantity'].sum()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    
    # Calculate previous period for comparison
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
    
    # Calculate deltas
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
# KPI Cards (Modern Design)
# -----------------------
st.markdown("### 📈 Key Performance Indicators")
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.metric(
        label="💰 Total Revenue",
        value=f"${metrics['total_revenue']:,.0f}",
        delta=f"{metrics['revenue_delta']:.1f}% vs prev period"
    )

with kpi2:
    st.metric(
        label="🛒 Total Orders",
        value=f"{metrics['total_orders']:,}",
        delta=f"{metrics['orders_delta']:.1f}%"
    )

with kpi3:
    st.metric(
        label="👥 Unique Customers",
        value=f"{metrics['unique_customers']:,}",
        delta=f"{metrics['customers_delta']:.1f}%"
    )

with kpi4:
    st.metric(
        label="📦 Products Sold",
        value=f"{metrics['total_quantity']:,}"
    )

with kpi5:
    st.metric(
        label="💵 Avg Order Value",
        value=f"${metrics['avg_order_value']:.2f}"
    )

st.markdown("---")

# -----------------------
# Helper for Plotly Styling
# -----------------------
def style_fig(fig, title="", title_font=20, axis_font=12):
    """Apply consistent styling to Plotly figures"""
    fig.update_layout(
        title=dict(text=title, font=dict(size=title_font, color="#2c3e50")),
        font=dict(size=axis_font, color="#34495e"),
        margin=dict(l=60, r=60, t=80, b=60),
        template=chart_theme,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    fig.update_xaxes(showgrid=False, showline=True, linewidth=1, linecolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='#ecf0f1')
    return fig

# -----------------------
# Main Dashboard Tabs
# -----------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Revenue Analysis", 
    "👥 Customer Intelligence", 
    "📦 Product Performance", 
    "🌍 Geographic Insights",
    "📉 Advanced Analytics"
])

# === TAB 1: Revenue Analysis ===
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Revenue Trend Over Time")
        
        # Monthly revenue with trend line
        monthly_revenue = df_filtered.groupby(df_filtered['order_date'].dt.to_period('M'))['total_price'].sum().reset_index()
        monthly_revenue['order_date'] = monthly_revenue['order_date'].dt.to_timestamp()
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=monthly_revenue['order_date'],
            y=monthly_revenue['total_price'],
            mode='lines+markers',
            name='Revenue',
            line=dict(color='#3498db', width=3),
            marker=dict(size=8),
            fill='tozeroy',
            fillcolor='rgba(52, 152, 219, 0.1)'
        ))
        
        # Add trend line
        z = np.polyfit(range(len(monthly_revenue)), monthly_revenue['total_price'], 1)
        p = np.poly1d(z)
        fig_trend.add_trace(go.Scatter(
            x=monthly_revenue['order_date'],
            y=p(range(len(monthly_revenue))),
            mode='lines',
            name='Trend',
            line=dict(color='#e74c3c', width=2, dash='dash')
        ))
        
        st.plotly_chart(style_fig(fig_trend), use_container_width=True)
    
    with col2:
        st.subheader("🏆 Top Countries")
        country_revenue = df_filtered.groupby('country')['total_price'].sum().nlargest(5).reset_index()
        
        fig_pie = px.pie(
            country_revenue,
            values='total_price',
            names='country',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(style_fig(fig_pie), use_container_width=True)
    
    # Revenue by day of week
    st.subheader("📅 Revenue by Day of Week")
    dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_revenue = df_filtered.groupby('day_of_week')['total_price'].sum().reindex(dow_order).reset_index()
    
    fig_dow = px.bar(
        dow_revenue,
        x='day_of_week',
        y='total_price',
        color='total_price',
        color_continuous_scale='Teal',
        text_auto='.2s'
    )
    st.plotly_chart(style_fig(fig_dow, "Weekly Revenue Pattern"), use_container_width=True)

# === TAB 2: Customer Intelligence ===
with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"🌟 Top {top_n} Customers by Revenue")
        top_customers = df_filtered.groupby('customer_id').agg({
            'total_price': 'sum',
            'order_id': 'nunique'
        }).nlargest(top_n, 'total_price').reset_index()
        top_customers.columns = ['customer_id', 'total_revenue', 'order_count']
        
        fig_customers = px.bar(
            top_customers,
            x='total_revenue',
            y='customer_id',
            orientation='h',
            text_auto='.2s',
            color='total_revenue',
            color_continuous_scale='Viridis',
            hover_data=['order_count']
        )
        st.plotly_chart(style_fig(fig_customers), use_container_width=True)
    
    with col2:
        st.subheader("🔄 Customer Retention")
        
        # Customer order frequency
        order_frequency = df_filtered.groupby('customer_id')['order_id'].nunique().value_counts().sort_index().reset_index()
        order_frequency.columns = ['orders', 'customer_count']
        
        fig_freq = px.bar(
            order_frequency,
            x='orders',
            y='customer_count',
            text_auto=True,
            color='customer_count',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(style_fig(fig_freq, "Order Frequency Distribution"), use_container_width=True)
    
    # Customer segmentation
    st.subheader("📊 Customer Segmentation (RFM Analysis)")
    
    # Calculate RFM metrics
    snapshot_date = df_filtered['order_date'].max() + timedelta(days=1)
    rfm = df_filtered.groupby('customer_id').agg({
        'order_date': lambda x: (snapshot_date - x.max()).days,
        'order_id': 'nunique',
        'total_price': 'sum'
    }).reset_index()
    rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']
    
    # Simple segmentation
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
    segment_summary.columns = ['segment', 'customer_count', 'total_revenue']
    
    col1, col2 = st.columns(2)
    with col1:
        fig_seg_count = px.bar(segment_summary, x='segment', y='customer_count', 
                               color='segment', text_auto=True)
        st.plotly_chart(style_fig(fig_seg_count, "Customers by Segment"), use_container_width=True)
    
    with col2:
        fig_seg_rev = px.bar(segment_summary, x='segment', y='total_revenue',
                            color='segment', text_auto='.2s')
        st.plotly_chart(style_fig(fig_seg_rev, "Revenue by Segment"), use_container_width=True)

# === TAB 3: Product Performance ===
with tab3:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader(f"🎯 Top {top_n} Products by Revenue")
        top_products_rev = df_filtered.groupby('product_name').agg({
            'total_price': 'sum',
            'quantity': 'sum'
        }).nlargest(top_n, 'total_price').reset_index()
        
        fig_prod_rev = px.bar(
            top_products_rev,
            x='total_price',
            y='product_name',
            orientation='h',
            text_auto='.2s',
            color='total_price',
            color_continuous_scale='Sunset',
            hover_data=['quantity']
        )
        st.plotly_chart(style_fig(fig_prod_rev), use_container_width=True)
    
    with col2:
        st.subheader("📦 Quantity vs Revenue")
        top_products_qty = df_filtered.groupby('product_name')['quantity'].sum().nlargest(top_n).reset_index()
        
        fig_prod_qty = px.bar(
            top_products_qty,
            x='quantity',
            y='product_name',
            orientation='h',
            text_auto=True,
            color='quantity',
            color_continuous_scale='Teal'
        )
        st.plotly_chart(style_fig(fig_prod_qty), use_container_width=True)
    
    # Price distribution
    st.subheader("💲 Price Distribution Analysis")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_price = px.histogram(
            df_filtered,
            x='unit_price',
            nbins=50,
            marginal="box",
            color_discrete_sequence=['#9b59b6']
        )
        st.plotly_chart(style_fig(fig_price, "Unit Price Distribution"), use_container_width=True)
    
    with col2:
        price_stats = df_filtered['unit_price'].describe()
        st.markdown("**Price Statistics:**")
        st.metric("Mean Price", f"${price_stats['mean']:.2f}")
        st.metric("Median Price", f"${price_stats['50%']:.2f}")
        st.metric("Std Dev", f"${price_stats['std']:.2f}")
        st.metric("Max Price", f"${price_stats['max']:.2f}")

# === TAB 4: Geographic Insights ===
with tab4:
    st.subheader("🌍 Revenue by Country")
    
    country_analysis = df_filtered.groupby('country').agg({
        'total_price': 'sum',
        'order_id': 'nunique',
        'customer_id': 'nunique'
    }).reset_index()
    country_analysis.columns = ['country', 'revenue', 'orders', 'customers']
    country_analysis = country_analysis.sort_values('revenue', ascending=False)
    
    # Bar chart
    fig_country = px.bar(
        country_analysis,
        x='country',
        y='revenue',
        text_auto='.2s',
        color='revenue',
        color_continuous_scale='Viridis',
        hover_data=['orders', 'customers']
    )
    st.plotly_chart(style_fig(fig_country, "Revenue by Country"), use_container_width=True)
    
    # Detailed table
    st.subheader("📋 Country Performance Details")
    country_analysis['avg_order_value'] = country_analysis['revenue'] / country_analysis['orders']
    country_analysis['revenue'] = country_analysis['revenue'].apply(lambda x: f"${x:,.0f}")
    country_analysis['avg_order_value'] = country_analysis['avg_order_value'].apply(lambda x: f"${x:.2f}")
    
    st.dataframe(
        country_analysis,
        use_container_width=True,
        hide_index=True,
        column_config={
            "country": "Country",
            "revenue": "Total Revenue",
            "orders": st.column_config.NumberColumn("Orders", format="%d"),
            "customers": st.column_config.NumberColumn("Customers", format="%d"),
            "avg_order_value": "Avg Order Value"
        }
    )

# === TAB 5: Advanced Analytics ===
with tab5:
    st.subheader("🔬 Advanced Analytics & Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📊 Cohort Analysis**")
        # Simplified cohort
        df_filtered['cohort_month'] = df_filtered.groupby('customer_id')['order_date'].transform('min').dt.to_period('M')
        cohort_data = df_filtered.groupby(['cohort_month', df_filtered['order_date'].dt.to_period('M')]).agg({
            'customer_id': 'nunique',
            'total_price': 'sum'
        }).reset_index()
        
        st.info("Cohort analysis shows customer behavior over time. First-time customers are grouped by their first purchase month.")
        st.dataframe(cohort_data.head(10), use_container_width=True)
    
    with col2:
        st.markdown("**💹 Revenue Growth Rate**")
        growth_data = monthly_revenue.copy()
        growth_data['growth_rate'] = growth_data['total_price'].pct_change() * 100
        
        fig_growth = px.line(
            growth_data,
            x='order_date',
            y='growth_rate',
            markers=True,
            line_shape='spline'
        )
        fig_growth.add_hline(y=0, line_dash="dash", line_color="gray")
        st.plotly_chart(style_fig(fig_growth, "Month-over-Month Growth %"), use_container_width=True)
    
    # Correlation analysis
    st.markdown("**🔗 Correlation: Quantity vs Price**")
    fig_scatter = px.scatter(
        df_filtered.sample(min(1000, len(df_filtered))),
        x='quantity',
        y='unit_price',
        color='total_price',
        size='total_price',
        color_continuous_scale='Plasma',
        opacity=0.6
    )
    st.plotly_chart(style_fig(fig_scatter), use_container_width=True)

# -----------------------
# Footer with Export Options
# -----------------------
st.markdown("---")
st.markdown("### 📥 Export Data")

col1, col2, col3 = st.columns(3)

with col1:
    st.download_button(
        "📊 Download Filtered Dataset (CSV)",
        df_filtered.to_csv(index=False).encode('utf-8'),
        file_name=f"ecommerce_filtered_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with col2:
    st.download_button(
        "🏆 Download Top Customers (CSV)",
        top_customers.to_csv(index=False).encode('utf-8'),
        file_name=f"top_customers_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with col3:
    st.download_button(
        "📦 Download Top Products (CSV)",
        top_products_rev.to_csv(index=False).encode('utf-8'),
        file_name=f"top_products_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #7f8c8d; padding: 20px;'>
        <p>📊 Executive E-commerce Dashboard v2.0 | Built with Streamlit & Plotly</p>
        <p>Data refreshed: {}</p>
    </div>
""".format(datetime.now().strftime('%Y-%m-%d %H:%M')), unsafe_allow_html=True)
