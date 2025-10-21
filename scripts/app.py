import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================
# PAGE CONFIGURATION
# =====================
st.set_page_config(
    page_title="E-commerce Dashboard",
    page_icon="🛒",
    layout="wide",
)

# =====================
# CUSTOM STYLES (HIGH CONTRAST, EXECUTIVE THEME)
# =====================
st.markdown(
    """
    <style>
    /* ======== PALETA BASE ======== */
    :root {
      --bg-dark: #111827;
      --bg-panel: #1F2937;
      --text-primary: #F3F4F6;
      --text-secondary: #CBD5E1;
      --text-muted: #9CA3AF;
      --accent-blue: #60A5FA;
      --accent-indigo: #3B82F6;
      --accent-gradient: linear-gradient(90deg, #3B82F6 0%, #60A5FA 100%);
      --highlight: #A5B4FC;
    }

    html, body, [class*="css"]  {
      background-color: var(--bg-dark) !important;
      color: var(--text-primary) !important;
    }

    /* ======== TITULOS DE SECCION ======== */
    h1, h2, h3 {
      font-weight: 700;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      background: var(--accent-gradient);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 0.6rem;
    }

    h4, h5, h6 {
      color: var(--highlight);
      font-weight: 600;
    }

    /* ======== KPI CARDS ======== */
    .kpi-card {
      background: var(--bg-panel);
      color: var(--text-primary);
      border-radius: 14px;
      border: 1px solid rgba(96,165,250,0.25);
      padding: 1.5rem;
      text-align: center;
      box-shadow: 0 0 12px rgba(59,130,246,0.25);
      transition: all 0.3s ease-in-out;
    }
    .kpi-card:hover {
      box-shadow: 0 0 18px rgba(96,165,250,0.35);
      transform: translateY(-3px);
    }

    .kpi-value {
      font-size: 2.2rem;
      font-weight: 800;
      color: #FFFFFF;
      text-shadow: 0 0 10px rgba(96,165,250,0.35);
    }
    .kpi-label {
      color: var(--text-secondary);
      font-size: 0.95rem;
      margin-top: 0.3rem;
    }

    /* ======== BOTONES Y ELEMENTOS INTERACTIVOS ======== */
    button, .stButton>button {
      background: var(--accent-gradient);
      color: #FFFFFF !important;
      font-weight: 700;
      border-radius: 10px;
      border: none;
      padding: 0.6rem 1.1rem;
      transition: all 0.2s ease-in-out;
    }
    button:hover {
      background: linear-gradient(90deg, #2563EB, #60A5FA);
      transform: translateY(-1px);
    }

    /* ======== TABS Y CONTROLES ======== */
    .stTabs [role="tab"] {
      color: var(--text-secondary) !important;
      font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
      color: var(--text-primary) !important;
      border-bottom: 3px solid var(--accent-blue);
    }

    /* ======== PLOTLY CHARTS ======== */
    .plotly .axis-title {
      fill: var(--text-primary) !important;
      font-weight: 700 !important;
    }
    .plotly .xtick text, 
    .plotly .ytick text {
      fill: var(--text-secondary) !important;
      font-size: 0.9rem !important;
    }
    .plotly .legend text {
      fill: var(--text-primary) !important;
      font-weight: 600 !important;
    }
    .plotly .bar text, 
    .plotly .scatter text {
      fill: var(--text-primary) !important;
      font-weight: 700 !important;
    }
    .plotly-tooltip, .hoverlayer text {
      color: #F9FAFB !important;
      background-color: rgba(31,41,55,0.9) !important;
      border: 1px solid rgba(96,165,250,0.5);
      border-radius: 6px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# =====================
# LOAD DATASET
# =====================
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/nabihazahid/ecommerce-dataset-for-sql-analysis/main/ecommerce_dataset_10000.csv"
    df = pd.read_csv(url)
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    return df

df = load_data()

# =====================
# KPIs
# =====================
col1, col2, col3, col4 = st.columns(4)

total_revenue = df['Revenue'].sum()
total_orders = df['InvoiceNo'].nunique()
total_customers = df['CustomerID'].nunique()
avg_order_value = total_revenue / total_orders

with col1:
    st.markdown('<div class="kpi-card"><div class="kpi-value">${:,.0f}</div><div class="kpi-label">Total Revenue</div></div>'.format(total_revenue), unsafe_allow_html=True)
with col2:
    st.markdown('<div class="kpi-card"><div class="kpi-value">{:,}</div><div class="kpi-label">Total Orders</div></div>'.format(total_orders), unsafe_allow_html=True)
with col3:
    st.markdown('<div class="kpi-card"><div class="kpi-value">{:,}</div><div class="kpi-label">Unique Customers</div></div>'.format(total_customers), unsafe_allow_html=True)
with col4:
    st.markdown('<div class="kpi-card"><div class="kpi-value">${:,.2f}</div><div class="kpi-label">Average Order Value</div></div>'.format(avg_order_value), unsafe_allow_html=True)

st.markdown("---")

# =====================
# REVENUE TREND CHART
# =====================
st.subheader("REVENUE TREND")
revenue_trend = df.groupby(df['InvoiceDate'].dt.to_period('M'))['Revenue'].sum().reset_index()
revenue_trend['InvoiceDate'] = revenue_trend['InvoiceDate'].dt.to_timestamp()

fig = px.line(revenue_trend, x='InvoiceDate', y='Revenue', title='Monthly Revenue Trend', markers=True)
fig.update_layout(
    plot_bgcolor='rgba(17,24,39,0)',
    paper_bgcolor='rgba(17,24,39,0)',
    font=dict(color='rgb(243,244,246)', size=14),
    title_font=dict(size=18, color='rgb(243,244,246)', family='Arial Black'),
    xaxis=dict(title='Date', gridcolor='rgba(75,85,99,0.25)', zeroline=False),
    yaxis=dict(title='Revenue', gridcolor='rgba(75,85,99,0.25)', zeroline=False),
)
st.plotly_chart(fig, use_container_width=True)

# =====================
# TOP PRODUCTS CHART
# =====================
st.subheader("TOP PRODUCTS BY REVENUE")
top_products = df.groupby('Description')['Revenue'].sum().nlargest(10).reset_index()

fig2 = px.bar(top_products, x='Revenue', y='Description', orientation='h', title='Top 10 Products', color='Revenue', color_continuous_scale='Blues')
fig2.update_layout(
    plot_bgcolor='rgba(17,24,39,0)',
    paper_bgcolor='rgba(17,24,39,0)',
    font=dict(color='rgb(243,244,246)', size=13),
    title_font=dict(size=18, color='rgb(243,244,246)', family='Arial Black'),
    xaxis=dict(title='Revenue', gridcolor='rgba(75,85,99,0.25)'),
    yaxis=dict(title='Product', gridcolor='rgba(75,85,99,0.25)'),
    coloraxis_showscale=False
)
fig2.update_traces(texttemplate='%{x:$,.0f}', textposition='outside')
st.plotly_chart(fig2, use_container_width=True)

# =====================
# COUNTRY REVENUE CHART
# =====================
st.subheader("REVENUE BY COUNTRY")
country_revenue = df.groupby('Country')['Revenue'].sum().nlargest(10).reset_index()
fig3 = px.bar(country_revenue, x='Country', y='Revenue', title='Revenue by Country', color='Revenue', color_continuous_scale='Blues')
fig3.update_layout(
    plot_bgcolor='rgba(17,24,39,0)',
    paper_bgcolor='rgba(17,24,39,0)',
    font=dict(color='rgb(243,244,246)', size=13),
    title_font=dict(size=18, color='rgb(243,244,246)', family='Arial Black'),
    xaxis=dict(title='Country', gridcolor='rgba(75,85,99,0.25)'),
    yaxis=dict(title='Revenue', gridcolor='rgba(75,85,99,0.25)'),
    coloraxis_showscale=False
)
st.plotly_chart(fig3, use_container_width=True)

# =====================
# FOOTER
# =====================
st.markdown("""
    <div style='text-align:center; color:#9CA3AF; font-size:0.9rem; margin-top:2rem;'>
    © 2025 Yenismara Pelayo — Data Analyst | Python · SQL · Tableau · Data Analytics
    </div>
""", unsafe_allow_html=True)
