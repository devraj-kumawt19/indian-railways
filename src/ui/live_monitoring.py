"""
Advanced Live Monitoring Page
Real-time train detection with enhanced visualization
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import textwrap

# Add CSS for animations and improvements
css = """
<style>
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 10px rgba(0, 255, 0, 0.3); }
        50% { box-shadow: 0 0 20px rgba(0, 255, 0, 0.6); }
    }
    
    .status-pulse {
        display: inline-block;
        width: 8px;
        height: 8px;
        background: #00ff00;
        border-radius: 50%;
        animation: pulse 1.5s infinite;
        margin-right: 6px;
    }
    
    .camera-feed {
        border-radius: 12px;
        overflow: hidden;
    }
    
    .settings-panel {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    
    .settings-panel:hover {
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
    }
</style>
"""
st.markdown(textwrap.dedent(css), unsafe_allow_html=True)

try:
    from PIL import Image
except ImportError:
    Image = None

from src.repositories.train_repository import TrainRepository


def display_live_monitoring_dashboard():
    """Display comprehensive live monitoring dashboard."""
    
    # Professional Header
    header_html = """
<div style="background: linear-gradient(135deg, #00d4ff 0%, #0099ff 50%, #006dcc 100%); color: white; padding: 2.5rem; 
            border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 8px 30px rgba(0, 157, 255, 0.3);">
    <h1 style="margin: 0 0 0.5rem 0; font-size: 2.5rem;">⚡ LIVE MONITORING DASHBOARD</h1>
    <p style="margin: 0; opacity: 0.95; font-size: 1.1rem;">Real-time Train Detection & Live Platform Status</p>
    <div style="margin-top: 1rem; display: flex; gap: 2rem; font-size: 0.9rem;">
        <div>📊 Live Feed Status: <span style="color: #00ff00; font-weight: bold;">ACTIVE</span></div>
        <div>🔴 Signal: <span style="color: #00ff00; font-weight: bold;">STRONG</span></div>
        <div>⏱️ Last Update: Now</div>
    </div>
</div>
"""
    st.markdown(textwrap.dedent(header_html), unsafe_allow_html=True)
    
    # Real-time Statistics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="🚂 Active Trains",
            value="5",
            delta="+2",
            delta_color="off"
        )
    
    with col2:
        st.metric(
            label="📍 Occupied Platforms",
            value="6/8",
            delta="-1",
            delta_color="off"
        )
    
    with col3:
        st.metric(
            label="🔍 Coaches Detected",
            value="24",
            delta="+3",
            delta_color="off"
        )
    
    with col4:
        st.metric(
            label="⚠️ Alerts",
            value="2",
            delta="2 Critical",
            delta_color="inverse"
        )
    
    with col5:
        st.metric(
            label="🎯 Accuracy",
            value="94.2%",
            delta="+0.5%",
            delta_color="off"
        )
    
    st.markdown("---")
    
    # Real-time Train Status
    st.subheader("🚆 Real-Time Train Status")
    
    display_train_status()
    
    st.markdown("---")
    
    # Platform Status Monitor
    st.subheader("📍 Platform Status Monitor")
    
    display_platform_status()
    
    st.markdown("---")
    
    # Coach Detection Analysis
    st.subheader("🚃 Coach Detection Analysis")
    
    display_coach_analysis()
    
    st.markdown("---")
    
    # Live Alerts & Notifications
    st.subheader("🔔 Live Alerts & Notifications")
    
    display_live_alerts()


def display_train_status():
    """Display real-time train status with improved UI."""
    
    # Sample train data
    trains_data = {
        "Train No": ["12301", "20844", "15017", "22915", "16351"],
        "Train Name": ["RAJDHANI EXP", "DELHI EXPRESS", "BANDRA EXP", "KERALA EXP", "DOON EXPRESS"],
        "Status": ["Arrived", "Departing Soon", "In Transit", "On Time", "Delayed"],
        "Arrival": ["14:30", "15:00", "16:15", "17:45", "15:20"],
        "Platform": ["1", "3", "5", "2", "4"],
        "Delay": ["0 min", "0 min", "On Time", "0 min", "+12 min"],
    }
    
    df = pd.DataFrame(trains_data)
    
    # Custom styling for the real-time table
    st.markdown("""
    <style>
    .train-status-table {
        width: 100%;
        border-collapse: collapse;
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        border: 1px solid #e9ecef;
    }
    
    .train-status-table th {
        background: linear-gradient(135deg, #00d4ff 0%, #0099ff 50%, #006dcc 100%);
        color: white;
        padding: 1rem 1.2rem;
        text-align: left;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 0.5px;
        border-bottom: 2px solid #0088cc;
    }
    
    .train-status-table td {
        padding: 1rem 1.2rem;
        border-bottom: 1px solid #f0f0f0;
        font-size: 0.9rem;
    }
    
    .train-status-table tr:hover {
        background: linear-gradient(90deg, #f8fbff 0%, #f0f7ff 100%);
        transition: all 0.3s ease;
    }
    
    .train-status-table tr:last-child td {
        border-bottom: none;
    }
    
    .status-badge {
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
        letter-spacing: 0.3px;
    }
    
    .status-arrived {
        background: #e8ffe8;
        color: #00aa00;
    }
    
    .status-departing-soon {
        background: #fff3e8;
        color: #ff8800;
    }
    
    .status-in-transit {
        background: #e8f7ff;
        color: #0099ff;
    }
    
    .status-on-time {
        background: #e8ffe8;
        color: #00aa00;
    }
    
    .status-delayed {
        background: #ffe8e8;
        color: #ff0000;
    }
    
    .platform-badge {
        background: #e8f4f8;
        color: #0066cc;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        font-weight: 600;
        border: 1px solid #b3d9ff;
    }
    
    .delay-on-time {
        color: #00aa00;
        font-weight: 700;
    }
    
    .delay-delayed {
        color: #ff0000;
        font-weight: 700;
    }
    
    .train-number {
        color: #2c3e50;
        font-weight: 700;
        font-size: 0.95rem;
    }
    
    .train-name {
        color: #444;
        font-weight: 600;
    }
    </style>
    """), unsafe_allow_html=True)
    
    # Build HTML table
    html = """
<table class="train-status-table">
    <tr>
        <th style="width: 12%;">🚂 Train No</th>
        <th style="width: 20%;">Train Name</th>
        <th style="width: 18%;">Status</th>
        <th style="width: 15%;">⏱️ Arrival</th>
        <th style="width: 12%;">📍 Platform</th>
        <th style="width: 23%;">⏳ Delay Status</th>
    </tr>
"""
    
    for idx, row in df.iterrows():
        train_no = row['Train No']
        train_name = row['Train Name']
        status = row['Status']
        arrival = row['Arrival']
        platform = row['Platform']
        delay = row['Delay']
        
        # Status badge class
        status_class = f"status-{status.lower().replace(' ', '-')}"
        
        # Delay color class
        delay_class = "delay-on-time" if '0 min' in delay or 'On Time' in delay else "delay-delayed"
        
        html += f"""
    <tr>
        <td><span class="train-number">{train_no}</span></td>
        <td><span class="train-name">{train_name}</span></td>
        <td><span class="status-badge {status_class}">{status}</span></td>
        <td style="font-weight: 600; color: #2c3e50;">{arrival}</td>
        <td><span class="platform-badge">{platform}</span></td>
        <td><span class="{delay_class}">{delay}</span></td>
    </tr>
"""
    
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True, key="train_status_table")


def display_platform_status():
    """Display platform status monitor."""
    
    platforms_data = {
        "Platform": ["1", "2", "3", "4", "5", "6", "7", "8"],
        "Status": ["Occupied", "Free", "Occupied", "Maintenance", "Free", "Occupied", "Free", "Free"],
        "Train": ["12301", "-", "15017", "-", "-", "16351", "-", "-"],
        "Coaches": ["24", "-", "22", "-", "-", "20", "-", "-"],
    }
    
    cols = st.columns(4)
    
    for idx, platform in enumerate(platforms_data["Platform"]):
        col = cols[idx % 4]
        
        status = platforms_data["Status"][idx]
        train = platforms_data["Train"][idx]
        coaches = platforms_data["Coaches"][idx]
        
        # Color coding based on status
        if status == "Occupied":
            color = "#00d4ff"
            bg_color = "#e8f7ff"
        elif status == "Free":
            color = "#00aa00"
            bg_color = "#e8ffe8"
        else:  # Maintenance
            color = "#ff8800"
            bg_color = "#ffe8d4"
        
        with col:
            st.markdown(f"""
            <div style="background: {bg_color}; padding: 1.2rem; border-radius: 10px; 
                        border-left: 4px solid {color}; text-align: center; margin-bottom: 0.5rem;">
                <div style="font-size: 1.5rem; font-weight: bold; color: {color};">Platform {platform}</div>
                <div style="color: #666; font-size: 0.9rem; margin-top: 0.3rem;">{status}</div>
                {f'<div style="color: #2c3e50; font-size: 0.8rem; margin-top: 0.5rem;"><strong>Train:</strong> {train}</div>' if train != '-' else ''}
                {f'<div style="color: #2c3e50; font-size: 0.8rem;"><strong>Coaches:</strong> {coaches}</div>' if coaches != '-' else ''}
            </div>
            """), unsafe_allow_html=True)


def display_coach_analysis():
    """Display real-time coach detection and analysis from camera feeds."""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; border: 1px solid #e0e0e0;">
            <h4 style="margin: 0 0 1rem 0; color: #2c3e50;">🚃 Real-Time Coach Detection Analysis</h4>
            
            <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                    <div>
                        <div style="font-size: 0.8rem; color: #666; font-weight: 600; margin-bottom: 0.3rem;">LIVE COACHES DETECTED</div>
                        <div style="font-size: 2.5rem; font-weight: bold; color: #00d4ff;">24/24</div>
                        <div style="font-size: 0.75rem; color: #00aa00; margin-top: 0.2rem;">✓ 100% Detection Rate</div>
                    </div>
                    <div>
                        <div style="font-size: 0.8rem; color: #666; font-weight: 600; margin-bottom: 0.3rem;">DETECTION ACCURACY</div>
                        <div style="font-size: 2.5rem; font-weight: bold; color: #00aa00;">94.2%</div>
                        <div style="font-size: 0.75rem; color: #666; margin-top: 0.2rem;">High Confidence Level</div>
                    </div>
                </div>
            </div>
            
            <div style="margin-bottom: 1rem;">
                <div style="font-size: 0.8rem; color: #666; font-weight: 600; margin-bottom: 0.5rem;">📊 Coach Type Distribution (Real-Time)</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;">
                    <div style="background: #e8f4f8; padding: 0.8rem; border-radius: 6px; border-left: 4px solid #0099ff;">
                        <div style="font-weight: bold; color: #0099ff; margin-bottom: 0.2rem;">🚄 AC 1st Class</div>
                        <div style="font-size: 1.3rem; font-weight: bold; color: #2c3e50;">2</div>
                        <div style="font-size: 0.75rem; color: #666;">coaches</div>
                    </div>
                    <div style="background: #e8f4f8; padding: 0.8rem; border-radius: 6px; border-left: 4px solid #0099ff;">
                        <div style="font-weight: bold; color: #0099ff; margin-bottom: 0.2rem;">🚃 AC 2nd Class</div>
                        <div style="font-size: 1.3rem; font-weight: bold; color: #2c3e50;">4</div>
                        <div style="font-size: 0.75rem; color: #666;">coaches</div>
                    </div>
                    <div style="background: #e8f4f8; padding: 0.8rem; border-radius: 6px; border-left: 4px solid #0099ff;">
                        <div style="font-weight: bold; color: #0099ff; margin-bottom: 0.2rem;">🚂 AC 3rd Class</div>
                        <div style="font-size: 1.3rem; font-weight: bold; color: #2c3e50;">8</div>
                        <div style="font-size: 0.75rem; color: #666;">coaches</div>
                    </div>
                    <div style="background: #e8f4f8; padding: 0.8rem; border-radius: 6px; border-left: 4px solid #0099ff;">
                        <div style="font-weight: bold; color: #0099ff; margin-bottom: 0.2rem;">🛏️ Sleeper Class</div>
                        <div style="font-size: 1.3rem; font-weight: bold; color: #2c3e50;">10</div>
                        <div style="font-size: 0.75rem; color: #666;">coaches</div>
                    </div>
                </div>
            </div>
            
            <div style="background: #f0f9ff; padding: 0.8rem; border-radius: 6px; border-left: 4px solid #00d4ff; font-size: 0.85rem;">
                <strong style="color: #0066cc;">📍 Detection Source:</strong> Live camera feeds from all platforms with real-time YOLOv8 analysis
            </div>
        </div>
        """), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; border: 1px solid #e0e0e0; height: 100%;">
            <h4 style="margin: 0 0 1rem 0; color: #2c3e50; font-size: 0.95rem;">⚡ Detection Settings</h4>
            
            <div style="margin-bottom: 1rem; font-size: 0.85rem;">
                <strong style="color: #666;">Detection Model</strong><br>
                <span style="background: #e8f4f8; padding: 0.4rem 0.6rem; border-radius: 4px; display: inline-block; margin-top: 0.3rem; color: #0066cc; font-weight: bold;">YOLOv8 Large</span>
            </div>
            
            <div style="margin-bottom: 1rem; font-size: 0.85rem;">
                <strong style="color: #666;">Confidence Threshold</strong><br>
                <span style="background: #e8f4f8; padding: 0.4rem 0.6rem; border-radius: 4px; display: inline-block; margin-top: 0.3rem; color: #0066cc; font-weight: bold;">94.2%</span>
            </div>
            
            <div style="margin-bottom: 1rem; font-size: 0.85rem;">
                <strong style="color: #666;">Processing Mode</strong><br>
                <span style="background: #e8ffe8; padding: 0.4rem 0.6rem; border-radius: 4px; display: inline-block; margin-top: 0.3rem; color: #00aa00; font-weight: bold;">Real-Time</span>
            </div>
            
            <div style="margin-bottom: 1rem; font-size: 0.85rem;">
                <strong style="color: #666;">Data Source</strong><br>
                <span style="background: #e8f4f8; padding: 0.4rem 0.6rem; border-radius: 4px; display: inline-block; margin-top: 0.3rem; color: #0066cc; font-weight: bold;">Live Cameras</span>
            </div>
            
            <hr style="margin: 0.8rem 0; border: none; border-top: 1px solid #e0e0e0;">
            
            <button style="width: 100%; padding: 0.7rem; background: #00d4ff; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 0.85rem; margin-bottom: 0.5rem;">
                🔄 Recalibrate Detection
            </button>
            
            <button style="width: 100%; padding: 0.7rem; background: #00aa00; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 0.85rem;">
                ✓ Export Report
            </button>
        </div>
        """), unsafe_allow_html=True)


def display_live_alerts():
    """Display live alerts and notifications with improved styling."""
    
    alerts = [
        {
            "severity": "⚠️ CRITICAL",
            "title": "Platform 2: Train 20844 Boarding Delay",
            "message": "Unexpected delay in passenger boarding. Security checkpoint congestion detected.",
            "time": "2 mins ago",
            "color": "#ff0000",
            "bg_color": "#ffe8e8"
        },
        {
            "severity": "⚡ WARNING",
            "title": "Coach Detection: Train 15017 Accuracy Low",
            "message": "Lighting conditions affecting detection accuracy. Confidence: 87%",
            "time": "5 mins ago",
            "color": "#ff8800",
            "bg_color": "#fff3e8"
        },
        {
            "severity": "✅ INFO",
            "title": "System Status: All Systems Operational",
            "message": "All detection systems running at optimal performance.",
            "time": "30 secs ago",
            "color": "#00aa00",
            "bg_color": "#e8ffe8"
        },
    ]
    
    for alert in alerts:
        st.markdown(f"""
        <div style="background: {alert['bg_color']}; padding: 1.2rem; border-radius: 10px; 
                    border-left: 5px solid {alert['color']}; margin-bottom: 1rem;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08); transition: all 0.3s ease;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem;">
                <div style="flex: 1;">
                    <div style="color: {alert['color']}; font-weight: 700; margin-bottom: 0.4rem; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.5px;">
                        {alert['severity']}
                    </div>
                    <div style="font-weight: 600; color: #2c3e50; margin-bottom: 0.4rem; font-size: 0.95rem;">
                        {alert['title']}
                    </div>
                    <div style="color: #555; font-size: 0.85rem; line-height: 1.5;">
                        {alert['message']}
                    </div>
                </div>
                <div style="color: #999; font-size: 0.8rem; white-space: nowrap; padding: 0.3rem 0.6rem; background: rgba(0,0,0,0.05); border-radius: 4px;">
                    {alert['time']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    display_live_monitoring_dashboard()
