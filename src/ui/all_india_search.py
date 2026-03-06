"""
All India Train Search Module
Comprehensive search for trains across Indian Railways
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from src.repositories.train_repository import TrainRepository
from src.utils.suggestions import display_suggestions

# Initialize session state
if "search_results" not in st.session_state:
    st.session_state.search_results = []

@st.cache_data(ttl=3600)  # Cache for 1 hour
def cached_train_search(departure_station, arrival_station, journey_date_str):
    """Cached train search to improve performance."""
    repo = TrainRepository()
    return repo.search_trains_api(departure_station, arrival_station, journey_date_str)


def display_all_india_train_search():
    """Display comprehensive all-India train search interface."""

    # Enhanced Header with Modern Design
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
                color: white; padding: 3rem 2.5rem; border-radius: 20px; margin-bottom: 2rem;
                box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3); position: relative; overflow: hidden;">
        <div style="position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
                    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
                    animation: pulse 4s ease-in-out infinite;"></div>
        <div style="position: relative; z-index: 1;">
            <h1 style="margin: 0 0 0.5rem 0; font-size: 3rem; font-weight: 800; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                🇮🇳 ALL INDIA TRAIN SEARCH
            </h1>
            <p style="margin: 0; opacity: 0.95; font-size: 1.2rem; font-weight: 300; letter-spacing: 0.5px;">
                Discover & Book Trains Across India's Vast Railway Network
            </p>
            <div style="margin-top: 1rem; display: flex; gap: 1rem; flex-wrap: wrap;">
                <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 25px; font-size: 0.9rem; backdrop-filter: blur(10px);">
                    🚀 Live Updates
                </span>
                <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 25px; font-size: 0.9rem; backdrop-filter: blur(10px);">
                    🎯 Real-time Availability
                </span>
                <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 25px; font-size: 0.9rem; backdrop-filter: blur(10px);">
                    💎 Premium Experience
                </span>
            </div>
        </div>
    </div>

    <style>
        @keyframes pulse {
            0%, 100% { opacity: 0.5; }
            50% { opacity: 1; }
        }
    </style>
    """), unsafe_allow_html=True)

    # Modern Tab Design
    st.markdown("""
    <style>
        .stTabs [data-baseweb="tab-list"] {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 15px;
            padding: 0.5rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border: 1px solid #dee2e6;
        }

        .stTabs [data-baseweb="tab"] {
            padding: 1rem 2rem;
            font-weight: 600;
            color: #6c757d;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border-radius: 10px;
            margin: 0 0.25rem;
            border: none;
            background: transparent;
            position: relative;
            overflow: hidden;
        }

        .stTabs [data-baseweb="tab"]:hover {
            color: #495057;
            background: rgba(255,255,255,0.8);
            transform: translateY(-2px);
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            color: #fff;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
            transform: translateY(-2px);
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"]:before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            animation: shimmer 2s infinite;
        }

        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }
    </style>
    """), unsafe_allow_html=True)

    # Enhanced Search Tabs
    search_tab1, search_tab2, search_tab3, search_tab4 = st.tabs([
        "🔍 Direct Search",
        "🗺️ Popular Routes",
        "📍 Station Search",
        "⚙️ Advanced Filters"
    ])

    with search_tab1:
        display_train_search()

    with search_tab2:
        display_route_search()

    with search_tab3:
        display_station_search()

    with search_tab4:
        display_advanced_search()


