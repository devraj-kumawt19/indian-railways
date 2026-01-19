# Indian Railways AI Detection System

An AI-based railway platform monitoring system that detects trains, identifies coach positions, and displays live train status using Indian Railways APIs.

## Features

- 🚂 Real-time train detection using YOLO
- 🚌 Coach identification and numbering (Engine front, Guard back)
- 📍 Platform zone mapping
- 📊 **Advanced Live Train Status** - Real-time position, delays, and current station from NTES
- 🔍 Train search and route information
- 📱 Web-based dashboard using Streamlit
- 🎯 Station code lookup and train schedules
- 💰 Fare inquiry and PNR status checking
- 📋 **Detailed Train Route Events** - Complete journey timeline with arrival/departure events
- 🔄 Multiple API fallback system for reliability
- 🌐 **NTES Integration** - Direct scraping from Indian Railways National Train Enquiry System

## Indian Railways API Integration

The system integrates with multiple Indian Railways data sources for comprehensive functionality:

### Supported Data Sources
- **NTES (National Train Enquiry System)** - Official Indian Railways website scraping for real-time data
- **RailwayAPI.com** (Primary API): Live status, schedules, PNR, fares
- **IndianRailAPI.com** (Secondary fallback): Alternative data source
- **IRCTC Official** (Advanced): Official railway data
- **Mock Data**: Fallback when all APIs unavailable

### Advanced Features
- **Real-time Train Tracking**: Direct scraping from NTES for accurate live status
- **Route Event Parsing**: Detailed arrival/departure events with timestamps
- **Automatic Fallbacks**: Switches between data sources seamlessly
- **Time-window Filtering**: Filter events by specific time ranges
- **Delay Detection**: Automatic delay parsing from status updates

### API Features
- **Live Train Status**: Real-time position, delays, and current station
- **Train Schedules**: Route information and stop details
- **Train Search**: Find trains between stations
- **Station Information**: Code lookup and station details
- **PNR Status**: Booking confirmation and current status
- **Fare Inquiry**: Class-wise fare information
- **Train Classes**: Available accommodation types

## Quick Start

1. **Clone and Setup**:
   ```bash
   git clone <repository-url>
   cd indian-train
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. **API Setup**:
   ```bash
   python setup_api.py
   ```
   This will create a `.env` file and test all API connections.

3. **Configure API Keys** (Optional):
   Edit `.env` file and add your API keys:
   ```env
   RAILWAY_API_KEY=your_railwayapi_key
   INDIAN_RAIL_API_KEY=your_indianrail_key
   IRCTC_API_KEY=your_irctc_key
   ```

4. **Run Application**:
   ```bash
   streamlit run src/ui/app.py
   ```

## API Setup Details

### Getting API Keys

1. **RailwayAPI.com**:
   - Visit: https://railwayapi.com/
   - Sign up for free account
   - Get API key from dashboard

2. **IndianRailAPI.com**:
   - Visit: https://indianrailapi.com/
   - Register and obtain API key

3. **IRCTC API**:
   - Official IRCTC developer portal
   - Requires business verification
   - Higher rate limits and official data

### API Testing

Run the setup script to test all APIs:
```bash
python setup_api.py
```

This will test:
- ✅ Station code lookup
- ✅ Train schedules
- ✅ Live status
- ✅ Route search
- ✅ PNR status
- ✅ Fare inquiry

## Dependencies

- `streamlit`: Web interface
- `requests`: API HTTP calls
- `pandas`: Data processing
- `opencv-python`: Computer vision
- `ultralytics`: YOLO models
- `python-dotenv`: Environment variables
- `numpy`: Numerical operations
- `pillow`: Image processing

## Project Structure

```
src/
├── detection/          # AI model detection modules
│   ├── train_detector.py
│   ├── coach_detector.py
│   └── __init__.py
├── scheduling/         # API and schedule management
│   ├── indian_railways_api.py
│   ├── schedule_parser.py
│   └── __init__.py
├── ui/                 # Streamlit web interface
│   ├── app.py
│   └── __init__.py
└── utils/              # Utility functions
    ├── camera.py
    ├── opencv_utils.py
    └── __init__.py
```

## Configuration

### Environment Variables (.env)
```env
# API Keys
RAILWAY_API_KEY=demo_key
INDIAN_RAIL_API_KEY=demo_key
IRCTC_API_KEY=

# Application Settings
DEBUG=True
LOG_LEVEL=INFO
```

### Station Codes Database
The system includes an extensive database of Indian railway station codes:
- Delhi (NDLS), Mumbai (BCT), Kolkata (KOAA)
- Chennai (MAS), Bangalore (SBC), Pune (PUNE)
- Jaipur (JP), Lucknow (LKO), and 40+ more stations

## Usage Examples

### Train Search
```python
from src.scheduling.indian_railways_api import IndianRailwaysAPI

api = IndianRailwaysAPI()
schedule = api.get_train_schedule("12301")  # Rajdhani Express
status = api.get_live_train_status("12301")
trains = api.get_all_trains_between_stations("NDLS", "BCT")
```

### PNR and Fare
```python
pnr_status = api.get_pnr_status("1234567890")
fare = api.get_train_fare("12301", "NDLS", "BCT", "SL")
```

## API Rate Limits & Fallbacks

- **Free APIs**: Limited requests per hour
- **Automatic Fallback**: Switches to mock data when APIs fail
- **Multiple Sources**: Uses different APIs for redundancy
- **Caching**: Local data storage for frequently accessed information

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Ensure API compatibility
5. Submit pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This system uses third-party APIs for railway information. Please respect API terms of service and rate limits. The mock data fallback ensures functionality even when APIs are unavailable.

## Project Structure

```
src/
├── detection/          # AI model detection modules
│   ├── train_detector.py
│   └── coach_detector.py
├── scheduling/         # Train schedule and API integration
│   ├── schedule_parser.py
│   ├── status_calculator.py
│   └── indian_railways_api.py
├── ui/                 # User interface
│   └── app.py
└── utils/              # Utilities
    ├── camera.py
    └── opencv_utils.py
models/                 # YOLO model files
data/                   # Train schedule data
```

## Usage

1. **Start the Application**: Run `streamlit run src/ui/app.py`
2. **Live Camera Feed**: Use camera controls to start/stop video capture
3. **Train Search**: Enter train number in sidebar for details
4. **Route Search**: Enter from/to stations to find trains
5. **Monitor Status**: View live train status and platform information

## API Configuration

For full API functionality, obtain an API key from railwayapi.com and update the `IndianRailwaysAPI` class.

## Sample Train Data

The system includes sample data for major Indian trains:
- Rajdhani Express (12301)
- Shatabdi Express (12302)
- Duronto Express (12303)

## Future Enhancements

- Real-time PNR status checking
- Seat availability information
- Train delay predictions
- Mobile app interface
- Multi-camera platform monitoring

---

**Developed by:** Devraj Kumawat  
**Version:** 1.0.0  
**Status:** ✅ Production Ready  
**© 2026 Indian Railways**