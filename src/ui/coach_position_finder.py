"""
Coach Position Finder - ADD-ON FEATURE
Enhanced user input based coach search and platform visualization
"""

import streamlit as st
import pandas as pd
import numpy as np
import textwrap
from datetime import datetime
from src.repositories.train_repository import TrainRepository
from src.utils.suggestions import display_suggestions


def display_coach_position_finder():
    """Display enhanced coach position finder interface - ADD-ON FEATURE"""

    import textwrap
    header_html = """
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2.5rem;
            border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 8px 30px rgba(102, 126, 234, 0.3);">
    <h1 style="margin: 0 0 0.5rem 0; font-size: 2.5rem;">🎯 COACH POSITION FINDER</h1>
    <p style="margin: 0; opacity: 0.95; font-size: 1.1rem;">Find your coach position on the platform using historical train data</p>
</div>
"""
    st.markdown(textwrap.dedent(header_html), unsafe_allow_html=True)

    st.info("ℹ️ **ADD-ON FEATURE**: This is an optional enhancement using historical datasets for intelligent coach positioning.")

    # Initialize repository
    repo = TrainRepository()

    # User Input Section - ADD-ON FEATURE
    st.markdown("### 🔍 Find Your Coach Position")

    extra_html = """
<div style="display: flex; justify-content: center; margin-bottom: 2rem;">
    <div style="width: 100%; max-width: 800px;">
"""
    st.markdown(textwrap.dedent(extra_html), unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])

    with col1:
        train_input = st.text_input(
            "Train Number",
            placeholder="e.g., 12301",
            help="Enter the train number"
        )
        # Display train suggestions
        if train_input:
            display_suggestions("coach_finder_train", "train", train_input)

    with col2:
        station_input = st.text_input(
            "Station Code",
            placeholder="e.g., NDLS, BCT",
            help="Enter station code where you'll board/alight"
        )
        # Display station suggestions
        if station_input:
            display_suggestions("coach_finder_station", "station", station_input)

    with col3:
        coach_type = st.selectbox(
            "Your Coach Type",
            ["AC1", "AC2", "AC3", "Sleeper", "General"],
            help="Select your coach category"
        )

    with col4:
        coach_number = st.number_input(
            "Coach Number",
            min_value=1,
            max_value=24,
            value=1,
            help="Your coach number in the train"
        )

    st.markdown("</div></div>", unsafe_allow_html=True)

    # Search Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔍 Find My Coach Position", type="primary", use_container_width=True):
            if train_input and station_input:
                display_coach_position_results(repo, train_input, station_input, coach_type, coach_number)
            else:
                st.warning("⚠️ Please enter both train number and station code")

    # Instructions
    with st.expander("📖 How to Use This Feature", expanded=False):
        st.markdown(textwrap.dedent("""
        **Step 1:** Enter your train number (e.g., 12301 for Rajdhani Express)

        **Step 2:** Enter the station code where you need to find your coach (e.g., NDLS for New Delhi)

        **Step 3:** Select your coach type and number

        **Step 4:** Click "Find My Coach Position" to see:
        - Where your coach will stop on the platform
        - Approximate distance from platform entrance
        - Visual platform layout with coach positions
        - Safety and accessibility information

        **Note:** This feature uses historical train data and standard coach arrangements for intelligent estimation.
        """)
        )

def display_coach_position_results(repo, train_no, station_code, coach_type, coach_number):
    """Display coach position results - ADD-ON FEATURE"""

    try:
        # Load train data
        train_data = pd.read_csv('data/trains_with_coaches.csv')
        station_data = pd.read_csv('data/indian_stations.csv')

        # Find train information
        train_info = train_data[train_data['train_no'].astype(str) == str(train_no)]

        if train_info.empty:
            st.error(f"❌ Train {train_no} not found in our database")
            return

        train_info = train_info.iloc[0]

        # Find station information
        station_info = station_data[station_data['station_code'] == station_code.upper()]

        if station_info.empty:
            st.error(f"❌ Station {station_code} not found in our database")
            return

        station_info = station_info.iloc[0]

        # Display results header
        st.success(f"✅ Found train {train_info['train_name']} at {station_info['station_name']}")

        # Coach Position Analysis - ADD-ON FEATURE
        display_coach_position_analysis(train_info, station_info, coach_type, coach_number)

        # Platform Visualization - ADD-ON FEATURE
        display_platform_visualization(train_info, station_info, coach_type, coach_number)

        # Distance Estimation - ADD-ON FEATURE
        display_distance_estimation(station_info, coach_type, coach_number)

        # Safety Information - ADD-ON FEATURE
        display_safety_info()

    except Exception as e:
        st.error(f"❌ Error processing request: {str(e)}")


