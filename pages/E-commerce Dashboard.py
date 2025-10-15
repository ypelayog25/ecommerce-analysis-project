import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="E-commerce Dashboard",
    page_icon="🛒",
    layout="wide"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    }
    
    /* Header */
    .dashboard-header {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        border: 1px solid rgba(59, 130, 246, 0.1);
    }
    
    .breadcrumb {
        color: #94A3B8;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    .breadcrumb a {
        color: #60A5FA;
        text-decoration: none;
    }
    
    .dashboard-title {
        color: #F8FAFC;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    /* KPI Card */
    .kpi-card {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid rgba(59, 130, 246, 0.15);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        height: 100%;
    }
    
    .kpi-label {
        color: #94A3B8;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    .kpi-value {
        color: #F8FAFC;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .kpi-change {
        font-size: 0.9rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    .kpi-change.positive {
        color: #10B981;
    }
    
    .kpi-change.negative {
        color: #EF4444;
    }
    
    /* Chart container */
    .chart-container {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid rgba(59, 130, 246, 0.15);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        margin-bottom: 1.5rem;
    }
    
    .chart-title {
        color: #F8FAFC;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        letter-spacing: -0.01em;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Plotly chart styling */
    .js-plotly-plot {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Generate sample data
@st.cache_data
def generate_sample_data():
    np.random.seed(42)
    
    # Date range (last 30 days)
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    
    # Daily sales data
    daily_sales = pd.DataFrame({
        'date': dates,
        'revenue': np.random.randint(15000, 45000, 30),
        'orders': np.random.randint(80, 250, 30),
        'visitors': np.random.randint(1500, 4500, 30)
    })
    daily_sales['conversion_rate'] = (daily_sales['orders'] / daily_sales['visitors'] * 100).round(2)
    
    # Product data
    products = pd.DataFrame({
        'product': ['Laptop Pro 15"', 'Wireless Mouse', 'USB-C Hub', 'Mechanical Keyboard', 
                    'Monitor 27"', 'Webcam HD', 'Headphones', 'Desk Mat', 'Phone Stand', 'Cable Pack'],
        'category': ['Electronics', 'Accessories', 'Accessories', 'Peripherals',
                     'Electronics', 'Accessories', 'Audio', 'Accessories', 'Accessories', 'Accessories'],
        'units_sold': [245, 890, 567, 423, 189, 334, 678, 445, 556, 789],
        'revenue': [294000, 26700, 28350, 42300, 94500, 23370, 67800, 13350, 16680, 15780]
    })
    products['avg_price'] = (products['revenue'] / products['units_sold']).round(2)
    
    # Category summary
    category_sales = products.groupby('category').agg({
        'revenue': 'sum',
        'units_sold': 'sum'
    }).reset_index().sort_values('revenue', ascending=False)
    
    return daily_sales, products, category_sales

daily_sales, products, category_sales = generate_sample_data()

# Header
st.markdown("""
<div class="dashboard-header">
    <div class="breadcrumb">
        <a href="/">🏠 Home</a> / E-commerce Dashboard
    </div>
    <h1 class="dashboard-title">🛒 E-commerce Dashboard</h1>
</div>
""", unsafe_allow_html=True)

# Filters row
col_filter1, col_filter2, col_filter3, col_filter4 = st.columns([2, 2, 2, 1])

with col_filter1:
    date_range = st.selectbox(
        "Período",
        ["Últimos 7 días", "Últimos 30 días", "Últimos 90 días", "Este año"],
        index=1
    )

with col_filter2:
    category_filter = st.multiselect(
        "Categorías",
        options=products['category'].unique(),
        default=products['category'].unique()
    )

with col_filter3:
    comparison = st.selectbox(
        "Comparar con",
        ["Período anterior", "Mismo período año pasado", "Sin comparación"],
        index=0
    )

with col_filter4:
    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
    if st.button("🔄 Actualizar", use_container_width=True):
        st.rerun()

st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

# Calculate KPIs
total_revenue = daily_sales['revenue'].sum()
total_orders = daily_sales['orders'].sum()
avg_order_value = total_revenue / total_orders
avg_conversion = daily_sales['conversion_rate'].mean()

# Previous period (for comparison)
prev_revenue = total_revenue * np.random.uniform(0.85, 0.95)
prev_orders = total_orders * np.random.uniform(0.88, 0.98)
prev_aov = avg_order_value * np.random.uniform(0.92, 1.02)
prev_conversion = avg_conversion * np.random.uniform(0.9, 1.0)

revenue_change = ((total_revenue - prev_revenue) / prev_revenue * 100)
orders_change = ((total_orders - prev_orders) / prev_orders * 100)
aov_change = ((avg_order_value - prev_aov) / prev_aov * 100)
conversion_change = ((avg_conversion - prev_conversion) / prev_conversion * 100)

# KPI Cards
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    change_class = "positive" if revenue_change > 0 else "negative"
    arrow = "▲" if revenue_change > 0 else "▼"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">💰 Ingresos Totales</div>
        <div class="kpi-value">${total_revenue:,.0f}</div>
        <div class="kpi-change {change_class}">{arrow} {abs(revenue_change):.1f}% vs período anterior</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    change_class = "positive" if orders_change > 0 else "negative"
    arrow = "▲" if orders_change > 0 else "▼"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">📦 Total Pedidos</div>
        <div class="kpi-value">{total_orders:,}</div>
        <div class="kpi-change {change_class}">{arrow} {abs(orders_change):.1f}% vs período anterior</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    change_class = "positive" if aov_change > 0 else "negative"
    arrow = "▲" if aov_change > 0 else "▼"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">🛍️ Valor Promedio Pedido</div>
        <div class="kpi-value">${avg_order_value:,.0f}</div>
        <div class="kpi-change {change_class}">{arrow} {abs(aov_change):.1f}% vs período anterior</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    change_class = "positive" if conversion_change > 0 else "negative"
    arrow = "▲" if conversion_change > 0 else "▼"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">📊 Tasa Conversión</div>
        <div class="kpi-value">{avg_conversion:.2f}%</div>
        <div class="kpi-change {change_class}">{arrow} {abs(conversion_change):.1f}% vs período anterior</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

# Charts row 1: Revenue trend + Orders trend
chart1, chart2 = st.columns(2)

with chart1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📈 Tendencia de Ingresos (30 días)</div>', unsafe_allow_html=True)
    
    fig_revenue = go.Figure()
    fig_revenue.add_trace(go.Scatter(
        x=daily_sales['date'],
        y=daily_sales['revenue'],
        mode='lines+markers',
        name='Ingresos',
        line=dict(color='#3B82F6', width=3),
        marker=dict(size=6, color='#60A5FA'),
        fill='tozeroy',
        fillcolor='rgba(59, 130, 246, 0.1)'
    ))
    
    fig_revenue.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC', family='Inter'),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(148, 163, 184, 0.1)',
            title=None
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(148, 163, 184, 0.1)',
            title='Ingresos ($)'
        ),
        hovermode='x unified',
        margin=dict(l=20, r=20, t=20, b=20),
        height=300
    )
    
    st.plotly_chart(fig_revenue, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with chart2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📦 Pedidos y Conversión</div>', unsafe_allow_html=True)
    
    fig_orders = go.Figure()
    fig_orders.add_trace(go.Bar(
        x=daily_sales['date'],
        y=daily_sales['orders'],
        name='Pedidos',
        marker_color='#10B981',
        yaxis='y'
    ))
    
    fig_orders.add_trace(go.Scatter(
        x=daily_sales['date'],
        y=daily_sales['conversion_rate'],
        name='Conversión %',
        line=dict(color='#F59E0B', width=2),
        marker=dict(size=5),
        yaxis='y2'
    ))
    
    fig_orders.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC', family='Inter'),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(148, 163, 184, 0.1)',
            title=None
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(148, 163, 184, 0.1)',
            title='Pedidos',
            side='left'
        ),
        yaxis2=dict(
            title='Conversión (%)',
            overlaying='y',
            side='right',
            showgrid=False
        ),
        hovermode='x unified',
        margin=dict(l=20, r=20, t=20, b=20),
        height=300,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    
    st.plotly_chart(fig_orders, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

# Charts row 2: Top products + Category distribution
chart3, chart4 = st.columns([1.2, 1])

with chart3:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">🏆 Top 10 Productos por Ingresos</div>', unsafe_allow_html=True)
    
    top_products = products.nlargest(10, 'revenue')
    
    fig_products = go.Figure()
    fig_products.add_trace(go.Bar(
        y=top_products['product'],
        x=top_products['revenue'],
        orientation='h',
        marker=dict(
            color=top_products['revenue'],
            colorscale='Blues',
            showscale=False
        ),
        text=top_products['revenue'].apply(lambda x: f'${x:,.0f}'),
        textposition='outside'
    ))
    
    fig_products.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC', family='Inter'),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(148, 163, 184, 0.1)',
            title='Ingresos ($)'
        ),
        yaxis=dict(
            showgrid=False,
            title=None,
            autorange='reversed'
        ),
        margin=dict(l=20, r=20, t=20, b=20),
        height=400
    )
    
    st.plotly_chart(fig_products, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with chart4:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📊 Distribución por Categoría</div>', unsafe_allow_html=True)
    
    fig_category = go.Figure()
    fig_category.add_trace(go.Pie(
        labels=category_sales['category'],
        values=category_sales['revenue'],
        hole=0.4,
        marker=dict(colors=['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']),
        textinfo='label+percent',
        textfont=dict(size=12, color='#F8FAFC')
    ))
    
    fig_category.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC', family='Inter'),
        margin=dict(l=20, r=20, t=20, b=20),
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_category, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

# Product table
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="chart-title">📋 Detalle de Productos</div>', unsafe_allow_html=True)

# Format dataframe
products_display = products.copy()
products_display['revenue'] = products_display['revenue'].apply(lambda x: f'${x:,.0f}')
products_display['avg_price'] = products_display['avg_price'].apply(lambda x: f'${x:,.2f}')
products_display.columns = ['Producto', 'Categoría', 'Unidades Vendidas', 'Ingresos', 'Precio Promedio']

st.dataframe(
    products_display,
    use_container_width=True,
    hide_index=True,
    height=350
)

st.markdown('</div>', unsafe_allow_html=True)
