import streamlit as st
import plotly.graph_objects as go

# ==============================
#  COLOR PALETTE CONSTANTS
# ==============================
COLORS = {
    # Backgrounds
    'bg_primary': '#0F172A',      # slate-900
    'bg_secondary': '#1E293B',    # slate-800
    'bg_tertiary': '#334155',     # slate-700

    # Accent colors
    'primary': '#3B82F6',         # blue-500
    'primary_light': '#60A5FA',   # blue-400
    'success': '#10B981',         # emerald-500
    'warning': '#F59E0B',         # amber-500
    'danger': '#EF4444',          # red-500
    'info': '#06B6D4',            # cyan-500
    'purple': '#8B5CF6',          # violet-500

    # Text (improved contrast and hierarchy)
    'text_primary': '#E2E8F0',    # brighter for main titles
    'text_secondary': '#CBD5E1',  # medium contrast
    'text_tertiary': '#94A3B8',   # subtle details

    # Borders
    'border_subtle': 'rgba(59, 130, 246, 0.1)',
    'border_medium': 'rgba(59, 130, 246, 0.15)',
    'border_strong': 'rgba(59, 130, 246, 0.3)',
}

# ==============================
#  GLOBAL CSS STYLES
# ==============================
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

/* Hide Streamlit branding */
#MainMenu, footer, header {visibility: hidden;}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%);
    border-right: 1px solid rgba(59, 130, 246, 0.1);
    color: #CBD5E1 !important;
}

/* ===== TEXT COLOR IMPROVEMENTS ===== */

/* Dashboard Titles */
.dashboard-title, .section-header, h1, h2, h3 {
    color: #F1F5F9 !important; /* brighter white-blue tone */
    font-weight: 700;
    letter-spacing: -0.02em;
}

/* Subtitles and secondary text */
.dashboard-subtitle, .breadcrumb, h4, h5, h6, label, p, span {
    color: #CBD5E1 !important;
}

/* KPI cards */
.kpi-label {
    color: #A5B4FC !important; /* soft indigo tone */
    font-weight: 600;
    text-transform: uppercase;
}

.kpi-value {
    color: #F8FAFC !important;
    font-weight: 800;
}

.kpi-change.positive { color: #10B981 !important; }
.kpi-change.negative { color: #EF4444 !important; }

/* Section headers */
.section-header {
    border-bottom: 2px solid rgba(59, 130, 246, 0.3);
}

/* Buttons and tabs */
.stButton > button {
    color: #F8FAFC !important;
}

/* Table text */
.dataframe thead tr th {
    color: #E2E8F0 !important;
}
.dataframe tbody tr {
    color: #F1F5F9 !important;
}

/* Input labels */
.stSelectbox label, .stMultiSelect label, .stDateInput label {
    color: #CBD5E1 !important;
}

/* Tooltip and info boxes */
.stAlert {
    color: #E2E8F0 !important;
}
</style>
"""

# ==============================
#  APPLY THEME FUNCTION
# ==============================
def apply_theme():
    """Apply global dark theme to Streamlit app"""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ==============================
#  PLOTLY TEMPLATE
# ==============================
def get_plotly_template():
    """Return custom Plotly template with improved contrast"""
    template = go.layout.Template()

    template.layout = go.Layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            color=COLORS['text_primary'],
            family='Inter, sans-serif',
            size=13
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(148, 163, 184, 0.15)',
            zeroline=False,
            color=COLORS['text_secondary'],
            titlefont=dict(color=COLORS['text_primary']),
            tickfont=dict(color=COLORS['text_secondary'])
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(148, 163, 184, 0.15)',
            zeroline=False,
            color=COLORS['text_secondary'],
            titlefont=dict(color=COLORS['text_primary']),
            tickfont=dict(color=COLORS['text_secondary'])
        ),
        hovermode='closest',
        hoverlabel=dict(
            bgcolor='rgba(51,65,85,0.95)',
            bordercolor='rgba(59,130,246,0.3)',
            font=dict(color='#F8FAFC', family='Inter', size=12)
        ),
        legend=dict(
            bgcolor='rgba(17,24,39,0.8)',
            bordercolor='rgba(59,130,246,0.2)',
            borderwidth=1,
            font=dict(color=COLORS['text_primary'])
        ),
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return template

# ==============================
#  HEADER AND SECTION HELPERS
# ==============================
def create_header(title, subtitle=None, breadcrumb=None):
    """Create consistent dashboard header"""
    breadcrumb_html = f'<div class="breadcrumb">{breadcrumb}</div>' if breadcrumb else ""
    subtitle_html = f'<div class="dashboard-subtitle">{subtitle}</div>' if subtitle else ""
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

# ==============================
#  OTHER HELPERS (UNCHANGED)
# ==============================
def get_color_by_change(value, reverse=False):
    if value == 0:
        return 'neutral'
    if reverse:
        return 'negative' if value > 0 else 'positive'
    return 'positive' if value > 0 else 'negative'

def format_number(value, format_type='number', decimals=0):
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
