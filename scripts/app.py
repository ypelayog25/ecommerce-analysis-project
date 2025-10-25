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

# Initialize session state for theme customization
if 'theme_preset' not in st.session_state:
    st.session_state.theme_preset = "Enhanced (Default)"
if 'font_scale' not in st.session_state:
    st.session_state.font_scale = 1.0
if 'color_palette' not in st.session_state:
    st.session_state.color_palette = "Default"

# Theme Preset Configurations
THEME_PRESETS = {
    "Enhanced (Default)": {
        "h1_size": 38, "h2_size": 32, "h3_size": 24,
        "metric_value": 42, "metric_label": 15, "metric_delta": 16,
        "body_text": 16, "metric_padding": 28,
        "text_color": "rgb(229, 231, 235)", "text_bright": "rgb(248, 250, 252)",
        "metric_label_color": "rgb(203, 213, 225)"
    },
    "High Contrast": {
        "h1_size": 40, "h2_size": 34, "h3_size": 26,
        "metric_value": 46, "metric_label": 16, "metric_delta": 18,
        "body_text": 18, "metric_padding": 32,
        "text_color": "rgb(255, 255, 255)", "text_bright": "rgb(255, 255, 255)",
        "metric_label_color": "rgb(255, 255, 255)"
    },
    "Extra Large Text": {
        "h1_size": 48, "h2_size": 40, "h3_size": 32,
        "metric_value": 56, "metric_label": 20, "metric_delta": 22,
        "body_text": 20, "metric_padding": 36,
        "text_color": "rgb(243, 244, 246)", "text_bright": "rgb(255, 255, 255)",
        "metric_label_color": "rgb(229, 231, 235)"
    },
    "Compact View": {
        "h1_size": 28, "h2_size": 24, "h3_size": 18,
        "metric_value": 32, "metric_label": 12, "metric_delta": 13,
        "body_text": 13, "metric_padding": 18,
        "text_color": "rgb(209, 213, 219)", "text_bright": "rgb(243, 244, 246)",
        "metric_label_color": "rgb(156, 163, 175)"
    }
}

# Colorblind-Friendly Palettes
COLOR_PALETTES = {
    "Default": ['rgb(96, 165, 250)', 'rgb(129, 140, 248)', 'rgb(167, 139, 250)', 'rgb(236, 72, 153)', 'rgb(251, 146, 60)'],
    "Deuteranopia": ['rgb(0, 114, 178)', 'rgb(230, 159, 0)', 'rgb(86, 180, 233)', 'rgb(240, 228, 66)', 'rgb(213, 94, 0)'],
    "Protanopia": ['rgb(0, 92, 171)', 'rgb(255, 179, 0)', 'rgb(128, 186, 236)', 'rgb(246, 229, 82)', 'rgb(220, 110, 0)'],
    "Tritanopia": ['rgb(200, 36, 35)', 'rgb(66, 136, 181)', 'rgb(246, 112, 112)', 'rgb(149, 197, 226)', 'rgb(106, 76, 147)'],
    "High Contrast": ['rgb(0, 176, 240)', 'rgb(255, 192, 0)', 'rgb(146, 208, 80)', 'rgb(255, 102, 255)', 'rgb(255, 51, 51)']
}

# Get current theme settings
preset = THEME_PRESETS[st.session_state.theme_preset]
font_scale = st.session_state.font_scale

