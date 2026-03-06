import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict
import pandas as pd


def render_platform_layout_html(platform_length: float, train_length: float, platform_name: str = "Platform 1"):
    """
    Render HTML-based platform layout visualization with train positioning.
    
    Args:
        platform_length: Length of platform in meters
        train_length: Length of train in meters
        platform_name: Name of the platform
    """
    # Calculate percentages for visualization
    train_percentage = (train_length / platform_length) * 100 if platform_length > 0 else 0
    
    # Determine status color based on fit
    if train_percentage <= 100:
        status = "✓ Perfect Fit"
        status_color = "#51cf66"
    elif train_percentage <= 110:
        status = "⚠ Slight Overhang"
        status_color = "#ffa94d"
    else:
        status = "✗ Too Long"
        status_color = "#ff6b6b"
    
    import textwrap
    html_content = f"""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            border-radius: 12px; padding: 1.5rem; margin: 1rem 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1); color: white;">
    
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
        <h3 style="margin: 0; font-size: 1.3rem;">{platform_name}</h3>
        <span style="background: {status_color}; padding: 0.5rem 1rem; border-radius: 20px; 
                    font-weight: bold; font-size: 0.9rem;">{status}</span>
    </div>
    
    <!-- Platform Visualization -->
    <div style="background: white; padding: 2rem; border-radius: 8px; margin-bottom: 1.5rem;">
        <!-- Platform Bar -->
        <div style="position: relative; height: 60px; background: #f8f9fa; border: 2px dashed #ddd; 
                   border-radius: 8px; margin-bottom: 2rem; overflow: hidden;">
            <!-- Platform Rectangle -->
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 30px; 
                       background: linear-gradient(90deg, #e7f5ff 0%, #d0ebff 100%);
                       border-bottom: 2px solid #74c0fc; display: flex; align-items: center;
                       justify-content: center; font-weight: bold; color: #1971c2; font-size: 0.8rem;">
                PLATFORM - {platform_length}m
            </div>
            
            <!-- Train Rectangle (positioned based on fit) -->
            <div style="position: absolute; top: 32px; left: 0; height: 28px; 
                       width: min({train_percentage}%, 100%); background: linear-gradient(90deg, #ffd43b 0%, #fab005 100%);
                       border: 2px solid #f08c00; border-radius: 4px; display: flex; align-items: center;
                       justify-content: center; color: white; font-weight: bold; font-size: 0.75rem;
                       overflow: hidden;">
                TRAIN - {train_length}m
            </div>
        </div>
        
        <!-- Statistics -->
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
            <div style="background: #f0f4ff; padding: 1rem; border-radius: 8px; text-align: center; border-left: 4px solid #667eea;">
                <div style="color: #666; font-size: 0.85rem; margin-bottom: 0.5rem;">Platform Length</div>
                <div style="font-weight: bold; color: #667eea; font-size: 1.2rem;">{platform_length}m</div>
            </div>
            <div style="background: #fff4e6; padding: 1rem; border-radius: 8px; text-align: center; border-left: 4px solid #fab005;">
                <div style="color: #666; font-size: 0.85rem; margin-bottom: 0.5rem;">Train Length</div>
                <div style="font-weight: bold; color: #fab005; font-size: 1.2rem;">{train_length}m</div>
            </div>
            <div style="background: {'#e7f5ff' if train_percentage <= 100 else '#ffe0e0'}; padding: 1rem; border-radius: 8px; text-align: center; border-left: 4px solid {status_color};">
                <div style="color: #666; font-size: 0.85rem; margin-bottom: 0.5rem;">Occupancy</div>
                <div style="font-weight: bold; color: {status_color}; font-size: 1.2rem;">{train_percentage:.1f}%</div>
            </div>
        </div>
    </div>
    
    <!-- Additional Info -->
    <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid white;">
        <div style="font-size: 0.9rem; line-height: 1.6;">
            <div>✓ Platform can accommodate: <strong>{int(platform_length / train_length)} {('train' if int(platform_length / train_length) == 1 else 'trains')} of {train_length}m length</strong></div>
            <div>✓ Remaining space: <strong>{max(0, platform_length - train_length):.1f}m</strong></div>
        </div>
    </div>
</div>
"""

    html_content = textwrap.dedent(html_content)
    st.markdown(html_content, unsafe_allow_html=True)


