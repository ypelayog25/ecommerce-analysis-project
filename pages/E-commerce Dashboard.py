import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(page_title="E-commerce Dashboard", page_icon="🛒", layout="wide")

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp { background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); }
    
    .dashboard-header {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        border: 1px solid rgba(59, 130, 246, 0.1);
    }
    .breadcrumb { color: #94A3B8; font-size: 0.9rem; margin-bottom: 0.5rem; }
    .breadcrumb a { color: #60A5FA; text-decoration: none; }
    .dashboard-title { color: #F8FAFC; font-size: 2rem; font-weight: 700; margin: 0; letter-spacing: -0.02em; }
    
    .kpi-card {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid rgba(59, 130, 246, 0.15);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        height: 100%;
    }
    .kpi-label { color: #94A3B8; font-size: 0.85rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; }
    .kpi-value { color: #F8FAFC; font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem; letter-spacing: -0.02em; }
    .kpi-change { font-size: 0.9rem; font-weight: 600; display: flex; align-items: center; gap: 0.25rem; }
    .kpi-change.positive { color: #10B981; }
    .kpi-change.negative { color: #EF4444; }
    .kpi-subtitle { color: #64748B; font-size: 0.75rem; margin-top: 0.25rem; }
    
    .chart-container {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid rgba(59, 130, 246, 0.15);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        margin-bottom: 1.5rem;
    }
    .chart-title { color: #2986cc; font-size: 1.2rem; font-weight: 600; margin-bottom: 1rem; letter-spacing: -0.01em; }
    
    .insight-box {
        background: linear-gradient(135deg, #0F1E4A 0%, #162C7A 100%);
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        border-left: 4px solid #3B82F6;
    }
    .insight-title { color: #93C5FD; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.5rem; text-transform: uppercase; }
    .insight-text { color: #F8FAFC; font-size: 0.95rem; line-height: 1.5; }
    
    .filter-chip {
        display: inline-block;
        background: rgba(59, 130, 246, 0.2);
        color: #93C5FD;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Generate sample data
@st.cache_data
def generate_sample_data():
    np.random.seed(42)
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    
    daily_sales = pd.DataFrame({
        'date': dates,
        'revenue': np.random.randint(15000, 45000, 30),
        'orders': np.random.randint(80, 250, 30),
        'visitors': np.random.randint(1500, 4500, 30)
    })
    daily_sales['conversion_rate'] = (daily_sales['orders'] / daily_sales['visitors'] * 100).round(2)
    
    products = pd.DataFrame({
        'product': ['Laptop Pro 15"', 'Wireless Mouse', 'USB-C Hub', 'Mechanical Keyboard', 
                    'Monitor 27"', 'Webcam HD', 'Headphones', 'Desk Mat', 'Phone Stand', 'Cable Pack'],
        'category': ['Electronics', 'Accessories', 'Accessories', 'Peripherals',
                     'Electronics', 'Accessories', 'Audio', 'Accessories', 'Accessories', 'Accessories'],
        'units_sold': [245, 890, 567, 423, 189, 334, 678, 445, 556, 789],
        'revenue': [294000, 26700, 28350, 42300, 94500, 23370, 67800, 13350, 16680, 15780]
    })
    products['avg_price'] = (products['revenue'] / products['units_sold']).round(2)
    
    category_sales = products.groupby('category').agg({
        'revenue': 'sum',
        'units_sold': 'sum'
    }).reset_index().sort_values('revenue', ascending=False)
    
    return daily_sales, products, category_sales

daily_sales, products, category_sales = generate_sample_data()

# Header
st.markdown("""
<div class="dashboard-header">
    <div class="breadcrumb">🏠 Home / E-commerce Dashboard</div>
    <h1 class="dashboard-title">🛒 E-commerce Dashboard</h1>
    <div style="color: #64748B; font-size: 0.9rem; margin-top: 0.5rem;">
        📅 Actualizado: {datetime.now().strftime('%d %b %Y, %H:%M')} | Período: Últimos 30 días
    </div>
</div>
""".format(datetime=datetime), unsafe_allow_html=True)

# Filters
col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns([2, 2, 2, 1, 1])
with col_f1:
    date_range = st.selectbox("📆 Período", ["Últimos 7 días", "Últimos 30 días", "Últimos 90 días", "Este año"], index=1)
with col_f2:
    category_filter = st.multiselect("🏷️ Categorías", options=products['category'].unique(), default=products['category'].unique())
with col_f3:
    comparison = st.selectbox("📊 Comparar con", ["Período anterior", "Mismo período año pasado", "Sin comparación"], index=0)
with col_f4:
    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
    if st.button("🔄", use_container_width=True):
        st.rerun()
with col_f5:
    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
    if st.button("↺ Reset", use_container_width=True):
        st.rerun()

# Show active filters
if category_filter != list(products['category'].unique()):
    st.markdown(f"<div style='margin: 1rem 0;'>{''.join([f'<span class=\"filter-chip\">{cat} ×</span>' for cat in category_filter])}</div>", unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

# Calculate KPIs with better context
total_revenue = daily_sales['revenue'].sum()
total_orders = daily_sales['orders'].sum()
avg_order_value = total_revenue / total_orders
avg_conversion = daily_sales['conversion_rate'].mean()

prev_revenue = total_revenue * np.random.uniform(0.85, 0.95)
prev_orders = total_orders * np.random.uniform(0.88, 0.98)
prev_aov = avg_order_value * np.random.uniform(0.92, 1.02)
prev_conversion = avg_conversion * np.random.uniform(0.9, 1.0)

revenue_change = ((total_revenue - prev_revenue) / prev_revenue * 100)
orders_change = ((total_orders - prev_orders) / prev_orders * 100)
aov_change = ((avg_order_value - prev_aov) / prev_aov * 100)
conversion_change = ((avg_conversion - prev_conversion) / prev_conversion * 100)

# KPI Cards mejoradas
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpis_data = [
    (kpi1, "💰", "Ingresos Totales", total_revenue, revenue_change, f"${prev_revenue:,.0f} período anterior"),
    (kpi2, "📦", "Total Pedidos", total_orders, orders_change, f"{prev_orders:,.0f} período anterior"),
    (kpi3, "🛍️", "Valor Promedio Pedido", avg_order_value, aov_change, f"${prev_aov:,.0f} período anterior"),
    (kpi4, "📊", "Tasa Conversión", avg_conversion, conversion_change, f"{prev_conversion:.2f}% período anterior")
]

for col, icon, label, value, change, subtitle in kpis_data:
    with col:
        change_class = "positive" if change > 0 else "negative"
        arrow = "▲" if change > 0 else "▼"
        formatted_value = f"${value:,.0f}" if "$" not in label else f"{value:,.2f}%" if "Conversión" in label else f"{int(value):,}"
        
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{icon} {label}</div>
            <div class="kpi-value">{formatted_value}</div>
            <div class="kpi-change {change_class}">{arrow} {abs(change):.1f}% vs período anterior</div>
            <div class="kpi-subtitle">{subtitle}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

# Auto-insights
top_product = products.nlargest(1, 'revenue').iloc[0]
top_category = category_sales.iloc[0]
best_day = daily_sales.nlargest(1, 'revenue').iloc[0]
category_concentration = (top_category['revenue'] / category_sales['revenue'].sum() * 100)

st.markdown(f"""
<div class="insight-box">
    <div class="insight-title">🔍 Insights Principales</div>
    <div class="insight-text">
        • <strong>{top_product['product']}</strong> genera ${top_product['revenue']:,.0f} ({top_product['revenue']/total_revenue*100:.1f}% del revenue total)<br>
        • Categoría <strong>{top_category['category']}</strong> domina con {category_concentration:.1f}% de ingresos<br>
        • Mejor día: <strong>{best_day['date'].strftime('%d/%m')}</strong> con ${best_day['revenue']:,.0f} (+{(best_day['revenue']/daily_sales['revenue'].mean()-1)*100:.0f}% vs promedio)
    </div>
</div>
""", unsafe_allow_html=True)

# Charts row 1: Revenue trend + Orders trend
chart1, chart2 = st.columns(2)

with chart1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📈 Tendencia de Ingresos (30 días)</div>', unsafe_allow_html=True)
    
    # Add trend line
    z = np.polyfit(range(len(daily_sales)), daily_sales['revenue'], 1)
    p = np.poly1d(z)
    trend_line = p(range(len(daily_sales)))
    
    fig_revenue = go.Figure()
    fig_revenue.add_trace(go.Scatter(
        x=daily_sales['date'], y=daily_sales['revenue'],
        mode='lines+markers', name='Ingresos',
        line=dict(color='#3B82F6', width=3),
        marker=dict(size=6, color='#60A5FA'),
        fill='tozeroy', fillcolor='rgba(59, 130, 246, 0.1)',
        hovertemplate='%{x|%d %b}<br>$%{y:,.0f}<extra></extra>'
    ))
    fig_revenue.add_trace(go.Scatter(
        x=daily_sales['date'], y=trend_line,
        mode='lines', name='Tendencia',
        line=dict(color='#F59E0B', width=2, dash='dash'),
        hovertemplate='Tendencia: $%{y:,.0f}<extra></extra>'
    ))
    
    # Mark peak
    peak_idx = daily_sales['revenue'].idxmax()
    fig_revenue.add_annotation(
        x=daily_sales.loc[peak_idx, 'date'],
        y=daily_sales.loc[peak_idx, 'revenue'],
        text=f"Pico: ${daily_sales.loc[peak_idx, 'revenue']:,.0f}",
        showarrow=True, arrowhead=2,
        bgcolor='#1E293B', bordercolor='#3B82F6',
        font=dict(color='#F8FAFC', size=10)
    )
    
    fig_revenue.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC', family='Inter'),
        xaxis=dict(showgrid=True, gridcolor='rgba(148, 163, 184, 0.1)', title=None),
        yaxis=dict(showgrid=True, gridcolor='rgba(148, 163, 184, 0.1)', title='Ingresos ($)'),
        hovermode='x unified', margin=dict(l=20, r=20, t=40, b=20), height=300,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    
    st.plotly_chart(fig_revenue, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with chart2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📦 Pedidos y Conversión</div>', unsafe_allow_html=True)
    
    fig_orders = go.Figure()
    fig_orders.add_trace(go.Bar(
        x=daily_sales['date'], y=daily_sales['orders'],
        name='Pedidos', marker_color='#10B981', yaxis='y',
        hovertemplate='%{x|%d %b}<br>Pedidos: %{y}<extra></extra>'
    ))
    fig_orders.add_trace(go.Scatter(
        x=daily_sales['date'], y=daily_sales['conversion_rate'],
        name='Conversión %', line=dict(color='#F59E0B', width=2),
        marker=dict(size=5), yaxis='y2',
        hovertemplate='Conversión: %{y:.2f}%<extra></extra>'
    ))
    
    fig_orders.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC', family='Inter'),
        xaxis=dict(showgrid=True, gridcolor='rgba(148, 163, 184, 0.1)', title=None),
        yaxis=dict(showgrid=True, gridcolor='rgba(148, 163, 184, 0.1)', title='Pedidos', side='left'),
        yaxis2=dict(title='Conversión (%)', overlaying='y', side='right', showgrid=False),
        hovermode='x unified', margin=dict(l=20, r=20, t=20, b=20), height=300,
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
    top_products['revenue_pct'] = (top_products['revenue'] / top_products['revenue'].sum() * 100)
    
    fig_products = go.Figure()
    fig_products.add_trace(go.Bar(
        y=top_products['product'], x=top_products['revenue'],
        orientation='h',
        marker=dict(color=top_products['revenue'], colorscale='Blues', showscale=False),
        text=top_products.apply(lambda x: f"${x['revenue']:,.0f} ({x['revenue_pct']:.1f}%)", axis=1),
        textposition='outside',
        hovertemplate='%{y}<br>Ingresos: $%{x:,.0f}<extra></extra>'
    ))
    
    fig_products.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC', family='Inter'),
        xaxis=dict(showgrid=True, gridcolor='rgba(148, 163, 184, 0.1)', title='Ingresos ($)'),
        yaxis=dict(showgrid=False, title=None, autorange='reversed'),
        margin=dict(l=20, r=100, t=20, b=20), height=400
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
        textfont=dict(size=12, color='#F8FAFC'),
        hovertemplate='%{label}<br>$%{value:,.0f}<br>%{percent}<extra></extra>'
    ))
    
    fig_category.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC', family='Inter'),
        margin=dict(l=20, r=20, t=20, b=20), height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_category, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

# Product table con estilo mejorado
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="chart-title">📋 Detalle de Productos</div>', unsafe_allow_html=True)

products_display = products.copy()
products_display['revenue_formatted'] = products_display['revenue'].apply(lambda x: f'${x:,.0f}')
products_display['avg_price_formatted'] = products_display['avg_price'].apply(lambda x: f'${x:,.2f}')
products_display['contribution'] = (products_display['revenue'] / products_display['revenue'].sum() * 100).round(1)

display_df = products_display[['product', 'category', 'units_sold', 'revenue_formatted', 'avg_price_formatted', 'contribution']]
display_df.columns = ['Producto', 'Categoría', 'Unidades', 'Ingresos', 'Precio Prom.', '% Total']

st.dataframe(display_df, use_container_width=True, hide_index=True, height=350)

st.markdown('</div>', unsafe_allow_html=True)