# Generate Dynamic CSS
def generate_css():
    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Roboto:wght@300;400;500;700;900&display=swap');
    
    * {{ 
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }}
    
    .main {{ 
        background: linear-gradient(135deg, rgb(17, 24, 39) 0%, rgb(31, 41, 55) 50%, rgb(17, 24, 39) 100%);
        padding: 1.5rem 2rem;
    }}
    
    [data-testid="stSidebar"] {{ 
        background: linear-gradient(180deg, rgb(31, 41, 55) 0%, rgb(17, 24, 39) 100%);
    }}
    
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] div {{
        color: rgb(243, 244, 246) !important;
        font-weight: 500;
    }}
    
    [data-testid="stSidebar"] div[data-testid="stExpander"] {{
        background-color: rgb(55, 65, 81) !important;
        border: 1px solid rgb(75, 85, 99);
        border-radius: 8px;
    }}
    
    [data-testid="stSidebar"] div[data-testid="stExpander"] > div {{
        background-color: rgb(55, 65, 81) !important;
    }}
    
    [data-testid="stSidebar"] div[data-testid="stExpander"] > div > div {{
        background-color: rgb(55, 65, 81) !important;
        padding: 18px;
        border-radius: 8px;
    }}
    
    [data-testid="stSidebar"] details[data-testid="stExpander"] {{
        background-color: rgb(55, 65, 81) !important;
    }}
    
    [data-testid="stSidebar"] details[data-testid="stExpander"] summary {{
        background-color: rgb(55, 65, 81) !important;
        padding: 14px 18px !important;
        border-radius: 8px;
        font-size: {int(15 * font_scale)}px !important;
        font-weight: 600 !important;
    }}
    
    [data-testid="stSidebar"] details[open] {{
        background-color: rgb(55, 65, 81) !important;
    }}
    
    [data-testid="stSidebar"] details[open] > summary {{
        background-color: rgb(55, 65, 81) !important;
        border-bottom: 1px solid rgb(75, 85, 99);
        margin-bottom: 12px;
    }}
    
    [data-testid="stSidebar"] .stExpander {{
        background-color: rgb(55, 65, 81) !important;
    }}
    
    [data-testid="stSidebar"] [data-testid="stExpanderDetails"] {{
        background-color: rgb(55, 65, 81) !important;
    }}
    
    [data-testid="stSidebar"] input[type="date"], [data-testid="stSidebar"] input[type="text"] {{
        background-color: rgb(55, 65, 81) !important;
        color: rgb(243, 244, 246) !important;
        border: 1px solid rgb(75, 85, 99) !important;
        border-radius: 6px;
        padding: 12px;
        font-weight: 500;
        font-size: {int(15 * font_scale)}px !important;
    }}
    
    [data-testid="stSidebar"] [data-baseweb="select"] {{
        background-color: rgb(55, 65, 81) !important;
        border-radius: 6px;
    }}
    
    [data-testid="stSidebar"] [data-baseweb="select"] > div {{
        background-color: rgb(55, 65, 81) !important;
        color: rgb(243, 244, 246) !important;
        border: 1px solid rgb(75, 85, 99) !important;
        font-size: {int(15 * font_scale)}px !important;
    }}
    
    [data-testid="stSidebar"] [data-baseweb="popover"] {{
        background-color: rgb(31, 41, 55) !important;
    }}
    
    [data-testid="stSidebar"] ul {{
        background-color: rgb(31, 41, 55) !important;
    }}
    
    [data-testid="stSidebar"] li {{
        background-color: rgb(31, 41, 55) !important;
        color: rgb(243, 244, 246) !important;
        font-size: {int(15 * font_scale)}px !important;
    }}
    
    [data-testid="stSidebar"] .stCheckbox {{
        background-color: transparent !important;
    }}
    
    [data-testid="stSidebar"] .stCheckbox label {{
        font-size: {int(15 * font_scale)}px !important;
        color: rgb(243, 244, 246) !important;
    }}
    
    [data-testid="stSidebar"] .stSlider {{
        background-color: transparent !important;
    }}
    
    [data-testid="stSidebar"] .stMultiSelect {{
        background-color: rgb(55, 65, 81) !important;
    }}
    
    [data-testid="stSidebar"] .stMultiSelect > div {{
        background-color: rgb(55, 65, 81) !important;
    }}
    
    [data-testid="stSidebar"] .stDateInput > div {{
        background-color: rgb(55, 65, 81) !important;
    }}
    
    [data-testid="stSidebar"] input {{
        background-color: rgb(55, 65, 81) !important;
        color: rgb(243, 244, 246) !important;
        font-size: {int(15 * font_scale)}px !important;
    }}
    
    [data-testid="stSidebar"] .row-widget {{
        background-color: transparent !important;
    }}
    
    [data-testid="stSidebar"] .stMarkdown {{
        background-color: transparent !important;
    }}
    
    h1 {{ 
        color: {preset['text_bright']} !important;
        font-weight: 800 !important;
        letter-spacing: -0.8px;
        font-size: {int(preset['h1_size'] * font_scale)}px !important;
    }}
    
    h2 {{ 
        color: {preset['text_bright']} !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
        font-size: {int(preset['h2_size'] * font_scale)}px !important;
    }}
    
    h3 {{ 
        color: {preset['text_bright']} !important;
        font-weight: 700 !important;
        letter-spacing: -0.4px;
        font-size: {int(preset['h3_size'] * font_scale)}px !important;
    }}
    
    [data-testid="stMetricValue"] {{
        font-size: {int(preset['metric_value'] * font_scale)}px !important;
        font-weight: 800 !important;
        color: rgb(147, 197, 253) !important;
        letter-spacing: -0.8px;
    }}
    
    [data-testid="stMetricLabel"] {{
        font-size: {int(preset['metric_label'] * font_scale)}px !important;
        font-weight: 700 !important;
        color: {preset['metric_label_color']} !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }}
    
    [data-testid="stMetricDelta"] {{
        font-size: {int(preset['metric_delta'] * font_scale)}px !important;
        font-weight: 700 !important;
    }}
    
    div[data-testid="metric-container"] {{
        background: linear-gradient(135deg, rgb(30, 58, 138) 0%, rgb(29, 78, 216) 100%);
        padding: {int(preset['metric_padding'])}px !important;
        border-radius: 14px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
        border: 1px solid rgba(59, 130, 246, 0.4);
        transition: all 0.3s ease;
        margin-bottom: 16px;
    }}
    
    div[data-testid="metric-container"]:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.5);
        border-color: rgba(96, 165, 250, 0.6);
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        background-color: rgb(31, 41, 55);
        padding: 8px;
        border-radius: 12px;
        border: 1px solid rgb(55, 65, 81);
        margin-bottom: 24px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        background-color: rgba(55, 65, 81, 0.5);
        border-radius: 10px;
        color: rgb(203, 213, 225);
        font-weight: 700;
        font-size: {int(15 * font_scale)}px;
        padding: 0 24px;
        border: 1px solid transparent;
        transition: all 0.2s ease;
        letter-spacing: 0.4px;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: rgb(55, 65, 81);
        color: rgb(229, 231, 235);
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, rgb(30, 58, 138) 0%, rgb(29, 78, 216) 100%);
        color: rgb(248, 250, 252) !important;
        border-color: rgba(59, 130, 246, 0.6);
        box-shadow: 0 3px 10px rgba(59, 130, 246, 0.4);
    }}
    
    .stButton button {{
        background: linear-gradient(135deg, rgb(30, 58, 138) 0%, rgb(29, 78, 216) 100%);
        color: rgb(243, 244, 246) !important;
        border: 1px solid rgba(59, 130, 246, 0.5);
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 700;
        font-size: {int(15 * font_scale)}px;
        transition: all 0.2s ease;
        letter-spacing: 0.4px;
    }}
    
    .stButton button:hover {{
        background: linear-gradient(135deg, rgb(37, 99, 235) 0%, rgb(59, 130, 246) 100%);
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.5);
        transform: translateY(-2px);
    }}
    
    .stDownloadButton button {{
        background: linear-gradient(135deg, rgb(5, 150, 105) 0%, rgb(16, 185, 129) 100%);
        color: rgb(243, 244, 246) !important;
        border: 1px solid rgba(16, 185, 129, 0.5);
        font-weight: 700;
        font-size: {int(15 * font_scale)}px;
        padding: 12px 24px;
    }}
    
    .stDownloadButton button:hover {{
        background: linear-gradient(135deg, rgb(16, 185, 129) 0%, rgb(52, 211, 153) 100%);
        box-shadow: 0 5px 15px rgba(16, 185, 129, 0.5);
    }}
    
    p, span, label {{ 
        color: {preset['text_color']} !important;
        font-size: {int(preset['body_text'] * font_scale)}px;
        font-weight: 500;
        line-height: 1.7;
    }}
    
    .stMarkdown h3 {{
        color: rgb(147, 197, 253) !important;
        font-weight: 800;
        font-size: {int(preset['h3_size'] * 1.1 * font_scale)}px !important;
        margin-top: 24px;
        margin-bottom: 20px;
        padding-left: 16px;
        border-left: 5px solid rgb(59, 130, 246);
        letter-spacing: -0.5px;
    }}
    
    .stMarkdown h4 {{
        color: rgb(203, 213, 225) !important;
        font-weight: 700;
        font-size: {int(20 * font_scale)}px !important;
        margin-bottom: 14px;
        letter-spacing: -0.3px;
    }}
    
    [data-testid="stDataFrame"] {{
        border: 1px solid rgb(55, 65, 81);
        border-radius: 10px;
    }}
    
    [data-testid="stDataFrame"] table {{
        background-color: rgb(31, 41, 55) !important;
    }}
    
    [data-testid="stDataFrame"] th {{
        background-color: rgb(30, 58, 138) !important;
        color: rgb(248, 250, 252) !important;
        font-weight: 700 !important;
        font-size: {int(15 * font_scale)}px !important;
        padding: 14px !important;
    }}
    
    [data-testid="stDataFrame"] td {{
        color: {preset['text_bright']} !important;
        background-color: rgb(31, 41, 55) !important;
        font-size: {int(15 * font_scale)}px !important;
        padding: 12px !important;
    }}
    
    [data-testid="stDataFrame"] tr:hover {{
        background-color: rgb(55, 65, 81) !important;
    }}
    
    .stAlert {{
        background-color: rgba(30, 58, 138, 0.25);
        border-radius: 10px;
        border-left: 5px solid rgb(59, 130, 246);
        color: {preset['text_bright']} !important;
        font-weight: 500;
        font-size: {int(preset['body_text'] * font_scale)}px;
        padding: 16px 20px;
    }}
    
    hr {{
        border-color: rgb(55, 65, 81);
        margin: 35px 0;
    }}
    
    .stSuccess {{
        background-color: rgba(5, 150, 105, 0.2);
        border-left-color: rgb(16, 185, 129);
        color: rgb(240, 253, 244) !important;
        font-size: {int(preset['body_text'] * font_scale)}px;
    }}
    
    .stWarning {{
        background-color: rgba(217, 119, 6, 0.2);
        border-left-color: rgb(251, 146, 60);
        color: rgb(254, 252, 232) !important;
        font-size: {int(preset['body_text'] * font_scale)}px;
    }}
    
    .stError {{
        background-color: rgba(220, 38, 38, 0.2);
        border-left-color: rgb(239, 68, 68);
        color: rgb(254, 242, 242) !important;
        font-size: {int(preset['body_text'] * font_scale)}px;
    }}
    
    .stInfo {{
        background-color: rgba(30, 58, 138, 0.2);
        border-left-color: rgb(59, 130, 246);
        color: rgb(239, 246, 255) !important;
        font-size: {int(preset['body_text'] * font_scale)}px;
    }}
    
    @media (max-width: 768px) {{
        h1 {{ font-size: {int(preset['h1_size'] * 0.75 * font_scale)}px !important; }}
        h2 {{ font-size: {int(preset['h2_size'] * 0.8 * font_scale)}px !important; }}
        h3 {{ font-size: {int(preset['h3_size'] * 0.85 * font_scale)}px !important; }}
        [data-testid="stMetricValue"] {{ font-size: {int(preset['metric_value'] * 0.7 * font_scale)}px !important; }}
        div[data-testid="metric-container"] {{ padding: {int(preset['metric_padding'] * 0.7)}px !important; margin-bottom: 14px; }}
        .stButton button {{ width: 100%; font-size: {int(15 * font_scale)}px !important; }}
        p, span, label {{ font-size: {int(preset['body_text'] * 0.9 * font_scale)}px; }}
    }}
    </style>
