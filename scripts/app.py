# app.py
# Corregido y simplificado para evitar SyntaxError por CSS/HTML suelto
# Conserva las funcionalidades principales del dashboard Executive E-commerce

import os
import io
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# -----------------------
# Page config
# -----------------------
st.set_page_config(
    page_title="Executive E-commerce Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊"
)

# -----------------------
# Consolidated CSS (inside triple quotes) — evita cualquier CSS fuera de strings
# -----------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    body { background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%); color: #e8eaf6; }
    h1 { color: #ffffff !important; font-weight: 800 !important; }
    .card-container { background: rgba(255,255,255,0.04); padding: 16px; border-radius: 12px; }
    .glowing-title { animation: glow 2s ease-in-out infinite; }
    @keyframes glow { 0%,100%{text-shadow:0 0 15px rgba(79,195,247,0.4);} 50%{text-shadow:0 0 25px rgba(79,195,247,0.6);} }
    /* Responsive tweaks */
    @media (max-width: 768px) {
        h1 { font-size: 28px !important; }
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------
# Helpers and styling for Plotly
# -----------------------
def style_fig(fig, title="", title_font=18, axis_font=12):
    theme_to_use = st.session_state.get('selected_theme', 'plotly_dark')
    fig.update_layout(
        title=dict(text=title, font=dict(size=title_font, color="#4fc3f7"), x=0.5),
        font=dict(size=axis_font, color="#b0bec5"),
        margin=dict(l=40, r=40, t=60, b=40),
        template=theme_to_use,
        hovermode='x unified',
        plot_bgcolor='rgba(26,26,46,0.5)' if theme_to_use == 'plotly_dark' else 'white',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

# -----------------------
# Data loader with caching
# -----------------------
@st.cache_data(ttl=3600)
def load_data():
    # Ajusta la ruta si en deploy está en otra carpeta
    dataset_parquet = "data/processed/ecommerce_dataset_10000_cleaned.parquet"
    dataset_csv = "data/processed/ecommerce_dataset_10000_cleaned.csv"

    try:
        if os.path.exists(dataset_parquet):
            df = pd.read_parquet(dataset_parquet)
        elif os.path.exists(dataset_csv):
            df = pd.read_csv(dataset_csv)
        else:
            return None

        # Normalizaciones y columnas necesarias
        if 'order_date' in df.columns:
            df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        else:
            df['order_date'] = pd.NaT

        # Fill defaults for expected columns to avoid KeyErrors
        for c in ['country', 'total_price', 'order_id', 'customer_id', 'quantity', 'unit_price', 'product_name']:
            if c not in df.columns:
                if c in ['total_price', 'quantity', 'unit_price']:
                    df[c] = 0
                else:
                    df[c] = ""

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
    st.error("❌ No dataset found or dataset vacío. Comprueba la ruta en `data/processed/`.")
    st.stop()

# -----------------------
# Sidebar controls
# -----------------------
with st.sidebar:
    st.title("⚡ Control Center")
    min_date = df['order_date'].min().date() if not df['order_date'].isna().all() else datetime.today().date()
    max_date = df['order_date'].max().date() if not df['order_date'].isna().all() else datetime.today().date()

    start_date = st.date_input("From", min_date, min_value=min_date, max_value=max_date)
    end_date = st.date_input("To", max_date, min_value=min_date, max_value=max_date)

    countries = sorted(df['country'].dropna().unique())
    if len(countries) == 0:
        selected_countries = []
    else:
        selected_countries = st.multiselect("Countries", countries, default=countries[:5])

    top_n = st.slider("Top N Items", 5, 50, 10, 5)

    chart_theme = st.selectbox("Chart Theme", ["plotly_dark", "plotly_white", "ggplot2", "seaborn"], index=0)
    st.session_state.selected_theme = chart_theme

# -----------------------
# Filtering and validation
# -----------------------
try:
    start_date_dt = pd.to_datetime(start_date)
    end_date_dt = pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
except Exception:
    start_date_dt = df['order_date'].min()
    end_date_dt = df['order_date'].max()

if selected_countries:
    df_filtered = df[
        (df['country'].isin(selected_countries)) &
        (df['order_date'] >= start_date_dt) &
        (df['order_date'] <= end_date_dt)
    ].copy()
else:
    df_filtered = df[
        (df['order_date'] >= start_date_dt) &
        (df['order_date'] <= end_date_dt)
    ].copy()

if df_filtered.empty:
    st.warning("⚠️ No hay datos para los filtros seleccionados. Ajusta fechas o países.")
    st.stop()

# -----------------------
# Metrics calculator (safe)
# -----------------------
def calculate_metrics(df_current):
    total_revenue = float(df_current['total_price'].sum()) if 'total_price' in df_current else 0.0
    total_orders = int(df_current['order_id'].nunique()) if 'order_id' in df_current else 0
    unique_customers = int(df_current['customer_id'].nunique()) if 'customer_id' in df_current else 0
    total_quantity = int(df_current['quantity'].sum()) if 'quantity' in df_current else 0
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0.0
    return {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'unique_customers': unique_customers,
        'total_quantity': total_quantity,
        'avg_order_value': avg_order_value
    }

metrics = calculate_metrics(df_filtered)

# -----------------------
# Header & KPI cards
# -----------------------
st.markdown("""
    <div style='text-align:center; padding: 25px; border-radius: 12px;'>
        <h1 class='glowing-title'>📊 EXECUTIVE E-COMMERCE DASHBOARD</h1>
        <p style='color:#c5cae9;'>Real-Time Business Intelligence & Advanced Analytics</p>
    </div>
""", unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("💰 REVENUE", f"${metrics['total_revenue']:,.0f}")
k2.metric("🛒 ORDERS", f"{metrics['total_orders']:,}")
k3.metric("👥 CUSTOMERS", f"{metrics['unique_customers']:,}")
k4.metric("📦 UNITS", f"{metrics['total_quantity']:,}")
k5.metric("💵 AVG ORDER", f"${metrics['avg_order_value']:.2f}")

st.markdown("---")

# -----------------------
# Tabs
# -----------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 REVENUE",
    "👥 CUSTOMERS",
    "📦 PRODUCTS",
    "🌍 GEOGRAPHY",
    "🔬 ADVANCED"
])

# === TAB 1: Revenue ===
with tab1:
    st.subheader("📈 Monthly Revenue Trend")
    monthly_revenue = df_filtered.groupby(df_filtered['order_date'].dt.to_period('M'))['total_price'].sum().reset_index()
    if not monthly_revenue.empty:
        monthly_revenue['order_date'] = monthly_revenue['order_date'].dt.to_timestamp()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly_revenue['order_date'],
            y=monthly_revenue['total_price'],
            mode='lines+markers',
            name='Revenue',
            line=dict(width=3)
        ))
        st.plotly_chart(style_fig(fig, "Monthly Revenue"), use_container_width=True)
    else:
        st.info("No hay datos mensuales para mostrar.")

