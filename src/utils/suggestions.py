"""
Search Suggestions Utility
Provides autocomplete suggestions for search inputs using existing datasets
"""

import streamlit as st
import pandas as pd
from typing import List, Optional
import os

@st.cache_data
def load_suggestion_data():
    """Load and cache suggestion data from existing CSV files."""
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    try:
        # Load train data
        trains_df = pd.read_csv(os.path.join(base_path, 'data', 'trains_with_coaches.csv'))
        train_numbers = trains_df['train_no'].astype(str).unique().tolist()
        train_names = trains_df['train_name'].unique().tolist()

        # Load station data
        stations_df = pd.read_csv(os.path.join(base_path, 'data', 'indian_stations.csv'))
        station_codes = stations_df['station_code'].unique().tolist()
        station_names = stations_df['station_name'].unique().tolist()

        # Load additional station data
        railway_stations_df = pd.read_csv(os.path.join(base_path, 'data', 'railway_stations.csv'))
        railway_codes = railway_stations_df['station_code'].unique().tolist()
        railway_names = railway_stations_df['station_name'].unique().tolist()

        # Combine station data
        all_station_codes = list(set(station_codes + railway_codes))
        all_station_names = list(set(station_names + railway_names))

        # Get platform numbers
        platforms = []
        if 'platform_number' in railway_stations_df.columns:
            platforms = railway_stations_df['platform_number'].dropna().astype(str).unique().tolist()
        if 'platform_count' in stations_df.columns:
            platform_counts = stations_df['platform_count'].dropna().astype(int).unique().tolist()
            platforms.extend([str(p) for p in platform_counts])

        platforms = list(set(platforms))

        return {
            'train_numbers': train_numbers,
            'train_names': train_names,
            'station_codes': all_station_codes,
            'station_names': all_station_names,
            'platforms': platforms
        }

    except Exception as e:
        st.warning(f"Could not load suggestion data: {e}")
        return {
            'train_numbers': [],
            'train_names': [],
            'station_codes': [],
            'station_names': [],
            'platforms': []
        }

def get_suggestions(query: str, suggestion_type: str, max_suggestions: int = 10) -> List[str]:
    """Get filtered suggestions based on query and type."""
    if not query or len(query) < 1:
        return []

    data = load_suggestion_data()
    suggestions = []

    if suggestion_type == 'train':
        # Search in train numbers and names
        query_lower = query.lower()
        for train_no in data['train_numbers']:
            if query_lower in str(train_no).lower():
                suggestions.append(str(train_no))
        for train_name in data['train_names']:
            if query_lower in train_name.lower():
                suggestions.append(train_name)

    elif suggestion_type == 'station':
        # Search in station codes and names
        query_lower = query.lower()
        for code in data['station_codes']:
            if query_lower in code.lower():
                suggestions.append(code)
        for name in data['station_names']:
            if query_lower in name.lower():
                suggestions.append(name)

    elif suggestion_type == 'platform':
        # Search in platform numbers
        query_lower = query.lower()
        for platform in data['platforms']:
            if query_lower in str(platform).lower():
                suggestions.append(str(platform))

    # Remove duplicates and limit
    suggestions = list(set(suggestions))[:max_suggestions]
    return sorted(suggestions)

def display_suggestions(input_key: str, suggestion_type: str, current_value: str = ""):
    """Display suggestions for a given input field."""
    if current_value and len(current_value) >= 2:
        suggestions = get_suggestions(current_value, suggestion_type)

        if suggestions:
            st.markdown(f"**💡 Suggestions for '{current_value}':**")
            cols = st.columns(min(len(suggestions), 5))

            for i, suggestion in enumerate(suggestions):
                with cols[i % 5]:
                    if st.button(
                        suggestion,
                        key=f"suggest_{input_key}_{i}",
                        help=f"Click to use '{suggestion}'"
                    ):
                        st.session_state[input_key] = suggestion
                        st.rerun()
        elif len(current_value) >= 3:
            st.caption("No suggestions found. Try a different search term.")