"""

# Apply Dynamic CSS
st.markdown(generate_css(), unsafe_allow_html=True)

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
st.markdown(f"""
    <div style='text-align:center; padding: 50px 0 40px 0; background: linear-gradient(135deg, rgba(31, 41, 55, 0.8) 0%, rgba(17, 24, 39, 0.9) 100%); border-radius: 18px; margin-bottom: 35px; border: 1px solid rgb(55, 65, 81);'>
        <h1 style='font-size: {int(56 * font_scale)}px; margin-bottom: 14px; color: {preset['text_bright']}; font-weight: 800; letter-spacing: -1.2px;'>
            📊 Executive E-Commerce Dashboard
        </h1>
        <p style='font-size: {int(20 * font_scale)}px; color: rgb(203, 213, 225); font-weight: 600; letter-spacing: 1.5px;'>
            Real-Time Business Intelligence & Advanced Analytics
        </p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown(f"""
        <div style='text-align: center; padding: 24px 0 18px 0;'>
            <div style='font-size: 52px; margin-bottom: 12px;'>⚡</div>
            <h2 style='margin: 0; font-size: {int(24 * font_scale)}px; color: rgb(147, 197, 253); font-weight: 800; letter-spacing: 0.6px;'>
                Control Center
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    # THEME CUSTOMIZATION
    with st.expander("🎨 THEME CUSTOMIZATION", expanded=False):
        st.markdown("**Visual Preset**")
        theme_preset = st.selectbox(
            "Choose a theme preset",
            list(THEME_PRESETS.keys()),
            index=list(THEME_PRESETS.keys()).index(st.session_state.theme_preset),
            key="theme_selector",
            label_visibility="collapsed"
        )
        
        if theme_preset != st.session_state.theme_preset:
            st.session_state.theme_preset = theme_preset
            st.rerun()
        
        st.markdown("**Font Size Scaling**")
        font_scale_new = st.slider(
            "Adjust font sizes",
            0.7, 1.5, st.session_state.font_scale, 0.05,
            help="Scale all text sizes proportionally",
            label_visibility="collapsed"
        )
        
        if abs(font_scale_new - st.session_state.font_scale) > 0.01:
            st.session_state.font_scale = font_scale_new
            st.rerun()
        
        st.markdown("**Color Palette**")
        color_palette = st.selectbox(
            "Choose color palette",
            list(COLOR_PALETTES.keys()),
            index=list(COLOR_PALETTES.keys()).index(st.session_state.color_palette),
            key="palette_selector",
            help="Colorblind-friendly options available",
            label_visibility="collapsed"
        )
        
        if color_palette != st.session_state.color_palette:
            st.session_state.color_palette = color_palette
            st.rerun()
        
        # Theme Info
        st.markdown("---")
        st.info(f"""
        **Current Settings:**
        - Preset: {st.session_state.theme_preset}
        - Scale: {st.session_state.font_scale:.0%}
        - Palette: {st.session_state.color_palette}
        """)
        
        # Reset Button
        if st.button("🔄 Reset to Defaults", use_container_width=True):
            st.session_state.theme_preset = "Enhanced (Default)"
            st.session_state.font_scale = 1.0
            st.session_state.color_palette = "Default"
            st.rerun()
    
    # DATE RANGE FILTER
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
    
    # GEOGRAPHIC FILTER
    with st.expander("🌍 GEOGRAPHIC FILTER", expanded=True):
        countries = sorted(df['country'].dropna().unique())
        select_all = st.checkbox("✅ Select All Countries", value=True)
        
        if select_all:
            selected_countries = countries
        else:
            selected_countries = st.multiselect("Choose Countries", countries, default=countries[:3])
    
    # DISPLAY SETTINGS
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

# Export Visual Style Guide
    with st.expander("📄 EXPORT STYLE GUIDE", expanded=False):
        if st.button("📥 Generate Style Guide", use_container_width=True):
            current_colors = COLOR_PALETTES[st.session_state.color_palette]
            style_guide_html = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: 'Inter', sans-serif; margin: 40px; background: #f5f5f5; }}
                    .header {{ background: linear-gradient(135deg, #1e3a8a, #1d4ed8); color: white; padding: 30px; border-radius: 10px; text-align: center; }}
                    .section {{ background: white; padding: 25px; margin: 20px 0; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
                    .color-box {{ display: inline-block; width: 120px; height: 120px; margin: 10px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }}
                    .font-sample {{ margin: 15px 0; padding: 15px; background: #f9fafb; border-left: 4px solid #3b82f6; }}
                    h2 {{ color: #1e3a8a; border-bottom: 3px solid #60a5fa; padding-bottom: 10px; }}
                    table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
                    th {{ background: #1e3a8a; color: white; padding: 12px; text-align: left; }}
                    td {{ padding: 10px; border-bottom: 1px solid #e5e7eb; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>📊 E-Commerce Dashboard Style Guide</h1>
                    <p>Visual Design System Documentation</p>
                    <p>Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}</p>
                </div>
                
                <div class="section">
                    <h2>🎨 Current Theme Configuration</h2>
                    <table>
                        <tr><th>Property</th><th>Value</th></tr>
                        <tr><td>Theme Preset</td><td><strong>{st.session_state.theme_preset}</strong></td></tr>
                        <tr><td>Font Scale</td><td>{st.session_state.font_scale:.0%}</td></tr>
                        <tr><td>Color Palette</td><td>{st.session_state.color_palette}</td></tr>
                    </table>
                </div>
                
                <div class="section">
                    <h2>📏 Typography Scale (Active Configuration)</h2>
                    <p style="background: #fef3c7; padding: 12px; border-radius: 6px; border-left: 4px solid #f59e0b; margin-bottom: 20px;">
                        <strong>Note:</strong> All sizes shown reflect the current font scaling of <strong>{font_scale:.0%}</strong>. 
                        Base preset sizes are multiplied by this scale factor to produce the final rendered sizes.
                    </p>
                    <div class="font-sample">
                        <p style="font-size: {int(preset['h1_size'] * font_scale)}px; font-weight: 800; margin: 10px 0;">H1 Heading - {int(preset['h1_size'] * font_scale)}px</p>
                    </div>
                    <div class="font-sample">
                        <p style="font-size: {int(preset['h2_size'] * font_scale)}px; font-weight: 700; margin: 10px 0;">H2 Heading - {int(preset['h2_size'] * font_scale)}px</p>
                    </div>
                    <div class="font-sample">
                        <p style="font-size: {int(preset['h3_size'] * font_scale)}px; font-weight: 700; margin: 10px 0;">H3 Heading - {int(preset['h3_size'] * font_scale)}px</p>
                    </div>
                    <div class="font-sample">
                        <p style="font-size: {int(preset['body_text'] * font_scale)}px; font-weight: 500; margin: 10px 0;">Body Text - {int(preset['body_text'] * font_scale)}px</p>
                    </div>
                    
                    <h3>Metric Typography</h3>
                    <table>
                        <tr><th>Element</th><th>Base Size</th><th>Scaled Size</th><th>Weight</th></tr>
                        <tr><td>Metric Value</td><td>{preset['metric_value']}px</td><td>{int(preset['metric_value'] * font_scale)}px</td><td>800</td></tr>
                        <tr><td>Metric Label</td><td>{preset['metric_label']}px</td><td>{int(preset['metric_label'] * font_scale)}px</td><td>700</td></tr>
                        <tr><td>Metric Delta</td><td>{preset['metric_delta']}px</td><td>{int(preset['metric_delta'] * font_scale)}px</td><td>700</td></tr>
                    </table>
                </div>
                
                <div class="section">
                    <h2>🎨 Color Palette - {st.session_state.color_palette}</h2>
                    <div style="text-align: center;">
                        {''.join([f'<div class="color-box" style="background-color: {color};"><p style="text-align: center; padding-top: 45px; color: white; font-weight: 700; text-shadow: 0 1px 3px rgba(0,0,0,0.5);">{color}</p></div>' for color in current_colors])}
                    </div>
                    
                    <h3>Color Values</h3>
                    <table>
                        <tr><th>Color</th><th>RGB Value</th><th>Usage</th></tr>
                        {' '.join([f'<tr><td><div style="width: 30px; height: 30px; background-color: {color}; border-radius: 4px; display: inline-block;"></div></td><td>{color}</td><td>Chart {i+1}</td></tr>' for i, color in enumerate(current_colors)])}
                    </table>
                </div>
                
                <div class="section">
                    <h2>📦 Spacing & Layout</h2>
                    <table>
                        <tr><th>Property</th><th>Base Value</th><th>Scaled Value</th></tr>
                        <tr><td>Metric Card Padding</td><td>{preset['metric_padding']}px</td><td>{int(preset['metric_padding'])}px (static)</td></tr>
                        <tr><td>Section Margin</td><td>35px vertical</td><td>35px (static)</td></tr>
                        <tr><td>Border Radius (Cards)</td><td>14px</td><td>14px (static)</td></tr>
                        <tr><td>Border Radius (Buttons)</td><td>10px</td><td>10px (static)</td></tr>
                    </table>
                    <p style="font-size: 13px; color: #6b7280; margin-top: 10px;">
                        <em>Note: Spacing values are static and do not scale with font size adjustments. Only typography scales dynamically.</em>
                    </p>
                </div>
                
                <div class="section">
                    <h2>💡 Implementation Notes</h2>
                    <ul>
                        <li><strong>Font Family:</strong> Inter, Roboto, system fonts</li>
                        <li><strong>Font Smoothing:</strong> Antialiased for optimal rendering</li>
                        <li><strong>Responsive Design:</strong> Mobile breakpoint at 768px with automatic font scaling</li>
                        <li><strong>Accessibility:</strong> Colorblind-friendly palettes available (Deuteranopia, Protanopia, Tritanopia)</li>
                        <li><strong>Theme:</strong> Dark mode optimized with gradient backgrounds</li>
                        <li><strong>Dynamic Scaling:</strong> Font scaling ({font_scale:.0%}) is applied multiplicatively to all text elements</li>
                        <li><strong>Theme Presets:</strong> 4 presets available - Enhanced (Default), High Contrast, Extra Large Text, Compact View</li>
                        <li><strong>Chart Colors:</strong> Palette-driven with 5 colorblind-friendly options</li>
                    </ul>
                    
                    <h3 style="margin-top: 20px;">Scaling System</h3>
                    <p style="background: #eff6ff; padding: 15px; border-radius: 6px; border-left: 4px solid #3b82f6;">
                        The dashboard uses a two-tier scaling system:
                    </p>
                    <ol style="margin-left: 20px;">
                        <li><strong>Preset-Based Sizing:</strong> Each theme preset defines base font sizes for different elements (H1: {preset['h1_size']}px, Body: {preset['body_text']}px, etc.)</li>
                        <li><strong>User Scaling:</strong> The font scale slider ({font_scale:.0%}) multiplies all base sizes to produce final rendered sizes</li>
                        <li><strong>Final Size Formula:</strong> Rendered Size = Base Preset Size × Font Scale Factor</li>
                        <li><strong>Example:</strong> H1 at {font_scale:.0%} scale = {preset['h1_size']}px × {font_scale:.2f} = {int(preset['h1_size'] * font_scale)}px</li>
                    </ol>
                    
                    <h3 style="margin-top: 20px;">Design Handoff Guidelines</h3>
                    <ul style="margin-left: 20px;">
                        <li>Use scaled sizes (right column in typography table) for actual implementation</li>
                        <li>Maintain Inter font family throughout with specified weights</li>
                        <li>Apply selected color palette to all data visualizations</li>
                        <li>Preserve 35px vertical spacing between major sections</li>
                        <li>Keep dark gradient backgrounds for consistency</li>
                    </ul>
                </div>
                
                <div style="margin-top: 40px; text-align: center; color: #6b7280; border-top: 1px solid #d1d5db; padding-top: 20px;">
                    <p>Executive E-commerce Dashboard Style Guide</p>
                    <p>© 2025 - Visual Design System Documentation</p>
                </div>
            </body>
            </html>
            """
            
            st.download_button(
                "📥 Download Style Guide",
                style_guide_html,
                file_name=f"style_guide_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
                mime="text/html",
                use_container_width=True
            )
            st.success("✅ Style guide generated! Download to view.")

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

# Get active color palette
colors = COLOR_PALETTES[st.session_state.color_palette]

# Plotly Helper with Enhanced Typography and Tooltips
def style_fig(fig, title=""):
    theme = st.session_state.get('selected_theme', 'plotly_dark')
    
    is_light_theme = theme in ['plotly_white', 'seaborn', 'ggplot2']
    
    title_color = "rgb(31, 41, 55)" if is_light_theme else "rgb(243, 244, 246)"
    text_color = "rgb(55, 65, 81)" if is_light_theme else "rgb(229, 231, 235)"
    grid_color = "rgba(0, 0, 0, 0.15)" if is_light_theme else "rgba(75, 85, 99, 0.3)"
    paper_bg = "rgba(255, 255, 255, 0.95)" if is_light_theme else "rgba(0, 0, 0, 0)"
    plot_bg = "rgba(249, 250, 251, 1)" if is_light_theme else "rgba(31, 41, 55, 0.3)"
    
    fig.update_layout(
        title=dict(
            text=title, 
            font=dict(size=int(24 * font_scale), color=title_color, family="Inter", weight=700),
            x=0.5, 
            xanchor='center'
        ),
        font=dict(size=int(15 * font_scale), color=text_color, family="Inter", weight=500),
        margin=dict(l=60, r=60, t=80, b=60),
        template=theme,
        hovermode='x unified',
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        hoverlabel=dict(
            bgcolor="rgb(31, 41, 55)" if not is_light_theme else "white",
            font_size=int(16 * font_scale),
            font_family="Inter",
            font_color="white" if not is_light_theme else "rgb(31, 41, 55)",
            bordercolor="rgb(59, 130, 246)",
            align="left"
        ),
        legend=dict(
            font=dict(size=int(14 * font_scale), color=text_color),
            bgcolor="rgba(31, 41, 55, 0.8)" if not is_light_theme else "rgba(255, 255, 255, 0.8)",
            bordercolor="rgb(75, 85, 99)",
            borderwidth=1
        )
    )
    
    axis_config = dict(
        showgrid=True, 
        gridcolor=grid_color,
        title_font=dict(color=text_color, size=int(15 * font_scale), weight=600),
        tickfont=dict(color=text_color, size=int(13 * font_scale), weight=500),
        linecolor=grid_color
    )
    
    fig.update_xaxes(**axis_config)
    fig.update_yaxes(**axis_config)
    
    for trace in fig.data:
        if hasattr(trace, 'textfont'):
            trace.textfont.color = text_color
            trace.textfont.size = int(13 * font_scale)
        if hasattr(trace, 'marker') and hasattr(trace.marker, 'line'):
            trace.marker.line.width = 0.5
    
    return fig

def get_text_color():
    theme = st.session_state.get('selected_theme', 'plotly_dark')
    return "rgb(31, 41, 55)" if theme in ['plotly_white', 'seaborn', 'ggplot2'] else "rgb(229, 231, 235)"

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
            line=dict(color=colors[0], width=4),
            marker=dict(size=10, color=colors[0]),
            fill='tozeroy', fillcolor=f'rgba{colors[0][3:-1]}, 0.1)',
            textfont=dict(color=get_text_color(), size=int(13 * font_scale)),
            hovertemplate='<b>%{x|%B %Y}</b><br>Revenue: $%{y:,.2f}<extra></extra>'
        ))
        
        z = np.polyfit(range(len(monthly_revenue)), monthly_revenue['total_price'], 1)
        p = np.poly1d(z)
        fig_trend.add_trace(go.Scatter(
            x=monthly_revenue['order_date'], y=p(range(len(monthly_revenue))),
            mode='lines', name='Trend',
            line=dict(color=colors[4], width=3, dash='dash'),
            hovertemplate='<b>Trend</b><br>$%{y:,.2f}<extra></extra>'
        ))
        
        st.plotly_chart(style_fig(fig_trend, "Monthly Performance"), use_container_width=True)
    
    with col2:
        st.markdown("### 🏆 TOP COUNTRIES")
        country_revenue = df_filtered.groupby('country')['total_price'].sum().nlargest(5).reset_index()
        
        fig_pie = px.pie(country_revenue, values='total_price', names='country', hole=0.45, color_discrete_sequence=colors)
        fig_pie.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            textfont=dict(size=int(14 * font_scale), color='white', weight=700),
            hovertemplate='<b>%{label}</b><br>Revenue: $%{value:,.2f}<br>Share: %{percent}<extra></extra>'
        )
        fig_pie.update_layout(
            paper_bgcolor='rgba(0, 0, 0, 0)', 
            showlegend=True,
            legend=dict(font=dict(color=get_text_color(), size=int(14 * font_scale)))
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("---")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("### 📅 DAILY TREND")
        daily_revenue = df_filtered.groupby('order_date')['total_price'].sum().reset_index()
        
        fig_daily = go.Figure()
        fig_daily.add_trace(go.Scatter(
            x=daily_revenue['order_date'], y=daily_revenue['total_price'],
            mode='lines', name='Daily Revenue',
            line=dict(color=colors[1], width=2.5),
            fill='tozeroy', fillcolor=f'rgba{colors[1][3:-1]}, 0.15)',
            hovertemplate='<b>%{x|%B %d, %Y}</b><br>Revenue: $%{y:,.2f}<extra></extra>'
        ))
        
        st.plotly_chart(style_fig(fig_daily, "Daily Revenue Trend"), use_container_width=True)
    
    with col4:
        st.markdown("### 📊 DAY OF WEEK")
        dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_revenue = df_filtered.groupby('day_of_week')['total_price'].sum().reindex(dow_order).reset_index()
        
        fig_dow = px.bar(dow_revenue, x='day_of_week', y='total_price', color_discrete_sequence=[colors[2]])
        fig_dow.update_traces(
            text=[f"${v:,.0f}" for v in dow_revenue['total_price']], 
            textposition='outside',
            textfont=dict(color=get_text_color(), size=int(13 * font_scale), weight=600),
            hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>'
        )
        
        st.plotly_chart(style_fig(fig_dow, "Revenue by Day"), use_container_width=True)

# TAB 2: Customers
with tab2:
    st.markdown("### 👥 CUSTOMER INSIGHTS")
    
    top_customers = df_filtered.groupby('customer_id').agg({
        'total_price': 'sum',
        'order_id': 'nunique',
        'quantity': 'sum'
    }).reset_index()
    top_customers.columns = ['customer_id', 'total_revenue', 'order_count', 'total_quantity']
    top_customers = top_customers.sort_values('total_revenue', ascending=False)
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.markdown("#### 🏆 Top Performers")
        for idx, row in top_customers.head(10).iterrows():
            st.metric(
                f"Customer {row['customer_id']}", 
                f"${row['total_revenue']:,.0f}",
                f"{row['order_count']} orders"
            )
    
    with c2:
        st.markdown("#### 📊 Customer Revenue Distribution")
        fig_cust = px.bar(
            top_customers.head(top_n), 
            x='customer_id', 
            y='total_revenue',
            color='order_count',
            color_continuous_scale='blues'
        )
        fig_cust.update_traces(
            text=[f"${v:,.0f}" for v in top_customers.head(top_n)['total_revenue']], 
            textposition='outside',
            textfont=dict(color=get_text_color(), size=int(13 * font_scale), weight=600),
            hovertemplate='<b>Customer %{x}</b><br>Revenue: $%{y:,.2f}<br>Orders: %{marker.color}<extra></extra>'
        )
        st.plotly_chart(style_fig(fig_cust, f"Top {top_n} Customers"), use_container_width=True)
    
    st.markdown("---")
    
    col_rfm1, col_rfm2 = st.columns(2)
    
    with col_rfm1:
        st.markdown("#### 🎯 RFM SEGMENTATION")
        
        current_date = df_filtered['order_date'].max()
        rfm = df_filtered.groupby('customer_id').agg({
            'order_date': lambda x: (current_date - x.max()).days,
            'order_id': 'nunique',
            'total_price': 'sum'
        }).reset_index()
        rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']
        
        rfm['R_score'] = pd.qcut(rfm['recency'], 4, labels=[4, 3, 2, 1], duplicates='drop')
        rfm['F_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4], duplicates='drop')
        rfm['M_score'] = pd.qcut(rfm['monetary'], 4, labels=[1, 2, 3, 4], duplicates='drop')
        
        rfm['RFM_score'] = rfm['R_score'].astype(str) + rfm['F_score'].astype(str) + rfm['M_score'].astype(str)
        
        def segment_customer(score):
            r, f, m = int(score[0]), int(score[1]), int(score[2])
            if r >= 3 and f >= 3 and m >= 3:
                return 'Champions'
            elif r >= 3 and f >= 2:
                return 'Loyal'
            elif r >= 3:
                return 'Potential'
            elif f >= 3 and m >= 3:
                return 'At Risk'
            else:
                return 'Lost'
        
        rfm['segment'] = rfm['RFM_score'].apply(segment_customer)
        
        segment_counts = rfm['segment'].value_counts().reset_index()
        segment_counts.columns = ['segment', 'count']
        
        fig_seg = px.pie(
            segment_counts, 
            values='count', 
            names='segment', 
            hole=0.5,
            color_discrete_sequence=colors
        )
        fig_seg.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            textfont=dict(size=int(14 * font_scale), color='white', weight=700),
            hovertemplate='<b>%{label}</b><br>Customers: %{value}<br>Share: %{percent}<extra></extra>'
        )
        fig_seg.update_layout(
            paper_bgcolor='rgba(0, 0, 0, 0)',
            showlegend=True,
            legend=dict(font=dict(color=get_text_color(), size=int(14 * font_scale)))
        )
        st.plotly_chart(fig_seg, use_container_width=True)
    
    with col_rfm2:
        st.markdown("#### 📊 Segment Metrics")
        
        segment_metrics = rfm.groupby('segment').agg({
            'customer_id': 'count',
            'monetary': 'mean',
            'frequency': 'mean',
            'recency': 'mean'
        }).reset_index()
        segment_metrics.columns = ['Segment', 'Customers', 'Avg Revenue', 'Avg Orders', 'Avg Recency']
        segment_metrics = segment_metrics.sort_values('Avg Revenue', ascending=False)
        
        st.dataframe(
            segment_metrics.style.format({
                'Customers': '{:,.0f}',
                'Avg Revenue': '${:,.2f}',
                'Avg Orders': '{:.1f}',
                'Avg Recency': '{:.0f} days'
            }),
            use_container_width=True,
            height=300
        )

# TAB 3: Products
with tab3:
    st.markdown("### 📦 PRODUCT PERFORMANCE")
    
    top_prod = df_filtered.groupby('product_name').agg({
        'total_price': 'sum',
        'quantity': 'sum',
        'order_id': 'nunique'
    }).reset_index()
    top_prod = top_prod.sort_values('total_price', ascending=False)
    
    col_p1, col_p2 = st.columns([2, 1])
    
    with col_p1:
        st.markdown("#### 🏆 Top Products by Revenue")
        fig_prod = px.bar(
            top_prod.head(top_n), 
            x='total_price', 
            y='product_name',
            orientation='h',
            color='quantity',
            color_continuous_scale='viridis'
        )
        fig_prod.update_traces(
            text=[f"${v:,.0f}" for v in top_prod.head(top_n)['total_price']], 
            textposition='outside',
            textfont=dict(color=get_text_color(), size=int(13 * font_scale), weight=600),
            hovertemplate='<b>%{y}</b><br>Revenue: $%{x:,.2f}<br>Units: %{marker.color}<extra></extra>'
        )
        st.plotly_chart(style_fig(fig_prod, f"Top {top_n} Products"), use_container_width=True)
    
    with col_p2:
        st.markdown("#### 📊 Product Stats")
        for idx, row in top_prod.head(10).iterrows():
            st.metric(
                row['product_name'][:20], 
                f"${row['total_price']:,.0f}",
                f"{row['quantity']:,.0f} units"
            )
    
    st.markdown("---")
    
    col_p3, col_p4 = st.columns(2)
    
    with col_p3:
        st.markdown("#### 📈 Revenue Distribution")
        fig_prod_dist = px.histogram(
            df_filtered, 
            x='total_price', 
            nbins=30,
            color_discrete_sequence=[colors[0]]
        )
        fig_prod_dist.update_traces(
            hovertemplate='<b>Order Value: $%{x:.2f}</b><br>Count: %{y}<extra></extra>'
        )
        st.plotly_chart(style_fig(fig_prod_dist, "Order Value Distribution"), use_container_width=True)
    
    with col_p4:
        st.markdown("#### 🎯 Pareto Analysis")
        
        prod_pareto = top_prod.copy()
        prod_pareto['cumulative_revenue'] = prod_pareto['total_price'].cumsum()
        prod_pareto['cumulative_pct'] = (prod_pareto['cumulative_revenue'] / prod_pareto['total_price'].sum()) * 100
        prod_pareto = prod_pareto.head(top_n)
        
        fig_pareto = go.Figure()
        fig_pareto.add_trace(go.Bar(
            x=list(range(1, len(prod_pareto) + 1)),
            y=prod_pareto['total_price'],
            name='Revenue',
            marker=dict(color=colors[1]),
            yaxis='y',
            hovertemplate='<b>Product #%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>'
        ))
        fig_pareto.add_trace(go.Scatter(
            x=list(range(1, len(prod_pareto) + 1)),
            y=prod_pareto['cumulative_pct'],
            name='Cumulative %',
            line=dict(color=colors[4], width=3),
            marker=dict(size=8),
            yaxis='y2',
            hovertemplate='<b>Top %{x} Products</b><br>Cumulative: %{y:.1f}%<extra></extra>'
        ))
        
        fig_pareto.update_layout(
            yaxis=dict(title='Revenue', side='left'),
            yaxis2=dict(title='Cumulative %', overlaying='y', side='right', range=[0, 100])
        )
        
        st.plotly_chart(style_fig(fig_pareto, "80/20 Product Analysis"), use_container_width=True)

# TAB 4: Geography
with tab4:
    st.markdown("### 🌍 GEOGRAPHIC ANALYSIS")
    
    country_analysis = df_filtered.groupby('country').agg({
        'total_price': 'sum',
        'order_id': 'nunique',
        'customer_id': 'nunique',
        'quantity': 'sum'
    }).reset_index()
    country_analysis.columns = ['country', 'revenue', 'orders', 'customers', 'quantity']
    country_analysis = country_analysis.sort_values('revenue', ascending=False)
    
    col_g1, col_g2 = st.columns([2, 1])
    
    with col_g1:
        st.markdown("#### 🗺️ Revenue by Country")
        fig_geo = px.bar(
            country_analysis.head(top_n), 
            x='country', 
            y='revenue',
            color='customers',
            color_continuous_scale='turbo'
        )
        fig_geo.update_traces(
            text=[f"${v:,.0f}" for v in country_analysis.head(top_n)['revenue']], 
            textposition='outside',
            textfont=dict(color=get_text_color(), size=int(13 * font_scale), weight=600),
            hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.2f}<br>Customers: %{marker.color}<extra></extra>'
        )
        st.plotly_chart(style_fig(fig_geo, f"Top {top_n} Countries"), use_container_width=True)
    
    with col_g2:
        st.markdown("#### 📊 Country Metrics")
        for idx, row in country_analysis.head(10).iterrows():
            st.metric(
                row['country'], 
                f"${row['revenue']:,.0f}",
                f"{row['customers']:,.0f} customers"
            )
    
    st.markdown("---")
    st.markdown("#### 📋 Detailed Country Table")
    st.dataframe(
        country_analysis.style.format({
            'revenue': '${:,.0f}',
            'orders': '{:,.0f}',
            'customers': '{:,.0f}',
            'quantity': '{:,.0f}'
        }),
        use_container_width=True,
        height=400
    )

