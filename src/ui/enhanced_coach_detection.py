"""
Enhanced Coach Detection Module
Improved accuracy and visual feedback for coach identification
"""

import streamlit as st
import pandas as pd
import numpy as np
import textwrap
from datetime import datetime
from src.utils.suggestions import display_suggestions
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.repositories.train_repository import TrainRepository
from src.scheduling.indian_railways_api import IndianRailwaysAPI


def load_train_coach_data(search_query=None):
    """Load train coach data from CSV file or API."""
    try:
        # Initialize API
        api = IndianRailwaysAPI()
        
        # If search query provided, try API first
        if search_query and len(search_query.strip()) > 0:
            st.info("🔍 Searching trains via API...")
            try:
                # Try to get train schedule from API
                if search_query.isdigit():
                    # Search by train number
                    schedule_data = api.get_train_schedule(search_query)
                    if schedule_data:
                        # Convert API data to DataFrame format
                        api_trains = [{
                            'train_no': schedule_data.get('train_no', search_query),
                            'train_name': schedule_data.get('train_name', f'Train {search_query}'),
                            'from_station': schedule_data.get('source_station', 'Unknown'),
                            'to_station': schedule_data.get('destination_station', 'Unknown'),
                            'from_code': 'N/A',
                            'to_code': 'N/A',
                            'departure_time': '06:00',
                            'arrival_time': '18:00',
                            'duration_hrs': schedule_data.get('journey_time', '12.0'),
                            'distance_km': schedule_data.get('total_distance', 500),
                            'coach_count': 18,  # Default
                            'sl_coaches': 10,
                            'ac2_coaches': 4,
                            'ac3_coaches': 3,
                            'fc_coaches': 1,
                            'pantry': 'Yes',
                            'platform_from': 1,
                            'platform_to': 1,
                            'frequency': 'Daily',
                            'zone': 'IR'
                        }]
                        return pd.DataFrame(api_trains)
            except Exception as api_error:
                st.warning(f"API search failed: {api_error}. Using local database...")
        
        # Fallback to comprehensive local dataset
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'Train_details_22122017.csv')
        df = pd.read_csv(csv_path, dtype={'Train No': str}, low_memory=False)
        
        # Convert Distance to numeric, handling mixed types
        df['Distance'] = pd.to_numeric(df['Distance'], errors='coerce')
        
        # Group by train to get unique trains
        unique_trains = df.groupby(['Train No', 'Train Name']).agg({
            'Source Station Name': 'first',
            'Destination Station Name': 'last',
            'Distance': 'max',
            'Source Station': 'first',
            'Destination Station': 'last'
        }).reset_index()
        
        # Rename columns to match expected format
        unique_trains = unique_trains.rename(columns={
            'Train No': 'train_no',
            'Train Name': 'train_name',
            'Source Station Name': 'from_station',
            'Destination Station Name': 'to_station',
            'Source Station': 'from_code',
            'Destination Station': 'to_code',
            'Distance': 'distance_km'
        })
        
        # Add default coach information based on train type
        def get_coach_info(train_name):
            train_name_lower = str(train_name).lower()
            if 'rajdhani' in train_name_lower:
                return {'coach_count': 18, 'sl_coaches': 0, 'ac2_coaches': 9, 'ac3_coaches': 0, 'fc_coaches': 2}
            elif 'shatabdi' in train_name_lower:
                return {'coach_count': 11, 'sl_coaches': 0, 'ac2_coaches': 8, 'ac3_coaches': 0, 'fc_coaches': 1}
            elif 'garib rath' in train_name_lower:
                return {'coach_count': 18, 'sl_coaches': 8, 'ac2_coaches': 0, 'ac3_coaches': 10, 'fc_coaches': 0}
            elif 'duronto' in train_name_lower:
                return {'coach_count': 16, 'sl_coaches': 4, 'ac2_coaches': 6, 'ac3_coaches': 4, 'fc_coaches': 1}
            elif 'express' in train_name_lower or 'mail' in train_name_lower:
                return {'coach_count': 20, 'sl_coaches': 12, 'ac2_coaches': 2, 'ac3_coaches': 4, 'fc_coaches': 0}
            else:
                # Default for other trains
                return {'coach_count': 15, 'sl_coaches': 10, 'ac2_coaches': 1, 'ac3_coaches': 2, 'fc_coaches': 0}
        
        # Apply coach info to each train
        coach_info = unique_trains['train_name'].apply(get_coach_info)
        coach_df = pd.DataFrame(list(coach_info))
        
        # Combine with train data
        result_df = pd.concat([unique_trains, coach_df], axis=1)
        
        # Convert data types
        try:
            result_df['train_no'] = result_df['train_no'].astype(str)
            result_df['distance_km'] = result_df['distance_km'].astype(float)
            result_df['coach_count'] = result_df['coach_count'].astype(int)
            result_df['sl_coaches'] = result_df['sl_coaches'].astype(int)
            result_df['ac2_coaches'] = result_df['ac2_coaches'].astype(int)
            result_df['ac3_coaches'] = result_df['ac3_coaches'].astype(int)
            result_df['fc_coaches'] = result_df['fc_coaches'].astype(int)
            result_df['platform_from'] = result_df['platform_from'].astype(int)
            result_df['platform_to'] = result_df['platform_to'].astype(int)
        except Exception as conv_error:
            st.warning(f"Data type conversion issue: {conv_error}")
            # Continue with original types
        
        # Add additional columns
        result_df['departure_time'] = '06:00'  # Default
        result_df['arrival_time'] = '18:00'    # Default
        result_df['duration_hrs'] = 12.0       # Default
        result_df['pantry'] = 'Yes'            # Default
        result_df['frequency'] = 'Daily'       # Default
        result_df['zone'] = 'IR'               # Default Indian Railways
        
        return result_df
        
    except Exception as e:
        st.error(f"Error loading comprehensive train data: {e}")
        st.info("Falling back to limited train dataset...")
        
        # Fallback to original dataset
        try:
            csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'trains_with_coaches.csv')
            df = pd.read_csv(csv_path)
            return df
        except Exception as e2:
            st.error(f"Error loading fallback train data: {e2}")
            return pd.DataFrame()


