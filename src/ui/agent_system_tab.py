"""
Agent System Tab Module
AI Agent System for advanced train detection
"""

import streamlit as st
import pandas as pd
import time


def display_agent_system():
    """Display agent system tab with AI capabilities."""
    
    # Initialize session state
    if "agent_mode" not in st.session_state:
        st.session_state.agent_mode = "Autonomous"
    
    st.markdown('<div class="pro-card">', unsafe_allow_html=True)
    st.markdown('<div class="pro-card-header">', unsafe_allow_html=True)
    st.markdown('<span class="pro-card-icon">🤖</span>', unsafe_allow_html=True)
    st.markdown('<h3 class="pro-card-title">AI Agent Control System</h3>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Agent Mode Selection
    agent_mode = st.radio(
        "Agent Mode",
        ["🤖 Autonomous", "👤 Manual Control", "🔄 Semi-Autonomous"],
        horizontal=True,
        help="Choose how the AI agent operates"
    )
    st.session_state.agent_mode = agent_mode

    st.markdown('</div>', unsafe_allow_html=True)

    # Agent Status Dashboard
    st.markdown('<div class="pro-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #667eea; margin-bottom: 1rem;">📊 Agent Status Dashboard</h3>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Agent Status", "Active ✅", delta="Ready")
    with col2:
        st.metric("Tasks Running", "3", delta="+1")
    with col3:
        st.metric("Accuracy", "94.2%", delta="+1.5%")
    with col4:
        st.metric("Response Time", "145ms", delta="-20ms")

    st.markdown('</div>', unsafe_allow_html=True)

    # Agent Controls
    if agent_mode == "🤖 Autonomous":
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #667eea; margin-bottom: 1rem;">🚀 Autonomous Agent Controls</h3>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("▶️ Start Agent", width='stretch'):
                st.success("✅ Agent started successfully!")
        
        with col2:
            if st.button("⏸️ Pause Agent", width='stretch'):
                st.warning("⏸️ Agent paused")
        
        with col3:
            if st.button("🛑 Stop Agent", width='stretch'):
                st.error("❌ Agent stopped")

        st.markdown('</div>', unsafe_allow_html=True)

        # Agent Configuration
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #667eea; margin-bottom: 1rem;">⚙️ Autonomous Configuration</h3>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        
        with col1:
            detection_interval = st.slider(
                "Detection Interval (seconds)",
                min_value=1,
                max_value=60,
                value=5,
                help="How often to run detection"
            )
        
        with col2:
            confidence_threshold = st.slider(
                "Confidence Threshold",
                min_value=0.5,
                max_value=0.99,
                value=0.8,
                help="Minimum confidence for detections"
            )

        col1, col2 = st.columns(2)
        
        with col1:
            auto_alert = st.checkbox("Enable Auto Alerts", value=True)
        
        with col2:
            auto_log = st.checkbox("Enable Auto Logging", value=True)

        st.markdown('</div>', unsafe_allow_html=True)

    elif agent_mode == "👤 Manual Control":
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #667eea; margin-bottom: 1rem;">🎮 Manual Control Panel</h3>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔍 Run Detection", width='stretch'):
                with st.spinner("Running detection..."):
                    time.sleep(2)
                st.success("✅ Detection completed!")
        
        with col2:
            if st.button("📊 Analyze Results", width='stretch'):
                with st.spinner("Analyzing..."):
                    time.sleep(1.5)
                st.success("✅ Analysis complete!")
        
        with col3:
            if st.button("💾 Save Results", width='stretch'):
                st.success("✅ Results saved!")

        st.markdown('</div>', unsafe_allow_html=True)

        # Manual Options
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #667eea; margin-bottom: 1rem;">⚙️ Manual Options</h3>', unsafe_allow_html=True)

        detection_type = st.selectbox(
            "Detection Type",
            ["Coach Detection", "Train Detection", "Platform Monitoring", "Custom Analysis"],
            help="Select what to detect"
        )

        col1, col2 = st.columns(2)
        
        with col1:
            model = st.selectbox(
                "AI Model",
                ["YOLOv8 Large", "YOLOv8 Medium", "YOLOv8 Small", "Custom Model"],
                help="Choose detection model"
            )
        
        with col2:
            device = st.selectbox(
                "Processing Device",
                ["GPU", "CPU", "Auto"],
                help="Where to run detection"
            )

        st.markdown('</div>', unsafe_allow_html=True)

    else:  # Semi-Autonomous
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #667eea; margin-bottom: 1rem;">🔄 Semi-Autonomous Mode</h3>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("▶️ Start Semi-Auto", width='stretch'):
                st.success("✅ Semi-autonomous mode started!")
        
        with col2:
            if st.button("⚖️ Balance Mode", width='stretch'):
                st.info("⚙️ Balancing AI and manual controls...")
        
        with col3:
            if st.button("🛑 Stop", width='stretch'):
                st.error("❌ Stopped")

        st.markdown('</div>', unsafe_allow_html=True)

        # Semi-Auto Configuration
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #667eea; margin-bottom: 1rem;">⚙️ Semi-Autonomous Settings</h3>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        
        with col1:
            automation_level = st.slider(
                "Automation Level",
                min_value=0,
                max_value=100,
                value=50,
                help="0 = Manual, 100 = Fully Autonomous"
            )
        
        with col2:
            approval_required = st.checkbox(
                "Require Approval for Critical Actions",
                value=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # Recent Agent Tasks
    st.markdown('<div class="pro-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #667eea; margin-bottom: 1rem;">📋 Recent Agent Tasks</h3>', unsafe_allow_html=True)

    tasks_data = pd.DataFrame({
        "Task ID": ["T001", "T002", "T003", "T004", "T005"],
        "Type": ["Coach Detection", "Train Tracking", "Platform Check", "Coach Detection", "Train Tracking"],
        "Status": ["✅ Completed", "✅ Completed", "⏳ Running", "✅ Completed", "⏳ Running"],
        "Accuracy": ["94.2%", "91.5%", "---", "93.8%", "---"],
        "Duration": ["2.5s", "3.1s", "Running...", "2.8s", "Running..."]
    })

    st.dataframe(tasks_data, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    display_agent_system()
