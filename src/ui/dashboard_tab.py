"""
Dashboard Tab Module
Improved Analytics and Dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import textwrap


def display_improved_dashboard():
    """Display improved dashboard with comprehensive analytics."""
    
    # Dashboard Header
    header_html = """
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; 
            padding: 2rem; border-radius: 15px; margin-bottom: 2rem; 
            box-shadow: 0 8px 30px rgba(102, 126, 234, 0.3);">
    <h1 style="margin: 0 0 0.5rem 0; font-size: 2.5rem;">📈 Analytics Dashboard</h1>
    <p style="margin: 0; opacity: 0.95; font-size: 1.1rem;">Comprehensive System Performance & Analytics</p>
</div>
"""
    st.markdown(textwrap.dedent(header_html), unsafe_allow_html=True)

    # Key Metrics Row
    st.markdown('<div class="pro-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #667eea; margin-bottom: 1rem;">📊 Key Performance Metrics</h3>', unsafe_allow_html=True)

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    metrics = [
        ("🚂 Total Trains", "1,247", "+23"),
        ("📍 Stations", "598", "Active"),
        ("🚃 Coaches Detected", "8,942", "+234"),
        ("📈 Accuracy", "94.2%", "+1.2%"),
        ("⚡ Processing Speed", "32 FPS", "Stable"),
        ("🟢 System Uptime", "99.8%", "24h"),
    ]

    for (label, value, change), col in zip(metrics, [col1, col2, col3, col4, col5, col6]):
        with col:
            st.metric(label, value, delta=change)

    st.markdown('</div>', unsafe_allow_html=True)

    # Analytics Tabs
    st.markdown('<div class="pro-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #667eea; margin-bottom: 1rem;">📋 Detailed Analytics</h3>', unsafe_allow_html=True)

    analytics_tab1, analytics_tab2, analytics_tab3, analytics_tab4 = st.tabs([
        "📊 Performance", 
        "📈 Trends", 
        "🎯 Accuracy", 
        "⚙️ System"
    ])

    with analytics_tab1:
        st.subheader("System Performance")
        
        # Performance data
        performance_data = {
            "Component": ["Train Detection", "Coach Detection", "Platform Monitoring", "Data Processing", "API Response"],
            "Load %": [45, 62, 38, 55, 32],
            "Status": ["✅ Optimal", "⚠️ Moderate", "✅ Optimal", "⚠️ Moderate", "✅ Optimal"]
        }

        perf_df = pd.DataFrame(performance_data)
        st.dataframe(perf_df, hide_index=True)

        # Performance chart
        st.bar_chart(perf_df.set_index("Component")["Load %"])

    with analytics_tab2:
        st.subheader("Trends & Growth")
        
        # Trend data
        days = pd.date_range('2026-01-01', periods=30, freq='D')
        trends_data = pd.DataFrame({
            "Date": days,
            "Detections": np.random.randint(100, 300, 30),
            "Accuracy": np.linspace(90, 95, 30) + np.random.normal(0, 0.5, 30),
            "Trains Monitored": np.random.randint(50, 200, 30)
        })

        st.line_chart(trends_data.set_index("Date"))

    with analytics_tab3:
        st.subheader("Detection Accuracy")
        
        # Accuracy data
        accuracy_data = {
            "Model": ["YOLOv8 Large", "YOLOv8 Medium", "YOLOv8 Small", "Custom Model"],
            "Accuracy": [94.2, 91.5, 88.3, 93.8],
            "Speed (FPS)": [12, 25, 40, 28],
            "Memory (MB)": [2048, 1024, 512, 1536]
        }

        acc_df = pd.DataFrame(accuracy_data)
        st.dataframe(acc_df, hide_index=True)

        # Accuracy chart
        st.bar_chart(acc_df.set_index("Model")["Accuracy"])

    with analytics_tab4:
        st.subheader("System Health")
        
        health_data = {
            "Component": ["CPU", "Memory", "Disk", "Network", "GPU"],
            "Usage %": [45, 62, 38, 25, 55],
            "Status": ["✅ Good", "⚠️ Moderate", "✅ Good", "✅ Good", "✅ Good"]
        }

        health_df = pd.DataFrame(health_data)
        st.dataframe(health_df, hide_index=True)

        # Health gauge chart
        st.bar_chart(health_df.set_index("Component")["Usage %"])

    st.markdown('</div>', unsafe_allow_html=True)

    # Summary Statistics
    st.markdown('<div class="pro-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #667eea; margin-bottom: 1rem;">📋 Summary Statistics</h3>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        train_stats_html = """
<div style="background: #f8f9fa; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #667eea;">
    <h4 style="margin-top: 0; color: #667eea;">🚂 Train Statistics</h4>
    <ul style="margin: 0; padding-left: 1.5rem;">
        <li>Total Trains: 1,247</li>
        <li>Active Trains: 412</li>
        <li>On Schedule: 385 (93.4%)</li>
        <li>Delayed: 27 (6.6%)</li>
        <li>Average Delay: 12 minutes</li>
    </ul>
</div>
"""
        st.markdown(textwrap.dedent(train_stats_html), unsafe_allow_html=True)

    with col2:
        coach_stats_html = """
<div style="background: #f8f9fa; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #667eea;">
    <h4 style="margin-top: 0; color: #667eea;">🚃 Coach Statistics</h4>
    <ul style="margin: 0; padding-left: 1.5rem;">
        <li>Total Coaches: 8,942</li>
        <li>Detected: 8,428 (94.2%)</li>
        <li>Not Detected: 514 (5.8%)</li>
        <li>Average Accuracy: 94.2%</li>
        <li>Detection Speed: 32 FPS</li>
    </ul>
</div>
"""
        st.markdown(textwrap.dedent(coach_stats_html), unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Recent Events
    st.markdown('<div class="pro-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #667eea; margin-bottom: 1rem;">📋 Recent Events</h3>', unsafe_allow_html=True)

    events_data = {
        "Time": ["20:30", "20:15", "20:00", "19:45", "19:30"],
        "Event": ["Train Arrival", "Coach Detection", "Platform Update", "Train Departure", "Alert Generated"],
        "Train/Platform": ["12301", "12302", "Platform 1", "12303", "Platform 3"],
        "Status": ["✅ Success", "✅ Success", "✅ Updated", "✅ Departed", "⚠️ Alert"]
    }

    events_df = pd.DataFrame(events_data)
    st.dataframe(events_df, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    display_improved_dashboard()