# TAB 5: Advanced
with tab5:
    adv_tab1, adv_tab2, adv_tab3, adv_tab4 = st.tabs(["🔔 ALERTS", "📈 FORECAST", "📊 YoY", "📄 REPORT"])
    
    # SMART ALERTS
    with adv_tab1:
        st.markdown("### 🔔 SMART BUSINESS ALERTS")
        
        st.markdown("#### 🎯 Revenue Alerts")
        
        revenue_trend = df_filtered.groupby(df_filtered['order_date'].dt.to_period('M'))['total_price'].sum()
        if len(revenue_trend) >= 2:
            last_month = revenue_trend.iloc[-1]
            prev_month = revenue_trend.iloc[-2]
            mom_change = ((last_month - prev_month) / prev_month * 100) if prev_month > 0 else 0
            
            if mom_change < -10:
                st.error(f"🚨 Revenue down {abs(mom_change):.1f}% from last month!")
            elif mom_change < 0:
                st.warning(f"⚠️ Revenue down {abs(mom_change):.1f}% from last month")
            else:
                st.success(f"✅ Revenue up {mom_change:.1f}% from last month")
        
        st.markdown("#### 👥 Customer Alerts")
        
        aov_threshold = df['total_price'].sum() / df['order_id'].nunique()
        if metrics['avg_order_value'] < aov_threshold * 0.8:
            st.warning(f"⚠️ AOV below average: ${metrics['avg_order_value']:.2f} vs ${aov_threshold:.2f}")
        else:
            st.success(f"✅ AOV healthy: ${metrics['avg_order_value']:.2f}")
        
        top_5_revenue = top_customers.head(5)['total_revenue'].sum()
        total_revenue = top_customers['total_revenue'].sum()
        top_5_revenue_pct = (top_5_revenue / total_revenue * 100) if total_revenue > 0 else 0
        
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
                    line=dict(color=colors[0], width=4),
                    marker=dict(size=10),
                    hovertemplate='<b>%{x|%B %Y}</b><br>Revenue: $%{y:,.2f}<extra></extra>'
                ))
                
                fore = forecast_df[forecast_df['type'] == 'Forecast']
                fig_forecast.add_trace(go.Scatter(
                    x=fore['date'], y=fore['revenue'],
                    mode='lines+markers', name='Forecast',
                    line=dict(color=colors[3], width=4, dash='dash'),
                    marker=dict(size=10),
                    hovertemplate='<b>%{x|%B %Y}</b><br>Forecast: $%{y:,.2f}<extra></extra>'
                ))
                
                std_dev = monthly_data['total_price'].std()
                fig_forecast.add_trace(go.Scatter(
                    x=fore['date'].tolist() + fore['date'].tolist()[::-1],
                    y=(fore['revenue'] + std_dev).tolist() + (fore['revenue'] - std_dev).tolist()[::-1],
                    fill='toself',
                    fillcolor=f'rgba{colors[3][3:-1]}, 0.2)',
                    line=dict(color='rgba(255,255,255,0)'),
                    name='Confidence Interval',
                    hovertemplate='<b>Confidence Range</b><extra></extra>'
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
                marker=dict(color=colors[0]),
                text=[f"${v:,.0f}" for v in m_y1['revenue']], 
                textposition='outside',
                textfont=dict(color=get_text_color(), size=int(13 * font_scale), weight=700),
                hovertemplate=f'<b>%{{x}} {year1}</b><br>Revenue: $%{{y:,.2f}}<extra></extra>'
            ))
            fig_yoy.add_trace(go.Bar(
                x=m_y2['month_name'], y=m_y2['revenue'], name=str(year2),
                marker=dict(color=colors[1]),
                text=[f"${v:,.0f}" for v in m_y2['revenue']], 
                textposition='outside',
                textfont=dict(color=get_text_color(), size=int(13 * font_scale), weight=700),
                hovertemplate=f'<b>%{{x}} {year2}</b><br>Revenue: $%{{y:,.2f}}<extra></extra>'
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
        
        if st.button("📄 GENERATE REPORT", use_container_width=True, type="primary"):
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
    <div style='text-align: center; padding: 35px; background: linear-gradient(135deg, rgba(31, 41, 55, 0.6) 0%, rgba(17, 24, 39, 0.8) 100%); border-radius: 14px; border: 1px solid rgb(55, 65, 81);'>
        <div style='font-size: 42px; margin-bottom: 14px;'>⚡</div>
        <h3 style='color: {preset['text_bright']}; margin: 12px 0; font-size: {int(26 * font_scale)}px; font-weight: 800; letter-spacing: -0.6px;'>Executive Dashboard v4.0</h3>
        <p style='color: rgb(203, 213, 225); font-size: {int(16 * font_scale)}px; margin: 12px 0; font-weight: 600;'>Built with Streamlit, Plotly & Machine Learning</p>
        <div style='display: flex; justify-content: center; gap: 14px; margin: 24px 0; flex-wrap: wrap;'>
            <span style='background: rgba(96, 165, 250, 0.25); padding: 8px 16px; border-radius: 22px; font-size: {int(13 * font_scale)}px; color: rgb(191, 219, 254); font-weight: 700; border: 1px solid rgba(96, 165, 250, 0.4);'>🎨 Theme Presets</span>
            <span style='background: rgba(129, 140, 248, 0.25); padding: 8px 16px; border-radius: 22px; font-size: {int(13 * font_scale)}px; color: rgb(199, 210, 254); font-weight: 700; border: 1px solid rgba(129, 140, 248, 0.4);'>📏 Font Scaling</span>
            <span style='background: rgba(251, 146, 60, 0.25); padding: 8px 16px; border-radius: 22px; font-size: {int(13 * font_scale)}px; color: rgb(254, 215, 170); font-weight: 700; border: 1px solid rgba(251, 146, 60, 0.4);'>♿ Accessibility</span>
            <span style='background: rgba(16, 185, 129, 0.25); padding: 8px 16px; border-radius: 22px; font-size: {int(13 * font_scale)}px; color: rgb(167, 243, 208); font-weight: 700; border: 1px solid rgba(16, 185, 129, 0.4);'>📄 Style Guide</span>
            <span style='background: rgba(236, 72, 153, 0.25); padding: 8px 16px; border-radius: 22px; font-size: {int(13 * font_scale)}px; color: rgb(249, 168, 212); font-weight: 700; border: 1px solid rgba(236, 72, 153, 0.4);'>💡 Smart Tooltips</span>
        </div>
        <p style='color: rgb(156, 163, 175); font-size: {int(13 * font_scale)}px; margin: 14px 0; font-weight: 600;'>📅 Last Updated: {datetime.now().strftime('%B %d, %Y - %H:%M')}</p>
        <div style='margin-top: 20px; padding-top: 20px; border-top: 1px solid rgb(55, 65, 81);'>
            <p style='color: rgb(203, 213, 225); font-size: {int(12 * font_scale)}px; margin: 0; font-weight: 600;'>💼 Data Analytics & Business Intelligence Portfolio</p>
            <p style='color: rgb(156, 163, 175); font-size: {int(11 * font_scale)}px; margin: 10px 0 0 0; font-weight: 500;'>🎯 RFM Segmentation • Pareto Analysis • Predictive Analytics • Interactive Visualizations • Customizable Themes</p>
        </div>
    </div>
""", unsafe_allow_html=True)
