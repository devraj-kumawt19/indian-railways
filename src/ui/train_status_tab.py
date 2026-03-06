"""
Train Status Tab Module
Monitor specific trains and nearby platforms
"""

import streamlit as st
import streamlit.components.v1 as components
import textwrap
from src.repositories.train_repository import TrainRepository
from src.utils.suggestions import display_suggestions


def display_train_status_tab():
    """Display train status tab - requires user to enter train number or select location."""
    
    # Initialize session state
    if "monitor_nearby" not in st.session_state:
        st.session_state.monitor_nearby = False
    
    repo = TrainRepository()
    
    # Monitoring Mode Selection
    monitoring_header_html = """
<div class="pro-card">
    <div class="pro-card-header">
        <span class="pro-card-icon">🎯</span>
        <h3 class="pro-card-title">Select Monitoring Mode</h3>
    </div>
</div>
"""
    st.markdown(textwrap.dedent(monitoring_header_html), unsafe_allow_html=True)

    monitoring_mode = st.radio(
        "Choose how you want to monitor:",
        ["🚂 Specific Train", "📍 Nearby Platforms"],
        horizontal=True,
        help="Monitor a specific train or see all trains at nearby platforms"
    )

    train_number = None

    # Specific Train Monitoring
    if monitoring_mode == "🚂 Specific Train":
        train_input_header_html = """
<div class="pro-card">
    <div class="pro-card-header">
        <span class="pro-card-icon">🚆</span>
        <h3 class="pro-card-title">Enter Train Number to Monitor</h3>
    </div>
</div>
"""
        st.markdown(textwrap.dedent(train_input_header_html), unsafe_allow_html=True)

        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            train_number = st.text_input(
                "🚂 Train Number",
                placeholder="e.g., 12301, 12302, 12303",
                key="train_status_input",
                help="Enter the specific train number you want to monitor"
            )
            # Display train number suggestions
            if train_number:
                display_suggestions("train_status_input", "train", train_number)
        
        with col2:
            search_button = st.button("🔍 Monitor Train", width='stretch', key="monitor_train_btn")
        
        with col3:
            if st.button("ℹ️ Sample Numbers", width='stretch', key="sample_trains_btn"):
                st.info("📌 **Sample Train Numbers:**\n\n• 12301 - Rajdhani Express\n• 12302 - Shatabdi Express\n• 12303 - Duronto Express")

            if st.button("ℹ️ Sample Numbers", width='stretch', key="sample_trains_btn"):
                st.info("📌 **Sample Train Numbers:**\n\n• 12301 - Rajdhani Express\n• 12302 - Shatabdi Express\n• 12303 - Duronto Express")

        # Display monitoring only if train number is provided
        if train_number:
            # Validate train number
            try:
                int(train_number)
            except ValueError:
                st.error(f"❌ Invalid Train Number: {train_number} - must be numeric")
                st.stop()

            # Quick Actions
            quick_actions_html = """
<div class="pro-card">
    <div class="pro-card-header">
        <span class="pro-card-icon">⚡</span>
        <h3 class="pro-card-title">Quick Actions</h3>
    </div>
</div>
"""
            st.markdown(textwrap.dedent(quick_actions_html), unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🔄 Refresh Status", width='stretch', key="refresh_status"):
                    st.rerun()
            with col2:
                st.button("📊 Export Report", width='stretch', key="export_report")
            with col3:
                st.button("🔔 Set Alerts", width='stretch', key="set_alerts")

            with col3:
                st.button("🔔 Set Alerts", width='stretch', key="set_alerts")

            # Live Train Status
            train_status_header_html = f"""
<div class="pro-card">
    <div class="pro-card-header">
        <span class="pro-card-icon">🚆</span>
        <h3 class="pro-card-title">Live Train Status - {train_number}</h3>
    </div>
</div>
"""
            st.markdown(textwrap.dedent(train_status_header_html), unsafe_allow_html=True)

            # Display sample train status
            train_status_html = f"""
            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #667eea;">
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem;">
                    <div>
                        <strong>Status:</strong> On Schedule ✅
                    </div>
                    <div>
                        <strong>Current Location:</strong> Delhi Junction
                    </div>
                    <div>
                        <strong>Delay:</strong> 0 mins
                    </div>
                </div>
            </div>
            """
            st.markdown(train_status_html, unsafe_allow_html=True)

            # Train Route Events
            route_events_header_html = """
<div class="pro-card">
    <div class="pro-card-header">
        <span class="pro-card-icon">🛤️</span>
        <h3 class="pro-card-title">Train Route Events</h3>
    </div>
</div>
"""
            st.markdown(textwrap.dedent(route_events_header_html), unsafe_allow_html=True)

            # Display route events as expandable items
            stations = [
                {"name": "Delhi Junction", "arr": "08:00", "dep": "08:00", "delay": 0},
                {"name": "Meerut City", "arr": "09:30", "dep": "09:35", "delay": 0},
                {"name": "Muzaffarnagar", "arr": "10:45", "dep": "11:00", "delay": 0},
                {"name": "Saharanpur", "arr": "12:30", "dep": "12:35", "delay": 0},
            ]

            for station in stations:
                with st.expander(f"🚉 {station['name']} - Arr: {station['arr']}, Dep: {station['dep']}"):
                    st.write(f"Platform: 1 | Delay: {station['delay']} mins")

            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # Show instruction when no train number entered
            st.markdown('<div class="pro-card" style="text-align: center; padding: 2rem;">', unsafe_allow_html=True)
            st.markdown("""
            <div style="opacity: 0.7;">
                <h3 style="color: #888; margin-bottom: 1rem;">📍 No Train Selected</h3>
                <p style="color: #666; font-size: 1.1rem;">
                    Please enter a train number above to see live monitoring and train events.
                </p>
                <p style="color: #666; font-size: 0.95rem; margin-top: 1rem;">
                    <strong>Popular Train Numbers:</strong><br>
                    12301 (Rajdhani) • 12302 (Shatabdi) • 12303 (Duronto)
                </p>
            </div>
            """), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Location-Based Monitoring
    else:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.markdown('<div class="pro-card-header">', unsafe_allow_html=True)
        st.markdown('<span class="pro-card-icon">📍</span>', unsafe_allow_html=True)
        st.markdown('<h3 class="pro-card-title">Live Monitoring - Nearby Platforms</h3>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            selected_location = st.selectbox(
                "📍 Select Junction/Station",
                ["Jaipur Junction", "Delhi Junction", "Mumbai Central", "Chennai Central", "Bangalore City"],
                help="Select your current location"
            )
        
        with col2:
            platform_range = st.number_input(
                "Platform Range",
                min_value=1,
                max_value=5,
                value=2,
                help="Monitor platforms within this range"
            )
        
        with col3:
            if st.button("🔍 Monitor Nearby", width='stretch', key="monitor_nearby_btn"):
                st.session_state.monitor_nearby = True

        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display nearby platform monitoring
        if st.session_state.get("monitor_nearby", False):
            st.markdown('<div class="pro-card">', unsafe_allow_html=True)
            st.markdown(f'<h3 style="color: #667eea;">🚂 Trains at {selected_location}</h3>', unsafe_allow_html=True)
            
            # Sample nearby trains
            nearby_trains = [
                {"no": "12301", "name": "Rajdhani Express", "platform": 1, "status": "On Time"},
                {"no": "12302", "name": "Shatabdi Express", "platform": 2, "status": "On Time"},
                {"no": "12303", "name": "Duronto Express", "platform": 3, "status": "Delayed 5 mins"},
            ]

            for train in nearby_trains:
                # note: close markdown call after dedent; unsafe_allow_html is argument to st.markdown
                html = textwrap.dedent(f"""
                <div style="background: white; padding: 1rem; border-radius: 10px; margin-bottom: 0.5rem; 
                           border-left: 4px solid #667eea; display: flex; justify-content: space-between;">
                    <div><strong>{train['no']} - {train['name']}</strong></div>
                    <div>Platform {train['platform']} | {train['status']}</div>
                </div>
                """
                )
                st.markdown(html, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="pro-card" style="text-align: center; padding: 2rem;">', unsafe_allow_html=True)
            st.markdown("""
            <div style="opacity: 0.7;">
                <h3 style="color: #888; margin-bottom: 1rem;">📍 Location Based Monitoring</h3>
                <p style="color: #666; font-size: 1.1rem;">
                    Select your current location and platform range, then click "Monitor Nearby" 
                    to see live trains at nearby platforms.
                </p>
            </div>
            """), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    display_train_status_tab()
