import streamlit as st
import plotly.graph_objects as go

# ============================================================
# ENHANCED COLOR PALETTE (Optimized for Professional Readability)
# ============================================================
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

    # Text (Enhanced contrast for readability)
    'text_primary': '#F9FAFB',    # near white for high contrast
    'text_secondary': '#CBD5E1',  # lighter than before for better contrast
    'text_tertiary': '#94A3B8',   # subtle for muted elements

    # Borders
    'border_subtle': 'rgba(59, 130, 246, 0.1)',
    'border_medium': 'rgba(59, 130, 246, 0.2)',
    'border_strong': 'rgba(59, 130, 246, 0.35)',
}

# ============================================================
# GLOBAL STYLESHEET (Updated Typography & Visual Hierarchy)
# ============================================================
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
    box-sizing: border-box;
}

/* Hide Streamlit branding */
#MainMenu, footer, header {visibility: hidden;}

/* MAIN APP BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #0F172A 0
