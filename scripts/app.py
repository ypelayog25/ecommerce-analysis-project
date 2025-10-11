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
        self.create_components()

    def setup_page(self):
        st.set_page_config(
            page_title="Executive Dashboard | E-commerce Analytics",
            layout="wide",
            initial_sidebar_state="expanded",
            page_icon="📊"
        )

    def load_data(self):
        @st.cache_data(ttl=3600)
        def _load_data():
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
                df['day_of_week'] = df['order_date'].dt.day_name()
                return df
            except Exception as e:
                st.error(f"⚠️ Error loading data: {e}")
                return None

        self.df = _load_data()
        if self.df is None or self.df.empty:
            st.error("❌ No dataset found or dataset is empty.")
            st.stop()
            class ChartFactory:
    @staticmethod
    def create_revenue_trend(df, title="Revenue Trend"):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['order_date'],
            y=df['total_price'],
            mode='lines+markers',
            line=dict(color='#0078D4', width=3),
            marker=dict(size=8),
            fill='tozeroy',
            fillcolor='rgba(0, 120, 212, 0.1)',
            hovertemplate='<b>%{x|%b %Y}</b><br>$%{y:,.0f>'
        ))
        return fig

    @staticmethod
    def create_customer_segmentation(df):
        fig = go.Figure()
        fig.add_trace(go.Pie(
            labels=df['segment'],
            values=df['customer_id'],
            hole=0.4,
            marker=dict(colors=['#0078D4', '#00BCF2', '#FFB900', '#E81123']),
            textinfo='label+percent',
            textfont=dict(size=11),
            hovertemplate='<b>%{label}</b><br>Customers: %{value}<br>%{percent}'
        ))
        return fig

class UserExperience:
    @staticmethod
    def create_date_filter():
        return st.expander("📅 Date Filters", expanded=True)
    
    @staticmethod
    def create_quick_select():
        options = {
            '7D': timedelta(days=7),
            '30D': timedelta(days=30),
            '90D': timedelta(days=90),
            'YTD': 'year_to_date'
        }
        return st.selectbox("Quick Select", list(options.keys()))

if __name__ == "__main__":
    app = EcommerceDashboard()