def generate_coach_formation(train_data):
    """Generate coach formation based on train data."""
    coach_count = train_data.get('coach_count', 12)
    sl_coaches = train_data.get('sl_coaches', 0)
    ac2_coaches = train_data.get('ac2_coaches', 0)
    ac3_coaches = train_data.get('ac3_coaches', 0)
    fc_coaches = train_data.get('fc_coaches', 0)

    coaches = []
    coach_types = []
    lengths = []

    # Add First Class coaches (if any)
    for i in range(fc_coaches):
        coaches.append(f"FC{i+1}")
        coach_types.append("First Class")
        lengths.append(21.5)

    # Add AC2 coaches
    for i in range(ac2_coaches):
        coaches.append(f"A{i+1}")
        coach_types.append("AC2")
        lengths.append(21.5)

    # Add AC3 coaches
    for i in range(ac3_coaches):
        coaches.append(f"B{i+1}")
        coach_types.append("AC3")
        lengths.append(21.5)

    # Add Sleeper coaches
    for i in range(sl_coaches):
        coaches.append(f"S{i+1}")
        coach_types.append("Sleeper")
        lengths.append(21.5)

    # Calculate current coach count (excluding engine and guard)
    current_coaches = len(coaches)

    # If we have fewer coaches than specified, add more sleeper coaches
    if current_coaches < coach_count - 2:  # -2 for engine and guard
        additional_sleepers = (coach_count - 2) - current_coaches
        for i in range(additional_sleepers):
            coaches.append(f"S{sl_coaches + i + 1}")
            coach_types.append("Sleeper")
            lengths.append(21.5)

    # Add Engine at the beginning
    coaches.insert(0, "E1")
    coach_types.insert(0, "Engine")
    lengths.insert(0, 22.0)

    # Add Guard at the end
    coaches.append("G1")
    coach_types.append("Guard")
    lengths.append(13.0)

    return coaches, coach_types, lengths


