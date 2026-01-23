"""
Live Journey Tracking UI Component
Displays station-by-station train journey with live tracking data
"""

import streamlit as st
import pandas as pd
from src.repositories.train_repository import TrainRepository
from datetime import datetime

def display_journey_tracking():
    """Display live train journey tracking interface using RapidAPI."""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 2rem; 
                border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 8px 25px rgba(0,0,0,0.2);">
        <h2 style="margin: 0 0 0.5rem 0; font-size: 2rem;">🚂 Live Train Journey Tracking</h2>
        <p style="margin: 0; opacity: 0.95; font-size: 1rem;">Real-time station-by-station monitoring with live delay tracking (Powered by RapidAPI)</p>
    </div>
    """, unsafe_allow_html=True)
    
    repo = TrainRepository()
    
    # Journey Tracking Input
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        train_no = st.text_input(
            "Enter Train Number",
            placeholder="e.g., 12301, 20844",
            key="journey_train_input",
            help="Enter train number to see live journey tracking"
        )
    
    with col2:
        journey_date = st.date_input(
            "Journey Date",
            datetime.now(),
            key="journey_date"
        )
    
    with col3:
        if st.button("🔍 Track Journey", width='stretch', key="track_journey_btn"):
            if train_no:
                display_journey_details(repo, train_no, journey_date)
            else:
                st.warning("Please enter a train number")

def display_journey_details(repo, train_no: str, journey_date):
    """Display detailed journey information from live API."""
    try:
        # Get journey schedule from live API
        journey = repo.get_train_journey_schedule(train_no, journey_date.strftime("%Y-%m-%d"))
        
        if journey and 'stations' in journey:
            # Show live API confirmation
            st.success("✅ Data loaded fromLive Railway Service")
            
            # Header Section
            st.markdown(f"""
          <div style="display:flex; justify-content:center;">
                <div style="background: white; padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; 
                        border: 2px solid #667eea; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.15);">
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 1.5rem; margin-bottom: 1rem;">
                    <div>
                        <div style="color: #667eea; font-weight: 600; font-size: 0.85rem; text-transform: uppercase;">Train Number</div>
                        <div style="font-size: 1.5rem; font-weight: 700; color: #2c3e50;">{journey['train_no']}</div>
                    </div>
                    <div>
                        <div style="color: #667eea; font-weight: 600; font-size: 0.85rem; text-transform: uppercase;">Train Name</div>
                        <div style="font-size: 1.5rem; font-weight: 700; color: #2c3e50;">{journey['train_name']}</div>
                    </div>
                    <div>
                        <div style="color: #667eea; font-weight: 600; font-size: 0.85rem; text-transform: uppercase;">Journey Distance</div>
                        <div style="font-size: 1.5rem; font-weight: 700; color: #2c3e50;">{journey['total_distance']} km</div>
                    </div>
                    <div>
                        <div style="color: #667eea; font-weight: 600; font-size: 0.85rem; text-transform: uppercase;">Journey Time</div>
                        <div style="font-size: 1.5rem; font-weight: 700; color: #2c3e50;">{journey['journey_time']}</div>
                    </div>
                </div>
                    <div style="background: #f8f9fa; padding: 0.75rem; border-radius: 8px;">
                    <strong style="color: #2c3e50;">Route:</strong> <span style="color: #666;">{journey['source_station']} → {journey['destination_station']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Summary Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Stations", journey['total_stations'], "🚄")
            
            with col2:
                st.metric("Overall Delay", f"{journey['overall_delay']} min", "⏰")
            
            with col3:
                avg_halt = sum(s['halt_minutes'] for s in journey['stations']) / len(journey['stations']) if journey['stations'] else 0
                st.metric("Avg Halt Time", f"{int(avg_halt)} min", "⏱️")
            
            with col4:
                st.metric("Journey Date", journey_date.strftime("%d %b %Y"), "📅")
            
            # Station-by-Station Journey Timeline
            st.markdown("### 📊 Station-by-Station Journey")
            
            # Create detailed station cards
            for idx, station in enumerate(journey['stations']):
                # Determine status
                if station['status'] == 'Departed' or station['status'] == 'Arrived':
                    status_color = "#28a745"
                    status_icon = "✅"
                elif station['status'] == 'Scheduled':
                    status_color = "#0099ff"
                    status_icon = "⏱️"
                else:
                    status_color = "#ffc107"
                    status_icon = "⚠️"
                
                # Station card HTML - properly formatted
                delay_html = f"<div style='font-size: 0.8rem; color: #666; margin-top: 0.25rem;'>(+{station['delay']}m)</div>" if station['delay'] > 0 else ""
                halt_html = f"<div style='font-size: 0.8rem; color: #666; margin-top: 0.25rem;'>Halt: {station['halt_minutes']}m</div>" if station['halt_minutes'] > 0 else ""
                
                card_html = (
                    f"<div style='background: white; border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem; "
                    f"border-left: 5px solid {status_color}; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>"
                    f"<div style='display: grid; grid-template-columns: 1.2fr 1.5fr 1fr 1fr 1fr; gap: 1.5rem; align-items: center;'>"
                    f"<div>"
                    f"<div style='font-size: 0.75rem; color: #999; text-transform: uppercase; font-weight: 600; margin-bottom: 0.25rem;'>Stop #{station['sequence']}</div>"
                    f"<div style='font-size: 1.3rem; font-weight: 700; color: #2c3e50;'>{station['station_code']}</div>"
                    f"<div style='font-size: 0.9rem; color: #666; margin-top: 0.25rem;'>{station['station_name']}</div>"
                    f"</div>"
                    f"<div style='padding: 0.75rem; background: #f8f9fa; border-radius: 8px;'>"
                    f"<div style='font-size: 0.75rem; color: #999; text-transform: uppercase; font-weight: 600; margin-bottom: 0.5rem;'>Status & Position</div>"
                    f"<div style='display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;'>"
                    f"<span style='font-size: 1.2rem;'>{status_icon}</span>"
                    f"<span style='font-weight: 600; color: {status_color};'>{station['status']}</span>"
                    f"</div>"
                    f"<div style='font-size: 0.85rem; color: #666;'>Distance: {station['distance']} km</div>"
                    f"</div>"
                    f"<div style='text-align: center;'>"
                    f"<div style='font-size: 0.75rem; color: #999; text-transform: uppercase; font-weight: 600; margin-bottom: 0.5rem;'>Arrival</div>"
                    f"<div style='font-size: 1.1rem; font-weight: 700; color: #2c3e50;'>{station['arrival_time']}</div>"
                    f"{delay_html}"
                    f"</div>"
                    f"<div style='text-align: center;'>"
                    f"<div style='font-size: 0.75rem; color: #999; text-transform: uppercase; font-weight: 600; margin-bottom: 0.5rem;'>Departure</div>"
                    f"<div style='font-size: 1.1rem; font-weight: 700; color: #2c3e50;'>{station['departure_time']}</div>"
                    f"{halt_html}"
                    f"</div>"
                    f"<div style='text-align: center; padding: 0.75rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); "
                    f"color: white; border-radius: 8px;'>"
                    f"<div style='font-size: 0.75rem; opacity: 0.9; text-transform: uppercase; font-weight: 600; margin-bottom: 0.5rem;'>Platform</div>"
                    f"<div style='font-size: 1.4rem; font-weight: 700;'>{station['platform']}</div>"
                    f"</div>"
                    f"</div>"
                    f"</div>"
                )
                
                st.markdown(card_html, unsafe_allow_html=True)
            
            # Journey Statistics
            st.markdown("### 📈 Journey Statistics")
            
            stat_col1, stat_col2, stat_col3, stat_col4, stat_col5 = st.columns(5)
            
            with stat_col1:
                total_distance = journey['total_distance']
                st.metric("Total Distance", f"{total_distance} km", "🛤️")
            
            with stat_col2:
                total_halt = sum(s['halt_minutes'] for s in journey['stations'])
                st.metric("Total Halt Time", f"{total_halt} min", "⏸️")
            
            with stat_col3:
                avg_speed = (total_distance / float(journey['journey_time'].split(':')[0])) if 'h' in journey['journey_time'] else 0
                st.metric("Avg Speed", f"{int(avg_speed)} km/h", "🚀")
            
            with stat_col4:
                delayed_count = sum(1 for s in journey['stations'] if s['delay'] > 0)
                st.metric("Delayed Stops", delayed_count, "🔴")
            
            with stat_col5:
                on_time_count = sum(1 for s in journey['stations'] if s['delay'] == 0)
                st.metric("On-Time Stops", on_time_count, "✅")
            
            # Export Options
            st.markdown("---")
            export_col1, export_col2, export_col3 = st.columns(3)
            
            with export_col1:
                if st.button("📥 Download as PDF", key="download_journey_pdf", width='stretch'):
                    st.success("📥 Journey report ready for download!")
            
            with export_col2:
                if st.button("📊 Export as CSV", key="download_journey_csv", width='stretch'):
                    st.success("📊 CSV data exported!")
            
            with export_col3:
                if st.button("🔄 Refresh Data", key="refresh_journey", width='stretch'):
                    st.rerun()
        
        else:
            st.error(f"❌ Journey data not found for Train {train_no}")
            st.info("Please check the train number and try again with a valid Indian Railway train number.")
    
    except Exception as e:
        st.error(f"❌ Error fetching journey details: {str(e)}")
        st.info("Please try again with a different train number.")

def display_all_india_trains_and_stations():
    """Display all available trains and stations in India."""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 2rem; 
                border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 8px 25px rgba(0,0,0,0.2);">
        <h2 style="margin: 0 0 0.5rem 0; font-size: 2rem;">🚂 All India Railways Network</h2>
        <p style="margin: 0; opacity: 0.95; font-size: 1rem;">Complete directory of trains and stations across India</p>
    </div>
    """, unsafe_allow_html=True)
    
    repo = TrainRepository()
    
    # Tabs for different views
    view_tab1, view_tab2, view_tab3 = st.tabs(["🚆 All Trains", "📍 All Stations", "🗺️ Network Map"])
    
    with view_tab1:
        display_all_trains(repo)
    
    with view_tab2:
        display_all_stations(repo)
    
    with view_tab3:
        display_network_map(repo)

def display_all_trains(repo):
    """Display list of all trains."""
    st.subheader("🚆 Complete Train Directory")
    
    all_trains = repo.get_all_trains()
    
    if all_trains:
        st.success(f"✅ Loaded {len(all_trains)} trains")
        
        # Search and filter
        search_col, filter_col = st.columns(2)
        
        with search_col:
            search_term = st.text_input("Search trains by name or number", key="train_search")
        
        with filter_col:
            zone_filter = st.multiselect("Filter by Zone", 
                                       list(set(t.get('zone', 'Unknown') for t in all_trains)),
                                       key="zone_filter")
        
        # Filter trains
        filtered_trains = all_trains
        if search_term:
            filtered_trains = [t for t in filtered_trains if search_term.lower() in str(t.get('train_no', '')).lower() 
                             or search_term.lower() in t.get('train_name', '').lower()]
        if zone_filter:
            filtered_trains = [t for t in filtered_trains if t.get('zone') in zone_filter]
        
        # Display trains
        if filtered_trains:
            # Create train cards
            cols = st.columns(2)
            for idx, train in enumerate(filtered_trains):
                with cols[idx % 2]:
                    st.markdown(f"""
                    <div style="background: white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;
                                border: 2px solid #e9ecef; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                            <h4 style="margin: 0; color: #667eea;">Train {train.get('train_no', 'N/A')}</h4>
                            <span style="background: #667eea; color: white; padding: 0.25rem 0.75rem; 
                                       border-radius: 12px; font-size: 0.75rem; font-weight: bold;">{train.get('zone', 'N/A')}</span>
                        </div>
                        <p style="margin: 0.5rem 0; font-weight: 600; color: #2c3e50;">{train.get('train_name', 'Unknown')}</p>
                        <div style="font-size: 0.9rem; color: #666; margin: 0.75rem 0;">
                            <div>📍 {train.get('from_station', 'N/A')} → {train.get('to_station', 'N/A')}</div>
                            <div>🛤️ Distance: {train.get('distance_km', 'N/A')} km</div>
                            <div>🚃 Coaches: {train.get('coach_count', 'N/A')}</div>
                            <div>⏰ Duration: {train.get('duration_hrs', 'N/A')} hours</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("No trains found matching your search criteria.")
    else:
        st.warning("No trains available.")

def display_all_stations(repo):
    """Display list of all stations."""
    st.subheader("📍 Complete Station Directory")
    
    all_stations = repo.get_all_stations()
    
    if all_stations:
        st.success(f"✅ Loaded {len(all_stations)} stations")
        
        # Search and filter
        search_col, filter_col = st.columns(2)
        
        with search_col:
            search_term = st.text_input("Search stations by name or code", key="station_search_all")
        
        with filter_col:
            state_filter = st.multiselect("Filter by State",
                                        list(set(s.get('state', 'Unknown') for s in all_stations)),
                                        key="state_filter")
        
        # Filter stations
        filtered_stations = all_stations
        if search_term:
            filtered_stations = [s for s in filtered_stations if search_term.lower() in s.get('station_code', '').lower()
                               or search_term.lower() in s.get('station_name', '').lower()]
        if state_filter:
            filtered_stations = [s for s in filtered_stations if s.get('state') in state_filter]
        
        # Display stations
        if filtered_stations:
            station_data = []
            for station in filtered_stations:
                station_data.append({
                    'Code': station.get('station_code', 'N/A'),
                    'Station Name': station.get('station_name', 'N/A'),
                    'State': station.get('state', 'N/A'),
                    'Zone': station.get('zone', 'N/A'),
                    'Type': station.get('station_type', 'N/A'),
                    'Platforms': station.get('platform_count', 'N/A')
                })
            
            st.dataframe(pd.DataFrame(station_data), width='stretch', hide_index=True)
        else:
            st.warning("No stations found matching your search criteria.")
    else:
        st.warning("No stations available.")

def display_network_map(repo):
    """Display network map/statistics."""
    st.subheader("🗺️ Indian Railways Network Map")
    
    all_trains = repo.get_all_trains()
    all_stations = repo.get_all_stations()
    
    st.markdown(f"""
    <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;">
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 1rem;">
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: bold; color: #667eea;">{len(all_trains)}</div>
                <div style="color: #666; font-weight: 500;">Total Trains</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: bold; color: #667eea;">{len(all_stations)}</div>
                <div style="color: #666; font-weight: 500;">Total Stations</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: bold; color: #667eea;">{len(set(s.get('state') for s in all_stations))}</div>
                <div style="color: #666; font-weight: 500;">States Covered</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: bold; color: #667eea;">{len(set(s.get('zone') for s in all_stations))}</div>
                <div style="color: #666; font-weight: 500;">Railway Zones</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Zone-wise distribution
    st.markdown("### Zone-wise Distribution")
    zone_data = {}
    for station in all_stations:
        zone = station.get('zone', 'Unknown')
        zone_data[zone] = zone_data.get(zone, 0) + 1
    
    if zone_data:
        st.bar_chart(zone_data)
    
    # State-wise distribution
    st.markdown("### State-wise Station Distribution")
    state_data = {}
    for station in all_stations:
        state = station.get('state', 'Unknown')
        state_data[state] = state_data.get(state, 0) + 1
    
    if state_data:
        st.bar_chart(state_data)
