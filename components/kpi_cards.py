import streamlit as st
import plotly.graph_objects as go
from typing import Optional, List, Dict, Any
from components.style import COLORS, format_number, get_color_by_change

def render_kpi_card(
    label: str,
    value: float,
    icon: str = "📊",
    change: Optional[float] = None,
    change_label: str = "vs período anterior",
    format_type: str = "number",
    decimals: int = 0,
    reverse_colors: bool = False,
    sparkline_data: Optional[List[float]] = None,
    trend_color: Optional[str] = None
):
    """Render a single KPI card with optional comparison and sparkline
    
    Args:
        label: KPI label text
        value: Main KPI value
        icon: Emoji or icon to display
        change: Percentage change vs comparison period
        change_label: Label for the change indicator
        format_type: 'number', 'currency', 'percent', or 'compact'
        decimals: Number of decimal places
        reverse_colors: If True, negative change is good (e.g., cost reduction)
        sparkline_data: Optional list of values for mini trend chart
        trend_color: Optional color override for sparkline
    """
    
    # Format main value
    formatted_value = format_number(value, format_type, decimals)
    
    # Build change HTML
    change_html = ""
    if change is not None:
        change_class = get_color_by_change(change, reverse_colors)
        arrow = "▲" if change > 0 else "▼" if change < 0 else "●"
        change_html = f'''
        <div class="kpi-change {change_class}">
            {arrow} {abs(change):.1f}% {change_label}
        </div>
        '''
    
    # Build sparkline if data provided
    sparkline_html = ""
    if sparkline_data:
        if trend_color is None:
            if change is not None:
                trend_color = COLORS['success'] if change > 0 else COLORS['danger']
            else:
                trend_color = COLORS['primary']
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=sparkline_data,
            mode='lines',
            line=dict(color=trend_color, width=2),
            fill='tozeroy',
            fillcolor=f'{trend_color}33',
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            height=60,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            hovermode=False
        )
        
        sparkline_placeholder = st.empty()
        sparkline_html = "<!-- Sparkline rendered separately -->"
    
    # Build complete card HTML
    card_html = f'''
    <div class="kpi-card">
        <span class="kpi-icon">{icon}</span>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{formatted_value}</div>
        {change_html}
    </div>
    '''
    
    st.markdown(card_html, unsafe_allow_html=True)
    
    # Render sparkline if data provided
    if sparkline_data:
        sparkline_placeholder.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


def render_kpi_row(kpis: List[Dict[str, Any]], columns: int = 4):
    """Render a row of KPI cards in a grid layout
    
    Args:
        kpis: List of dictionaries with KPI parameters
              Each dict should contain: label, value, and optionally:
              icon, change, change_label, format_type, decimals, reverse_colors
        columns: Number of columns in the grid
    
    Example:
        kpis = [
            {
                'label': 'Total Revenue',
                'value': 125000,
                'icon': '💰',
                'change': 15.3,
                'format_type': 'currency'
            },
            {
                'label': 'Orders',
                'value': 1250,
                'icon': '📦',
                'change': -2.1,
                'format_type': 'number'
            }
        ]
        render_kpi_row(kpis, columns=2)
    """
    
    cols = st.columns(columns)
    
    for idx, kpi in enumerate(kpis):
        with cols[idx % columns]:
            render_kpi_card(
                label=kpi.get('label', 'KPI'),
                value=kpi.get('value', 0),
                icon=kpi.get('icon', '📊'),
                change=kpi.get('change'),
                change_label=kpi.get('change_label', 'vs período anterior'),
                format_type=kpi.get('format_type', 'number'),
                decimals=kpi.get('decimals', 0),
                reverse_colors=kpi.get('reverse_colors', False),
                sparkline_data=kpi.get('sparkline_data'),
                trend_color=kpi.get('trend_color')
            )


def render_simple_metric(
    label: str,
    value: float,
    format_type: str = "number",
    decimals: int = 0,
    color: str = "primary"
):
    """Render a simple metric without card styling (inline display)
    
    Args:
        label: Metric label
        value: Metric value
        format_type: 'number', 'currency', 'percent', or 'compact'
        decimals: Number of decimal places
        color: Color key from COLORS dict ('primary', 'success', 'warning', etc.)
    """
    
    formatted_value = format_number(value, format_type, decimals)
    metric_color = COLORS.get(color, COLORS['primary'])
    
    metric_html = f'''
    <div style="display: inline-block; margin-right: 2rem;">
        <div style="color: {COLORS['text_secondary']}; font-size: 0.85rem; font-weight: 500; margin-bottom: 0.25rem;">
            {label}
        </div>
        <div style="color: {metric_color}; font-size: 1.5rem; font-weight: 700;">
            {formatted_value}
        </div>
    </div>
    '''
    
    st.markdown(metric_html, unsafe_allow_html=True)


