import streamlit as st
import plotly.graph_objects as go

# Color palette constants
COLORS = {
    # Backgrounds
    'bg_primary': '#0F172A',      # slate-900
    'bg_secondary': '#1E293B',    # slate-800
    'bg_tertiary': '#334155',     # slate-700
    
    # Surfaces
    'surface_dark': '#1E293B',
    'surface_light': '#334155',
    
    # Accent colors
    'primary': '#3B82F6',         # blue-500
    'primary_light': '#60A5FA',   # blue-400
    'success': '#10B981',         # emerald-500
    'warning': '#F59E0B',         # amber-500
    'danger': '#EF4444',          # red-500
    'info': '#06B6D4',            # cyan-500
    'purple': '#8B5CF6',          # violet-500
    
    # Text
    'text_primary': '#F8FAFC',    # slate-50
    'text_secondary': '#94A3B8',  # slate-400
    'text_tertiary': '#64748B',   # slate-500
    
    # Borders
    'border_subtle': 'rgba(59, 130, 246, 0.1)',
    'border_medium': 'rgba(59, 130, 246, 0.15)',
    'border_strong': 'rgba(59, 130, 246, 0.3)',
}

# Global CSS theme
GLOBAL_CSS = """
<style>
    /* Import Inter font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global reset */
    * {
        font-family: 'Inter', sans-serif;
        box-sizing: border-box;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main app background */
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%);
        border-right: 1px solid rgba(59, 130, 246, 0.1);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #94A3B8;
    }
    
    /* Dashboard header */
    .dashboard-header {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        border: 1px solid rgba(59, 130, 246, 0.1);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .breadcrumb {
        color: #94A3B8;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
        font-weight: 400;
    }
    
    .breadcrumb a {
        color: #60A5FA;
        text-decoration: none;
        transition: color 0.2s ease;
    }
    
    .breadcrumb a:hover {
        color: #3B82F6;
    }
    
    .dashboard-title {
        color: #F8FAFC;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .dashboard-subtitle {
        color: #94A3B8;
        font-size: 1rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid rgba(59, 130, 246, 0.15);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        height: 100%;
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.3);
        border-color: rgba(59, 130, 246, 0.3);
    }
    
    .kpi-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
        display: inline-block;
    }
    
    .kpi-label {
        color: #94A3B8;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .kpi-value {
        color: #F8FAFC;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
        display: block;
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
    
    .kpi-change.neutral {
        color: #94A3B8;
    }
    
    /* Chart containers */
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
    
    .chart-subtitle {
        color: #94A3B8;
        font-size: 0.9rem;
        margin-top: -0.5rem;
        margin-bottom: 1rem;
    }
    
    /* Section headers */
    .section-header {
        color: #F8FAFC;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 2rem 0 1.5rem 0;
        letter-spacing: -0.01em;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid rgba(59, 130, 246, 0.2);
    }
    
    /* Data tables */
    .dataframe {
        border: 1px solid rgba(59, 130, 246, 0.15) !important;
        border-radius: 8px !important;
    }
    
    .dataframe thead tr th {
        background: #1E293B !important;
        color: #F8FAFC !important;
        font-weight: 600 !important;
        border-bottom: 2px solid rgba(59, 130, 246, 0.3) !important;
    }
    
    .dataframe tbody tr {
        background: #334155 !important;
        color: #F8FAFC !important;
    }
    
    .dataframe tbody tr:hover {
        background: #475569 !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #F8FAFC;
        font-size: 2rem;
        font-weight: 700;
    }
    
    [data-testid="stMetricDelta"] {
        font-weight: 600;
    }
    
    /* Input widgets */
    .stSelectbox label, .stMultiSelect label, .stDateInput label {
        color: #94A3B8 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        color: #F8FAFC;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        border: 1px solid rgba(59, 130, 246, 0.15);
        border-radius: 8px;
        color: #F8FAFC !important;
        font-weight: 600;
    }
    
    /* Alerts/Info boxes */
    .stAlert {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        border-left: 4px solid #3B82F6;
        border-radius: 8px;
        color: #F8FAFC;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #3B82F6 !important;
    }
</style>
"""

def apply_theme():
    """Apply global dark theme to Streamlit app"""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

def get_plotly_template():
    """Return custom Plotly template with dark theme"""
    template = go.layout.Template()
    
    template.layout = go.Layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            color=COLORS['text_primary'],
            family='Inter, sans-serif',
            size=12
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(148, 163, 184, 0.1)',
            zeroline=False,
            color=COLORS['text_secondary']
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(148, 163, 184, 0.1)',
            zeroline=False,
            color=COLORS['text_secondary']
        ),
        hovermode='closest',
        hoverlabel=dict(
            bgcolor=COLORS['bg_tertiary'],
            font_size=12,
            font_family='Inter'
        ),
        margin=dict(l=40, r=40, t=40, b=40),
        legend=dict(
            bgcolor='rgba(30, 41, 59, 0.8)',
            bordercolor=COLORS['border_medium'],
            borderwidth=1,
            font=dict(color=COLORS['text_primary'])
        )
    )
    
    return template

def create_header(title, subtitle=None, breadcrumb=None):
    """Create consistent dashboard header
    
    Args:
        title: Main title text
        subtitle: Optional subtitle text
        breadcrumb: Optional breadcrumb navigation (e.g., "Home / Dashboard")
    """
    breadcrumb_html = ""
    if breadcrumb:
        breadcrumb_html = f'<div class="breadcrumb">{breadcrumb}</div>'
    
    subtitle_html = ""
    if subtitle:
        subtitle_html = f'<div class="dashboard-subtitle">{subtitle}</div>'
    
    header_html = f"""
    <div class="dashboard-header">
        {breadcrumb_html}
        <h1 class="dashboard-title">{title}</h1>
        {subtitle_html}
    </div>
    """
    
    st.markdown(header_html, unsafe_allow_html=True)

def create_section_header(title):
    """Create section divider with styled header"""
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)

def get_color_by_change(value, reverse=False):
    """Get color class based on value change
    
    Args:
        value: Numeric value (positive or negative)
        reverse: If True, negative values are good (e.g., cost reduction)
    
    Returns:
        String with color class ('positive', 'negative', or 'neutral')
    """
    if value == 0:
        return 'neutral'
    
    if reverse:
        return 'negative' if value > 0 else 'positive'
    
    return 'positive' if value > 0 else 'negative'

def format_number(value, format_type='number', decimals=0):
    """Format numbers consistently
    
    Args:
        value: Numeric value to format
        format_type: 'number', 'currency', 'percent', or 'compact'
        decimals: Number of decimal places
    
    Returns:
        Formatted string
    """
    if format_type == 'currency':
        return f"${value:,.{decimals}f}"
    elif format_type == 'percent':
        return f"{value:.{decimals}f}%"
    elif format_type == 'compact':
        if value >= 1_000_000:
            return f"${value/1_000_000:.1f}M"
        elif value >= 1_000:
            return f"${value/1_000:.1f}K"
        return f"${value:.0f}"
    else:
        return f"{value:,.{decimals}f}"