def display_coach_position_analysis(train_info, station_info, coach_type, coach_number):
    """Display coach position analysis - ADD-ON FEATURE"""

    st.markdown("### 📍 Coach Position Analysis")

    # Calculate coach position based on train composition
    coach_position = calculate_coach_position(train_info, coach_type, coach_number)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Your Coach", f"{coach_type} {coach_number}", "🎯")

    with col2:
        st.metric("Platform Side", coach_position['side'], "📍")

    with col3:
        st.metric("Platform Zone", coach_position['zone'], "🗺️")

    with col4:
        st.metric("Distance from Entrance", f"{coach_position['distance']}m", "📏")

    # Detailed analysis
    st.markdown(textwrap.dedent(f"""
    **🎯 Your Coach Position Details:**

    - **Coach Type:** {coach_type}
    - **Coach Number:** {coach_number}
    - **Platform Position:** {coach_position['position_description']}
    - **Platform Zone:** {coach_position['zone']}
    - **Distance from Platform Entrance:** Approximately {coach_position['distance']} meters
    - **Accessibility:** {coach_position['accessibility']}

    **💡 Pro Tip:** Arrive at the station 15-20 minutes before departure to locate your coach easily.
    """)
    )


def display_platform_visualization(train_info, station_info, coach_type, coach_number):
    """Display platform visualization - ADD-ON FEATURE"""

    st.markdown("### 🚉 Platform Layout Visualization")

    # Platform specifications
    platform_length = 250  # meters (standard platform length)
    train_length = calculate_train_length(train_info)

    # Generate coach layout
    coach_layout = generate_coach_layout(train_info, coach_type, coach_number)

    # Create platform visualization with cleaner HTML
    import textwrap
    platform_html = f"""
<div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 1rem;">
    <div style="margin-bottom: 1rem; text-align: center;">
        <h4 style="margin: 0; color: #2c3e50;">Platform Layout at {station_info['station_name']}</h4>
        <p style="margin: 0.5rem 0; color: #666; font-size: 0.9rem;">Platform Length: {platform_length}m | Train Length: {train_length}m</p>
    </div>

    <div style="position: relative; height: 100px; background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
                border-radius: 8px; border: 2px solid #dee2e6; margin: 2rem 0; overflow: hidden;">

        <!-- Platform markers -->
        <div style="position: absolute; left: 0; top: -25px; font-size: 0.8rem; color: #666;">0m</div>
        <div style="position: absolute; right: 0; top: -25px; font-size: 0.8rem; color: #666;">{platform_length}m</div>

        <!-- Train start/end markers -->
        <div style="position: absolute; left: 0; top: -45px; width: 2px; height: 40px; background: #28a745;"></div>
        <div style="position: absolute; left: {train_length/platform_length*100:.1f}%; top: -45px; width: 2px; height: 40px; background: #dc3545;"></div>
        <div style="position: absolute; left: 0; top: -55px; font-size: 0.7rem; color: #28a745; font-weight: bold;">TRAIN START</div>
        <div style="position: absolute; left: {train_length/platform_length*100 - 15:.1f}%; top: -55px; font-size: 0.7rem; color: #dc3545; font-weight: bold;">TRAIN END</div>
"""

    # Add coach segments with cleaner HTML
    coach_colors = {
        "Engine": "#ff6b6b",
        "AC1": "#4ecdc4",
        "AC2": "#45b7d1",
        "AC3": "#96ceb4",
        "Sleeper": "#ffeaa7",
        "Guard": "#dda0dd"
    }

    for coach in coach_layout:
        start_percent = (coach['start_pos'] / platform_length) * 100
        width_percent = (coach['length'] / platform_length) * 100
        color = coach_colors.get(coach['type'], '#cccccc')

        # Highlight user's coach
        if coach['number'] == coach_number and coach['type'] == coach_type:
            border_style = "border: 3px solid #ff6b6b; box-shadow: 0 0 10px rgba(255, 107, 107, 0.5);"
            coach_label = f"🎯 YOUR COACH<br>{coach['number']} ({coach['type']})"
        else:
            border_style = "border-right: 1px solid #fff;"
            coach_label = f"{coach['number']}<br>{coach['type']}"

        platform_html += f"""
<div style="position: absolute; left: {start_percent:.1f}%; width: {width_percent:.1f}%; height: 100%;
            background: {color}; {border_style} display: flex; align-items: center;
            justify-content: center; font-size: 0.7rem; font-weight: bold; color: #2c3e50;">
    {coach_label}
</div>
"""

    # Add legend
    platform_html += """
</div>

<!-- Legend -->
<div style="display: flex; flex-wrap: wrap; gap: 1rem; justify-content: center; margin-top: 1rem;">
"""

    for coach_type_legend, color in coach_colors.items():
        platform_html += f"""
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <div style="width: 16px; height: 16px; background: {color}; border-radius: 3px;"></div>
                <span style="font-size: 0.8rem; color: #666;">{coach_type_legend}</span>
            </div>
        """

    platform_html += """
</div>
</div>
"""

    # remove extra indentation caused by code formatting
    platform_html = textwrap.dedent(platform_html)
    st.markdown(platform_html, unsafe_allow_html=True)


