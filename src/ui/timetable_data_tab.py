"""
Timetable Data Display Module
Shows train timetable data from data.gov.in API
"""

import streamlit as st
import pandas as pd
from typing import List, Dict, Optional
from src.scheduling.indian_railways_api import IndianRailwaysAPI


def display_timetable_data():
    """Display train timetable data from data.gov.in API."""

    st.header("🚂 Indian Railways Timetable Data")
    st.markdown("Official train schedule data from data.gov.in")

    # Initialize API
    api = IndianRailwaysAPI()

    # Controls
    col1, col2, col3 = st.columns([2, 2, 2])

    with col1:
        limit = st.selectbox(
            "Records per page",
            options=[10, 25, 50, 100],
            index=0,
            help="Number of records to fetch per page"
        )

    with col2:
        offset = st.number_input(
            "Page offset",
            min_value=0,
            value=0,
            step=limit,
            help="Starting record number (0-based)"
        )

    with col3:
        if st.button("🔄 Refresh Data", help="Fetch fresh data from API"):
            st.rerun()

    # Fetch data
    with st.spinner("Fetching timetable data..."):
        records = api.get_timetable_from_datagovin(limit=limit, offset=offset)

    if records:
        # Convert to DataFrame for better display
        df = pd.DataFrame(records)

        # Rename columns for better readability
        column_mapping = {
            'train_no': 'Train No',
            'train_name': 'Train Name',
            'seq': 'Sequence',
            'station_code': 'Station Code',
            'station_name': 'Station Name',
            'arrival_time': 'Arrival Time',
            'departure_time': 'Departure Time',
            'distance': 'Distance (km)',
            'source_station': 'Source Station',
            'source_station_name': 'Source Station Name',
            'destination_station': 'Destination Station',
            'destination_station_name': 'Destination Station Name'
        }

        df = df.rename(columns=column_mapping)

        # Display stats
        st.success(f"✅ Fetched {len(records)} records (Total available: 186,124)")

        # Show data
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        # Additional features
        st.markdown("---")
        col1, col2, col3 = st.columns(3)

        with col1:
            # Filter by train number
            train_numbers = sorted(df['Train No'].unique())
            selected_train = st.selectbox(
                "Filter by Train Number",
                options=["All"] + list(train_numbers)
            )

        with col2:
            # Filter by station
            stations = sorted(df['Station Code'].unique())
            selected_station = st.selectbox(
                "Filter by Station",
                options=["All"] + list(stations)
            )

        with col3:
            # Export option
            if st.button("📥 Export to CSV"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="train_timetable.csv",
                    mime="text/csv"
                )

        # Apply filters
        filtered_df = df.copy()
        if selected_train != "All":
            filtered_df = filtered_df[filtered_df['Train No'] == selected_train]
        if selected_station != "All":
            filtered_df = filtered_df[filtered_df['Station Code'] == selected_station]

        if len(filtered_df) != len(df):
            st.markdown(f"**Filtered Results:** {len(filtered_df)} records")
            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True
            )

        # Train route visualization for selected train
        if selected_train != "All" and len(filtered_df) > 0:
            st.markdown("---")
            st.subheader(f"🚂 Route for Train {selected_train}")

            # Sort by sequence
            route_df = filtered_df.sort_values('Sequence')

            # Create route summary
            route_info = []
            for _, row in route_df.iterrows():
                route_info.append({
                    'Stop': int(row['Sequence']),
                    'Station': f"{row['Station Code']} - {row['Station Name']}",
                    'Arrival': row['Arrival Time'],
                    'Departure': row['Departure Time'],
                    'Distance': row['Distance (km)']
                })

            route_summary = pd.DataFrame(route_info)
            st.dataframe(route_summary, use_container_width=True, hide_index=True)

    else:
        st.error("❌ Failed to fetch timetable data. Please check your internet connection and try again.")

        # Show sample data from CSV as fallback
        st.warning("📋 Showing sample data from local CSV file:")
        try:
            csv_df = pd.read_csv("data/Train_details_22122017.csv", nrows=10)
            st.dataframe(csv_df, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"Could not load sample data: {e}")


def display_timetable_stats():
    """Display statistics about the timetable data."""

    st.subheader("📊 Timetable Statistics")

    try:
        # Load local CSV for stats
        df = pd.read_csv("data/Train_details_22122017.csv", low_memory=False)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Records", f"{len(df):,}")

        with col2:
            unique_trains = df['Train No'].nunique()
            st.metric("Unique Trains", f"{unique_trains:,}")

        with col3:
            unique_stations = df['Station Code'].nunique()
            st.metric("Stations", f"{unique_stations:,}")

        with col4:
            total_distance = df['Distance'].max()
            st.metric("Max Distance", f"{total_distance} km")

        # Most common routes
        st.markdown("---")
        st.subheader("🔥 Popular Routes")

        route_counts = df.groupby(['Source Station', 'Destination Station']).size().reset_index(name='Count')
        route_counts = route_counts.sort_values('Count', ascending=False).head(10)

        st.dataframe(
            route_counts,
            column_config={
                'Source Station': 'From',
                'Destination Station': 'To',
                'Count': 'Trains'
            },
            use_container_width=True,
            hide_index=True
        )

    except Exception as e:
        st.error(f"Could not load statistics: {e}")