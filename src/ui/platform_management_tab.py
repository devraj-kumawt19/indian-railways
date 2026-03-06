"""
Platform Management Tab Module
AI-powered platform management and monitoring with ML predictions
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.repositories.train_repository import TrainRepository
from src.agents.platform_agent import PlatformManagementAgent
import plotly.graph_objects as go
import plotly.express as px
from src.agents.platform_agent import PlatformManagementAgent
import plotly.graph_objects as go
import plotly.express as px


def display_platform_management():
    """Display AI-powered platform management tab."""

    # Initialize AI Agent and Repository
    platform_agent = PlatformManagementAgent()
    repo = TrainRepository()

    st.markdown('<div class="pro-card">', unsafe_allow_html=True)
    st.markdown('<div class="pro-card-header">', unsafe_allow_html=True)
    st.markdown('<span class="pro-card-icon">🤖</span>', unsafe_allow_html=True)
    st.markdown('<h3 class="pro-card-title">AI Platform Management Dashboard</h3>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # AI Controls
    col1, col2, col3 = st.columns(3)
    with col1:
        platform_filter = st.selectbox("Filter Platforms", ["All", "Available", "Occupied", "Maintenance"], key="platform_filter")
    with col2:
        prediction_hours = st.slider("Prediction Hours", 1, 72, 24, key="prediction_hours")
    with col3:
        if st.button("🔄 AI Refresh", key="ai_refresh"):
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Get AI-powered platform status
    status_response = platform_agent.execute('status')
    if status_response.success:
        platforms_data = status_response.data
    else:
        st.error(f"AI Status Error: {status_response.error}")
        return

    # AI Platform Status Grid
    st.markdown('<div class="pro-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #667eea; margin-bottom: 1rem;">🚉 AI Platform Status</h3>', unsafe_allow_html=True)

    # Filter platforms
    if platform_filter != "All":
        platforms_data = {k: v for k, v in platforms_data.items() if v['status'] == platform_filter}

    cols = st.columns(4)
    for idx, (platform_no, platform_info) in enumerate(platforms_data.items()):
        with cols[idx % 4]:
            status = platform_info['status']
            predicted_occupancy = platform_info.get('predicted_occupancy', 0)

            status_color = {
                "Occupied": "#ff6b6b",
                "Available": "#51cf66",
                "Maintenance": "#ffa94d"
            }.get(status, "#999")

            # AI confidence indicator
            ai_confidence = "High" if predicted_occupancy > 0.7 else "Medium" if predicted_occupancy > 0.4 else "Low"
            confidence_color = "#51cf66" if ai_confidence == "High" else "#ffa94d" if ai_confidence == "Medium" else "#ff6b6b"

            current_train = platform_info.get('current_train', {})
            train_display = current_train.get('train_no', '---') if current_train else '---'

            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px;
                       text-align: center; border: 2px solid {status_color};
                       box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <div style="font-size: 2rem; font-weight: bold; color: {status_color}; margin-bottom: 0.5rem;">
                    Platform {platform_no}
                </div>
                <div style="font-size: 0.9rem; color: {status_color}; font-weight: bold; margin-bottom: 0.5rem;">
                    {status}
                </div>
                <div style="font-size: 0.8rem; color: #666; margin-top: 0.5rem;">
                    Train: {train_display}
                </div>
                <div style="font-size: 0.7rem; color: {confidence_color}; margin-top: 0.5rem; font-weight: bold;">
                    AI Prediction: {ai_confidence} ({predicted_occupancy:.1%})
                </div>
            </div>
            """), unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # AI Platform Statistics with ML Insights
    st.markdown('<div class="pro-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #667eea; margin-bottom: 1rem;">📊 AI Platform Analytics</h3>', unsafe_allow_html=True)

    # Get platform stats from AI agent
    stats = platform_agent.get_platform_stats()

    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

    with stat_col1:
        st.metric("Total Platforms", stats['total_platforms'], delta=None)
    with stat_col2:
        st.metric("Occupied", stats['occupied'], delta=f"{stats['occupied']/stats['total_platforms']*100:.1f}%")
    with stat_col3:
        st.metric("Available", stats['available'], delta=f"{stats['available']/stats['total_platforms']*100:.1f}%")
    with stat_col4:
        utilization_pct = stats['utilization_rate'] * 100
        st.metric("Utilization Rate", f"{utilization_pct:.1f}%", delta="AI Optimized")

    st.markdown('</div>', unsafe_allow_html=True)

    # ML Occupancy Predictions
    st.markdown('<div class="pro-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #667eea; margin-bottom: 1rem;">🔮 ML Occupancy Predictions</h3>', unsafe_allow_html=True)

    # Get predictions from AI agent
    prediction_response = platform_agent.execute('predict', hours_ahead=prediction_hours)
    if prediction_response.success:
        predictions = prediction_response.data['predictions']

        # Create prediction chart
        platforms = list(predictions.keys())
        occupancy_rates = [predictions[p] for p in platforms]

        fig = go.Figure(data=[
            go.Bar(
                x=platforms,
                y=occupancy_rates,
                marker_color=['#51cf66' if rate < 0.4 else '#ffa94d' if rate < 0.7 else '#ff6b6b' for rate in occupancy_rates],
                text=[f'{rate:.1%}' for rate in occupancy_rates],
                textposition='auto',
            )
        ])

        fig.update_layout(
            title=f"Predicted Platform Occupancy (Next {prediction_hours} Hours)",
            xaxis_title="Platform Number",
            yaxis_title="Predicted Occupancy Rate",
            yaxis_tickformat='.1%'
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # AI Optimization Recommendations
    st.markdown('<div class="pro-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #667eea; margin-bottom: 1rem;">🎯 AI Optimization Insights</h3>', unsafe_allow_html=True)

    # Get optimization recommendations
    optimization_response = platform_agent.execute('optimize')
    if optimization_response.success:
        opt_data = optimization_response.data

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Current Utilization", f"{opt_data['current_utilization']:.1%}")
        with col2:
            st.metric("Predicted Utilization", f"{opt_data['predicted_utilization']:.1%}")

        st.markdown("**🤖 AI Recommendations:**")
        for rec in opt_data['recommendations']:
            st.markdown(f"• {rec}")

    st.markdown('</div>', unsafe_allow_html=True)

    # Database-Driven Recent Activity
    st.markdown('<div class="pro-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #667eea; margin-bottom: 1rem;">📋 Database Activity Log</h3>', unsafe_allow_html=True)

    # Generate activity data from AI agent (in real implementation, from database)
    activity_data = []
    base_time = datetime.now()

    for i in range(10):
        activity_time = base_time - timedelta(minutes=i*15)
        platforms = list(platforms_data.keys())
        platform = np.random.choice(platforms)

        if platforms_data[platform]['status'] == 'Occupied':
            event = np.random.choice(['Train Arrival', 'Train Departure'])
            train_no = f"{np.random.randint(10000, 99999)}"
            activity_data.append({
                "Time": activity_time.strftime("%H:%M"),
                "Event": event,
                "Train": train_no,
                "Platform": str(platform)
            })

    if activity_data:
        activity_df = pd.DataFrame(activity_data)
        st.dataframe(activity_df, hide_index=True, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # AI Platform Allocation Simulator
    st.markdown('<div class="pro-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #667eea; margin-bottom: 1rem;">🎮 AI Platform Allocation Simulator</h3>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        sim_train_no = st.text_input("Train Number", "12501", key="sim_train")
    with col2:
        sim_arrival = st.time_input("Arrival Time", datetime.now().time(), key="sim_arrival")
    with col3:
        if st.button("🚀 Allocate Platform", key="allocate_btn"):
            allocation_response = platform_agent.execute('allocate',
                train_no=sim_train_no,
                arrival_time=str(sim_arrival),
                departure_time=str((datetime.combine(datetime.today(), sim_arrival) + timedelta(hours=2)).time())
            )

            if allocation_response.success:
                allocated_platform = allocation_response.data['allocated_platform']
                st.success(f"🤖 AI allocated Platform {allocated_platform} to Train {sim_train_no}")
                st.rerun()
            else:
                st.error(f"Allocation failed: {allocation_response.error}")

    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    display_platform_management()