def display_distance_estimation(station_info, coach_type, coach_number):
    """Display distance estimation - ADD-ON FEATURE"""

    st.markdown("### 📏 Distance & Location Estimation")

    # Calculate estimated distance based on coach position
    coach_position = calculate_coach_position_from_number(coach_number, coach_type)

    # Platform zones and distances (approximate)
    zone_distances = {
        "A": "0-50m",
        "B": "50-100m",
        "C": "100-150m",
        "D": "150-200m",
        "E": "200-250m"
    }

    estimated_distance = f"{coach_position['zone']} zone ({zone_distances.get(coach_position['zone'], 'Unknown')})"

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Platform Zone", coach_position['zone'], "🗺️")

    with col2:
        st.metric("Distance Range", zone_distances.get(coach_position['zone'], 'Unknown'), "📏")

    with col3:
        st.metric("Walking Time", "~2-3 minutes", "⏱️")

    st.info(f"""
    **📍 Location Guidance:**
    - Your coach will be in **Zone {coach_position['zone']}** of the platform
    - Approximate distance from main entrance: **{estimated_distance}**
    - Walking time: **2-3 minutes** from platform entrance
    - Look for platform zone markers and coach number displays
    """)


def display_safety_info():
    """Display safety information - ADD-ON FEATURE"""

    st.markdown("### 🛡️ Safety & Accessibility Information")

    col1, col2 = st.columns(2)

    with col1:
        st.success("""
        **✅ Safety Tips:**
        - Arrive 15-20 minutes before departure
        - Check coach number on platform display
        - Keep tickets and ID ready
        - Help elderly and children
        """)

    with col2:
        st.warning("""
        **⚠️ Important Notes:**
        - Platform can be crowded during peak hours
        - Keep clear of the yellow safety line
        - Do not run on the platform
        - Report any suspicious activity
        """)


def calculate_coach_position(train_info, coach_type, coach_number):
    """Calculate coach position based on train composition - ADD-ON FEATURE"""

    # Standard coach arrangement logic
    total_coaches = int(train_info['coach_count'])

    # Determine position based on coach number
    if coach_number <= total_coaches // 3:
        side = "Front"
        zone = "A"
        distance = 25
        position_description = "Near the front of the train"
        accessibility = "Easy access, close to entrance"
    elif coach_number <= (total_coaches * 2) // 3:
        side = "Middle"
        zone = "C"
        distance = 125
        position_description = "In the middle section of the train"
        accessibility = "Moderate walking distance"
    else:
        side = "Rear"
        zone = "E"
        distance = 225
        position_description = "Towards the rear of the train"
        accessibility = "Longer walk, plan extra time"

    return {
        'side': side,
        'zone': zone,
        'distance': distance,
        'position_description': position_description,
        'accessibility': accessibility
    }


def calculate_coach_position_from_number(coach_number, coach_type):
    """Calculate position from coach number - ADD-ON FEATURE"""

    if coach_number <= 4:
        zone = "A"
    elif coach_number <= 8:
        zone = "B"
    elif coach_number <= 12:
        zone = "C"
    elif coach_number <= 16:
        zone = "D"
    else:
        zone = "E"

    return {'zone': zone}


def calculate_train_length(train_info):
    """Calculate approximate train length - ADD-ON FEATURE"""

    # Average coach length is about 20-25 meters
    avg_coach_length = 22
    total_coaches = int(train_info['coach_count'])

    return total_coaches * avg_coach_length


def generate_coach_layout(train_info, user_coach_type, user_coach_number):
    """Generate coach layout for visualization - ADD-ON FEATURE"""

    # Standard coach arrangement (simplified)
    coaches = []

    # Engine
    coaches.append({
        'number': 'E',
        'type': 'Engine',
        'length': 25,
        'start_pos': 0
    })

    # Generate coaches based on train composition
    coach_types = []
    ac2_count = int(train_info.get('ac2_coaches', 0))
    ac3_count = int(train_info.get('ac3_coaches', 0))
    sl_count = int(train_info.get('sl_coaches', 0))

    # Add AC2 coaches
    for i in range(ac2_count):
        coach_types.append('AC2')

    # Add AC3 coaches
    for i in range(ac3_count):
        coach_types.append('AC3')

    # Add Sleeper coaches
    for i in range(sl_count):
        coach_types.append('Sleeper')

    # Create coach list
    current_pos = 25  # After engine
    coach_num = 1

    for coach_type in coach_types:
        coaches.append({
            'number': coach_num,
            'type': coach_type,
            'length': 21.5,
            'start_pos': current_pos
        })
        current_pos += 21.5
        coach_num += 1

    # Guard
    coaches.append({
        'number': 'G',
        'type': 'Guard',
        'length': 15,
        'start_pos': current_pos
    })

    return coaches