# === TAB 2: Customers ===
with tab2:
    st.subheader(f"🌟 Top {top_n} Customers by Revenue")
    top_customers = df_filtered.groupby('customer_id').agg({'total_price':'sum','order_id':'nunique'}).reset_index()
    if not top_customers.empty:
        top_customers = top_customers.sort_values('total_price', ascending=False).head(top_n)
        fig = px.bar(top_customers, x='total_price', y='customer_id', orientation='h', labels={'total_price':'Revenue','customer_id':'Customer'})
        st.plotly_chart(style_fig(fig, f"Top {top_n} Customers"), use_container_width=True)
    else:
        st.info("Sin datos de clientes.")

    st.markdown("### 🎯 RFM Segmentation (Simple)")
    try:
        snapshot_date = df_filtered['order_date'].max() + timedelta(days=1)
        rfm = df_filtered.groupby('customer_id').agg({
            'order_date': lambda x: (snapshot_date - x.max()).days,
            'order_id': 'nunique',
            'total_price': 'sum'
        }).reset_index().rename(columns={'order_date':'recency','order_id':'frequency','total_price':'monetary'})
        # Simple labeling
        rfm['segment'] = 'Regular'
        if not rfm.empty:
            rfm.loc[(rfm['frequency']>=rfm['frequency'].quantile(0.75)) & (rfm['monetary']>=rfm['monetary'].quantile(0.75)),'segment']='VIP'
        st.dataframe(rfm.head(20), use_container_width=True)
    except Exception as e:
        st.warning(f"RFM no disponible: {e}")

