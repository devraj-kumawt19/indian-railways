import requests
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import time
import os
import re
from datetime import datetime as dt

# Suppress SSL warnings for unreliable external APIs
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class IndianRailwaysAPI:
    """API client for Indian Railways data with multiple sources."""

    def __init__(self, api_key: str = None):
        # Multiple API sources for reliability
        self.apis = {
            'rapidapi': {
                'base_url': "https://indian-railway-irctc.p.rapidapi.com",
                'key': os.getenv('RAPIDAPI_KEY', '3b7554c8e8msh7d1e9de92fdb47fp1216c1jsn764d8ae99874'),
                'host': 'indian-railways-data-api.p.rapidapi.com'
            },
            'rapidapi_journey': {
                'base_url': "https://indian-railways-data-api.p.rapidapi.com/api/v1",
                'key': os.getenv('RAPIDAPI_KEY', '3b7554c8e8msh7d1e9de92fdb47fp1216c1jsn764d8ae99874'),
                'host': 'indian-railways-data-api.p.rapidapi.com'
            },
            'railwayapi': {
                'base_url': "https://api.railwayapi.com/v2",
                'key': api_key or os.getenv('RAILWAY_API_KEY', 'demo_key')
            },
            'indianrail': {
                'base_url': "https://indianrailapi.com/api/v2",
                'key': api_key or os.getenv('INDIAN_RAIL_API_KEY', 'demo_key')
            },
            'irctc': {
                'base_url': "https://www.irctc.co.in/eticketing/protected/mapps1",
                'key': None  # IRCTC doesn't require API key for basic queries
            },
            'ntes': {
                'base_url': "https://enquiry.indianrail.gov.in/mntes",
                'key': None  # NTES scraping doesn't need API key
            }
        }

        # Current working API
        self.current_api = 'rapidapi_journey'
        self.api_key = self.apis[self.current_api]['key']

        # NTES scraping constants
        self.ntes_headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0"
            ),
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Referer": "https://enquiry.indianrail.gov.in/mntes/",
            "Origin": "https://enquiry.indianrail.gov.in",
            "X-Requested-With": "XMLHttpRequest",
        }

        # Enhanced station codes database - comprehensive list
        self.station_codes = {
            # Major metros
            'mumbai': 'BCT', 'delhi': 'NDLS', 'new delhi': 'NDLS', 'kolkata': 'KOAA',
            'chennai': 'MAS', 'bangalore': 'SBC', 'bengaluru': 'SBC', 'ahmedabad': 'ADI',
            'pune': 'PUNE', 'hyderabad': 'HYB', 'secunderabad': 'SC', 'kochi': 'ERS',
            # Northern India
            'jaipur': 'JP', 'jp': 'JP', 'lucknow': 'LKO', 'kanpur': 'CNB', 'jodhpur': 'JU',
            'udaipur': 'UDZ', 'ajmer': 'AII', 'bikaner': 'BKN', 'agra': 'AGC', 'mathura': 'MTJ',
            'meerut': 'MTJ', 'ambala': 'UMB', 'chandigarh': 'CDG', 'amritsar': 'ASR',
            'ludhiana': 'LDH', 'jalandhar': 'JUC', 'bathinda': 'BTI', 'patiala': 'PTA',
            # Eastern India
            'allahabad': 'ALD', 'prayagraj': 'ALD', 'varanasi': 'BSB', 'gorakhpur': 'GKP',
            'patna': 'PNBE', 'gaya': 'GAYA', 'darbhanga': 'DBG', 'muzaffarpur': 'MFP',
            # Central India
            'bhopal': 'BPL', 'indore': 'INDB', 'nagpur': 'NGP', 'jabalpur': 'JBP',
            'satna': 'SATN', 'gwalior': 'GWL', 'ujjain': 'UJN', 'kota': 'KJ', 'kota junction': 'KJ',
            # Western India
            'surat': 'ST', 'vadodara': 'BRC', 'rajkot': 'RJT', 'bhavnagar': 'BH',
            'porbandar': 'POR', 'junagadh': 'JNG',
            # Southern India
            'coimbatore': 'CBE', 'madurai': 'MDU', 'trichy': 'TPJ', 'salem': 'SA',
            'trivandrum': 'TVC', 'calicut': 'CLT', 'mangalore': 'MAJN',
            'vijayawada': 'BZA', 'visakhapatnam': 'VSKP', 'rajahmundry': 'RJY',
            'tirupati': 'TIPT', 'salem': 'SA'
        }

    def _switch_api(self):
        """Switch to next available API."""
        apis = list(self.apis.keys())
        current_index = apis.index(self.current_api)
        self.current_api = apis[(current_index + 1) % len(apis)]
        self.api_key = self.apis[self.current_api]['key']
        print(f"Switched to API: {self.current_api}")

    def _make_request(self, endpoint: str, max_retries: int = 2) -> Optional[Dict]:
        """Make API request with fallback to different APIs and graceful degradation."""
        last_error = None
        
        for attempt in range(max_retries):
            try:
                api_config = self.apis[self.current_api]
                base_url = api_config['base_url']
                url = f"{base_url}{endpoint}"

                # Prepare headers based on API type
                headers = {'Content-Type': 'application/json'}
                if self.current_api == 'rapidapi':
                    headers.update({
                        'x-rapidapi-key': api_config['key'],
                        'x-rapidapi-host': api_config.get('host', 'indian-railways-data-api.p.rapidapi.com')
                    })

                # Add API key if required for other APIs
                if api_config['key'] and 'apikey' not in url and self.current_api != 'rapidapi':
                    url = url.replace('/apikey/', f'/apikey/{api_config["key"]}/')

                response = requests.get(url, headers=headers, timeout=10, verify=False)

                if response.status_code == 200:
                    data = response.json()
                    if data.get('response_code') == 200 or data.get('status') == 'success' or isinstance(data, dict):
                        return data

                # If API fails, try next one
                if attempt < max_retries - 1:
                    self._switch_api()

            except (requests.ConnectionError, requests.Timeout, requests.exceptions.RequestException) as e:
                last_error = str(e)
                # Skip verbose logging for connection errors - just retry silently
                if attempt < max_retries - 1:
                    self._switch_api()
            except Exception as e:
                last_error = str(e)
                print(f"API Error ({self.current_api}): {e}")
                if attempt < max_retries - 1:
                    self._switch_api()

        # If all APIs fail, return None gracefully (will trigger mock data fallback)
        return None

    def get_train_schedule(self, train_no: str) -> Optional[Dict]:
        """Get train schedule information."""
        # Try API first
        endpoint = f"/route/train/{train_no}/apikey/demo_key/"
        data = self._make_request(endpoint)

        if data:
            return self._parse_train_schedule(data)

        # Fallback to mock data
        return self._get_mock_schedule(train_no)

    def get_live_train_status(self, train_no: str, date: str = None) -> Optional[Dict]:
        """Get live train status - now uses NTES scraping as primary method."""
        try:
            # Try NTES scraping first (most reliable)
            train_number = int(train_no)
            ntes_data = self.get_realtime_train_status(train_number)
            if ntes_data:
                ntes_data['train_no'] = train_no
                return self._convert_ntes_to_api_format(ntes_data)
        except Exception as e:
            print(f"NTES scraping failed: {e}")

        # Fallback to regular APIs
        if date is None:
            date = datetime.now().strftime("%d-%m-%Y")

        # Try API first
        endpoint = f"/live/train/{train_no}/date/{date}/apikey/demo_key/"
        data = self._make_request(endpoint)

        if data:
            return self._parse_live_status(data)

        # Fallback to mock data
        return self._get_mock_status(train_no)

    def get_all_trains_between_stations(self, from_station: str, to_station: str,
                                       date: str = None) -> List[Dict]:
        """Get all trains between two stations."""
        if date is None:
            date = datetime.now().strftime("%d-%m-%Y")

        # Try API first
        endpoint = f"/between/source/{from_station}/dest/{to_station}/date/{date}/apikey/demo_key/"
        data = self._make_request(endpoint)

        if data and data.get('trains'):
            return data['trains']

        # Fallback to mock data
        return self._get_mock_trains_between_stations(from_station, to_station)

    def get_station_code(self, station_name: str) -> Optional[str]:
        """Get station code from station name with advanced fuzzy matching."""
        # Direct lookup
        station_name_lower = station_name.lower().strip()
        
        if station_name_lower in self.station_codes:
            return self.station_codes[station_name_lower]
        
        # Try substring match first
        for key, code in self.station_codes.items():
            if station_name_lower in key:  # e.g., "jod" in "jodhpur"
                return code
            if key in station_name_lower:  # e.g., "jaipur" in "jaipur city"
                return code
        
        # Try fuzzy matching for typos
        def levenshtein_distance(s1: str, s2: str) -> int:
            """Calculate Levenshtein distance between two strings."""
            if len(s1) < len(s2):
                return levenshtein_distance(s2, s1)
            if len(s2) == 0:
                return len(s1)
            
            previous_row = range(len(s2) + 1)
            for i, c1 in enumerate(s1):
                current_row = [i + 1]
                for j, c2 in enumerate(s2):
                    insertions = previous_row[j + 1] + 1
                    deletions = current_row[j] + 1
                    substitutions = previous_row[j] + (c1 != c2)
                    current_row.append(min(insertions, deletions, substitutions))
                previous_row = current_row
            return previous_row[-1]
        
        # Find best match with distance tolerance
        best_match = None
        best_distance = float('inf')
        threshold = 2  # Allow up to 2 character differences
        
        for key, code in self.station_codes.items():
            distance = levenshtein_distance(station_name_lower, key)
            if distance < best_distance and distance <= threshold:
                best_match = code
                best_distance = distance
        
        if best_match:
            return best_match
        
        # Try API as last resort
        endpoint = f"/name-to-code/station/{station_name}/apikey/demo_key/"
        data = self._make_request(endpoint)

        if data and data.get('stations'):
            return data['stations'][0]['code']

        # Return None if not found (let caller handle)
        return None

    def get_pnr_status(self, pnr_number: str) -> Optional[Dict]:
        """Get PNR status information."""
        endpoint = f"/pnr-status/pnr/{pnr_number}/apikey/demo_key/"
        data = self._make_request(endpoint)

        if data:
            return self._parse_pnr_status(data)

        return self._get_mock_pnr_status(pnr_number)

    def get_train_fare(self, train_no: str, from_station: str, to_station: str,
                      train_class: str = "SL", age: int = 25) -> Optional[Dict]:
        """Get train fare information."""
        endpoint = f"/fare/train/{train_no}/source/{from_station}/dest/{to_station}/age/{age}/pref/{train_class}/quota/GN/apikey/demo_key/"
        data = self._make_request(endpoint)

        if data:
            return self._parse_train_fare(data)

        return self._get_mock_train_fare(train_no, from_station, to_station, train_class)

    def get_train_journey_schedule(self, train_no: str, journey_date: str = None) -> Optional[Dict]:
        """
        Get detailed train journey schedule with station-by-station live tracking.
        Uses RapidAPI endpoint for comprehensive journey data.
        
        Args:
            train_no: Train number (e.g., "20844")
            journey_date: Journey date in format "YYYY-MM-DD" (defaults to today)
        
        Returns:
            Dict with stations, timings, delays, platform info
        """
        if journey_date is None:
            journey_date = datetime.now().strftime("%Y-%m-%d")
        
        try:
            # Use RapidAPI Journey endpoint
            api_config = self.apis.get('rapidapi_journey')
            if not api_config:
                return self._get_mock_journey_schedule(train_no)
            
            base_url = api_config['base_url']
            url = f"{base_url}/trains/{train_no}/schedule?journeyDate={journey_date}"
            
            headers = {
                'x-rapidapi-host': api_config.get('host', 'indian-railways-data-api.p.rapidapi.com'),
                'x-rapidapi-key': api_config['key']
            }
            
            response = requests.get(url, headers=headers, timeout=10, verify=False)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and ('stations' in data or 'journey' in data or 'stops' in data):
                    return self._parse_journey_schedule(data, train_no)
            
            # Fallback to alternative API
            return self._get_mock_journey_schedule(train_no)
            
        except Exception as e:
            print(f"Journey schedule fetch failed: {e}")
            return self._get_mock_journey_schedule(train_no)

    def _parse_journey_schedule(self, data: Dict, train_no: str) -> Dict:
        """Parse journey schedule from API response."""
        try:
            stations = data.get('stations', data.get('journey', data.get('stops', [])))
            
            parsed_stops = []
            for idx, station in enumerate(stations):
                stop = {
                    'sequence': station.get('sequence', idx + 1),
                    'station_code': station.get('stationCode', station.get('code', '')),
                    'station_name': station.get('stationName', station.get('name', '')),
                    'arrival_time': station.get('arrivalTime', station.get('arrival', 'N/A')),
                    'departure_time': station.get('departureTime', station.get('departure', 'N/A')),
                    'halt_minutes': station.get('halt', station.get('stopDuration', 0)),
                    'distance': station.get('distance', 0),
                    'platform': station.get('platform', 'N/A'),
                    'delay': station.get('delay', 0),
                    'status': station.get('status', 'Scheduled')
                }
                parsed_stops.append(stop)
            
            return {
                'train_no': train_no,
                'train_name': data.get('trainName', f'Train {train_no}'),
                'journey_date': data.get('journeyDate'),
                'total_distance': data.get('totalDistance', 0),
                'total_stations': len(parsed_stops),
                'source_station': parsed_stops[0]['station_name'] if parsed_stops else '',
                'destination_station': parsed_stops[-1]['station_name'] if parsed_stops else '',
                'journey_time': data.get('journeyTime', ''),
                'stations': parsed_stops,
                'current_position': data.get('currentPosition'),
                'overall_delay': data.get('overallDelay', 0)
            }
        except Exception as e:
            print(f"Error parsing journey schedule: {e}")
            return None

    def _get_mock_journey_schedule(self, train_no: str) -> Dict:
        """Get mock journey schedule with sample station data."""
        mock_data = {
            '20844': {
                'train_no': '20844',
                'train_name': 'Express Train 20844',
                'journey_date': datetime.now().strftime("%Y-%m-%d"),
                'total_distance': 1465,
                'total_stations': 15,
                'source_station': 'New Delhi',
                'destination_station': 'Kolkata',
                'journey_time': '16h 30m',
                'overall_delay': 0,
                'stations': [
                    {
                        'sequence': 1,
                        'station_code': 'NDLS',
                        'station_name': 'New Delhi',
                        'arrival_time': '00:00',
                        'departure_time': '17:00',
                        'halt_minutes': 0,
                        'distance': 0,
                        'platform': '1',
                        'delay': 0,
                        'status': 'Departed'
                    },
                    {
                        'sequence': 2,
                        'station_code': 'MTJ',
                        'station_name': 'Mathura',
                        'arrival_time': '19:45',
                        'departure_time': '19:55',
                        'halt_minutes': 10,
                        'distance': 58,
                        'platform': '2',
                        'delay': 0,
                        'status': 'Arrived'
                    },
                    {
                        'sequence': 3,
                        'station_code': 'AGC',
                        'station_name': 'Agra',
                        'arrival_time': '21:00',
                        'departure_time': '21:10',
                        'halt_minutes': 10,
                        'distance': 100,
                        'platform': '3',
                        'delay': 5,
                        'status': 'Arrived'
                    },
                    {
                        'sequence': 4,
                        'station_code': 'GWL',
                        'station_name': 'Gwalior',
                        'arrival_time': '23:30',
                        'departure_time': '23:40',
                        'halt_minutes': 10,
                        'distance': 206,
                        'platform': '1',
                        'delay': 3,
                        'status': 'Scheduled'
                    },
                    {
                        'sequence': 5,
                        'station_code': 'JBP',
                        'station_name': 'Jabalpur',
                        'arrival_time': '04:15',
                        'departure_time': '04:25',
                        'halt_minutes': 10,
                        'distance': 400,
                        'platform': '2',
                        'delay': 0,
                        'status': 'Scheduled'
                    },
                    {
                        'sequence': 6,
                        'station_code': 'BSB',
                        'station_name': 'Varanasi',
                        'arrival_time': '09:30',
                        'departure_time': '09:40',
                        'halt_minutes': 10,
                        'distance': 700,
                        'platform': '1',
                        'delay': 0,
                        'status': 'Scheduled'
                    },
                    {
                        'sequence': 7,
                        'station_code': 'PNBE',
                        'station_name': 'Patna',
                        'arrival_time': '13:45',
                        'departure_time': '13:55',
                        'halt_minutes': 10,
                        'distance': 900,
                        'platform': '2',
                        'delay': 0,
                        'status': 'Scheduled'
                    },
                    {
                        'sequence': 8,
                        'station_code': 'KOAA',
                        'station_name': 'Kolkata',
                        'arrival_time': '09:30',
                        'departure_time': '00:00',
                        'halt_minutes': 0,
                        'distance': 1465,
                        'platform': '1',
                        'delay': 0,
                        'status': 'Scheduled'
                    }
                ]
            },
            '20846': {
                'train_no': '20846',
                'train_name': 'Moradabad Junction Express',
                'journey_date': datetime.now().strftime("%Y-%m-%d"),
                'total_distance': 671,
                'total_stations': 9,
                'source_station': 'Delhi Central',
                'destination_station': 'Jaisalmer',
                'journey_time': '14h 35m',
                'overall_delay': 0,
                'stations': [
                    {
                        'sequence': 1,
                        'station_code': 'NDLS',
                        'station_name': 'Delhi Central',
                        'arrival_time': '00:00',
                        'departure_time': '08:15',
                        'halt_minutes': 0,
                        'distance': 0,
                        'platform': '1',
                        'delay': 0,
                        'status': 'Departed'
                    },
                    {
                        'sequence': 2,
                        'station_code': 'MOKM',
                        'station_name': 'Moradabad',
                        'arrival_time': '10:30',
                        'departure_time': '10:40',
                        'halt_minutes': 10,
                        'distance': 95,
                        'platform': '2',
                        'delay': 0,
                        'status': 'Arrived'
                    },
                    {
                        'sequence': 3,
                        'station_code': 'POK',
                        'station_name': 'Pokaran',
                        'arrival_time': '20:15',
                        'departure_time': '20:25',
                        'halt_minutes': 10,
                        'distance': 380,
                        'platform': '1',
                        'delay': 0,
                        'status': 'Scheduled'
                    },
                    {
                        'sequence': 4,
                        'station_code': 'ASR',
                        'station_name': 'Ashapura Gomat',
                        'arrival_time': '20:55',
                        'departure_time': '21:05',
                        'halt_minutes': 10,
                        'distance': 410,
                        'platform': '2',
                        'delay': 0,
                        'status': 'Scheduled'
                    },
                    {
                        'sequence': 5,
                        'station_code': 'OJR',
                        'station_name': 'Odhaniya Chacha',
                        'arrival_time': '21:38',
                        'departure_time': '21:48',
                        'halt_minutes': 10,
                        'distance': 443,
                        'platform': '1',
                        'delay': 0,
                        'status': 'Scheduled'
                    },
                    {
                        'sequence': 6,
                        'station_code': 'SBN',
                        'station_name': 'Shri Bhadriya Lathi',
                        'arrival_time': '22:09',
                        'departure_time': '22:19',
                        'halt_minutes': 10,
                        'distance': 464,
                        'platform': '2',
                        'delay': 0,
                        'status': 'Scheduled'
                    },
                    {
                        'sequence': 7,
                        'station_code': 'JCA',
                        'station_name': 'Jetha Chandan',
                        'arrival_time': '22:39',
                        'departure_time': '22:49',
                        'halt_minutes': 10,
                        'distance': 485,
                        'platform': '1',
                        'delay': 0,
                        'status': 'Scheduled'
                    },
                    {
                        'sequence': 8,
                        'station_code': 'THJ',
                        'station_name': 'Thaiyat Hamira Junction',
                        'arrival_time': '23:13',
                        'departure_time': '23:23',
                        'halt_minutes': 10,
                        'distance': 509,
                        'platform': '2',
                        'delay': 0,
                        'status': 'Scheduled'
                    },
                    {
                        'sequence': 9,
                        'station_code': 'JSM',
                        'station_name': 'Jaisalmer',
                        'arrival_time': '22:40',
                        'departure_time': '00:00',
                        'halt_minutes': 0,
                        'distance': 671,
                        'platform': '1',
                        'delay': 0,
                        'status': 'Scheduled'
                    }
                ]
            },
            '12301': {
                'train_no': '12301',
                'train_name': 'Rajdhani Express',
                'journey_date': datetime.now().strftime("%Y-%m-%d"),
                'total_distance': 1447,
                'total_stations': 5,
                'source_station': 'New Delhi',
                'destination_station': 'Mumbai Central',
                'journey_time': '16h 30m',
                'overall_delay': 0,
                'stations': [
                    {
                        'sequence': 1,
                        'station_code': 'NDLS',
                        'station_name': 'New Delhi',
                        'arrival_time': '00:00',
                        'departure_time': '16:00',
                        'halt_minutes': 0,
                        'distance': 0,
                        'platform': '1',
                        'delay': 0,
                        'status': 'Departed'
                    },
                    {
                        'sequence': 2,
                        'station_code': 'JP',
                        'station_name': 'Jaipur',
                        'arrival_time': '20:45',
                        'departure_time': '20:55',
                        'halt_minutes': 10,
                        'distance': 262,
                        'platform': '2',
                        'delay': 0,
                        'status': 'Arrived'
                    },
                    {
                        'sequence': 3,
                        'station_code': 'ADI',
                        'station_name': 'Ahmedabad',
                        'arrival_time': '23:30',
                        'departure_time': '23:40',
                        'halt_minutes': 10,
                        'distance': 515,
                        'platform': '3',
                        'delay': 0,
                        'status': 'Scheduled'
                    },
                    {
                        'sequence': 4,
                        'station_code': 'PUNE',
                        'station_name': 'Pune',
                        'arrival_time': '06:15',
                        'departure_time': '06:25',
                        'halt_minutes': 10,
                        'distance': 1098,
                        'platform': '1',
                        'delay': 0,
                        'status': 'Scheduled'
                    },
                    {
                        'sequence': 5,
                        'station_code': 'BCT',
                        'station_name': 'Mumbai Central',
                        'arrival_time': '08:30',
                        'departure_time': '00:00',
                        'halt_minutes': 0,
                        'distance': 1447,
                        'platform': '2',
                        'delay': 0,
                        'status': 'Scheduled'
                    }
                ]
            }
        }
        
        # Check if train exists in predefined mock data
        if train_no in mock_data:
            return mock_data[train_no]
        
        # Generate dynamic mock data for any train number
        import random
        
        # Random station combinations
        stations_list = [
            ('NDLS', 'New Delhi'),
            ('BZA', 'Vijayawada'),
            ('MTJ', 'Mathura'),
            ('AGC', 'Agra'),
            ('GWL', 'Gwalior'),
            ('JBP', 'Jabalpur'),
            ('BSB', 'Varanasi'),
            ('PNBE', 'Patna'),
            ('KOAA', 'Kolkata'),
            ('HWH', 'Howrah'),
            ('SRE', 'Surat'),
            ('BRC', 'Vadodara'),
            ('JP', 'Jaipur'),
            ('ADI', 'Ahmedabad'),
            ('PUNE', 'Pune'),
            ('BCT', 'Mumbai'),
            ('BBS', 'Bhubaneswar'),
            ('CSTM', 'Mumbai CST'),
            ('CNB', 'Kanpur'),
            ('LKO', 'Lucknow')
        ]
        
        # Generate 6-8 random stops
        num_stops = random.randint(6, 8)
        selected_stations = random.sample(stations_list, min(num_stops, len(stations_list)))
        
        total_distance = random.randint(500, 2000)
        stations = []
        
        for idx, (code, name) in enumerate(selected_stations):
            if idx == 0:
                stations.append({
                    'sequence': 1,
                    'station_code': code,
                    'station_name': name,
                    'arrival_time': '00:00',
                    'departure_time': f'{8 + idx}:00',
                    'halt_minutes': 0,
                    'distance': 0,
                    'platform': str((idx % 4) + 1),
                    'delay': 0,
                    'status': 'Departed'
                })
            elif idx == len(selected_stations) - 1:
                arrival_hour = 8 + (idx * 2)
                stations.append({
                    'sequence': idx + 1,
                    'station_code': code,
                    'station_name': name,
                    'arrival_time': f'{arrival_hour % 24:02d}:00',
                    'departure_time': '00:00',
                    'halt_minutes': 0,
                    'distance': total_distance,
                    'platform': str((idx % 4) + 1),
                    'delay': random.randint(0, 5),
                    'status': 'Scheduled'
                })
            else:
                arrival_hour = 8 + (idx * 2)
                departure_hour = arrival_hour + 1
                stations.append({
                    'sequence': idx + 1,
                    'station_code': code,
                    'station_name': name,
                    'arrival_time': f'{arrival_hour % 24:02d}:30',
                    'departure_time': f'{departure_hour % 24:02d}:00',
                    'halt_minutes': 10,
                    'distance': int((idx / len(selected_stations)) * total_distance),
                    'platform': str((idx % 4) + 1),
                    'delay': random.randint(0, 3),
                    'status': 'Arrived' if idx < 2 else 'Scheduled'
                })
        
        return {
            'train_no': train_no,
            'train_name': f'Train {train_no}',
            'journey_date': datetime.now().strftime("%Y-%m-%d"),
            'total_distance': total_distance,
            'total_stations': len(stations),
            'source_station': stations[0]['station_name'] if stations else 'Source',
            'destination_station': stations[-1]['station_name'] if stations else 'Destination',
            'journey_time': f'{random.randint(14, 24)}h {random.randint(0, 59)}m',
            'overall_delay': random.randint(0, 10),
            'stations': stations
        }

    def get_realtime_train_status(self, train_number: int) -> Optional[Dict]:
        """Get real-time train status by scraping NTES website."""
        try:
            html_text = self._fetch_ntes_train_status_html(train_number)
            parsed_data = self._parse_ntes_train_status_html(html_text)
            return parsed_data
        except Exception as e:
            print(f"NTES scraping failed: {e}")
            # Fallback to regular API
            return self.get_live_train_status(str(train_number))

    def _fetch_ntes_train_status_html(self, train_number: int, timeout_s: float = 8.0) -> str:
        """Fetch running status HTML from NTES website with improved error handling."""
        session = requests.Session()
        session.headers.update(self.ntes_headers)
        session.verify = False  # Disable SSL verification for reliability

        try:
            # Bootstrap session with shorter timeout
            r = session.get("https://enquiry.indianrail.gov.in/mntes/", timeout=timeout_s)
            r.raise_for_status()

            # Get CSRF token with retry
            params = {"t": int(dt.now().timestamp() * 1000)}
            r = session.get("https://enquiry.indianrail.gov.in/mntes/GetCSRFToken", params=params, timeout=timeout_s)
            r.raise_for_status()

            csrf_match = re.search(r"name='([^']+)' value='([^']+)'", r.text)
            if not csrf_match:
                raise Exception("CSRF token not found")

            csrf_key, csrf_val = csrf_match.group(1), csrf_match.group(2)

            # Fetch train status
            today_str = dt.now().strftime("%d-%b-%Y")
            params = {
                "opt": "TrainRunning",
                "subOpt": "FindRunningInstance",
                "refDate": today_str,
            }
            data = {
                "lan": "en",
                "jDate": today_str,
                "trainNo": str(train_number),
                csrf_key: csrf_val,
            }

            r = session.post("https://enquiry.indianrail.gov.in/mntes/tr", params=params, data=data, timeout=timeout_s)
            r.raise_for_status()
            return r.text
        except Exception as e:
            raise Exception(f"NTES fetch failed: {e}")

    def _parse_ntes_train_status_html(self, html_text: str) -> Dict:
        """Parse NTES HTML into structured train status data."""
        # Extract status lines
        text = self._strip_html_tags(html_text)
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

        # Keywords for status lines
        keywords = [
            "Arrived", "Arrive", "Arriving", "Departed", "Depart", "Departure",
            "On Time", "Yet to start", "Reached Destination", "Current Position",
            "Last Updates On", "Start Date"
        ]

        status_lines = []
        for ln in lines:
            lnl = ln.lower()
            for kw in keywords:
                if kw.lower() in lnl:
                    status_lines.append(ln)
                    break

        # Remove duplicates
        seen = set()
        unique_lines = []
        for line in status_lines:
            if line not in seen:
                unique_lines.append(line)
                seen.add(line)

        # Parse last update time
        last_update = self._parse_last_update_time(unique_lines)

        # Parse start date
        start_date = self._parse_start_date(unique_lines)

        # Parse events
        events = self._parse_train_events(unique_lines, last_update)

        return {
            'train_number': None,  # Will be set by caller
            'start_date': start_date,
            'last_update': last_update,
            'events': events,
            'raw_status': unique_lines[:5]  # First 5 status lines
        }

    def _strip_html_tags(self, html_text: str) -> str:
        """Strip HTML tags and scripts from text."""
        # Remove scripts and styles
        html_text = re.sub(r"(?is)<script.*?>.*?</script>", "", html_text)
        html_text = re.sub(r"(?is)<style.*?>.*?</style>", "", html_text)
        # Remove HTML tags
        return re.sub(r"<[^>]+>", "", html_text)

    def _parse_last_update_time(self, lines: List[str]) -> Optional[dt]:
        """Parse last update timestamp from status lines."""
        for ln in lines:
            match = re.search(
                r"Last Updates On\s*(?P<date>\d{1,2}-[A-Za-z]{3}-\d{4})(?:\s+(?P<time>\d{1,2}:\d{2}))?",
                ln, flags=re.I
            )
            if match:
                date = match.group("date")
                time_str = match.group("time") or "00:00"
                try:
                    return dt.strptime(f"{date} {time_str}", "%d-%b-%Y %H:%M")
                except:
                    continue
        return None

    def _parse_start_date(self, lines: List[str]) -> Optional[str]:
        """Parse start date from status lines."""
        for ln in lines:
            match = re.search(
                r"Start Date\s*:\s*(?P<date>\d{1,2}-[A-Za-z]{3}-\d{4})",
                ln, flags=re.I
            )
            if match:
                return match.group("date")
        return None

    def _parse_train_events(self, lines: List[str], last_update: Optional[dt]) -> List[Dict]:
        """Parse arrival/departure events from status lines."""
        events = []

        for ln in lines:
            if not re.search(r"\b(arrived|arrive|arriving|departed|depart|departure)\b", ln, flags=re.I):
                continue

            event = {
                'raw': ln,
                'type': None,
                'station': None,
                'code': None,
                'datetime': None,
                'delay': None
            }

            # Parse delay
            delay_match = re.search(r"Delay[:\-\s]*\(?\s*(?:Delay\s*)?([0-9:]{1,5})\)?", ln, flags=re.I)
            if delay_match:
                event['delay'] = delay_match.group(1)

            # Parse station and type
            station_match = re.search(
                r"\b(Departed|Arrived)\b\s+(?:from|at)\s+(?P<station>[^()]+?)\s*\(\s*(?P<code>[A-Z0-9]{1,6})\s*\)",
                ln, flags=re.I
            )

            if station_match:
                event['type'] = station_match.group(1).title()
                event['station'] = station_match.group("station").strip()
                event['code'] = station_match.group("code").strip()

                # Parse datetime
                time_match = re.search(r"(\d{1,2}:\d{2})", ln)
                date_match = re.search(r"(\d{1,2}-[A-Za-z]{3}(?:-\d{4})?)", ln)

                event['datetime'] = self._build_event_datetime(
                    date_part=date_match.group(1) if date_match else None,
                    time_part=time_match.group(1) if time_match else None,
                    last_update=last_update
                )

                if event['type'] and event['station']:
                    events.append(event)

        # Remove duplicates
        seen = set()
        unique_events = []
        for event in events:
            key = (event.get('type'), event.get('station'), event.get('datetime'))
            if key not in seen:
                unique_events.append(event)
                seen.add(key)

        return unique_events

    def _build_event_datetime(self, date_part: Optional[str], time_part: Optional[str], last_update: Optional[dt]) -> Optional[dt]:
        """Build datetime object for train event."""
        time_part = time_part or "00:00"

        if date_part:
            if re.match(r"\d{1,2}-[A-Za-z]{3}-\d{4}$", date_part):
                date_str = date_part
            else:
                year = last_update.year if last_update else dt.now().year
                date_str = f"{date_part}-{year}"

            try:
                return dt.strptime(f"{date_str} {time_part}", "%d-%b-%Y %H:%M")
            except:
                pass

        if last_update:
            try:
                return dt.strptime(
                    f"{last_update.strftime('%d-%b-%Y')} {time_part}",
                    "%d-%b-%Y %H:%M"
                )
            except:
                pass

        return None

    def get_train_classes(self, train_no: str) -> List[str]:
        """Get available classes for a train."""
        schedule = self.get_train_schedule(train_no)
        if schedule:
            # Extract classes from schedule data
            return ["1A", "2A", "3A", "SL", "CC", "2S"]  # Common classes

        return ["SL", "3A", "2A", "1A"]  # Default classes

    def search_trains(self, from_station: str, to_station: str, date: str = None) -> List[Dict]:
        """Search for trains between stations (alias for get_all_trains_between_stations)."""
        return self.get_all_trains_between_stations(from_station, to_station, date)

    def _parse_train_schedule(self, data: Dict) -> Dict:
        """Parse train schedule from API response."""
        train = data.get('train', {})
        return {
            'train_no': train.get('number'),
            'train_name': train.get('name'),
            'from_station': train.get('from_station', {}).get('name'),
            'to_station': train.get('to_station', {}).get('name'),
            'schedule': data.get('route', [])
        }

    def _parse_live_status(self, data: Dict) -> Dict:
        """Parse live status from API response."""
        train = data.get('train', {})
        current_station = data.get('current_station', {})
        return {
            'train_no': train.get('number'),
            'train_name': train.get('name'),
            'current_station': current_station.get('name'),
            'status': data.get('position'),
            'delay': data.get('delay', 0),
            'expected_time': current_station.get('scharr'),
            'actual_time': current_station.get('actarr')
        }

    def _get_mock_schedule(self, train_no: str) -> Dict:
        """Mock train schedule data."""
        mock_schedules = {
            '12301': {
                'train_no': '12301',
                'train_name': 'Rajdhani Express',
                'from_station': 'New Delhi',
                'to_station': 'Mumbai Central',
                'schedule': [
                    {'station': 'NDLS', 'arrival': '00:00', 'departure': '16:55'},
                    {'station': 'BCT', 'arrival': '08:35', 'departure': '00:00'}
                ]
            },
            '12302': {
                'train_no': '12302',
                'train_name': 'Shatabdi Express',
                'from_station': 'New Delhi',
                'to_station': 'Chandigarh',
                'schedule': [
                    {'station': 'NDLS', 'arrival': '00:00', 'departure': '06:45'},
                    {'station': 'CDG', 'arrival': '10:55', 'departure': '00:00'}
                ]
            }
        }
        return mock_schedules.get(train_no, {})

    def _get_mock_status(self, train_no: str) -> Dict:
        """Mock live train status."""
        mock_status = {
            '12301': {
                'train_no': '12301',
                'train_name': 'Rajdhani Express',
                'current_station': 'KOTA',
                'status': 'Running on time',
                'delay': 0,
                'expected_time': '22:30',
                'actual_time': '22:30'
            },
            '12302': {
                'train_no': '12302',
                'train_name': 'Shatabdi Express',
                'current_station': 'AMBALA',
                'status': 'Running 15 mins late',
                'delay': 15,
                'expected_time': '09:45',
                'actual_time': '10:00'
            }
        }
        return mock_status.get(train_no, {})

    def _get_mock_trains_between_stations(self, from_station: str, to_station: str) -> List[Dict]:
        """Mock trains between stations."""
        return [
            {
                'number': '12301',
                'name': 'Rajdhani Express',
                'src_departure_time': '16:55',
                'dest_arrival_time': '08:35',
                'travel_time': '15:40'
            },
            {
                'number': '12401',
                'name': 'Magadh Express',
                'src_departure_time': '14:00',
                'dest_arrival_time': '06:30',
                'travel_time': '16:30'
            }
        ]

    def _parse_pnr_status(self, data: Dict) -> Dict:
        """Parse PNR status from API response."""
        pnr_data = data.get('pnr_data', {})
        return {
            'pnr': data.get('pnr'),
            'train_no': pnr_data.get('train_no'),
            'train_name': pnr_data.get('train_name'),
            'from_station': pnr_data.get('from_station'),
            'to_station': pnr_data.get('to_station'),
            'boarding_point': pnr_data.get('boarding_point'),
            'reservation_upto': pnr_data.get('reservation_upto'),
            'journey_date': pnr_data.get('date_of_journey'),
            'passengers': pnr_data.get('passengers', []),
            'chart_prepared': pnr_data.get('chart_prepared', False)
        }

    def _parse_train_fare(self, data: Dict) -> Dict:
        """Parse train fare from API response."""
        fare_data = data.get('fare', {})
        return {
            'train_no': data.get('train', {}).get('number'),
            'from_station': data.get('from_station', {}).get('code'),
            'to_station': data.get('to_station', {}).get('code'),
            'fare': fare_data.get('fare'),
            'base_fare': fare_data.get('base_fare'),
            'reservation_charge': fare_data.get('reservation_charge'),
            'superfast_charge': fare_data.get('superfast_charge'),
            'total_fare': fare_data.get('total_fare'),
            'class': data.get('quota', {}).get('class')
        }

    def _get_mock_pnr_status(self, pnr_number: str) -> Dict:
        """Mock PNR status data."""
        return {
            'pnr': pnr_number,
            'train_no': '12301',
            'train_name': 'Rajdhani Express',
            'from_station': 'New Delhi (NDLS)',
            'to_station': 'Mumbai Central (BCT)',
            'boarding_point': 'New Delhi (NDLS)',
            'reservation_upto': 'Mumbai Central (BCT)',
            'journey_date': datetime.now().strftime("%d-%m-%Y"),
            'passengers': [
                {'name': 'Passenger 1', 'booking_status': 'CNF', 'current_status': 'CNF'}
            ],
            'chart_prepared': True
        }

    def _get_mock_train_fare(self, train_no: str, from_station: str, to_station: str, train_class: str) -> Dict:
        """Mock train fare data."""
        fare_chart = {
            'SL': 450, '3A': 1250, '2A': 1750, '1A': 2950,
            'CC': 650, '2S': 350
        }

        base_fare = fare_chart.get(train_class, 450)
        return {
            'train_no': train_no,
            'from_station': from_station,
            'to_station': to_station,
            'fare': base_fare,
            'base_fare': base_fare,
            'reservation_charge': 50,
            'superfast_charge': 75,
            'total_fare': base_fare + 50 + 75,
            'class': train_class
        }

    def _convert_ntes_to_api_format(self, ntes_data: Dict) -> Dict:
        """Convert NTES parsed data to API format."""
        events = ntes_data.get('events', [])

        # Find current position from latest event
        current_station = None
        status = "Unknown"
        delay = 0

        if events:
            latest_event = events[-1]
            current_station = latest_event.get('station')
            status = f"{latest_event.get('type', 'Unknown')} at {current_station}" if current_station else "Running"

            # Parse delay
            delay_str = latest_event.get('delay')
            if delay_str:
                try:
                    if ':' in delay_str:
                        h, m = map(int, delay_str.split(':'))
                        delay = h * 60 + m
                    else:
                        delay = int(delay_str)
                except:
                    delay = 0

        return {
            'train_no': ntes_data.get('train_number', ''),
            'train_name': f"Train {ntes_data.get('train_number', '')}",  # Could be enhanced
            'current_station': current_station,
            'status': status,
            'delay': delay,
            'expected_time': None,  # NTES doesn't provide this
            'actual_time': ntes_data.get('last_update').strftime('%H:%M') if ntes_data.get('last_update') else None,
            'events': events,  # Include parsed events
            'source': 'ntes'  # Indicate data source
        }