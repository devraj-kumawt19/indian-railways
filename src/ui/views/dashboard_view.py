"""Dashboard View - professional dashboard with metrics and analytics."""
import streamlit as st
from src.services import (
    TrainScheduleService,
    TrainPriorityService,
    StationService
)


class DashboardView:
    """Professional dashboard view with analytics."""
    
    def __init__(self):
        self.schedule_service = TrainScheduleService()
        self.priority_service = TrainPriorityService()
        self.station_service = StationService()
    
    def render_main_dashboard(self):
        """Render main dashboard with key metrics."""
        st.title("🚂 Indian Railways AI System")
        st.markdown("Professional Analytics & Route Management Platform")
        
        # Key metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        schedule_stats = self.schedule_service.get_statistics()
        priority_stats = self.priority_service.get_operational_status()
        
        with col1:
            st.metric(
                "Total Trains",
                schedule_stats['total_trains'],
                delta=None,
                delta_color="off"
            )
        
        with col2:
            st.metric(
                "On-Time %",
                f"{schedule_stats['on_time_percentage']:.1f}%",
                delta=None,
                delta_color="off"
            )
        
        with col3:
            st.metric(
                "Operational",
                priority_stats['operational'],
                delta=None,
                delta_color="off"
            )
        
        with col4:
            st.metric(
                "Total Stations",
                len(self.station_service.get_all_stations()),
                delta=None,
                delta_color="off"
            )
        
        st.divider()
        
        # Status breakdown
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Schedule Status")
            status_data = {
                'On Time': schedule_stats['on_time'],
                'Delayed': schedule_stats['delayed'],
                'Cancelled': schedule_stats['cancelled'],
                'Running': schedule_stats['running']
            }
            st.bar_chart(status_data)
        
        with col2:
            st.subheader("Priority Distribution")
            priority_data = {
                'Express': priority_stats['express_trains'],
                'Available': priority_stats['available_trains']
            }
            st.bar_chart(priority_data)
        
        with col3:
            st.subheader("Zone Distribution")
            zone_dist = self.station_service.get_zone_distribution()
            st.bar_chart(zone_dist)
    
    def render_quick_links(self):
        """Render quick navigation links."""
        st.sidebar.markdown("### 🔗 Quick Navigation")
        
        pages = {
            "Dashboard": "dashboard",
            "Find Trains": "find_trains",
            "Stations": "stations",
            "Schedule": "schedule",
            "Analytics": "analytics"
        }
        
        for label, page in pages.items():
            st.sidebar.button(label, key=page)