def display_train_search():
    """Display basic train search interface."""

    # Modern Search Form Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem;
                border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);">
        <h2 style="margin: 0 0 0.5rem 0; font-size: 1.8rem; font-weight: 700;">🚂 Direct Train Search</h2>
        <p style="margin: 0; opacity: 0.9; font-size: 1rem;">Find trains between any two stations across India</p>
    </div>
    """), unsafe_allow_html=True)

    # Initialize repository
    repo = TrainRepository()

    # Enhanced Search Form with Cards
    st.markdown("""
    <style>
        .search-card {
            background: white;
            border-radius: 15px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            border: 1px solid #e9ecef;
            transition: all 0.3s ease;
        }
        .search-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        }
        .form-group {
            margin-bottom: 1.5rem;
        }
        .form-label {
            font-weight: 600;
            color: #495057;
            margin-bottom: 0.5rem;
            display: block;
            font-size: 0.95rem;
        }
        .input-icon {
            position: relative;
        }
        .input-icon:before {
            content: attr(data-icon);
            position: absolute;
            left: 12px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 1.2rem;
            color: #6c757d;
            z-index: 1;
        }
        .modern-input {
            width: 100%;
            padding: 0.75rem 1rem 0.75rem 2.5rem;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            font-size: 1rem;
            transition: all 0.3s ease;
            background: #f8f9fa;
        }
        .modern-input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            background: white;
            outline: none;
        }
        .modern-selectbox {
            background: #f8f9fa;
            border-radius: 10px;
            border: 2px solid #e9ecef;
        }
        .search-buttons {
            display: flex;
            gap: 1rem;
            margin-top: 2rem;
        }
        .btn-primary-modern {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.875rem 2rem;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            flex: 1;
            text-align: center;
        }
        .btn-primary-modern:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }
        .btn-secondary-modern {
            background: #f8f9fa;
            color: #6c757d;
            border: 2px solid #e9ecef;
            padding: 0.875rem 2rem;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            flex: 1;
            text-align: center;
        }
        .btn-secondary-modern:hover {
            background: #e9ecef;
            transform: translateY(-2px);
        }
    </style>
    """), unsafe_allow_html=True)

    # Search Form Card
    st.markdown('<div class="search-card">', unsafe_allow_html=True)

    # Form Layout
    col1, col2, col3, col4 = st.columns([3, 3, 2, 2])

    with col1:
        st.markdown('<div class="form-group"><label class="form-label">📍 From Station</label>', unsafe_allow_html=True)
        departure_station = st.text_input(
            "departure_station",
            placeholder="e.g., Delhi, Mumbai, Chennai",
            label_visibility="collapsed",
            key="departure_input"
        )
        # Display departure station suggestions
        if departure_station:
            display_suggestions("departure_input", "station", departure_station)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="form-group"><label class="form-label">🎯 To Station</label>', unsafe_allow_html=True)
        arrival_station = st.text_input(
            "arrival_station",
            placeholder="e.g., Bangalore, Kolkata, Pune",
            label_visibility="collapsed",
            key="arrival_input"
        )
        # Display arrival station suggestions
        if arrival_station:
            display_suggestions("arrival_input", "station", arrival_station)
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="form-group"><label class="form-label">📅 Journey Date</label>', unsafe_allow_html=True)
        journey_date = st.date_input(
            "journey_date",
            datetime.now() + timedelta(days=1),
            label_visibility="collapsed",
            key="date_input"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="form-group"><label class="form-label">🎫 Class Preference</label>', unsafe_allow_html=True)
        class_type = st.selectbox(
            "class_type",
            ["All Classes", "1A (AC 1st)", "2A (AC 2nd)", "3A (AC 3rd)", "SL (Sleeper)", "2S (Sitting)"],
            label_visibility="collapsed",
            key="class_input"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # Action Buttons
    st.markdown('<div class="search-buttons">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔍 Search Trains", key="search_trains_btn", help="Find available trains"):
            if departure_station and arrival_station:
                with st.spinner("🔍 Searching trains..."):
                    # Use cached search for better performance
                    search_results = cached_train_search(departure_station, arrival_station, journey_date.strftime("%d-%m-%Y"))
                    if search_results:
                        st.session_state.search_results = search_results
                        st.session_state.search_params = {
                            'from': departure_station,
                            'to': arrival_station,
                            'date': journey_date,
                            'class': class_type
                        }
                        st.success(f"✅ Found {len(search_results)} trains!")
                    else:
                        st.error("❌ No trains found for the selected route. Please try different stations or date.")
            else:
                st.error("⚠️ Please enter both departure and destination stations")

    with col2:
        if st.button("🔄 Clear Search", key="clear_search_btn", help="Reset search form"):
            st.session_state.search_results = []
            if 'search_params' in st.session_state:
                del st.session_state.search_params
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display results
    if st.session_state.get("search_results"):
        st.markdown("---")
        display_train_results(st.session_state.search_results, st.session_state.get('search_params', {}))


    # Display results
    if st.session_state.get("search_results"):
        st.markdown("---")
        display_train_results(st.session_state.search_results, st.session_state.get('search_params', {}))


def display_train_results(search_results, search_params):
    """Display train search results with modern design."""

    from_station = search_params.get('from', 'Unknown')
    to_station = search_params.get('to', 'Unknown')

    # Results Header
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 2rem;
                border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 8px 25px rgba(40, 167, 69, 0.3);">
        <h3 style="margin: 0 0 0.5rem 0; font-size: 1.8rem; font-weight: 700;">✨ Available Trains</h3>
        <p style="margin: 0; opacity: 0.9; font-size: 1.1rem;">
            {from_station} → {to_station} • {search_params.get('date', 'N/A').strftime('%d-%b-%Y') if search_params.get('date') else 'N/A'}
        </p>
        <div style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">
            Found {len(search_results)} train option{'s' if len(search_results) != 1 else ''}
        </div>
    </div>
    """), unsafe_allow_html=True)

    if not search_results:
        st.warning("No trains found for the selected route.")
        return

    # Enhanced Results Styling
    st.markdown("""
    <style>
        .train-card {
            background: white;
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
            border: 1px solid #e9ecef;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        .train-card:before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .train-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }
        .train-header {
            display: flex;
            align-items: center;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid #f8f9fa;
        }
        .train-number {
            font-size: 1.4rem;
            font-weight: 800;
            color: #667eea;
            margin-right: 1rem;
        }
        .train-name {
            font-size: 1.2rem;
            font-weight: 600;
            color: #495057;
            flex: 1;
        }
        .train-meta {
            display: flex;
            align-items: center;
            gap: 1rem;
            font-size: 0.9rem;
            color: #6c757d;
        }
        .route-display {
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            align-items: center;
            gap: 2rem;
            margin: 2rem 0;
            position: relative;
        }
        .station-info {
            text-align: center;
            padding: 1.5rem;
            background: #f8f9fa;
            border-radius: 15px;
            border: 2px solid #e9ecef;
        }
        .departure-time {
            font-size: 2.5rem;
            font-weight: 800;
            color: #28a745;
            margin-bottom: 0.5rem;
        }
        .arrival-time {
            font-size: 2.5rem;
            font-weight: 800;
            color: #dc3545;
            margin-bottom: 0.5rem;
        }
        .station-name {
            font-size: 1rem;
            color: #6c757d;
            font-weight: 500;
        }
        .route-arrow {
            font-size: 2rem;
            color: #667eea;
            position: relative;
            z-index: 1;
        }
        .route-line {
            position: absolute;
            top: 50%;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #28a745 0%, #667eea 50%, #dc3545 100%);
            z-index: 0;
        }
        .train-details {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        .detail-item {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            border: 1px solid #e9ecef;
        }
        .detail-label {
            font-size: 0.85rem;
            color: #6c757d;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
        }
        .detail-value {
            font-size: 1.1rem;
            font-weight: 700;
            color: #495057;
        }
        .classes-available {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 1rem;
            border-radius: 12px;
            text-align: center;
            margin: 1.5rem 0;
        }
        .book-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 12px;
            font-weight: 700;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            width: 100%;
            text-align: center;
            text-decoration: none;
            display: inline-block;
        }
        .book-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }
    </style>
    """, unsafe_allow_html=True)

    # Display real search results
    for idx, train in enumerate(search_results):
        # Format train data for display
        train_no = train.get('number', 'N/A')
        train_name = train.get('name', 'Unknown Train')
        departure_time = train.get('src_departure_time', 'N/A')
        arrival_time = train.get('dest_arrival_time', 'N/A')
        duration = train.get('travel_time', 'N/A')
        # For now, show basic classes - can be enhanced later
        available_classes = ['SL', '3A', '2A', '1A']  # Default classes

        st.markdown(f"""
        <div class="train-card">
            <div class="train-header">
                <div class="train-number">{train_no}</div>
                <div class="train-name">{train_name}</div>
                <div class="train-meta">
                    <span>🕒 {duration}</span>
                    <span>🚂 Direct</span>
                </div>
            </div>

            <div class="route-display">
                <div class="route-line"></div>
                <div class="station-info">
                    <div class="departure-time">{departure_time}</div>
                    <div class="station-name">From {from_station}</div>
                </div>
                <div class="route-arrow">🚆</div>
                <div class="station-info">
                    <div class="arrival-time">{arrival_time}</div>
                    <div class="station-name">To {to_station}</div>
                </div>
            </div>

            <div class="train-details">
                <div class="detail-item">
                    <div class="detail-label">Duration</div>
                    <div class="detail-value">{duration}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Train Type</div>
                    <div class="detail-value">Express</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Available Classes</div>
                    <div class="detail-value">{len(available_classes)}</div>
                </div>
            </div>

            <div class="classes-available">
                <strong>Available Classes:</strong> {' • '.join(available_classes)}
            </div>

            <a href="#" class="book-button" onclick="alert('Booking functionality coming soon! 🚂')">🎫 Book This Train</a>
        </div>
        """, unsafe_allow_html=True)


