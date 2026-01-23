"""Train Route View - displays train routes between stations."""
import streamlit as st
from typing import List
from src.models import TrainRoute
from src.services import TrainRouteService


class TrainRouteView:
    """View component for displaying train routes."""
    
    def __init__(self):
        self.service = TrainRouteService()
    
    def render_route_search(self):
        """Render train route search interface."""
        st.subheader("🚂 Find Trains Between Stations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            from_code = st.selectbox(
                "From Station",
                options=self._get_station_codes(),
                key="from_station_route"
            )
        
        with col2:
            to_code = st.selectbox(
                "To Station",
                options=self._get_station_codes(),
                key="to_station_route"
            )
        
        if st.button("Search Routes", key="search_routes_btn"):
            self._display_routes(from_code, to_code)
    
    def _display_routes(self, from_code: str, to_code: str):
        """Display available routes."""
        routes = self.service.get_routes_between_stations(from_code, to_code)
        
        if not routes:
            st.warning("No trains available on this route.")
            return
        
        st.success(f"Found {len(routes)} trains")
        
        for route in routes:
            with st.container():
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Train No", route.train.train_no)
                
                with col2:
                    st.metric("Departure", route.train.departure_time)
                
                with col3:
                    st.metric("Duration", f"{route.journey_duration_hours():.1f}h")
                
                with col4:
                    st.metric("Avg Speed", f"{route.average_speed_kmh():.1f} km/h")
                
                st.info(f"📍 {route.train.train_name} ({route.train.frequency})")
                st.divider()
    
    def _get_station_codes(self) -> List[str]:
        """Get list of all station codes."""
        from src.services import StationService
        service = StationService()
        stations = service.get_all_stations()
        return [f"{s.station_code} - {s.station_name}" for s in stations]
