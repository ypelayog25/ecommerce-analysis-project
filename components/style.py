import streamlit as st
import plotly.graph_objects as go

# ============================
# 🎨 Color Palette
# ============================
COLORS = {
    # Backgrounds
    'bg_primary': '#0F172A',
    'bg_secondary': '#1E293B',
    'bg_tertiary': '#334155',

    # Accents
    'primary': '#3B82F6',
    'primary_light': '#60A5FA',
    'success': '#10B981',
    'warning': '#F59E0B',
    'danger': '#EF4444',
    'info': '#06B6D4',
    'purple': '#8B5CF6',

    # Text
    'text_primary': '#FFFFFF',
    'text_secondary': '#F1F5F9',
    'text_tertiary': '#E2E8F0',

    # Borders
    'border_subtle': 'rgba(59,130,246,0.1)',
    'border_medium': 'rgba(59,130,246,0.15)',
    'border_strong': 'rgba(59,130,246,0.3)',
}

# ============================
# 💎 Global CSS Styling
# ============================
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; box-sizing: border-box; }

/* Hide Streamlit branding */
#MainMenu, footer, header {visibility: hidden;}

/* Background gradient */
.stApp {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%);
    border-right: 1px solid rgba(59,130,246,0.1);
    color: #E2E8F0 !important;
}

/* =========================
   TITLES & SECTIONS
   ========================= */
.dashboard-title, .section-header, h1, h2, h3 {
    color: #FFFFFF !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em;
    text-transform: uppercase;
}

h4, h5, h6, .dashboard-subtitle, .breadcrumb, label, p, span {
    color: #F1F5F9 !important;
}

/* Breadcrumb links */
.breadcrumb a {
    color: #60A5FA !important;
}
.breadcrumb a:hover {
    color: #93C5FD !important;
}

/* =========================
   KPI CARDS
   ========================= */
.kpi-card {
    background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
    border-radius: 12px;
    padding: 1.5rem;
    border: 1px solid rgba(59,130,246,0.15);
    box-shadow: 0 4px 6px rgba(0,0,0,0.25);
    transition: all 0.3s ease;
}
.kpi-card:hover {
    transform: translateY(-2px);
    border-color: rgba(59,130,246,0.3);
}

/* KPI labels and values */
.kpi-label {
    color: #E0E7FF !important;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.kpi-value {
    color: #FFFFFF !important;
    font-weight: 800;
    font-size: 2rem;
}

.kpi-change {
    font-size: 0.9rem;
    font-weight: 700 !important;
}
.kpi-change.positive { color: #10B981 !important; }
.kpi-change.negative { color: #EF4444 !important; }
.kpi-change.neutral { color: #F8FAFC !important; }

/* =========================
   BLUE CARDS / METRIC HIGHLIGHTS
   ========================= */
.metric-highlight,
.metric-positive,
.metric-negative,
.blue-card-text {
    color: #FFFFFF !important;
    font-weight: 700;
}

.metric-note,
.metric-subtext {
    color: #E2E8F0 !important;
    font-weight: 500;
}

/* Icons inside metric cards */
.metric-icon,
.kpi-icon {
    color: #F8FAFC !important;
    font-size: 1.5rem;
}

/* =========================
   PLOTLY CHARTS
   ========================= */
.plotly .xtick text,
.plotly .ytick text,
.plotly .legend text,
.plotly .axis-title {
    fill: #F8FAFC !important;
    font-weight: 600 !important;
}

.plotly .legend text {
    fill: #FFFFFF !important;
}

.plotly-tooltip, .hoverlayer text {
    color: #0F172A !important;
    background: rgba(255,255,255,0.96) !important;
    border: 1px solid #CBD5E1 !important;
}

/* =========================
   BUTTONS & INPUTS
   ========================= */
.stButton > button {
    background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
    color: #FFFFFF !important;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1.5rem;
    font-weight: 600;
    transition: all 0.3s ease;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
    box-shadow: 0 4px 8px rgba(59,130,246,0.3);
}

.stSelectbox label, .stMultiSelect label, .stDateInput label {
    color: #E2E8F0 !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
}

/* =========================
   TABLES
   ========================= */
.dataframe {
    border: 1px solid rgba(59,130,246,0.15) !important;
    border-radius: 8px !important;
}
.dataframe thead tr th {
    background: #1E293B !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    border-bottom: 2px solid rgba(59,130,246,0.3) !important;
}
.dataframe tbody tr {
    background: #334155 !important;
    color: #FFFFFF !important;
}
.dataframe tbody tr:hover {
    background: #475569 !important;
}

/* =========================
   ALERTS / INFO BOXES
   ========================= */
.stAlert {
    background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
    border-left: 4px solid #3B82F6;
    border-radius: 8px;
    color: #FFFFFF !important;
}

/* =========================
   SPINNER
   ========================= */
.stSpinner > div {
    border-top-color: #3B82F6 !important;
}
</style>
"""

# ============================
# ⚙️ Theme Functions
# ============================
def apply_theme():
    """Apply the global dark theme to Streamlit app"""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def get_plotly_template():
    """Custom Plotly dark template"""
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
            gridcolor='rgba(148,163,184,0.12)',
            zeroline=False,
            color=COLORS['text_secondary']
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(148,163,184,0.12)',
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
            bgcolor='rgba(30,41,59,0.85)',
            bordercolor=COLORS['border_medium'],
            borderwidth=1,
            font=dict(color=COLORS['text_primary'])
        )
    )
    return template


def create_header(title, subtitle=None, breadcrumb=None):
    """Create a consistent dashboard header"""
    breadcrumb_html = f'<div class="breadcrumb">{breadcrumb}</div>' if breadcrumb else ''
    subtitle_html = f'<div class="dashboard-subtitle">{subtitle}</div>' if subtitle else ''
    header_html = f"""
    <div class="dashboard-header">
        {breadcrumb_html}
        <h1 class="dashboard-title">{title}</h1>
        {subtitle_html}
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


def create_section_header(title):
    """Section divider with styled header"""
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)


def get_color_by_change(value, reverse=False):
    """Return color class based on value change"""
    if value == 0:
        return 'neutral'
    if reverse:
        return 'negative' if value > 0 else 'positive'
    return 'positive' if value > 0 else 'negative'


def format_number(value, format_type='number', decimals=0):
    """Uniform numeric formatting"""
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