def display_route_search():
    """Display route-based search with modern design."""

    st.markdown("""
    <div style="background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%); color: white; padding: 2rem;
                border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 8px 25px rgba(255, 154, 158, 0.3);">
        <h3 style="margin: 0 0 0.5rem 0; font-size: 1.8rem; font-weight: 700;">🗺️ Popular Routes</h3>
        <p style="margin: 0; opacity: 0.9; font-size: 1rem;">Quick search on India's most popular train routes</p>
    </div>
    """, unsafe_allow_html=True)

    # Route Cards Styling
    st.markdown("""
    <style>
        .route-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        .route-card {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            border: 1px solid #e9ecef;
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        .route-card:before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
        }
        .route-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        }
        .route-name {
            font-size: 1.2rem;
            font-weight: 700;
            color: #495057;
            margin-bottom: 0.5rem;
        }
        .route-meta {
            font-size: 0.9rem;
            color: #6c757d;
            margin-bottom: 1rem;
        }
        .route-stats {
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            color: #6c757d;
        }
    </style>
    """, unsafe_allow_html=True)

    # Popular Routes Grid
    routes = [
        {"name": "Delhi - Mumbai", "distance": "1425 km", "trains": "25+", "duration": "16-18h"},
        {"name": "Mumbai - Bangalore", "distance": "985 km", "trains": "20+", "duration": "18-20h"},
        {"name": "Chennai - Delhi", "distance": "2180 km", "trains": "15+", "duration": "32-35h"},
        {"name": "Kolkata - Delhi", "distance": "1475 km", "trains": "22+", "duration": "24-26h"},
        {"name": "Hyderabad - Chennai", "distance": "710 km", "trains": "18+", "duration": "12-14h"},
        {"name": "Pune - Mumbai", "distance": "185 km", "trains": "35+", "duration": "3-4h"},
        {"name": "Ahmedabad - Delhi", "distance": "935 km", "trains": "20+", "duration": "14-16h"},
        {"name": "Jaipur - Delhi", "distance": "305 km", "trains": "15+", "duration": "5-6h"},
    ]

    st.markdown('<div class="route-grid">', unsafe_allow_html=True)

    for route in routes:
        st.markdown(f"""
        <div class="route-card" onclick="this.style.transform='scale(0.98)'">
            <div class="route-name">🚂 {route['name']}</div>
            <div class="route-meta">📏 {route['distance']} • ⏱️ {route['duration']}</div>
            <div class="route-stats">
                <span>🚆 {route['trains']} trains</span>
                <span>⭐ Popular</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Route Search Form
    st.markdown("""
    <div style="background: white; border-radius: 15px; padding: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.08);">
        <h4 style="margin-bottom: 1.5rem; color: #495057;">🔍 Search Specific Route</h4>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        route = st.selectbox(
            "Select Route",
            [
                "Delhi - Mumbai",
                "Mumbai - Bangalore",
                "Chennai - Delhi",
                "Kolkata - Delhi",
                "Hyderabad - Chennai",
                "Pune - Mumbai",
                "Ahmedabad - Delhi",
                "Jaipur - Delhi"
            ],
            key="route_select"
        )

    with col2:
        date = st.date_input("Travel Date", datetime.now() + timedelta(days=1), key="route_date")

    with col3:
        if st.button("🔍 Find Trains", type="primary", key="search_route_btn"):
            with st.spinner("Searching route..."):
                st.success(f"✅ Found trains on {route} for {date.strftime('%d-%b-%Y')}")
                # Mock results for now
                st.dataframe(
                    pd.DataFrame({
                        "Train No": ["12301", "20844", "15017"],
                        "Name": ["Rajdhani Express", "Delhi Express", "Bandra Express"],
                        "Depart": ["16:55", "14:00", "15:30"],
                        "Arrive": ["08:35 +1D", "06:30 +1D", "07:45 +1D"],
                        "Duration": ["15:40", "16:30", "16:15"],
                    }),
                    use_container_width=True
                )

    st.markdown('</div>', unsafe_allow_html=True)


def display_station_search():
    """Display station-based search with modern design."""

    st.markdown("""
    <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); color: white; padding: 2rem;
                border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 8px 25px rgba(168, 237, 234, 0.3);">
        <h3 style="margin: 0 0 0.5rem 0; font-size: 1.8rem; font-weight: 700;">📍 Station Search</h3>
        <p style="margin: 0; opacity: 0.9; font-size: 1rem;">Find all trains departing from a specific station</p>
    </div>
    """, unsafe_allow_html=True)

    # Station Search Form
    st.markdown("""
    <style>
        .station-search-card {
            background: white;
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            margin-bottom: 2rem;
        }
        .station-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 1.5rem 0;
        }
        .station-badge {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 25px;
            text-align: center;
            font-weight: 600;
            font-size: 0.9rem;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .station-badge:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="station-search-card">', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<h4 style="margin-bottom: 1rem; color: #495057;">🏙️ Select Station</h4>', unsafe_allow_html=True)

        # Popular Stations Grid
        stations = [
            "Delhi Junction (DEL)", "Mumbai Central (BCT)", "Bangalore City (SBC)",
            "Chennai Central (MAS)", "Kolkata (KOAA)", "Hyderabad (HYD)",
            "Pune Junction (PNVL)", "Ahmedabad Junction (ADI)"
        ]

        st.markdown('<div class="station-grid">', unsafe_allow_html=True)
        for station in stations:
            st.markdown(f'<div class="station-badge">{station}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        station = st.selectbox(
            "Or choose from dropdown:",
            stations,
            key="station_select"
        )

    with col2:
        st.markdown('<h4 style="margin-bottom: 1rem; color: #495057;">⏰ Time Filter</h4>', unsafe_allow_html=True)
        time_period = st.selectbox(
            "Departure Time",
            ["All Day", "Morning (06-12)", "Afternoon (12-18)", "Evening (18-00)"],
            key="time_filter"
        )

        st.markdown('<br>', unsafe_allow_html=True)

        if st.button("🔍 Show Trains", type="primary", key="show_station_trains", use_container_width=True):
            with st.spinner("Loading train schedule..."):
                st.success(f"📋 Trains from {station} ({time_period})")

                # Mock results
                st.dataframe(
                    pd.DataFrame({
                        "Train No": ["12301", "20844", "15017", "22915"],
                        "Train Name": ["Rajdhani Express", "Delhi Express", "Bandra Express", "Kerala Express"],
                        "Destination": ["Mumbai", "Delhi", "Mumbai", "Kerala"],
                        "Departure": ["16:55", "14:00", "15:30", "17:45"],
                        "Distance (km)": ["1425", "1425", "1500", "1650"],
                    }),
                    use_container_width=True
                )

    st.markdown('</div>', unsafe_allow_html=True)


def display_advanced_search():
    """Display advanced search options with modern design."""

    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%); color: white; padding: 2rem;
                border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);">
        <h3 style="margin: 0 0 0.5rem 0; font-size: 1.8rem; font-weight: 700;">⚙️ Advanced Filters</h3>
        <p style="margin: 0; opacity: 0.9; font-size: 1rem;">Fine-tune your search with advanced filtering options</p>
    </div>
    """, unsafe_allow_html=True)

    # Advanced Filters Styling
    st.markdown("""
    <style>
        .filters-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        .filter-card {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            border: 1px solid #e9ecef;
        }
        .filter-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: #495057;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .modern-multiselect {
            background: #f8f9fa;
            border-radius: 10px;
            border: 2px solid #e9ecef;
        }
        .modern-slider {
            padding: 1rem 0;
        }
        .modern-number-input {
            background: #f8f9fa;
            border-radius: 10px;
            border: 2px solid #e9ecef;
            padding: 0.5rem;
        }
        .apply-filters-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 12px;
            font-weight: 700;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            width: 100%;
            margin-top: 2rem;
        }
        .apply-filters-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }
        .filter-summary {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 12px;
            margin-top: 2rem;
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)

    # Filter Cards
    st.markdown('<div class="filters-grid">', unsafe_allow_html=True)

    # Train Type Filter
    st.markdown("""
    <div class="filter-card">
        <div class="filter-title">🚂 Train Types</div>
    """, unsafe_allow_html=True)

    train_type = st.multiselect(
        "train_type_filter",
        ["Express", "Rajdhani", "Shatabdi", "Local", "Fast Passenger", "Superfast", "Mail"],
        default=["Express", "Rajdhani"],
        key="train_type_filter",
        label_visibility="collapsed"
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # Journey Duration Filter
    st.markdown("""
    <div class="filter-card">
        <div class="filter-title">⏱️ Journey Duration</div>
    """, unsafe_allow_html=True)

    max_duration = st.slider(
        "duration_filter",
        min_value=0,
        max_value=48,
        value=36,
        key="duration_filter",
        label_visibility="collapsed"
    )
    st.caption(f"Up to {max_duration} hours")

    st.markdown('</div>', unsafe_allow_html=True)

    # Price Range Filter
    st.markdown("""
    <div class="filter-card">
        <div class="filter-title">💰 Price Range</div>
    """, unsafe_allow_html=True)

    max_price = st.number_input(
        "price_filter",
        min_value=100,
        value=5000,
        step=100,
        key="price_filter",
        label_visibility="collapsed"
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # Class Preferences
    st.markdown("""
    <div class="filter-card">
        <div class="filter-title">🎫 Class Preferences</div>
    """, unsafe_allow_html=True)

    preference_class = st.multiselect(
        "class_filter",
        ["1A (AC 1st)", "2A (AC 2nd)", "3A (AC 3rd)", "SL (Sleeper)", "2S (Sitting)"],
        default=["1A (AC 1st)", "2A (AC 2nd)"],
        key="class_filter",
        label_visibility="collapsed"
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # Rating & Availability
    st.markdown("""
    <div class="filter-card">
        <div class="filter-title">⭐ Quality Filters</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        min_rating = st.slider(
            "rating_filter",
            min_value=0.0,
            max_value=5.0,
            value=3.5,
            step=0.5,
            key="rating_filter",
            label_visibility="collapsed"
        )
        st.caption(f"{min_rating}+ stars")

    with col2:
        availability = st.selectbox(
            "availability_filter",
            ["Any", "High (>50 seats)", "Medium (20-50)", "Low (<20)"],
            key="availability_filter",
            label_visibility="collapsed"
        )

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Apply Filters Button
    if st.button("🚀 Apply Advanced Filters", key="apply_adv_filters_btn", help="Search with advanced filters"):
        with st.spinner("Applying filters..."):
            st.markdown("""
            <div class="filter-summary">
                <h4 style="margin: 0 0 0.5rem 0;">✅ Filters Applied Successfully!</h4>
                <p style="margin: 0; opacity: 0.9;">Searching trains with your custom preferences...</p>
            </div>
            """, unsafe_allow_html=True)

            # Mock filtered results
            st.dataframe(
                pd.DataFrame({
                    "Train": ["12301", "20844", "15017"],
                    "Type": ["Rajdhani", "Express", "Express"],
                    "Duration": ["15:40", "16:30", "16:15"],
                    "Price": ["₹3,200", "₹2,900", "₹2,800"],
                    "Rating": ["4.8/5", "4.6/5", "4.7/5"],
                    "Available": ["45", "60", "40"],
                }),
                use_container_width=True
            )
