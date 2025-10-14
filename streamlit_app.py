import streamlit as st

# ✅ Page configuration
st.set_page_config(
    page_title="BI Platform Launcher",
    page_icon="⚡",
    layout="wide"
)

# ✅ Global CSS Styling for Professional Dashboard UI
st.markdown("""
<style>
    :root {
      --primary-bg: linear-gradient(135deg, rgb(17, 24, 39) 0%, rgb(31, 41, 55) 50%, rgb(17, 24, 39) 100%);
      --card-bg: rgba(255,255,255,0.05);
      --hover-bg: rgba(96,165,250,0.15);
      --text-primary: #F3F4F6;
      --text-secondary: #9CA3AF;
      --accent-primary: #60A5FA;
    }

    body {
        font-family: 'Inter', sans-serif;
    }

    .launcher-container {
        padding: 60px 20px;
        border-radius: 16px;
        background: var(--primary-bg);
        text-align: center;
        border: 1px solid rgba(255,255,255,0.05);
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }

    .launcher-title {
        font-size: 42px;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -1px;
    }

    .launcher-subtitle {
        font-size: 16px;
        color: var(--text-secondary);
        letter-spacing: 1px;
        margin-bottom: 40px;
    }

    .app-card {
        background: var(--card-bg);
        border-radius: 14px;
        padding: 24px;
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.05);
        cursor: pointer;
        text-align: center;
    }

    .app-card:hover {
        background: var(--hover-bg);
        transform: translateY(-3px);
        border-color: rgba(96,165,250,0.4);
        box-shadow: 0 6px 14px rgba(0,0,0,0.3);
    }

    .app-icon {
        font-size: 48px;
        margin-bottom: 10px;
    }

    .app-title {
        font-size: 18px;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 5px;
    }

    .app-desc {
        font-size: 13px;
        color: var(--text-secondary);
    }
</style>
""", unsafe_allow_html=True)

# ✅ Header UI
st.markdown("""
<div class="launcher-container">
    <div class="launcher-title">⚡ Business Intelligence Suite</div>
    <div class="launcher-subtitle">Select a dashboard to launch</div>
</div>
""", unsafe_allow_html=True)

st.write("")  # Spacer

# ✅ Dictionary of available dashboards
apps = {
    "📊 E-commerce Dashboard": {
        "path": "apps/ecommerce_app.py",
        "description": "Advanced analytics for sales performance, customers, and revenue optimization."
    }
}

# ✅ Render app cards dynamically
cols = st.columns(len(apps) if len(apps) <= 3 else 3)

for index, (app_name, app_info) in enumerate(apps.items()):
    with cols[index % 3]:
        if st.button(f"{app_name}", key=app_name, help=app_info["description"]):
            st.switch_page(app_info["path"])
        st.markdown(f"""
            <div class="app-card">
                <div class="app-icon">{app_name.split()[0]}</div>
                <div class="app-title">{app_name.replace(app_name.split()[0] + " ", "")}</div>
                <div class="app-desc">{app_info["description"]}</div>
            </div>
        """, unsafe_allow_html=True)
        st.write("")

