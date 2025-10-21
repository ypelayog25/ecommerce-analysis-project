import streamlit as st
import plotly.graph_objects as go

# ==============================
#  COLOR PALETTE CONSTANTS
# ==============================
COLORS = {
    # Backgrounds
    'bg_primary': '#0F172A',
    'bg_secondary': '#1E293B',
    'bg_tertiary': '#334155',

    # Accent colors
    'primary': '#3B82F6',
    'primary_light': '#60A5FA',
    'success': '#10B981',
    'warning': '#F59E0B',
    'danger': '#EF4444',
    'info': '#06B6D4',
    'purple': '#8B5CF6',

    # Text (improved)
    'text_primary': '#F1F5F9',     # Brighter main text
    'text_secondary': '#CBD5E1',   # Softer secondary
    'text_tertiary': '#94A3B8',    # Subtle details

    # Borders
    'border_subtle': 'rgba(59,130,246,0.1)',
    'border_medium': 'rgba(59,130,246,0.15)',
    'border_strong': 'rgba(59,130,246,0.3)',
}

# ==============================
#  GLOBAL CSS STYLES
# ==============================
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }

/* Hide Streamlit branding */
#MainMenu, footer, header {visibility: hidden;}

/* Main app background */
.stApp {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%);
    border-right: 1px solid rgba(59,130,246,0.1);
    color: #CBD5E1 !important;
}

/* ===============================
   TEXT IMPROVEMENTS (HIGH CONTRAST)
   =============================== */

/* Section Titles (KEY PERFORMANCE INDICATORS, REVENUE TREND, EXPORT CENTER, etc.) */
.dashboard-title, .section-header, h1, h2, h3 {
    color: #F8FAFC !important; /* pure bright */
    font-weight: 800 !important;
    letter-spacing: -0.02em;
    text-transform: uppercase;
    text-shadow: 0 0 8px rgba(59,130,246,0.2);
}

/* Subtitles */
.dashboard-subtitle, .breadcrumb, h4, h5, h6, label, p, span {
    color: #CBD5E1 !important;
}

/* KPI Cards */
.kpi-label {
    color: #A5B4FC !important; /* light indigo for elegance */
    font-weight: 600;
    letter-spacing: 0.05em;
}

.kpi-value {
    color: #F8FAFC !important;
    font-weight: 800;
    text-shadow: 0 0 6px rgba(96,165,250,0.3);
}

.kpi-change {
    font-weight: 700;
    font-size: 0.95rem;
}

/* Highlight inside blue cards (Revenue grew..., OV ($745.08)... ) */
.kpi-change.positive,
.metric-positive, .metric-highlight, .blue-card-text {
    color: #E0F2FE !important; /* light cyan on blue background */
    text-shadow: 0 0 6px rgba(255,255,255,0.25);
    font-weight: 700 !important;
}

.kpi-change.negative {
    color: #FCA5A5 !important;
}

/* Section dividers */
.section-header {
    border-bottom: 2px solid rgba(59,130,246,0.3);
}

/* Buttons */
.stButton > button {
    color: #F8FAFC !important;
}

/* Dataframes */
.dataframe thead tr th {
    color: #E2E8F0 !important;
}
.dataframe tbody tr {
    color: #F1F5F9 !important;
}

/* Inputs */
.stSelectbox label, .stMultiSelect label, .stDateInput label {
    color: #CBD5E1 !important;
}

/* Alerts / Info boxes */
.stAlert {
    color: #E2E8F0 !important;
}

/* Plotly axes and legends */
.plotly .xtick text,
.plotly .ytick text,
.plotly .legend text,
.plotly .axis-title {
    fill: #E2E8F0 !important;
    font-weight: 600;
}

.plotly-tooltip, .hoverlayer text {
    color: #0F172A !important;
    background: rgba(255,255,255,0.95) !important;
    border: 1px solid #CBD5E1 !important;
}
</style>
"""

# ==============================
#  APPLY THEME FUNCTION
# ==============================
def apply_theme():
    """Apply global dark theme with enhanced text contrast"""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ==============================
#  PLOTLY TEMPLATE (IMPROVED)
# ==============================
def get_plotly_template():
    """Return custom Plotly template with better contrast"""
    template = go.layout.Template()
    template.layout = go.Layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text_primary'], family='Inter, sans-serif', size=13),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(148,163,184,0.15)',
            zeroline=False,
            color=COLORS['text_secondary'],
            titlefont=dict(color=COLORS['text_primary']),
            tickfont=dict(color=COLORS['text_secondary'])
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(148,163,184,0.15)',
            zeroline=False,
            color=COLORS['text_secondary'],
            titlefont=dict(color=COLORS['text_primary']),
            tickfont=dict(color=COLORS['text_secondary'])
        ),
        hoverlabel=dict(
            bgcolor='rgba(51,65,85,0.95)',
            bordercolor='rgba(59,130,246,0.3)',
            font=dict(color='#F8FAFC', size=12)
        ),
        legend=dict(
            bgcolor='rgba(17,24,39,0.8)',
            bordercolor='rgba(59,130,246,0.2)',
            font=dict(color=COLORS['text_primary'])
        )
    )
    return template