# === TAB 3: Products ===
with tab3:
    st.subheader(f"🎯 Top {top_n} Products by Revenue")
    prod = df_filtered.groupby('product_name').agg({'total_price':'sum','quantity':'sum'}).reset_index().sort_values('total_price', ascending=False).head(top_n)
    if not prod.empty:
        fig = px.bar(prod, x='total_price', y='product_name', orientation='h', labels={'total_price':'Revenue','product_name':'Product'})
        st.plotly_chart(style_fig(fig, "Top Products"), use_container_width=True)
    else:
        st.info("No hay datos de productos.")

# === TAB 4: Geography ===
with tab4:
    st.subheader("🌍 Revenue by Country")
    country_analysis = df_filtered.groupby('country').agg({'total_price':'sum','order_id':'nunique','customer_id':'nunique'}).reset_index().rename(columns={'total_price':'revenue','order_id':'orders','customer_id':'customers'})
    if not country_analysis.empty:
        fig = px.bar(country_analysis, x='country', y='revenue', labels={'revenue':'Revenue','country':'Country'})
        st.plotly_chart(style_fig(fig, "Revenue by Country"), use_container_width=True)
        # table
        display_df = country_analysis.copy()
        display_df['revenue'] = display_df['revenue'].apply(lambda x: f"${x:,.0f}")
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("No hay datos geográficos.")

# === TAB 5: Advanced ===
with tab5:
    st.subheader("📈 Forecast / Growth")
    try:
        monthly = df_filtered.groupby(df_filtered['order_date'].dt.to_period('M'))['total_price'].sum().reset_index()
        if len(monthly) >= 3:
            monthly['order_date'] = monthly['order_date'].dt.to_timestamp()
            monthly['i'] = range(len(monthly))
            z = np.polyfit(monthly['i'], monthly['total_price'], 2)
            p = np.poly1d(z)
            future_i = [monthly['i'].max() + i for i in range(1,4)]
            future_vals = [p(x) for x in future_i]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=monthly['order_date'], y=monthly['total_price'], name='Historical', mode='lines+markers'))
            future_dates = [monthly['order_date'].max() + timedelta(days=30*i) for i in range(1,4)]
            fig.add_trace(go.Scatter(x=future_dates, y=future_vals, name='Forecast', mode='lines+markers', line=dict(dash='dash')))
            st.plotly_chart(style_fig(fig, "Revenue Forecast (3 months)"), use_container_width=True)
        else:
            st.info("Se requieren al menos 3 meses de datos para forecasting.")
    except Exception as e:
        st.warning(f"Forecast falló: {e}")

# -----------------------
# Export buttons (CSV)
# -----------------------
st.markdown("---")
st.markdown("## 📥 Export")
col1, col2, col3 = st.columns(3)
with col1:
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button("📊 DATASET", csv, file_name=f"data_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", mime="text/csv")
with col2:
    if 'top_customers' in locals() and not top_customers.empty:
        st.download_button("🏆 CUSTOMERS", top_customers.to_csv(index=False).encode('utf-8'), file_name=f"customers_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")
    else:
        st.button("🏆 CUSTOMERS (no data)", disabled=True)
with col3:
    if 'prod' in locals() and not prod.empty:
        st.download_button("📦 PRODUCTS", prod.to_csv(index=False).encode('utf-8'), file_name=f"products_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")
    else:
        st.button("📦 PRODUCTS (no data)", disabled=True)

# -----------------------
# Footer
# -----------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;color:#b0bec5;'>Executive Dashboard • Updated: {datetime.now().strftime('%B %d, %Y - %H:%M')}</p>", unsafe_allow_html=True)
