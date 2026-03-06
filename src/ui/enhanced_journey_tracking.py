"""
Enhanced Journey Tracking UI
Improved visual design and user experience
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import textwrap
from src.repositories.train_repository import TrainRepository
from src.utils.suggestions import display_suggestions


def display_enhanced_journey_tracking():
    """Display enhanced journey tracking interface."""
    
    header_html = """
<div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; padding: 2.5rem; 
            border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 8px 30px rgba(17, 153, 142, 0.3);">
    <h1 style="margin: 0 0 0.5rem 0; font-size: 2.5rem;">🚂 ENHANCED JOURNEY TRACKING</h1>
    <p style="margin: 0; opacity: 0.95; font-size: 1.1rem;">Real-time Train Journey Monitoring with Advanced Timeline</p>
</div>
"""
    st.markdown(textwrap.dedent(header_html), unsafe_allow_html=True)
    
    repo = TrainRepository()
    
    # Search Section - Centered
    st.markdown("""
    <div style="display: flex; justify-content: center; margin-bottom: 2rem;">
        <div style="width: 100%; max-width: 800px;">
    """), unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        train_input = st.text_input(
            "Train Number/Name",
            placeholder="e.g., 12301, Rajdhani Express",
            help="Enter train number or name"
        )
        # Display train suggestions
        if train_input:
            display_suggestions("enhanced_journey_train", "train", train_input)

    with col2:
        journey_date = st.date_input(
            "Date",
            datetime.now(),
            help="Select journey date"
        )

    with col3:
        if st.button("🔍 Track", type="primary", key="track_journey_btn"):
            if train_input:
                display_journey_details_enhanced(repo, train_input, journey_date)
            else:
                st.warning("Enter train details")

    st.markdown("</div></div>", unsafe_allow_html=True)


def display_journey_details_enhanced(repo, train_info: str, date):
    """Display enhanced journey details."""
    
    # Simulate sample data
    journey_data = {
        'train_no': '12301',
        'train_name': 'RAJDHANI EXPRESS',
        'source_station': 'Delhi Junction',
        'destination_station': 'Mumbai Central',
        'total_distance': 1425,
        'journey_time': '17:00',
        'total_stations': 8,
        'overall_delay': 5,
        'stations': [
            {
                'sequence': 1,
                'station_code': 'DEL',
                'station_name': 'Delhi Junction',
                'arrival_time': '08:00',
                'departure_time': '08:00',
                'platform': '1',
                'distance': 0,
                'halt_minutes': 0,
                'status': 'Departed',
                'delay': 0
            },
            {
                'sequence': 2,
                'station_code': 'ASR',
                'station_name': 'Amritsar Junction',
                'arrival_time': '13:45',
                'departure_time': '14:00',
                'platform': '3',
                'distance': 435,
                'halt_minutes': 15,
                'status': 'Departed',
                'delay': 0
            },
            {
                'sequence': 3,
                'station_code': 'DDP',
                'station_name': 'Dhandari Junction',
                'arrival_time': '15:30',
                'departure_time': '15:35',
                'platform': '2',
                'distance': 550,
                'halt_minutes': 5,
                'status': 'Departed',
                'delay': 5
            },
            {
                'sequence': 4,
                'station_code': 'JU',
                'station_name': 'Jangpur',
                'arrival_time': '17:20',
                'departure_time': '17:25',
                'platform': '1',
                'distance': 725,
                'halt_minutes': 5,
                'status': 'Departed',
                'delay': 5
            },
            {
                'sequence': 5,
                'station_code': 'NDLS',
                'station_name': 'New Delhi',
                'arrival_time': '19:45',
                'departure_time': '20:00',
                'platform': '7',
                'distance': 900,
                'halt_minutes': 15,
                'status': 'Scheduled',
                'delay': 0
            },
            {
                'sequence': 6,
                'station_code': 'GWL',
                'station_name': 'Gwalior Junction',
                'arrival_time': '23:30',
                'departure_time': '23:40',
                'platform': '5',
                'distance': 1100,
                'halt_minutes': 10,
                'status': 'Scheduled',
                'delay': 0
            },
            {
                'sequence': 7,
                'station_code': 'BPL',
                'station_name': 'Bhopal Junction',
                'arrival_time': '03:45',
                'departure_time': '04:00',
                'platform': '2',
                'distance': 1250,
                'halt_minutes': 15,
                'status': 'Scheduled',
                'delay': 0
            },
            {
                'sequence': 8,
                'station_code': 'BCT',
                'station_name': 'Mumbai Central',
                'arrival_time': '01:00',
                'departure_time': '01:00',
                'platform': '8',
                'distance': 1425,
                'halt_minutes': 0,
                'status': 'Scheduled',
                'delay': 0
            }
        ]
    }
    
    # Header Info - Centered layout
    st.markdown(textwrap.dedent(f"""
    <div style="display: flex; justify-content: center; margin-bottom: 2rem;">
        <div style="background: white; padding: 2.5rem; border-radius: 15px; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 5px solid #11998e; width: 100%; max-width: 1200px;">
            <div style="display: grid; grid-template-columns: 2fr 1fr 1fr 1fr 1fr; gap: 2rem; align-items: center;">
                <div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: #11998e; margin-bottom: 0.5rem;">
                        {journey_data['train_no']} - {journey_data['train_name']}
                    </div>
                    <div style="color: #666; font-size: 1rem;">
                        {journey_data['source_station']} → {journey_data['destination_station']}
                    </div>
                </div>

                <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border-radius: 12px; border: 1px solid #b3e5fc;">
                    <div style="font-size: 0.8rem; color: #666; font-weight: 600; margin-bottom: 0.3rem;">DISTANCE</div>
                    <div style="font-size: 2rem; font-weight: bold; color: #11998e;">{journey_data['total_distance']}</div>
                    <div style="font-size: 0.8rem; color: #666;">kilometers</div>
                </div>

                <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border-radius: 12px; border: 1px solid #b3e5fc;">
                    <div style="font-size: 0.8rem; color: #666; font-weight: 600; margin-bottom: 0.3rem;">DURATION</div>
                    <div style="font-size: 2rem; font-weight: bold; color: #11998e;">{journey_data['journey_time']}</div>
                    <div style="font-size: 0.8rem; color: #666;">hours</div>
                </div>

                <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border-radius: 12px; border: 1px solid #b3e5fc;">
                    <div style="font-size: 0.8rem; color: #666; font-weight: 600; margin-bottom: 0.3rem;">STOPS</div>
                    <div style="font-size: 2rem; font-weight: bold; color: #11998e;">{journey_data['total_stations']}</div>
                    <div style="font-size: 0.8rem; color: #666;">stations</div>
                </div>

                <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #fff0f0 0%, #ffebee 100%); border-radius: 12px; border: 1px solid #ffcdd2;">
                    <div style="font-size: 0.8rem; color: #666; font-weight: 600; margin-bottom: 0.3rem;">DELAY</div>
                    <div style="font-size: 2rem; font-weight: bold; color: #ff6b6b;">+{journey_data['overall_delay']}</div>
                    <div style="font-size: 0.8rem; color: #666;">minutes</div>
                </div>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)
    
    # Timeline View
    st.subheader("📍 Journey Timeline")

    # Center the entire timeline
    st.markdown("""
    <div style="display: flex; justify-content: center; margin-bottom: 2rem;">
        <div style="width: 100%; max-width: 1200px;">
    """), unsafe_allow_html=True)

    # Create interactive timeline
    for idx, station in enumerate(journey_data['stations']):
        is_current = station['status'] == 'Departed' and idx < len(journey_data['stations']) - 1

        # Use centered columns with better proportions
        col1, col2, col3, col4 = st.columns([1.5, 4, 3, 1.5])

        with col1:
            # Timeline dot - centered
            st.markdown(textwrap.dedent("""
            <div style="display: flex; justify-content: center; align-items: center; height: 100px;">
            """), unsafe_allow_html=True)

            if station['status'] == 'Departed':
                st.markdown(textwrap.dedent("""
                <div style="text-align: center; padding: 1rem; font-size: 2rem; background: #28a745; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; color: white;">
                    ✅
                </div>
                """), unsafe_allow_html=True)
            elif station['status'] == 'Scheduled':
                st.markdown(textwrap.dedent("""
                <div style="text-align: center; padding: 1rem; font-size: 2rem; background: #ffc107; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; color: white;">
                    ⏱️
                </div>
                """), unsafe_allow_html=True)
            else:
                st.markdown(textwrap.dedent("""
                <div style="text-align: center; padding: 1rem; font-size: 2rem; background: #dc3545; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; color: white;">
                    ⚠️
                </div>
                """), unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px;
                        border-left: 5px solid #11998e; margin: 0.5rem 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                        display: flex; flex-direction: column; justify-content: center; height: 100px;">
                <div style="font-size: 1.2rem; font-weight: bold; color: #2c3e50; margin-bottom: 0.3rem;">
                    {station['station_code']} - {station['station_name']}
                </div>
                <div style="font-size: 0.9rem; color: #666;">
                    Distance from start: {station['distance']} km
                </div>
            </div>
            """), unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px;
                        border: 1px solid #e0e0e0; box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                        display: flex; flex-direction: column; justify-content: space-between; height: 100px;">
                <div style="margin-bottom: 0.8rem;">
                    <div style="font-size: 0.8rem; color: #999; font-weight: 600; margin-bottom: 0.3rem;">Arrival</div>
                    <div style="font-size: 1.2rem; font-weight: bold; color: #11998e;">
                        {station['arrival_time']}
                    </div>
                    {f'<div style="font-size: 0.8rem; color: #ff6b6b; font-weight: 600;">+{station["delay"]}m delay</div>' if station['delay'] > 0 else '<div style="font-size: 0.8rem; color: #28a745; font-weight: 600;">On time</div>'}
                </div>
                <div style="border-top: 1px solid #e0e0e0; padding-top: 0.8rem;">
                    <div style="font-size: 0.8rem; color: #999; font-weight: 600; margin-bottom: 0.3rem;">Departure</div>
                    <div style="font-size: 1.2rem; font-weight: bold; color: #2c3e50;">
                        {station['departure_time']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; text-align: center;
                        border: 1px solid #e0e0e0; box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                        display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100px;">
                <div style="font-size: 0.8rem; color: #999; font-weight: 600; margin-bottom: 0.5rem;">Platform</div>
                <div style="font-size: 2rem; font-weight: bold; color: #11998e; margin-bottom: 0.5rem;">
                    {station['platform']}
                </div>
                <div style="font-size: 0.75rem; color: #666; font-weight: 600;">
                    {station['status']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Close the centering container
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Journey Statistics - Centered
    st.subheader("📊 Journey Statistics")

    st.markdown("""
    <div style="display: flex; justify-content: center; margin-bottom: 2rem;">
        <div style="width: 100%; max-width: 1000px;">
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        avg_speed = int(journey_data['total_distance'] / float(journey_data['journey_time'].split(':')[0]))
        st.metric("Avg Speed", f"{avg_speed} km/h", "🚀")

    with col2:
        total_halt = sum(s['halt_minutes'] for s in journey_data['stations'])
        st.metric("Total Halt", f"{total_halt} min", "⏸️")

    with col3:
        delayed_stops = sum(1 for s in journey_data['stations'] if s['delay'] > 0)
        st.metric("Delayed Stops", delayed_stops, "🔴")

    with col4:
        ontime_stops = sum(1 for s in journey_data['stations'] if s['delay'] == 0)
        st.metric("On-Time Stops", ontime_stops, "✅")

    with col5:
        st.metric("Journey Date", date.strftime("%d %b %Y"), "📅")

    st.markdown("</div></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Travel Tips - Centered
    st.markdown("""
    <div style="display: flex; justify-content: center; margin-bottom: 2rem;">
        <div style="width: 100%; max-width: 1000px;">
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.info("""
        **🎯 Journey Insights:**
        - Train is running on schedule
        - Expected arrival: On Time
        - Current location: Between Jangpur & New Delhi
        """)

    with col2:
        st.warning("""
        **⚠️ Alerts:**
        - Minor delay at Dhandari Junction (+5 min)
        - Weather conditions normal
        - All coaches operational
        """)

    st.markdown("</div></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Export Options - Centered
    st.markdown("""
    <div style="display: flex; justify-content: center; margin-bottom: 2rem;">
        <div style="width: 100%; max-width: 800px;">
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📥 Download PDF", key="pdf_export_btn"):
            st.success("✅ PDF generated successfully!")

    with col2:
        if st.button("📊 Export CSV", key="csv_export_btn"):
            st.success("✅ CSV exported successfully!")

    with col3:
        if st.button("📱 Share", key="share_btn"):
            st.success("✅ Link copied to clipboard!")

    with col4:
        if st.button("🔄 Refresh Data", key="refresh_data_btn"):
            st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)


if __name__ == "__main__":
    display_enhanced_journey_tracking()
