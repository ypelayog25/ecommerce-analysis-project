import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

class EcommerceDashboard:
    def __init__(self):
        self.config = {
            'theme': {
                'primary': '#0078D4',
                'secondary': '#FFB600',
                'background': '#f5f5f5',
                'text': '#323130'
            },
            'layout': {
                'sidebar_width': 300,
                'header_height': 80,
                'card_spacing': 20
            }
        }
        self.setup_page()
        self.load_data()
    
    def setup_page(self):
        st.set_page_config(
            page_title="Executive Dashboard | E-commerce Analytics",
            layout="wide",
            initial_sidebar_state="expanded",
            page_icon="📊"
        )
        
        st.markdown("""
            <style>
            /* Import Professional Fonts */
            @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700&family=Roboto:wght@400;500;700&display=swap');
            
            /* Global Styles */
            * {
                font-family: 'Segoe UI', 'Roboto', sans-serif;
            }
            
            /* Main Background - Power BI Style */
            .main {
                background-color: #f5f5f5;
                padding: 0.5rem;
            }
            
            /* Sidebar - Power BI Navigation Style */
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #2d2d2d 0%, #1f1f1f 100%);
                border-right: 3px solid #FFB600;
            }
            
            [data-testid="stSidebar"] * {
                color: #ffffff !important;
            }
            
            /* Power BI Header Style */
            .powerbi-header {
                background: linear-gradient(90deg, #2d2d2d 0%, #1f1f1f 100%);
                padding: 1.5rem 2rem;
                border-radius: 8px;
                margin-bottom: 1.5rem;
                border-left: 5px solid #FFB600;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            
            /* KPI Cards - Power BI Style */
            div[data-testid="metric-container"] {
                background: linear-gradient(135deg, #ffffff 0%, #f9f9f9 100%);
                padding: clamp(15px, 3vw, 25px);
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
                border-left: 4px solid #0078D4;
                transition: all 0.3s ease;
                min-height: 120px;
            }
            
            div[data-testid="metric-container"]:hover {
                transform: translateY(-5px);
                box-shadow: 0 4px 20px rgba(0, 120, 212, 0.2);
                border-left-color: #FFB600;
            }
            
            /* Chart Container - Power BI Card Style */
            .chart-container {
                background: #ffffff;
                padding: clamp(15px, 2.5vw, 25px);
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
                margin-bottom: 1.5rem;
                border-top: 3px solid #0078D4;
            }
            
            /* Section Headers */
            .section-header {
                color: #323130;
                font-size: clamp(16px, 2.5vw, 20px);
                font-weight: 700;
                margin: 1.5rem 0 1rem 0;
                padding-left: 12px;
                border-left: 4px solid #0078D4;
            }
            
            /* Tabs - Power BI Style */
            .stTabs [data-baseweb="tab-list"] {
                gap: 4px;
                background-color: #ffffff;
                padding: 8px;
                border-radius: 8px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.06);
                flex-wrap: wrap;
            }
            
            .stTabs [data-baseweb="tab"] {
                height: auto;
                min-height: 45px;
                background-color: #f3f2f1;
                border-radius: 6px;
                color: #323130;
                font-weight: 600;
                font-size: clamp(12px, 1.8vw, 14px);
                padding: 10px clamp(12px, 2vw, 20px);
                border: 2px solid transparent;
                white-space: normal;
                word-wrap: break-word;
            }
            
            .stTabs [aria-selected="true"] {
                background-color: #0078D4;
                color: #ffffff !important;
                border-color: #0078D4;
            }
            
            /* Buttons - Power BI Style */
            .stButton button {
                background-color: #0078D4;
                color: white;
                border: none;
                border-radius: 4px;
                padding: clamp(8px, 1.5vw, 12px) clamp(16px, 2.5vw, 24px);
                font-weight: 600;
                font-size: clamp(12px, 1.8vw, 14px);
                transition: all 0.2s ease;
                box-shadow: 0 2px 4px rgba(0, 120, 212, 0.2);
                width: 100%;
            }
            
            .stButton button:hover {
                background-color: #106EBE;
                box-shadow: 0 4px 8px rgba(0, 120, 212, 0.3);
            }
            
            /* Download Button - Power BI Accent */
            .stDownloadButton button {
                background-color: #FFB600;
                color: #1f1f1f !important;
                font-weight: 700;
            }
            
            .stDownloadButton button:hover {
                background-color: #FFAA00;
            }
            
            /* Mobile Optimizations */
            @media (max-width: 768px) {
                .main {
                    padding: 0.25rem;
                }
                
                .powerbi-header {
                    padding: 1rem;
                    margin-bottom: 1rem;
                }
                
                div[data-testid="metric-container"] {
                    min-height: 100px;
                    margin-bottom: 0.5rem;
                }
                
                .chart-container {
                    padding: 12px;
                    margin-bottom: 1rem;
                }
                
                .stTabs [data-baseweb="tab"] {
                    padding: 8px 12px;
                    font-size: 12px;
                }
                
                [data-testid="column"] {
                    padding: 0 0.25rem;
                }
                
                .section-header {
                    font-size: 16px;
                    margin: 1rem 0 0.5rem 0;
                }
            }
            
            /* Extra Small Devices */
            @media (max-width: 480px) {
                .powerbi-title {
                    font-size: 18px;
                }
                
                .powerbi-subtitle {
                    font-size: 11px;
                }
                
                [data-testid="stMetricValue"] {
                    font-size: 20px !important;
                }
                
                .stButton button {
                    padding: 8px 12px;
                    font-size: 12px;
                }
            }
            </style>
        """, unsafe_allow_html=True)
    
    def load_data(self):
        @st.cache_data(ttl=3600)
        def _load_data():
            try:
                dataset_parquet = "data/processed/ecommerce_dataset_10000_cleaned.parquet"
                dataset_csv = "data/processed/ecommerce_dataset_10000_cleaned.csv"
                
                if os.path.exists(dataset_parquet):
                    df = pd.read_parquet(dataset_parquet)
                elif os.path.exists(dataset_csv):
                    df = pd.read_csv(dataset_csv)
                else:
                    return None
                
                df['order_date'] = pd.to_datetime(df['order_date'])
                df['year_month'] = df['order_date'].dt.to_period('M')
                df['day_of_week'] = df['order_date'].dt.day_name()
                return df
            except Exception as e:
                st.error(f"⚠️ Error loading data: {e}")
                return None
        
        self.df = _load_data()
        if self.df is None or self.df.empty:
            st.error("❌ No dataset found or dataset is empty.")
            st.stop()
    
    def create_header(self):
        st.markdown("""
            <div class='powerbi-header'>
                <h1 class='powerbi-title'>📊 Executive E-commerce Dashboard</h1>
                <p class='powerbi-subtitle'>REAL-TIME BUSINESS INTELLIGENCE & ANALYTICS</p>
            </div>
        """, unsafe_allow_html=True)
    
    def create_sidebar(self):
        with st.sidebar:
            st.markdown("""
                <div style='text-align: center; padding: 1.5rem 0; border-bottom: 2px solid #FFB600;'>
                    <div style='font-size: 48px; margin-bottom: 10px;'>📊</div>
                    <h2 style='margin: 0; font-size: 20px; color: #FFB600 !important;'>DASHBOARD</h2>
                    <p style='margin: 5px 0 0 0; font-size: 11px; color: #b0b0b0 !important;'>Control Panel</p>
                </div>
            """, unsafe_allow_html=True
