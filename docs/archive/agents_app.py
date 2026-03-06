"""Streamlit UI component for agent architecture."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import streamlit as st
import pandas as pd
import json
from src.agents import CoordinatorAgent, CoachPositionAgent, AgentStatus


class AgentUI:
    """Streamlit UI for agent system."""
    
    def __init__(self):
        self.coordinator = CoordinatorAgent()
        self.position_agent = CoachPositionAgent()
    
    def render_coach_position_finder(self):
        """Render coach position finder interface."""
        st.header("🚂 Coach Position Finder")
        st.write("Find the exact location of coaches on the platform")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            train_no = st.number_input(
                "Train Number",
                value=12345,
                step=1,
                help="Enter the train number"
            )
        
        with col2:
            station_code = st.text_input(
                "Station Code",
                "NDLS",
                help="3-4 letter station code (e.g., NDLS for New Delhi)"
            ).upper()
        
        with col3:
            platform_no = st.number_input(
                "Platform Number",
                value=5,
                step=1,
                min_value=1,
                help="Platform number at the station"
            )
        
        col1, col2 = st.columns(2)
        
        with col1:
            engine_direction = st.selectbox(
                "Engine Direction",
                ["towards_back", "towards_front"],
                help="Direction in which the engine is facing"
            )
        
        with col2:
            platform_length = st.number_input(
                "Platform Length (meters)",
                value=300,
                step=10,
                min_value=100,
                help="Total platform length"
            )
        
        if st.button("🔍 Find Coach Positions", type="primary"):
            self._execute_coach_position_search(
                train_no, station_code, platform_no, 
                platform_length, engine_direction
            )
    
    def _execute_coach_position_search(
        self, train_no, station_code, platform_no, 
        platform_length, engine_direction
    ):
        """Execute coach position search."""
        with st.spinner("🔄 Calculating coach positions..."):
            response = self.position_agent.execute(
                train_no=train_no,
                station_code=station_code,
                platform_no=platform_no,
                platform_length_m=platform_length,
                engine_direction=engine_direction
            )
        
        if response.success:
            self._display_coach_positions(response.data)
        else:
            st.error(f"❌ Error: {response.error}")
    
    def _display_coach_positions(self, data):
        """Display coach positions in a formatted way."""
        st.success("✅ Coach positions calculated successfully!")
        
        # Header info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Train", data.get("train_no", "N/A"))
        with col2:
            st.metric("Platform", data.get("platform_no", "N/A"))
        with col3:
            st.metric("Total Coaches", data.get("total_coaches", 0))
        
        # Coach details table
        st.subheader("Coach Positions")
        
        coaches_data = []
        for coach in data.get("coach_positions", []):
            coaches_data.append({
                "Coach #": coach["coach_number"],
                "Type": coach["coach_type"],
                "Start (m)": f"{coach['start_distance_m']:.1f}",
                "End (m)": f"{coach['end_distance_m']:.1f}",
                "Zones": ", ".join(coach["zones"]) or "Beyond platform"
            })
        
        if coaches_data:
            df = pd.DataFrame(coaches_data)
            st.dataframe(df, use_container_width=True)
            
            # Zone distribution chart
            st.subheader("Zone Distribution")
            self._display_zone_distribution(data.get("coach_positions", []))
            
            # Platform visualization
            st.subheader("Platform Layout")
            self._display_platform_visualization(data.get("coach_positions", []))
        else:
            st.warning("No coach data available")
    
    def _display_zone_distribution(self, positions):
        """Display zone distribution."""
        zone_data = {}
        for pos in positions:
            for zone in pos.get("zones", []):
                if zone not in zone_data:
                    zone_data[zone] = 0
                zone_data[zone] += 1
        
        if zone_data:
            df = pd.DataFrame(
                list(zone_data.items()),
                columns=["Zone", "Coaches"]
            )
            st.bar_chart(df.set_index("Zone"))
    
    def _display_platform_visualization(self, positions):
        """Display platform with coach positions."""
        if not positions:
            st.info("No position data to visualize")
            return
        
        # Create visualization text
        max_distance = max(p.get("end_distance_m", 0) for p in positions) if positions else 100
        
        viz_text = f"""
        **Platform Visualization** (Not to scale)
        
        ```
        0m {"─" * 20} {int(max_distance/2)}m {"─" * 20} {int(max_distance)}m
        |{"─" * 44}|
        
        """
        
        # Add coaches
        sorted_positions = sorted(positions, key=lambda x: x.get("start_distance_m", 0))
        for pos in sorted_positions:
            coach_num = pos.get("coach_number", 0)
            zones = ", ".join(pos.get("zones", ["N/A"]))
            start = pos.get("start_distance_m", 0)
            end = pos.get("end_distance_m", 0)
            viz_text += f"\n        Coach {coach_num:2d} [{zones}]: {start:6.1f}m - {end:6.1f}m"
        
        viz_text += "\n        ```"
        st.markdown(viz_text)
    
    def render_agent_architecture(self):
        """Render agent architecture view."""
        st.header("🏗️ Agent Architecture")
        
        with st.expander("System Architecture", expanded=True):
            st.markdown("""
            ### Coordinator Agent
            Master orchestrator that manages all sub-agents
            
            ```
            CoordinatorAgent
             ├─ TrainInfoAgent       (retrieves train information)
             ├─ CoachFormationAgent  (loads coach composition)
             ├─ CoachPositionAgent   (calculates coach positions)
             └─ StatusAgent          (aggregates all information)
            ```
            """)
        
        with st.expander("Agent Status"):
            status = self.coordinator.get_agent_status()
            
            col1, col2 = st.columns(2)
            
            for i, (agent_name, agent_status) in enumerate(status.items()):
                if i % 2 == 0:
                    col = col1
                else:
                    col = col2
                
                with col:
                    status_color = "🟢" if agent_status == "idle" else "🟡"
                    st.write(f"{status_color} **{agent_name}**: {agent_status}")
    
    def render_documentation(self):
        """Render API documentation."""
        st.header("📖 API Documentation")
        
        with st.expander("CoachPositionAgent", expanded=True):
            st.markdown("""
            #### Overview
            Calculates the position of coaches on a railway platform.
            
            #### Input Parameters
            - `train_no`: Train number (integer)
            - `station_code`: Station code (string)
            - `platform_no`: Platform number (integer)
            - `platform_length_m`: Platform length in meters (float, optional)
            - `engine_direction`: Direction of engine - "towards_back" or "towards_front"
            
            #### Process
            1. Load coach formation from database
            2. Decide engine direction based on station and route
            3. Calculate coach distances from engine (22m + coach_length * coach_number)
            4. Map distances to platform zones (A, B, C, D, E, F, G)
            5. Return coach position mapping
            
            #### Output
            ```json
            {
                "train_no": 12345,
                "station_code": "NDLS",
                "platform_no": 5,
                "engine_direction": "towards_back",
                "total_coaches": 12,
                "coach_positions": [
                    {
                        "coach_number": 1,
                        "coach_type": "A",
                        "start_distance_m": 22.0,
                        "end_distance_m": 43.5,
                        "zones": ["A", "B"]
                    }
                ]
            }
            ```
            
            #### Example Usage
            ```python
            from src.agents import CoachPositionAgent
            
            agent = CoachPositionAgent()
            response = agent.execute(
                train_no=12345,
                station_code="NDLS",
                platform_no=5,
                engine_direction="towards_back"
            )
            
            if response.success:
                print(response.data)
            ```
            """)
        
        with st.expander("CoordinatorAgent"):
            st.markdown("""
            #### Overview
            Master agent that orchestrates all sub-agents for complete train information.
            
            #### Sub-agents
            - **TrainInfoAgent**: Retrieves train schedule and status
            - **CoachFormationAgent**: Loads coach composition
            - **CoachPositionAgent**: Calculates coach positions
            - **StatusAgent**: Aggregates all information
            
            #### Usage
            ```python
            from src.agents import CoordinatorAgent
            
            coordinator = CoordinatorAgent()
            response = coordinator.execute(
                train_no=12345,
                station_code="NDLS",
                platform_no=5
            )
            ```
            """)


def main():
    """Main Streamlit app."""
    st.set_page_config(
        page_title="🚂 Indian Railways Agent System",
        page_icon="🚂",
        layout="wide"
    )
    
    st.title("🚂 Indian Railways Agent System")
    st.write("Intelligent agent-based system for train information and coach positioning")
    
    ui = AgentUI()
    
    # Sidebar navigation
    with st.sidebar:
        st.header("Navigation")
        page = st.radio(
            "Select a page",
            ["Coach Finder", "Architecture", "Documentation"],
            label_visibility="collapsed"
        )
    
    # Page rendering
    if page == "Coach Finder":
        ui.render_coach_position_finder()
    elif page == "Architecture":
        ui.render_agent_architecture()
    elif page == "Documentation":
        ui.render_documentation()


if __name__ == "__main__":
    main()
