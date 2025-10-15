import streamlit as st

# Page configuration
st.set_page_config(
    page_title="BI Analytics Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional dark theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    }
    
    .main-header {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        padding: 2rem 3rem;
        border-radius: 16px;
        margin-bottom: 3rem;
        border: 1px solid rgba(59, 130, 246, 0.1);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .main-header h1 {
        color: #F8FAFC;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .main-header p {
        color: #94A3B8;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    .dashboard-card {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        border-radius: 12px;
        padding: 2rem;
        border: 1px solid rgba(59, 130, 246, 0.15);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        height: 100%;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    
    .dashboard-card:hover {
        transform: translateY(-4px);
        border-color: rgba(59, 130, 246, 0.5);
        box-shadow: 0 12px 24px rgba(59, 130, 246, 0.15);
        background: linear-gradient(135deg, #334155 0%, #475569 100%);
    }
    
    .card-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .card-title {
        color: #F8FAFC;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        letter-spacing: -0.01em;
    }
    
    .card-description {
        color: #94A3B8;
        font-size: 0.95rem;
        line-height: 1.6;
        font-weight: 400;
    }
    
    .card-badge {
        display: inline-block;
        background: rgba(59, 130, 246, 0.2);
        color: #60A5FA;
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .section-title {
        color: #F8FAFC;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 2rem;
        letter-spacing: -0.01em;
    }
    
    .stButton > button {
        width: 100%;
        background: transparent;
        border: none;
        padding: 0;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        background: transparent;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# Header section
st.markdown("""
<div class="main-header">
    <h1>📊 Business Intelligence Platform</h1>
    <p>Interactive dashboards and executive analytics suite</p>
</div>
""", unsafe_allow_html=True)

# Dashboard cards configuration
dashboards = [
    {
        "icon": "🛒",
        "title": "E-commerce Dashboard",
        "description": "Full analytics for online sales, performance insights, top products and conversion tracking.",
        "page": "pages/01_📊_Ecommerce_Dashboard.py",
        "badge": "Primary"
    },
    {
        "icon": "📈",
        "title": "Sales Analytics",
        "description": "Sales metrics, trend analysis, revenue projections and sales rep performance.",
        "page": "pages/02_📈_Sales_Analytics.py",
        "badge": "Executive"
    },
    {
        "icon": "👥",
        "title": "Customer Insights",
        "description": "Customer segmentation, behavioral insights, retention and lifetime value (LTV) analysis.",
        "page": "pages/03_👥_Customer_Insights.py",
        "badge": "CRM"
    },
    {
        "icon": "📦",
        "title": "Inventory Control",
        "description": "Inventory management, automated alerts, stock rotation and warehouse analytics.",
        "page": "pages/04_📦_Inventory_Control.py",
        "badge": "Operations"
    },
    {
        "icon": "💰",
        "title": "Financial Overview",
        "description": "Financial statements, P&L breakdown, cashflow tracking and profitability analysis.",
        "page": "pages/05_💰_Financial_Overview.py",
        "badge": "Finance"
    },
    {
        "icon": "🎯",
        "title": "Marketing Performance",
        "description": "Campaign ROI, acquisition channels, conversion rates and traffic performance.",
        "page": "pages/06_🎯_Marketing_Performance.py",
        "badge": "Marketing"
    }
]

# Section title
st.markdown('<p class="section-title">Select a Dashboard</p>', unsafe_allow_html=True)

# Create grid layout for cards
cols = st.columns(3)

for idx, dashboard in enumerate(dashboards):
    with cols[idx % 3]:
        card_html = f"""
        <div class="dashboard-card">
            <span class="card-icon">{dashboard['icon']}</span>
            <div class="card-title">{dashboard['title']}</div>
            <div class="card-description">{dashboard['description']}</div>
            <span class="card-badge">{dashboard['badge']}</span>
        </div>
        """
        
        st.markdown(card_html, unsafe_allow_html=True)
        
        if st.button(f"Open {dashboard['title']}", key=f"btn_{idx}", help=f"Open {dashboard['title']}"):
            st.switch_page(dashboard['page'])

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748B; font-size: 0.9rem; padding: 2rem 0;'>
    <p>Built with Streamlit • Version 1.0.0 • © 2025 BI Analytics Platform</p>
</div>
""", unsafe_allow_html=True)
