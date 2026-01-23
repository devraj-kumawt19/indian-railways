"""Station View - displays station information and search."""
import streamlit as st
from typing import List
from src.models import Station
from src.services import StationService


class StationView:
    """View component for displaying station information."""
    
    def __init__(self):
        self.service = StationService()
    
    def render_station_search(self):
        """Render station search interface."""
        st.subheader("🏢 Search Stations")
        
        search_query = st.text_input(
            "Search by station name or code",
            placeholder="e.g., Delhi, NDLS",
            key="station_search"
        )
        
        if search_query:
            results = self.service.search_stations(search_query)
            self._display_station_results(results)
    
    def render_major_junctions(self):
        """Render major junctions display."""
        st.subheader("⭐ Major Railway Junctions")
        
        junctions = self.service.get_major_junctions()
        
        if junctions:
            for junction in junctions[:10]:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Code", junction.station_code)
                
                with col2:
                    st.metric("Platforms", junction.platform_count)
                
                with col3:
                    st.metric("Zone", junction.zone)
                
                with col4:
                    st.metric("State", junction.state)
                
                st.caption(junction.station_name)
                st.divider()
    
    def render_zone_distribution(self):
        """Render railway zone distribution."""
        st.subheader("📊 Stations by Railway Zone")
        
        distribution = self.service.get_zone_distribution()
        
        if distribution:
            col1, col2 = st.columns(2)
            
            with col1:
                st.bar_chart(distribution)
            
            with col2:
                st.write("**Zone Summary:**")
                for zone, count in sorted(distribution.items(), key=lambda x: x[1], reverse=True):
                    st.write(f"• {zone}: {count} stations")
    
    def _display_station_results(self, stations: List[Station]):
        """Display search results."""
        if not stations:
            st.warning("No stations found.")
            return
        
        st.success(f"Found {len(stations)} station(s)")
        
        for station in stations:
            with st.expander(station.full_name):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Type:** {station.station_type}")
                    st.write(f"**Platforms:** {station.platform_count}")
                
                with col2:
                    st.write(f"**State:** {station.state}")
                    st.write(f"**Zone:** {station.zone}")
                
                with col3:
                    is_major = "✓ Major Junction" if station.is_major_junction else "Regular Station"
                    st.write(is_major)
