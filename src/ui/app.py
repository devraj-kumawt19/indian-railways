"""
Indian Railways AI Detection System - Main Application
Streamlit app for train detection and monitoring
"""

import streamlit as st
import streamlit.components.v1 as components
import sys
import os
import textwrap
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Page configuration - MUST be first
st.set_page_config(
    page_title="Indian Railways AI System",
    page_icon="🚂",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": "https://www.example.com/help",
        "Report a bug": "https://www.example.com/bugs",
        "About": "Indian Railways AI Detection System v2.0 | Professional Enterprise Platform"
    }
)

# Import display functions from modules
from src.ui.live_monitoring import display_live_monitoring_dashboard
from src.ui.enhanced_coach_detection import display_enhanced_coach_detection
from src.ui.all_india_search import display_all_india_train_search
from src.ui.enhanced_journey_tracking import display_enhanced_journey_tracking
from src.ui.train_status_tab import display_train_status_tab
from src.ui.platform_management_tab import display_platform_management
from src.ui.agent_system_tab import display_agent_system
from src.ui.dashboard_tab import display_improved_dashboard
from src.ui.camera_platform_detection import display_dataset_coach_detection
from src.ui.coach_position_finder import display_coach_position_finder
from src.ui.timetable_data_tab import display_timetable_data

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Global Styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
    }

    /* Header Styles */
    .professional-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #3b5998 100%);
        color: white;
        padding: 2.5rem 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }

    .professional-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .professional-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0;
    }

    /* Professional Cards */
    .pro-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
        transition: all 0.3s ease;
    }

    .pro-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }

    .pro-card-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #f8f9fa;
    }

    .pro-card-icon {
        margin-right: 0.75rem;
        font-size: 1.5rem;
    }

    .pro-card-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 0;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #f8f9fa;
        border-bottom: 2px solid #e9ecef;
        border-radius: 8px 8px 0 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 1.5rem;
        font-weight: 600;
        color: #666;
        transition: all 0.3s ease;
        border: none;
        border-bottom: 3px solid transparent;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #667eea;
        background-color: white;
        border-bottom-color: #667eea;
        box-shadow: 0 -2px 8px rgba(102, 126, 234, 0.1);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #667eea;
        background-color: #f0f2f9;
    }

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }

    /* Navigation Sidebar */
    .nav-sidebar {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid #e9ecef;
    }

    .nav-item {
        display: flex;
        align-items: center;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
        border-radius: 8px;
        transition: all 0.3s ease;
        cursor: pointer;
        border: none;
        background: transparent;
        width: 100%;
        text-align: left;
    }

    .nav-item:hover {
        background: #f8f9fa;
        transform: translateX(5px);
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application runner."""
    
    # Professional Header
    st.markdown("""
    <div class="professional-header">
        <h1>&#128642; Indian Railways AI Detection System</h1>
        <p>Advanced Train Detection & Real-Time Scheduling Platform</p>
    </div>
    """, unsafe_allow_html=True)

    # Create tabs for better organization
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs([
        "🚃 DATASET COACH DETECTION", 
        "⚡ LIVE MONITORING", 
        "📊 ENHANCED JOURNEY TRACKING", 
        "🚆 Train Status", 
        "🚃 Enhanced Coach Detection", 
        "📍 Platform Management", 
        "🇮🇳 ALL INDIA SEARCH", 
        "🤖 Agent System", 
        "📈 Dashboard",
        "🎯 COACH POSITION FINDER",
        "📅 TIMETABLE DATA"
    ])

    # Sidebar Navigation
    with st.sidebar:
        # Logo and title
        logo_html = """
        <div style="text-align: center; padding: 1rem 0; border-bottom: 2px solid #e9ecef; margin-bottom: 1.5rem;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">&#128642;</div>
            <h2 style="margin: 0; color: #1e3c72; font-size: 1.2rem;">Indian Railways</h2>
            <p style="margin: 0.25rem 0 0 0; color: #666; font-size: 0.8rem;">AI Detection System v2.0</p>
        </div>
        """
        components.html(logo_html, height=120, scrolling=False)
        
        st.markdown('<div class="nav-sidebar">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-bottom: 1rem; color: #2c3e50;">🧭 Quick Navigation</h3>', unsafe_allow_html=True)

        # Navigation items
        nav_items = [
            ("📊 Dashboard", "System overview & analytics"),
            ("⚡ Live Monitoring", "Real-time train detection"),
            ("🚂 Journey Tracking", "Track train journeys"),
            ("🚃 Coach Detection", "AI-powered coach analysis"),
            ("📍 Platforms", "Platform status & management"),
            ("🇮🇳 Train Search", "Search all Indian trains"),
            ("🤖 AI Agents", "Advanced agent system"),
            ("🎯 Coach Finder", "Find your coach position"),
        ]

        for icon_text, description in nav_items:
            st.markdown(textwrap.dedent(f"""
            <div class="nav-item" style="padding: 0.75rem; background: #f8f9fa; border-radius: 6px; margin-bottom: 0.5rem; border-left: 3px solid transparent; cursor: pointer; transition: all 0.3s ease;">
                <strong style="color: #2c3e50;">{icon_text}</strong><br>
                <small style="opacity: 0.6; color: #666;">{description}</small>
            </div>
            """), unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # System Status Section
        st.markdown('---')
        st.markdown('<div class="nav-sidebar">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #2c3e50; margin-bottom: 1rem;">🔧 System Information</h4>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("API Status", "Active", delta="✅")
        with col2:
            st.metric("Uptime", "99.8%", delta="⚡")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Trains", "12", delta="+3")
        with col2:
            st.metric("Platforms", "8", delta="Ready")

        st.markdown('</div>', unsafe_allow_html=True)
        
        # Footer Info
        st.markdown('---')
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0; color: #999; font-size: 0.8rem;">
            <p style="margin: 0;">Version 2.0.0 (Enhanced)</p>
            <p style="margin: 0.25rem 0 0 0;">Enterprise Platform</p>
            <p style="margin: 0.25rem 0 0 0;">© 2026 Indian Railways</p>
        </div>
        """, unsafe_allow_html=True)

    # ============== TAB CONTENT ==============

    # Tab 1: Dataset Coach Detection
    with tab1:
        try:
            display_dataset_coach_detection()
        except Exception as e:
            st.error(f"⚠️ Error in Dataset Coach Detection: {str(e)}")

    # Tab 2: Live Monitoring
    with tab2:
        try:
            display_live_monitoring_dashboard()
        except Exception as e:
            st.error(f"⚠️ Error in Live Monitoring: {str(e)}")

    # Tab 3: Enhanced Journey Tracking
    with tab3:
        try:
            display_enhanced_journey_tracking()
        except Exception as e:
            st.error(f"⚠️ Error in Journey Tracking: {str(e)}")

    # Tab 4: Train Status
    with tab4:
        try:
            display_train_status_tab()
        except Exception as e:
            st.error(f"⚠️ Error in Train Status: {str(e)}")

    # Tab 5: Enhanced Coach Detection
    with tab5:
        try:
            display_enhanced_coach_detection()
        except Exception as e:
            st.error(f"⚠️ Error in Coach Detection: {str(e)}")

    # Tab 6: Platform Management
    with tab6:
        try:
            display_platform_management()
        except Exception as e:
            st.error(f"⚠️ Error in Platform Management: {str(e)}")

    # Tab 7: All India Train Search
    with tab7:
        try:
            display_all_india_train_search()
        except Exception as e:
            st.error(f"⚠️ Error in Train Search: {str(e)}")
    
    # Tab 8: Agent System
    with tab8:
        try:
            display_agent_system()
        except Exception as e:
            st.error(f"⚠️ Error in Agent System: {str(e)}")
    
    # Tab 9: Improved Dashboard
    with tab9:
        try:
            display_improved_dashboard()
        except Exception as e:
            st.error(f"⚠️ Error in Dashboard: {str(e)}")
    # Tab 10: Coach Position Finder - ADD-ON FEATURE
    with tab10:
        try:
            display_coach_position_finder()
        except Exception as e:
            st.error(f"⚠️ Error in Coach Position Finder: {str(e)}")
    
    # Tab 11: Timetable Data - NEW ADD-ON FEATURE
    with tab11:
        try:
            display_timetable_data()
        except Exception as e:
            st.error(f"⚠️ Error in Timetable Data: {str(e)}")
    
    # Footer with developer credit
    st.markdown("""
    ---
    <div style="text-align: center; opacity: 0.7; font-size: 0.9rem;">
    <p><strong>Indian Railways AI Detection System v2.0.0</strong></p>
    <p><strong>Features:</strong> Live Monitoring | Enhanced Journey Tracking | AI Coach Detection | All India Train Search | Advanced Dashboard | Coach Position Finder | Timetable Data</p>
    <p>Developed by <strong>Devraj Kumawat</strong> | © 2026 Indian Railways</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
