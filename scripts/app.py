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
    
    /* Mejorar contraste en tablas */
    [data-testid="stDataFrame"] table {
        background-color: rgb(31, 41, 55) !important;
    }
    
    [data-testid="stDataFrame"] th {
        background-color: rgb(30, 58, 138) !important;
        color: rgb(243, 244, 246) !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stDataFrame"] td {
        color: rgb(229, 231, 235) !important;
        background-color: rgb(31, 41, 55) !important;
    }
    
    [data-testid="stDataFrame"] tr:hover {
        background-color: rgb(55, 65, 81) !important;
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

# Executive overview visual system.  This intentionally overrides the older
# decorative theme above while leaving the dashboard calculations unchanged.
st.markdown("""
<style>
    .stApp, .main {
        background: #f6f8fb !important;
    }
    .block-container {
        max-width: 1440px;
        padding-top: 2rem;
        padding-bottom: 2.5rem;
    }
    h1, h2, h3, h4, p, span, label {
        font-family: 'Inter', sans-serif !important;
    }
    h1 { color: #172033 !important; }
    h2, h3, h4 { color: #22314a !important; }
    p, span, label { color: #5f6b7a !important; }
    .overview-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 1.5rem;
        padding: 0 0 1.35rem;
        margin-bottom: 1.25rem;
        border-bottom: 1px solid #dfe5ec;
    }
    .overview-eyebrow {
        color: #2563eb !important;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.45rem;
    }
    .overview-title {
        color: #172033 !important;
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.035em;
        line-height: 1.15;
        margin: 0;
    }
    .overview-subtitle {
        color: #667085 !important;
        font-size: 0.98rem;
        margin: 0.45rem 0 0;
    }
    .overview-meta {
        color: #667085 !important;
        font-size: 0.78rem;
        line-height: 1.55;
        text-align: right;
        padding-top: 0.3rem;
    }
    .filter-panel {
        background: #ffffff;
        border: 1px solid #dfe5ec;
        border-radius: 10px;
        padding: 1rem 1.15rem 0.25rem;
        margin: 0 0 1.25rem;
        box-shadow: 0 1px 2px rgba(16, 24, 40, 0.03);
    }
    .filter-panel [data-baseweb="select"] > div,
    .filter-panel input {
        background: #ffffff !important;
        color: #172033 !important;
        border-color: #cfd8e3 !important;
    }
    .filter-panel label { color: #475467 !important; font-size: 0.78rem !important; font-weight: 600 !important; }
    .kpi-card {
        min-height: 126px;
        background: #ffffff;
        border: 1px solid #dfe5ec;
        border-radius: 10px;
        padding: 1.05rem 1.15rem;
        box-shadow: 0 1px 2px rgba(16, 24, 40, 0.03);
    }
    .kpi-card--primary {
        border-left: 4px solid #2563eb;
        background: #fbfdff;
    }
    .kpi-label {
        color: #667085 !important;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 0.55rem;
    }
    .kpi-value {
        color: #172033 !important;
        font-size: 1.7rem;
        font-weight: 700;
        letter-spacing: -0.035em;
        line-height: 1.1;
    }
    .kpi-card--primary .kpi-value { color: #1d4ed8 !important; font-size: 2rem; }
    .kpi-delta { font-size: 0.82rem; font-weight: 600; margin-top: 0.6rem; }
    .kpi-delta--positive { color: #15803d !important; }
    .kpi-delta--negative { color: #b42318 !important; }
    .kpi-delta--neutral { color: #667085 !important; }
    .comparison-line {
        color: #667085 !important;
        font-size: 0.84rem;
        margin: 0.9rem 0 1.65rem;
    }
    .overview-section-title {
        color: #22314a !important;
        font-size: 1.12rem;
        font-weight: 700;
        letter-spacing: -0.01em;
        margin: 0 0 0.85rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        border: 0 !important;
        border-bottom: 1px solid #dfe5ec !important;
        border-radius: 0 !important;
        padding: 0 !important;
        gap: 1.25rem;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: #667085 !important;
        border: 0 !important;
        border-radius: 0 !important;
        height: 42px;
        padding: 0 0 0.65rem !important;
        font-size: 0.9rem;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: transparent !important;
        color: #1d4ed8 !important;
        box-shadow: none !important;
        border-bottom: 2px solid #2563eb !important;
    }
    .stButton > button, .stDownloadButton > button {
        background: #ffffff !important;
        color: #344054 !important;
        border: 1px solid #cfd8e3 !important;
        border-radius: 7px !important;
        box-shadow: none !important;
        font-weight: 600 !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background: #f8fafc !important;
        border-color: #98a2b3 !important;
        transform: none !important;
        box-shadow: none !important;
    }
    [data-testid="stDataFrame"] { border-color: #dfe5ec !important; }
    @media (max-width: 768px) {
        .overview-header { display: block; }
        .overview-meta { text-align: left; margin-top: 0.75rem; }
        .overview-title { font-size: 1.65rem; }
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

# Compact header and global filters
min_date = df['order_date'].min().date()
max_date = df['order_date'].max().date()
countries = sorted(df['country'].dropna().unique())
categories = sorted(df['category'].dropna().unique())

def reset_filters():
    st.session_state['filter_date_range'] = (min_date, max_date)
    st.session_state['filter_countries'] = countries
    st.session_state['filter_categories'] = categories

def set_date_preset(days=None, ytd=False):
    preset_start = datetime(max_date.year, 1, 1).date() if ytd else max_date - timedelta(days=days)
    st.session_state['filter_date_range'] = (max(min_date, preset_start), max_date)

st.markdown(f"""
    <div class='overview-header'>
        <div>
            <div class='overview-eyebrow'>Business intelligence</div>
            <h1 class='overview-title'>E-commerce Performance Analytics</h1>
            <p class='overview-subtitle'>Sales, customer and product performance overview</p>
        </div>
        <div class='overview-meta'>
            Source: processed e-commerce dataset<br>
            Available data: {min_date.strftime('%b %d, %Y')} – {max_date.strftime('%b %d, %Y')}
        </div>
    </div>
""", unsafe_allow_html=True)

with st.container(key="bi_filter_bar"):
    st.markdown("""
    <style>
    .st-key-bi_filter_bar {
        background: #ffffff;
        border: 1px solid #dfe5ec;
        border-radius: 10px;
        padding: 0.55rem 0.9rem;
        margin: 0 0 1.25rem;
        box-shadow: 0 1px 2px rgba(16, 24, 40, 0.03);
    }
    .st-key-bi_filter_bar [data-testid="stVerticalBlockBorderWrapper"] { border: none; }
    .st-key-bi_filter_bar [data-testid="stWidgetLabel"] p {
        color: #8a94a6 !important;
        font-size: 0.68rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 0.15rem !important;
    }
    .st-key-bi_filter_bar [data-baseweb="select"] > div,
    .st-key-bi_filter_bar [data-testid="stDateInput"] input,
    .st-key-bi_filter_bar [data-testid="stDateInputField"] {
        background: #ffffff !important;
        color: #172033 !important;
        border-color: #dfe5ec !important;
        border-radius: 7px !important;
        min-height: 2.15rem !important;
    }
    .st-key-bi_filter_bar [data-baseweb="select"] {
        min-height: 2.15rem !important;
    }
    .st-key-bi_filter_bar div[data-testid="stPopover"] > button,
    .st-key-bi_filter_bar button[kind="secondary"] {
        background: #f8fafc !important;
        color: #22314a !important;
        border: 1px solid #dfe5ec !important;
        border-radius: 7px !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        padding: 0.3rem 0.7rem !important;
        min-height: 2.15rem !important;
        box-shadow: none !important;
    }
    .st-key-bi_filter_bar div[data-testid="stPopover"] > button:hover,
    .st-key-bi_filter_bar button[kind="secondary"]:hover {
        border-color: #2563eb !important;
        color: #2563eb !important;
    }
    .st-key-bi_filter_bar [data-testid="column"]:nth-of-type(4) div[data-testid="stPopover"] > button {
        border-left: 2px solid #0d9488 !important;
    }
    .st-key-bi_filter_bar [data-testid="stElementContainer"] { margin-bottom: 0 !important; }
    .st-key-bi_filter_bar [data-testid="stHorizontalBlock"] { align-items: flex-end !important; }
    .st-key-bi_filter_bar [data-testid="stIconMaterial"] {
        font-family: 'Material Symbols Rounded' !important;
        font-weight: normal !important;
        font-style: normal !important;
        font-size: 1.15rem !important;
        line-height: 1 !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        -webkit-font-smoothing: antialiased;
    }
    </style>
    """, unsafe_allow_html=True)

    bar_col1, bar_col2, bar_col3, bar_col4, bar_col5 = st.columns([2.0, 1.3, 1.3, 0.85, 0.75])

    with bar_col1:
        selected_date_range = st.date_input(
            "Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date,
            key='filter_date_range'
        )

    with bar_col2:
        current_countries = st.session_state.get('filter_countries', countries)
        if len(current_countries) == 0:
            country_summary = "No countries"
        elif set(current_countries) == set(countries):
            country_summary = "All countries"
        else:
            country_summary = f"{len(current_countries)} countries selected"
        with st.popover(country_summary, width='stretch'):
            selected_countries = st.multiselect("Country", countries, default=countries, key='filter_countries')

    with bar_col3:
        current_categories = st.session_state.get('filter_categories', categories)
        if len(current_categories) == 0:
            category_summary = "No categories"
        elif set(current_categories) == set(categories):
            category_summary = "All categories"
        else:
            category_summary = f"{len(current_categories)} categories selected"
        with st.popover(category_summary, width='stretch'):
            selected_categories = st.multiselect("Category", categories, default=categories, key='filter_categories')

    with bar_col4:
        with st.popover("⚙ Options", width='stretch'):
            st.caption("Quick date ranges")
            qp1, qp2 = st.columns(2)
            with qp1:
                st.button("Last 7 days", key='preset_7_days', on_click=set_date_preset, args=(7,), width='stretch')
                st.button("Quarter", key='preset_quarter', on_click=set_date_preset, args=(90,), width='stretch')
            with qp2:
                st.button("Last 30 days", key='preset_30_days', on_click=set_date_preset, args=(30,), width='stretch')
                st.button("Year to date", key='preset_ytd', on_click=set_date_preset, kwargs={'ytd': True}, width='stretch')

            st.divider()
            st.caption("Display")
            top_n = st.slider("Top N items", 5, 50, 10, 5)
            chart_theme = st.selectbox("Chart theme", ["plotly_white", "plotly_dark", "seaborn", "ggplot2"])
            st.session_state.selected_theme = chart_theme

            st.divider()
            st.caption("Saved filters")
            if st.button("Save current filters", key='save_filters', width='stretch'):
                st.session_state.saved_filters = {
                    'start_date': selected_date_range[0],
                    'end_date': selected_date_range[-1],
                    'countries': selected_countries,
                    'categories': selected_categories,
                    'top_n': top_n
                }
                st.success("Filters saved for this session.")
            if 'saved_filters' in st.session_state and st.button("View saved filters", key='view_saved_filters', width='stretch'):
                saved = st.session_state.saved_filters
                st.info(f"Saved: {saved['start_date']} to {saved['end_date']}")

    with bar_col5:
        st.button("Reset", key='reset_filters_btn', on_click=reset_filters, width='stretch')


start_date = selected_date_range[0]
end_date = selected_date_range[-1]

# Filter data
start_date_dt = pd.to_datetime(start_date)
end_date_dt = pd.to_datetime(end_date)
df_filtered = df[
    (df['country'].isin(selected_countries)) &
    (df['category'].isin(selected_categories)) &
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

# KPI cards
def render_kpi(label, value, delta=None, primary=False):
    if delta is None:
        delta_html = "<div class='kpi-delta kpi-delta--neutral'>No prior-period comparison</div>"
    else:
        delta_class = 'positive' if delta > 0 else 'negative' if delta < 0 else 'neutral'
        delta_prefix = '+' if delta > 0 else ''
        delta_html = f"<div class='kpi-delta kpi-delta--{delta_class}'>{delta_prefix}{delta:.1f}% vs previous period</div>"
    primary_class = ' kpi-card--primary' if primary else ''
    st.markdown(
        f"<div class='kpi-card{primary_class}'><div class='kpi-label'>{label}</div>"
        f"<div class='kpi-value'>{value}</div>{delta_html}</div>",
        unsafe_allow_html=True
    )

st.markdown("<div class='overview-section-title'>Performance summary</div>", unsafe_allow_html=True)
kpi1, kpi2, kpi3, kpi4 = st.columns([1.25, 1, 1, 1])
with kpi1:
    render_kpi("Revenue", f"${metrics['total_revenue']:,.0f}", metrics['revenue_delta'], primary=True)
with kpi2:
    render_kpi("Orders", f"{metrics['total_orders']:,}", metrics['orders_delta'])
with kpi3:
    render_kpi("Average order value", f"${metrics['avg_order_value']:.2f}")
with kpi4:
    render_kpi("Customers", f"{metrics['unique_customers']:,}", metrics['customers_delta'])

selected_period = f"{start_date.strftime('%b %d, %Y')} – {end_date.strftime('%b %d, %Y')}"
st.markdown(
    f"<div class='comparison-line'>Selected period: {selected_period} · Compared with previous period · "
    f"Units sold: {metrics['total_quantity']:,}</div>",
    unsafe_allow_html=True
)

# Plotly Helper con mejor contraste
def style_fig(fig, title=""):
    theme = st.session_state.get('selected_theme', 'plotly_dark')
    
    # Colores de texto según el tema
    is_light_theme = theme in ['plotly_white', 'seaborn', 'ggplot2']
    
    title_color = "rgb(31, 41, 55)" if is_light_theme else "rgb(229, 231, 235)"
    text_color = "rgb(55, 65, 81)" if is_light_theme else "rgb(209, 213, 219)"
    grid_color = "rgba(0, 0, 0, 0.15)" if is_light_theme else "rgba(75, 85, 99, 0.3)"
    paper_bg = "rgba(255, 255, 255, 0.95)" if is_light_theme else "rgba(0, 0, 0, 0)"
    plot_bg = "rgba(249, 250, 251, 1)" if is_light_theme else "rgba(31, 41, 55, 0.3)"
    
    fig.update_layout(
        title=dict(
            text=title, 
            font=dict(size=20, color=title_color, family="Inter", weight=700),
            x=0.5, 
            xanchor='center'
        ),
        font=dict(size=13, color=text_color, family="Inter", weight=500),
        margin=dict(l=50, r=50, t=70, b=50),
        template=theme,
        hovermode='x unified',
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        hoverlabel=dict(
            bgcolor="rgb(31, 41, 55)" if not is_light_theme else "white",
            font_size=12,
            font_family="Inter",
            font_color="white" if not is_light_theme else "rgb(31, 41, 55)"
        )
    )
    
    # Ejes con mejor contraste
    axis_config = dict(
        showgrid=True, 
        gridcolor=grid_color,
        title_font=dict(color=text_color, size=13, weight=600),
        tickfont=dict(color=text_color, size=11, weight=500),
        linecolor=grid_color
    )
    
    fig.update_xaxes(**axis_config)
    fig.update_yaxes(**axis_config)
    
    # Actualizar colores de texto en trazas
    for trace in fig.data:
        if hasattr(trace, 'textfont'):
            trace.textfont.color = text_color
        if hasattr(trace, 'marker') and hasattr(trace.marker, 'line'):
            trace.marker.line.width = 0.5
    
    return fig

colors = ['rgb(96, 165, 250)', 'rgb(129, 140, 248)', 'rgb(167, 139, 250)', 'rgb(236, 72, 153)', 'rgb(251, 146, 60)']

# Función para obtener color de texto según tema
def get_text_color():
    theme = st.session_state.get('selected_theme', 'plotly_dark')
    return "rgb(31, 41, 55)" if theme in ['plotly_white', 'seaborn', 'ggplot2'] else "rgb(209, 213, 219)"

# Dashboard tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview", "Customers", "Products", "Geography", "Insights"])

# TAB 1: Executive overview
with tab1:
    st.markdown("<div class='overview-section-title'>Revenue performance</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([2.05, 1])
    
    with col1:
        monthly_revenue = df_filtered.groupby(df_filtered['order_date'].dt.to_period('M'))['total_price'].sum().reset_index()
        monthly_revenue['order_date'] = monthly_revenue['order_date'].dt.to_timestamp()
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=monthly_revenue['order_date'], y=monthly_revenue['total_price'],
            mode='lines+markers', name='Revenue',
            line=dict(color='rgb(37, 99, 235)', width=3),
            marker=dict(size=6, color='rgb(37, 99, 235)'),
            fill='tozeroy', fillcolor='rgba(37, 99, 235, 0.10)',
            textfont=dict(color=get_text_color())
        ))
        
        z = np.polyfit(range(len(monthly_revenue)), monthly_revenue['total_price'], 1)
        p = np.poly1d(z)
        fig_trend.add_trace(go.Scatter(
            x=monthly_revenue['order_date'], y=p(range(len(monthly_revenue))),
            mode='lines', name='Trend',
            line=dict(color='rgb(100, 116, 139)', width=2, dash='dash')
        ))
        st.plotly_chart(style_fig(fig_trend, "Monthly revenue"), width='stretch')
    
    with col2:
        country_revenue = df_filtered.groupby('country')['total_price'].sum().nlargest(5).sort_values().reset_index()
        fig_country_overview = go.Figure(data=[go.Bar(
            x=country_revenue['total_price'], y=country_revenue['country'], orientation='h',
            marker=dict(color='rgb(96, 165, 250)'),
            text=[f"${value:,.0f}" for value in country_revenue['total_price']],
            textposition='outside',
            textfont=dict(color=get_text_color(), size=10)
        )])
        st.plotly_chart(style_fig(fig_country_overview, "Top countries by revenue"), width='stretch')

    product_col, weekly_col = st.columns([1.45, 1])
    with product_col:
        top_products_overview = df_filtered.groupby('product_name')['total_price'].sum().nlargest(top_n).sort_values().reset_index()
        fig_products_overview = go.Figure(data=[go.Bar(
            x=top_products_overview['total_price'], y=top_products_overview['product_name'], orientation='h',
            marker=dict(color='rgb(79, 70, 229)'),
            text=[f"${value:,.0f}" for value in top_products_overview['total_price']],
            textposition='outside',
            textfont=dict(color=get_text_color(), size=10)
        )])
        st.plotly_chart(style_fig(fig_products_overview, "Top products by revenue"), width='stretch')
    
    with weekly_col:
        dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_revenue = df_filtered.groupby('day_of_week')['total_price'].sum().reindex(dow_order).reset_index()
        fig_dow = go.Figure(data=[go.Bar(
            x=dow_revenue['day_of_week'], y=dow_revenue['total_price'],
            marker=dict(color='rgb(148, 163, 184)'),
            text=[f"${val:,.0f}" for val in dow_revenue['total_price']],
            textposition='outside',
            textfont=dict(color=get_text_color(), size=10)
        )])
        st.plotly_chart(style_fig(fig_dow, "Revenue by day of week"), width='stretch')

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
            text=[f"${val:,.0f}" for val in top_customers['total_revenue']], 
            textposition='outside',
            textfont=dict(color=get_text_color(), size=11, weight=600)
        )])
        st.plotly_chart(style_fig(fig_cust, "Revenue Champions"), width='stretch')
    
    with col2:
        st.markdown("### 🔄 RETENTION")
        order_freq = df_filtered.groupby('customer_id')['order_id'].nunique().value_counts().sort_index().reset_index()
        order_freq.columns = ['orders', 'customer_count']
        
        fig_freq = go.Figure(data=[go.Bar(
            x=order_freq['orders'], y=order_freq['customer_count'],
            marker=dict(color=order_freq['customer_count'], colorscale='Turbo'),
            text=order_freq['customer_count'], 
            textposition='outside',
            textfont=dict(color=get_text_color(), size=12, weight=600)
        )])
        st.plotly_chart(style_fig(fig_freq, "Order Frequency"), width='stretch')
    
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
            text=segment_summary['customer_count'], 
            textposition='outside',
            textfont=dict(color=get_text_color(), size=12, weight=600)
        )])
        st.plotly_chart(style_fig(fig_seg, "Customers by Segment"), width='stretch')
    
    with sc2:
        fig_segrev = go.Figure(data=[go.Bar(
            x=segment_summary['segment'], y=segment_summary['total_revenue'],
            marker=dict(color=colors[:len(segment_summary)]),
            text=[f"${val:,.0f}" for val in segment_summary['total_revenue']], 
            textposition='outside',
            textfont=dict(color=get_text_color(), size=12, weight=600)
        )])
        st.plotly_chart(style_fig(fig_segrev, "Revenue by Segment"), width='stretch')

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
            text=[f"${val:,.0f}" for val in top_prod['total_price']], 
            textposition='outside',
            textfont=dict(color=get_text_color(), size=11, weight=600)
        )])
        st.plotly_chart(style_fig(fig_prod, "Revenue Leaders"), width='stretch')
    
    with pc2:
        st.markdown("### 📦 BY QUANTITY")
        top_qty = df_filtered.groupby('product_name')['quantity'].sum().nlargest(top_n).reset_index()
        
        fig_qty = go.Figure(data=[go.Bar(
            x=top_qty['quantity'], y=top_qty['product_name'], orientation='h',
            marker=dict(color=top_qty['quantity'], colorscale='Teal'),
            text=top_qty['quantity'], 
            textposition='outside',
            textfont=dict(color=get_text_color(), size=11, weight=600)
        )])
        st.plotly_chart(style_fig(fig_qty, "Volume Champions"), width='stretch')
    
    st.markdown("### 💲 PRICE DISTRIBUTION")
    prc1, prc2 = st.columns([2, 1])
    
    with prc1:
        fig_price = go.Figure()
        fig_price.add_trace(go.Histogram(
            x=df_filtered['unit_price'], nbinsx=50,
            marker=dict(color='rgb(126, 87, 194)'), name='Distribution'
        ))
        st.plotly_chart(style_fig(fig_price, "Unit Price Analysis"), width='stretch')
    
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
        text=[f"${val:,.0f}" for val in country_analysis['revenue']], 
        textposition='outside',
        textfont=dict(color=get_text_color(), size=12, weight=600)
    )])
    st.plotly_chart(style_fig(fig_country, "Global Distribution"), width='stretch')
    
    st.markdown("### 📋 DETAILED PERFORMANCE")
    country_analysis['avg_order_value'] = country_analysis['revenue'] / country_analysis['orders']
    display_df = country_analysis.copy()
    display_df['revenue'] = display_df['revenue'].apply(lambda x: f"${x:,.0f}")
    display_df['avg_order_value'] = display_df['avg_order_value'].apply(lambda x: f"${x:.2f}")
    st.dataframe(display_df, width='stretch', hide_index=True)

# TAB 5: Advanced
with tab5:
    st.markdown("### Supporting analysis")
    
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
            textposition='outside',
            textfont=dict(color=get_text_color(), size=11, weight=600)
        ))
        fig_growth.add_hline(y=0, line_dash="solid", line_color="rgba(255, 255, 255, 0.4)")
        st.plotly_chart(style_fig(fig_growth, "MoM Growth %"), width='stretch')
    
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
        st.plotly_chart(style_fig(fig_pareto, "80/20 Rule"), width='stretch')
    
    top_5_revenue_pct = (top_customers['total_revenue'].head(5).sum() / metrics['total_revenue']) * 100
    
    st.markdown("### Key takeaways")
    sum1, sum2, sum3, sum4 = st.columns(4)
    
    with sum1:
        top_country = country_analysis.iloc[0]
        st.markdown(f"**TOP COUNTRY**")
        st.metric("Top country", top_country['country'], f"${top_country['revenue']:,.0f}", label_visibility="collapsed")
    
    with sum2:
        best_prod = top_prod.iloc[0]
        st.markdown(f"**BEST PRODUCT**")
        st.metric("Best product", best_prod['product_name'][:15], f"${best_prod['total_price']:,.0f}", label_visibility="collapsed")
    
    with sum3:
        vip_count = rfm[rfm['segment'] == '💎 VIP'].shape[0]
        st.markdown(f"**VIP CUSTOMERS**")
        st.metric("VIP customers", vip_count, "Top Tier", label_visibility="collapsed")
    
    with sum4:
        growth_avg = growth_data['growth_rate'].mean()
        st.markdown(f"**AVG GROWTH**")
        st.metric("Average growth", f"{growth_avg:.1f}%", "MoM", label_visibility="collapsed")

# Export Section
st.markdown("---")
st.markdown("## Export data")

exp1, exp2, exp3, exp4 = st.columns(4)

with exp1:
    st.download_button(
        "📊 DATASET",
        df_filtered.to_csv(index=False).encode('utf-8'),
        file_name=f"data_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        width='stretch'
    )

with exp2:
    st.download_button(
        "🏆 CUSTOMERS",
        top_customers.to_csv(index=False).encode('utf-8'),
        file_name=f"customers_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        width='stretch'
    )

with exp3:
    st.download_button(
        "📦 PRODUCTS",
        top_prod.to_csv(index=False).encode('utf-8'),
        file_name=f"products_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        width='stretch'
    )

with exp4:
    st.download_button(
        "🌍 COUNTRIES",
        display_df.to_csv(index=False).encode('utf-8'),
        file_name=f"countries_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        width='stretch'
    )

# Additional analysis
st.markdown("---")
st.markdown("## Additional analysis")

adv_tab1, adv_tab2, adv_tab3, adv_tab4 = st.tabs([
    "Alerts", "Forecast", "YoY comparison", "Report"
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
            
            st.plotly_chart(style_fig(fig_forecast, "3-Month Forecast"), width='stretch')
        
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
            text=[f"${v:,.0f}" for v in m_y1['revenue']], 
            textposition='outside',
            textfont=dict(color=get_text_color(), size=11, weight=600)
        ))
        fig_yoy.add_trace(go.Bar(
            x=m_y2['month_name'], y=m_y2['revenue'], name=str(year2),
            marker=dict(color='rgb(129, 140, 248)'),
            text=[f"${v:,.0f}" for v in m_y2['revenue']], 
            textposition='outside',
            textfont=dict(color=get_text_color(), size=11, weight=600)
        ))
        
        st.plotly_chart(style_fig(fig_yoy, f"{year1} vs {year2}"), width='stretch')
        
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
    st.markdown("### Executive report")
    
    st.info("""
    **📋 Report Contents:**
    - Executive Summary with Key Metrics
    - Performance Trends & Growth Analysis
    - Top Customers & Products Tables
    - Geographic Distribution
    - Customer Segmentation (RFM)
    - Smart Alerts & Recommendations
    """)
    
    if st.button("📄 GENERATE REPORT", width='stretch', type="primary"):
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
                width='stretch'
            )
            
            st.success("✅ Report generated! Download above.")
            st.info("💡 Open HTML in browser, then Print → Save as PDF")

# Footer
st.markdown("---")
st.markdown(f"""
    <div style='text-align: center; padding: 12px 0; color: #667085; font-size: 12px;'>
        E-commerce Performance Analytics · Data refreshed in the current session: {datetime.now().strftime('%b %d, %Y %H:%M')}
    </div>
""", unsafe_allow_html=True)