def render_train_layout(coaches: List[Dict], engine_position: int = 0):
    """
    Render train layout with coaches using Plotly.
    
    Args:
        coaches: list of {'name': str, 'length_m': float}
        engine_position: index of engine (0=front)
    """
    names = [c.get('name', f'Coach {i}') for i, c in enumerate(coaches)]
    lengths = [c.get('length_m', 10) for c in coaches]

    fig = go.Figure()
    x0 = 0
    colors = []
    
    # Create coach rectangles
    for i, (n, l) in enumerate(zip(names, lengths)):
        # Alternate colors for visibility
        color = '#667eea' if i % 2 == 0 else '#764ba2'
        colors.append(color)
        
        fig.add_shape(
            type='rect', x0=x0, x1=x0+l, y0=0, y1=1,
            line=dict(color='black', width=2),
            fillcolor=color, opacity=0.7
        )
        fig.add_annotation(
            x=x0 + l/2, y=0.5, text=f"{n}<br>{l}m",
            showarrow=False, font=dict(size=10, color='white'), 
            align='center'
        )
        x0 += l

    # Mark engine position
    if engine_position < len(lengths):
        eng_x = sum(lengths[:engine_position])
        fig.add_shape(
            type='line', x0=eng_x, x1=eng_x, y0=-0.3, y1=1.3,
            line=dict(color='red', width=4)
        )
        fig.add_annotation(
            x=eng_x, y=-0.5, text="🚂 Engine",
            showarrow=False, font=dict(size=10, color='red')
        )
    
    # Update layout
    fig.update_xaxes(title_text="Distance (meters)", tickwidth=2)
    fig.update_yaxes(visible=False)
    fig.update_layout(
        title=f"Train Composition - Total Length: {sum(lengths):.1f}m",
        height=300,
        margin=dict(l=50, r=50, t=100, b=50),
        showlegend=False,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def display_platform_vs_train_comparison(platforms: List[Dict], trains: List[Dict]):
    """
    Display interactive comparison of platforms vs trains.
    
    Args:
        platforms: list of {'name': str, 'length_m': float}
        trains: list of {'name': str, 'length_m': float, 'coaches': int}
    """
    st.markdown('<h3 style="color: #667eea;">📊 Platform vs Train Comparison</h3>', unsafe_allow_html=True)
    
    # Create comparison dataframe
    comparison_data = []
    for platform in platforms:
        for train in trains:
            occupancy = (train['length_m'] / platform['length_m']) * 100
            fit_status = "✓ Fits" if occupancy <= 100 else "⚠ Overhang" if occupancy <= 110 else "✗ Too Long"
            
            comparison_data.append({
                'Platform': platform['name'],
                'Train': train['name'],
                'Platform Length (m)': platform['length_m'],
                'Train Length (m)': train['length_m'],
                'Occupancy (%)': f"{occupancy:.1f}%",
                'Status': fit_status
            })
    
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Create visualization
    fig = px.bar(
        df, 
        x='Platform', 
        y=['Platform Length (m)', 'Train Length (m)'],
        barmode='group',
        title='Platform vs Train Length Comparison',
        labels={'value': 'Length (meters)', 'variable': 'Type'},
        color_discrete_map={'Platform Length (m)': '#667eea', 'Train Length (m)': '#fab005'}
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)


def display_sample_platform_layouts():
    """Display sample platform layout visualizations with HTML rendering."""
    st.markdown('<h2 style="color: #667eea; margin-top: 2rem;">🚉 Sample Platform Layouts</h2>', unsafe_allow_html=True)
    
    # Sample data
    platforms = [
        {"name": "Platform 1", "length": 400},
        {"name": "Platform 2", "length": 450},
        {"name": "Platform 3", "length": 380},
    ]
    
    trains = [
        {"name": "Express Train", "length": 380},
        {"name": "Local Train", "length": 320},
        {"name": "Rajdhani", "length": 420},
    ]
    
    # Display platform layouts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h4 style="color: #667eea;">Platform Layouts</h4>', unsafe_allow_html=True)
        selected_platform = st.selectbox(
            "Select Platform",
            [p["name"] for p in platforms],
            key="platform_select"
        )
        platform_data = next(p for p in platforms if p["name"] == selected_platform)
        
        selected_train = st.selectbox(
            "Select Train",
            [t["name"] for t in trains],
            key="train_select"
        )
        train_data = next(t for t in trains if t["name"] == selected_train)
        
        render_platform_layout_html(
            platform_data["length"],
            train_data["length"],
            f"{platform_data['name']} ← {selected_train}"
        )
    
    with col2:
        st.markdown('<h4 style="color: #667eea;">Train Composition</h4>', unsafe_allow_html=True)
        
        # Sample coach data for the selected train
        coaches_data = {
            "Express Train": [
                {"name": "Engine", "length_m": 20},
                {"name": "Coach-1", "length_m": 25},
                {"name": "Coach-2", "length_m": 25},
                {"name": "Coach-3", "length_m": 25},
                {"name": "Coach-4", "length_m": 25},
                {"name": "Coach-5", "length_m": 25},
                {"name": "Guard Car", "length_m": 15},
            ],
            "Local Train": [
                {"name": "Engine", "length_m": 18},
                {"name": "Coach-1", "length_m": 22},
                {"name": "Coach-2", "length_m": 22},
                {"name": "Coach-3", "length_m": 22},
                {"name": "Coach-4", "length_m": 22},
                {"name": "Coach-5", "length_m": 22},
                {"name": "Coach-6", "length_m": 22},
                {"name": "Guard Car", "length_m": 12},
            ],
            "Rajdhani": [
                {"name": "Engine", "length_m": 22},
                {"name": "Coach-1", "length_m": 27},
                {"name": "Coach-2", "length_m": 27},
                {"name": "Coach-3", "length_m": 27},
                {"name": "Coach-4", "length_m": 27},
                {"name": "Coach-5", "length_m": 27},
                {"name": "Coach-6", "length_m": 27},
                {"name": "Guard Car", "length_m": 18},
            ]
        }
        
        coaches = coaches_data.get(selected_train, [])
        if coaches:
            render_train_layout(coaches, engine_position=0)