def render_comparison_card(
    label: str,
    current_value: float,
    previous_value: float,
    icon: str = "📊",
    format_type: str = "number",
    decimals: int = 0,
    reverse_colors: bool = False
):
    """Render a KPI card with side-by-side current vs previous comparison
    
    Args:
        label: KPI label
        current_value: Current period value
        previous_value: Previous period value
        icon: Emoji or icon
        format_type: 'number', 'currency', 'percent', or 'compact'
        decimals: Number of decimal places
        reverse_colors: If True, negative change is good
    """
    
    # Calculate change
    if previous_value != 0:
        change = ((current_value - previous_value) / previous_value) * 100
    else:
        change = 0
    
    change_class = get_color_by_change(change, reverse_colors)
    arrow = "▲" if change > 0 else "▼" if change < 0 else "●"
    
    formatted_current = format_number(current_value, format_type, decimals)
    formatted_previous = format_number(previous_value, format_type, decimals)
    
    card_html = f'''
    <div class="kpi-card">
        <span class="kpi-icon">{icon}</span>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{formatted_current}</div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid rgba(148, 163, 184, 0.1);">
            <div style="color: {COLORS['text_secondary']}; font-size: 0.85rem;">
                Anterior: {formatted_previous}
            </div>
            <div class="kpi-change {change_class}">
                {arrow} {abs(change):.1f}%
            </div>
        </div>
    </div>
    '''
    
    st.markdown(card_html, unsafe_allow_html=True)


def render_gauge_card(
    label: str,
    value: float,
    target: float,
    icon: str = "🎯",
    format_type: str = "number",
    decimals: int = 0,
    show_percentage: bool = True
):
    """Render a KPI card with gauge/progress indicator vs target
    
    Args:
        label: KPI label
        value: Current value
        target: Target value
        icon: Emoji or icon
        format_type: 'number', 'currency', 'percent', or 'compact'
        decimals: Number of decimal places
        show_percentage: If True, show percentage of target achieved
    """
    
    # Calculate percentage of target
    if target != 0:
        percentage = (value / target) * 100
    else:
        percentage = 0
    
    # Determine color based on achievement
    if percentage >= 100:
        gauge_color = COLORS['success']
        status = "✓ Objetivo alcanzado"
    elif percentage >= 80:
        gauge_color = COLORS['warning']
        status = "⚠ Cerca del objetivo"
    else:
        gauge_color = COLORS['danger']
        status = "↓ Por debajo del objetivo"
    
    formatted_value = format_number(value, format_type, decimals)
    formatted_target = format_number(target, format_type, decimals)
    
    # Cap percentage at 100 for visual display
    display_percentage = min(percentage, 100)
    
    card_html = f'''
    <div class="kpi-card">
        <span class="kpi-icon">{icon}</span>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{formatted_value}</div>
        <div style="margin-top: 0.75rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: {COLORS['text_secondary']}; font-size: 0.85rem;">
                    Objetivo: {formatted_target}
                </span>
                {f'<span style="color: {gauge_color}; font-size: 0.85rem; font-weight: 600;">{percentage:.1f}%</span>' if show_percentage else ''}
            </div>
            <div style="width: 100%; height: 8px; background: rgba(148, 163, 184, 0.2); border-radius: 4px; overflow: hidden;">
                <div style="width: {display_percentage}%; height: 100%; background: {gauge_color}; transition: width 0.3s ease;"></div>
            </div>
            <div style="color: {gauge_color}; font-size: 0.8rem; font-weight: 500; margin-top: 0.5rem;">
                {status}
            </div>
        </div>
    </div>
    '''
    
    st.markdown(card_html, unsafe_allow_html=True)


def render_stat_grid(stats: List[Dict[str, Any]], columns: int = 2):
    """Render a compact grid of statistics (lighter version of KPI cards)
    
    Args:
        stats: List of dicts with 'label', 'value', 'icon' (optional)
        columns: Number of columns
    
    Example:
        stats = [
            {'label': 'Active Users', 'value': 1234, 'icon': '👥'},
            {'label': 'Avg Session', 'value': '5m 32s', 'icon': '⏱️'}
        ]
    """
    
    cols = st.columns(columns)
    
    for idx, stat in enumerate(stats):
        with cols[idx % columns]:
            icon = stat.get('icon', '')
            icon_html = f'<span style="font-size: 1.2rem; margin-right: 0.5rem;">{icon}</span>' if icon else ''
            
            stat_html = f'''
            <div style="background: linear-gradient(135deg, #1E293B 0%, #334155 100%); 
                        border-radius: 8px; 
                        padding: 1rem; 
                        border: 1px solid rgba(59, 130, 246, 0.1);
                        margin-bottom: 1rem;">
                <div style="color: {COLORS['text_secondary']}; font-size: 0.8rem; margin-bottom: 0.5rem;">
                    {icon_html}{stat['label']}
                </div>
                <div style="color: {COLORS['text_primary']}; font-size: 1.3rem; font-weight: 600;">
                    {stat['value']}
                </div>
            </div>
            '''
            
            st.markdown(stat_html, unsafe_allow_html=True)