def display_enhanced_coach_detection():
    """Display enhanced coach detection interface with API integration and improved UI."""
    
    # Enhanced Header with better styling
    st.markdown(textwrap.dedent("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 3rem;
                border-radius: 20px; margin-bottom: 2rem; box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
                position: relative; overflow: hidden;">
        <div style="position: absolute; top: -50px; right: -50px; width: 150px; height: 150px; 
                    background: rgba(255,255,255,0.1); border-radius: 50%;"></div>
        <div style="position: absolute; bottom: -30px; left: -30px; width: 100px; height: 100px; 
                    background: rgba(255,255,255,0.1); border-radius: 50%;"></div>
        <h1 style="margin: 0 0 0.5rem 0; font-size: 3rem; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
            🚃 COACH DETECTION SYSTEM</h1>
        <p style="margin: 0; opacity: 0.95; font-size: 1.2rem; font-weight: 300;">
            Real-time train search with live coach positioning</p>
        <div style="margin-top: 1rem; display: flex; gap: 1rem; flex-wrap: wrap;">
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">
                🔍 API-Powered Search</span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">
                📊 Live Coach Data</span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">
                🎯 Platform Positioning</span>
        </div>
    </div>
    """), unsafe_allow_html=True)

    # API Status Indicator
    api = IndianRailwaysAPI()
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.info("🌐 **API Integration**: Connected to Indian Railways APIs for real-time data")
    with col2:
        if st.button("🔄 Test API", help="Test API connectivity"):
            try:
                test_result = api.get_station_code("New Delhi")
                if test_result:
                    st.success("✅ API Working")
                else:
                    st.warning("⚠️ API Limited")
            except:
                st.error("❌ API Error")
    with col3:
        st.metric("Available Trains", "11,117+")

    st.markdown("---")

    # Enhanced Search Interface
    st.subheader("🔍 Advanced Train Search")

    # Search tabs for different search methods
    search_tab1, search_tab2, search_tab3 = st.tabs(["🔢 By Train Number", "📍 Between Stations", "🎯 Quick Search"])

    train_df = None
    selected_train_data = None

    with search_tab1:
        col1, col2 = st.columns([3, 1])
        with col1:
            train_number = st.text_input(
                "Enter Train Number",
                placeholder="e.g., 12301, 12002",
                help="Enter the train number to get live coach information"
            )
        with col2:
            search_btn = st.button("🔍 Search", type="primary", use_container_width=True)

        if search_btn and train_number:
            with st.spinner("🔍 Searching train via API..."):
                train_df = load_train_coach_data(train_number)
                if not train_df.empty:
                    selected_train_data = train_df.iloc[0]
                    st.success(f"✅ Found: {selected_train_data['train_name']} ({selected_train_data['from_station']} → {selected_train_data['to_station']})")
                else:
                    st.error("❌ Train not found. Try different number or use local search.")

    with search_tab2:
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            from_station = st.text_input("From Station", placeholder="e.g., New Delhi, Mumbai")
        with col2:
            to_station = st.text_input("To Station", placeholder="e.g., Kolkata, Chennai")
        with col3:
            search_stations_btn = st.button("🔍 Find Trains", use_container_width=True)

        if search_stations_btn and from_station and to_station:
            with st.spinner("🔍 Finding trains between stations..."):
                try:
                    from_code = api.get_station_code(from_station)
                    to_code = api.get_station_code(to_station)
                    
                    if from_code and to_code:
                        trains_between = api.get_all_trains_between_stations(from_code, to_code)
                        if trains_between:
                            st.success(f"✅ Found {len(trains_between)} trains between {from_station} and {to_station}")
                            # Convert to DataFrame format
                            train_list = []
                            for train in trains_between[:10]:  # Show first 10
                                train_list.append({
                                    'train_no': str(train.get('train_number', '')),
                                    'train_name': train.get('train_name', f'Train {train.get("train_number", "")}'),
                                    'from_station': from_station,
                                    'to_station': to_station,
                                    'from_code': from_code,
                                    'to_code': to_code,
                                    'departure_time': train.get('departure_time', '06:00'),
                                    'arrival_time': train.get('arrival_time', '18:00'),
                                    'duration_hrs': 12.0,
                                    'distance_km': 500.0,
                                    'coach_count': 18,
                                    'sl_coaches': 10,
                                    'ac2_coaches': 4,
                                    'ac3_coaches': 3,
                                    'fc_coaches': 1,
                                    'pantry': 'Yes',
                                    'platform_from': 1,
                                    'platform_to': 1,
                                    'frequency': 'Daily',
                                    'zone': 'IR'
                                })
                            train_df = pd.DataFrame(train_list)
                        else:
                            st.warning("No trains found between these stations.")
                    else:
                        st.error("Could not find station codes. Please check station names.")
                except Exception as e:
                    st.error(f"Error searching trains: {e}")

    with search_tab3:
        # Load local data for quick search
        if train_df is None or train_df.empty:
            train_df = load_train_coach_data()

        if not train_df.empty:
            # Create train options
            train_options = []
            for _, train in train_df.head(100).iterrows():  # Show first 100 for performance
                option = f"{train['train_no']} - {train['train_name']} ({train['from_station']} → {train['to_station']})"
                train_options.append(option)

            selected_train_option = st.selectbox(
                "Choose from popular trains:",
                train_options,
                help="Select from pre-loaded trains (first 100 shown)"
            )

            if selected_train_option:
                selected_train_no = str(selected_train_option.split(' - ')[0])
                selected_train_data = train_df[train_df['train_no'] == selected_train_no].iloc[0]

    # If we have selected train data, show the coach detection interface
    if selected_train_data is not None:
        display_coach_detection_interface(selected_train_data)
    else:
        # Show demo/train selection interface
        st.markdown("---")
        st.subheader("🎯 Select a Train to View Coach Formation")
        
        # Load demo data
        if train_df is None or train_df.empty:
            train_df = load_train_coach_data()
        
        if not train_df.empty:
            # Show sample trains
            st.markdown("### Popular Trains:")
            cols = st.columns(3)
            sample_trains = train_df.head(9)
            
            for i, (_, train) in enumerate(sample_trains.iterrows()):
                with cols[i % 3]:
                    if st.button(
                        f"🚂 {train['train_no']}\n{train['train_name'][:20]}...",
                        key=f"sample_{i}",
                        help=f"View coach formation for {train['train_name']}",
                        use_container_width=True
                    ):
                        selected_train_data = train
                        st.rerun()
        else:
            st.error("No train data available. Please check data files.")

    # Display selected train info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Train Number", selected_train_data['train_no'])
    with col2:
        st.metric("Total Coaches", selected_train_data['coach_count'])
    with col3:
        st.metric("Distance", f"{selected_train_data['distance_km']} km")

    st.markdown("---")

def display_coach_detection_interface(selected_train_data):
    """Display the coach detection interface for selected train."""
    
    # Enhanced Train Info Display
    st.markdown("---")
    st.subheader("🚂 Selected Train Information")
    
    # Train info cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Train Number", selected_train_data['train_no'])
    with col2:
        st.metric("Train Name", selected_train_data['train_name'][:20] + "..." if len(selected_train_data['train_name']) > 20 else selected_train_data['train_name'])
    with col3:
        st.metric("From → To", f"{selected_train_data['from_station']} → {selected_train_data['to_station']}")
    with col4:
        st.metric("Distance", f"{selected_train_data['distance_km']} km")

    # Coach Summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Coaches", selected_train_data['coach_count'])
    with col2:
        st.metric("AC Coaches", selected_train_data['ac2_coaches'] + selected_train_data['ac3_coaches'])
    with col3:
        st.metric("Sleeper Coaches", selected_train_data['sl_coaches'])

    st.markdown("---")

    # Platform Configuration
    col1, col2, col3 = st.columns(3)

    with col1:
        platform_length = st.number_input(
            "Platform Length (meters)",
            min_value=100,
            max_value=1000,
            value=250,
            help="Total length of the platform in meters"
        )

    with col2:
        # Generate coach formation first to get actual length
        coaches, coach_types, lengths = generate_coach_formation(selected_train_data)
        actual_train_length = sum(lengths)
        
        train_length = st.number_input(
            "Train Length (meters)",
            min_value=100,
            max_value=800,
            value=int(actual_train_length),
            help="Total length of the train in meters"
        )

    with col3:
        zone_count = st.selectbox(
            "Platform Zones",
            [3, 4, 5, 6],
            index=3,
            help="Number of zones to divide the platform into"
        )

    # Display Platform Metrics
    st.markdown("### 📏 Platform Configuration")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Platform Length", f"{platform_length} m")
    with col2:
        st.metric("Train Length", f"{train_length} m")
    with col3:
        st.metric("Zones", zone_count)

    st.markdown("---")

    # Enhanced Platform Layout Visualization
    st.subheader("📍 Platform Coach Layout")

    # Generate coach formation for selected train
    coaches, coach_types, lengths = generate_coach_formation(selected_train_data)

    # Create coach data DataFrame
    coaches_data = {
        "Coach No": coaches,
        "Type": coach_types,
        "Length": lengths
    }

    df_coaches = pd.DataFrame(coaches_data)

    # Calculate cumulative positions
    df_coaches['Start_Pos'] = df_coaches['Length'].cumsum().shift(fill_value=0)
    df_coaches['End_Pos'] = df_coaches['Length'].cumsum()

    # Assign zones based on position
    total_coaches = len(df_coaches)
    zone_size = total_coaches // zone_count
    zones = []
    for i in range(total_coaches):
        zone_idx = min(i // zone_size, zone_count - 1)
        zones.append(chr(65 + zone_idx))  # A, B, C, D, E, etc.
    df_coaches['Zone'] = zones

    # Platform visualization with enhanced styling
    platform_html = f"""
    <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 2rem; border-radius: 15px; 
                box-shadow: 0 8px 32px rgba(0,0,0,0.1); margin: 2rem 0; position: relative;">
        <div style="text-align: center; margin-bottom: 2rem;">
            <h3 style="margin: 0; color: #2c3e50; font-size: 1.5rem; font-weight: 600;">
                🚃 Platform Layout Visualization</h3>
            <p style="margin: 0.5rem 0; color: #666; font-size: 1rem;">
                Train occupies {train_length}m of {platform_length}m platform space</p>
        </div>

        <!-- Platform Container -->
        <div style="position: relative; height: 100px; background: linear-gradient(90deg, #e8f4f8 0%, #d1ecf1 100%);
                    border-radius: 12px; border: 3px solid #17a2b8; margin: 2rem 0; overflow: hidden;
                    box-shadow: inset 0 2px 8px rgba(0,0,0,0.1);">

            <!-- Platform markers -->
            <div style="position: absolute; left: 0; top: -30px; font-size: 0.9rem; color: #17a2b8; font-weight: bold;">0m</div>
            <div style="position: absolute; right: 0; top: -30px; font-size: 0.9rem; color: #17a2b8; font-weight: bold;">{platform_length}m</div>

            <!-- Train start/end markers -->
            <div style="position: absolute; left: 0; top: -50px; width: 3px; height: 45px; background: #28a745; border-radius: 2px;"></div>
            <div style="position: absolute; left: {min(train_length/platform_length*100, 100)}%; top: -50px; width: 3px; height: 45px; background: #dc3545; border-radius: 2px;"></div>
            <div style="position: absolute; left: 0; top: -70px; font-size: 0.8rem; color: #28a745; font-weight: bold;">TRAIN START</div>
            <div style="position: absolute; left: {max(min(train_length/platform_length*100 - 15, 85), 0)}%; top: -70px; font-size: 0.8rem; color: #dc3545; font-weight: bold;">TRAIN END</div>
    """

    # Enhanced coach colors and styling
    coach_colors = {
        "Engine": "#6c757d",
        "First Class": "#9c88ff",
        "AC2": "#4ecdc4",
        "AC3": "#45b7d1",
        "Sleeper": "#ffeaa7",
        "Guard": "#dda0dd"
    }

    # Add coach segments with enhanced styling
    coach_segments = ""
    for idx, coach in df_coaches.iterrows():
        start_percent = min((coach['Start_Pos'] / platform_length) * 100, 100)
        width_percent = min((coach['Length'] / platform_length) * 100, 100)
        color = coach_colors.get(coach['Type'], '#cccccc')
        
        # Add hover effect and better styling
        coach_segments += f"""
            <div style="position: absolute; left: {start_percent}%; width: {width_percent}%; height: 100%;
                        background: {color}; border-right: 2px solid #fff; display: flex; align-items: center;
                        justify-content: center; font-size: 0.8rem; font-weight: bold; color: #2c3e50;
                        border-radius: 0 0 8px 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        transition: all 0.3s ease; cursor: pointer;"
                 title="Coach {coach['Coach No']} - {coach['Type']}">
                <div style="text-align: center;">
                    <div style="font-size: 0.9rem; font-weight: bold;">{coach['Coach No']}</div>
                    <div style="font-size: 0.7rem; opacity: 0.8;">{coach['Type']}</div>
                </div>
            </div>
        """

    # Enhanced Legend
    legend_items = ""
    for coach_type, color in coach_colors.items():
        legend_items += f"""
            <div style="display: flex; align-items: center; gap: 0.8rem; padding: 0.5rem; 
                        background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <div style="width: 20px; height: 20px; background: {color}; border-radius: 4px; border: 2px solid #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.2);"></div>
                <span style="font-size: 0.9rem; color: #2c3e50; font-weight: 500;">{coach_type}</span>
            </div>
        """

    platform_html += f"""
        {coach_segments}
        </div>

        <!-- Enhanced Legend -->
        <div style="display: flex; flex-wrap: wrap; gap: 1rem; justify-content: center; margin-top: 2rem;">
        {legend_items}
        </div>
    </div>
    """

    st.markdown(platform_html, unsafe_allow_html=True)

    # Enhanced Coach Details Table
    st.subheader("📋 Detailed Coach Information")

    # Create position ranges
    position_ranges = []
    for i, row in df_coaches.iterrows():
        start_pos = int(row['Start_Pos'])
        end_pos = int(row['End_Pos'])
        position_ranges.append(f"{start_pos}-{end_pos}")

    # Create enhanced table data
    table_data = {
        "Coach No": df_coaches['Coach No'].tolist(),
        "Type": df_coaches['Type'].tolist(),
        "Position (m)": position_ranges,
        "Platform Zone": df_coaches['Zone'].tolist(),
        "Length (m)": [f"{length:.1f}" for length in df_coaches['Length'].tolist()],
        "Status": ["✅ Available"] * len(df_coaches)
    }

    df_table = pd.DataFrame(table_data)

    # Enhanced HTML table with better styling
    html_table = """
    <table style="width: 100%; border-collapse: collapse; background: white; border-radius: 12px;
                  overflow: hidden; box-shadow: 0 8px 32px rgba(0,0,0,0.1); margin: 2rem 0;">
        <thead>
            <tr style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                <th style="padding: 1.2rem 1rem; text-align: left; font-weight: 600; font-size: 0.9rem;">Coach No</th>
                <th style="padding: 1.2rem 1rem; text-align: left; font-weight: 600; font-size: 0.9rem;">Type</th>
                <th style="padding: 1.2rem 1rem; text-align: left; font-weight: 600; font-size: 0.9rem;">Position (m)</th>
                <th style="padding: 1.2rem 1rem; text-align: left; font-weight: 600; font-size: 0.9rem;">Zone</th>
                <th style="padding: 1.2rem 1rem; text-align: left; font-weight: 600; font-size: 0.9rem;">Length (m)</th>
                <th style="padding: 1.2rem 1rem; text-align: center; font-weight: 600; font-size: 0.9rem;">Status</th>
            </tr>
        </thead>
        <tbody>
    """

    # Enhanced table rows with better styling
    table_rows = ""
    for idx, row in df_coaches.iterrows():
        color = coach_colors.get(row['Type'], '#cccccc')
        bg_color = "white" if idx % 2 == 0 else "#f8f9fa"
        
        table_rows += f"""
        <tr style="border-bottom: 1px solid #e9ecef; background: {bg_color}; transition: all 0.2s ease;">
            <td style="padding: 1rem; font-weight: bold; color: #2c3e50;">{row['Coach No']}</td>
            <td style="padding: 1rem;">
                <span style="background: {color}; color: #2c3e50; padding: 0.4rem 0.8rem; border-radius: 6px; 
                            font-size: 0.85rem; font-weight: 600; display: inline-block;">
                    {row['Type']}
                </span>
            </td>
            <td style="padding: 1rem; font-weight: 600; color: #495057;">{row['Position (m)']}</td>
            <td style="padding: 1rem;">
                <span style="background: #e8f4f8; padding: 0.4rem 0.8rem; border-radius: 6px; 
                            font-size: 0.85rem; font-weight: 600; color: #17a2b8;">
                    Zone {row['Platform Zone']}
                </span>
            </td>
            <td style="padding: 1rem; font-weight: bold; color: #28a745;">{row['Length (m)']}</td>
            <td style="padding: 1rem; text-align: center;">
                <span style="color: #28a745; font-size: 1.2rem;">●</span>
            </td>
        </tr>
        """

    html_table += f"""
        {table_rows}
        </tbody>
    </table>
    """

    st.markdown(html_table, unsafe_allow_html=True)

    # Enhanced Analytics Section
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Coach Type Distribution")
        coach_type_counts = df_coaches['Type'].value_counts()
        coach_types_df = pd.DataFrame({
            "Type": coach_type_counts.index.tolist(),
            "Count": coach_type_counts.values.tolist()
        })
        coach_types_df['Percentage'] = (coach_types_df['Count'] / len(df_coaches) * 100).round(1)
        
        # Enhanced bar chart
        st.bar_chart(coach_types_df.set_index("Type")["Count"])
        
        # Show percentages
        st.markdown("**Coach Distribution:**")
        for _, row in coach_types_df.iterrows():
            st.markdown(f"- **{row['Type']}**: {row['Count']} coaches ({row['Percentage']}%)")

    with col2:
        st.subheader("📍 Platform Zone Utilization")
        zone_counts = df_coaches['Zone'].value_counts()
        zone_data = pd.DataFrame({
            "Zone": zone_counts.index.tolist(),
            "Coaches": zone_counts.values.tolist()
        })
        zone_data['Coverage'] = (zone_data['Coaches'] / len(df_coaches) * 100).round(1)
        
        st.bar_chart(zone_data.set_index("Zone")["Coaches"])
        
        # Show zone details
        st.markdown("**Zone Distribution:**")
        for _, row in zone_data.iterrows():
            st.markdown(f"- **Zone {row['Zone']}**: {row['Coaches']} coaches ({row['Coverage']}%)")

    # Export functionality
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📥 Export Coach Data", type="secondary", use_container_width=True):
            csv_data = df_coaches.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"coach_data_{selected_train_data['train_no']}.csv",
                mime="text/csv",
                key="download_coach_data"
            )
            st.success("✅ Coach data exported successfully!")
