# 🚂 Indian Railways AI System - Professional Architecture

## Version 2.0 - Enterprise MVC Architecture

---

## **Architecture Overview**

```
┌─────────────────────────────────────────────────────────────┐
│                      VIEW LAYER (UI)                         │
│    app.py → Dashboard → Train Routes → Stations → Schedule   │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                    SERVICES LAYER                            │
│  TrainRouteService │ StationService │ ScheduleService        │
│    PriorityService │                                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  REPOSITORIES LAYER                          │
│              TrainRepository (Data Access)                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                    MODELS LAYER                              │
│   Train │ Station │ TrainRoute │ Schedule │ Priority         │
└─────────────────────────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   DATA LAYER (CSV)                           │
│  indian_stations.csv │ trains_with_coaches.csv               │
└─────────────────────────────────────────────────────────────┘
```

---

## **Core Components**

### **1. Models Layer** (`src/models/`)
Defines domain entities with business logic.

**Train** (`train.py`)
- Represents a train with coaches, timings, and route
- Methods: `is_express()`, `total_seats_estimate()`

**Station** (`station.py`)
- Railway station with zones, platforms, and state
- Properties: `is_major_junction()`, `full_name`

**TrainRoute** (`train_route.py`)
- Complete journey from source to destination
- Methods: `total_route_distance()`, `average_speed_kmh()`, `is_direct_route()`

**TrainSchedule** (`train_schedule.py`)
- Scheduled times and real-time status
- Enum: `TrainStatus` (ON_TIME, DELAYED, CANCELLED, RUNNING)

**TrainPriority** (`train_priority.py`)
- Priority classification and seat availability
- Enum: `PriorityLevel` (HIGH, MEDIUM, LOW)

**TouchDetail** (`touch_detail.py`)
- User interactions and booking inquiries
- Enum: `InteractionType` (SEARCH, VIEW_DETAILS, BOOKING_INQUIRY, etc.)

---

### **2. Repositories Layer** (`src/repositories/`)

**TrainRepository** (`train_repository.py`)
- Data access abstraction
- Loads CSVs on initialization
- Validates data completeness
- Methods:
  - `get_trains_between_stations(from_code, to_code)`
  - `get_station_by_code(code)`
  - `search_stations(query)`
  - `get_trains_from_station(station_code)`

**Data Validator** (`src/utils/data_validator.py`)
- Validates required columns
- Detects missing station codes
- Reports data inconsistencies

---

### **3. Services Layer** (`src/services/`)
Business logic and orchestration.

**TrainRouteService**
- `get_routes_between_stations(from_code, to_code)` → List[TrainRoute]
- `get_direct_routes(from_code, to_code)` → List[TrainRoute]
- `search_routes_by_criteria(from_code, to_code, max_duration, min_avg_speed)`
- Converts DTOs to domain models

**StationService**
- `get_all_stations()` → List[Station]
- `search_stations(query)` → List[Station]
- `get_stations_by_zone(zone)` → List[Station]
- `get_major_junctions()` → List[Station]
- `get_zone_distribution()` → Dict[str, int]

**TrainScheduleService**
- `create_schedule(train_no, departure, arrival, status)`
- `update_status(train_no, status, delay_minutes)`
- `get_delayed_trains()` → List[TrainSchedule]
- `get_statistics()` → Dict with metrics

**TrainPriorityService**
- `set_priority(train_no, priority_level, is_express, has_pantry)`
- `update_availability(train_no, seats_available, occupancy_percentage)`
- `get_high_priority_trains()` → List[TrainPriority]
- `get_operational_status()` → Dict with metrics

---

### **4. Views Layer** (`src/ui/views/`)
Professional UI components.

**DashboardView**
- Main metrics and analytics
- Train status breakdown
- Zone distribution charts

**TrainRouteView**
- Route search interface
- Results display with metrics
- Filtering by duration and speed

**StationView**
- Station search by name/code
- Major junctions display
- Zone distribution analytics

---

### **5. Main Application** (`src/ui/app_new.py`)
Professional Streamlit application with:
- Professional styling
- Sidebar navigation
- Multi-page routing
- System metrics dashboard
- All services integrated

---

## **Data Flow**

```
User Input (UI)
    ↓
View Component (TrainRouteView, StationView)
    ↓
Service Layer (TrainRouteService, StationService)
    ↓
Repository (TrainRepository)
    ↓
Data Files (CSV)
    ↓
Models (Train, Station, TrainRoute)
    ↓
View Layer (Display Results)
```

---

## **Key Features**

✅ **Professional Architecture** - MVC pattern with clear separation of concerns  
✅ **Type-Hinted Models** - Full dataclass models with business logic  
✅ **Service Abstraction** - Reusable business logic layer  
✅ **Data Validation** - CSV validation with error reporting  
✅ **Responsive UI** - Professional Streamlit components  
✅ **Extensible Design** - Easy to add new services/views  

---

## **File Structure**

```
src/
├── models/
│   ├── train.py              # Train entity
│   ├── station.py            # Station entity
│   ├── train_route.py        # Route logic
│   ├── train_schedule.py     # Schedule & status
│   ├── train_priority.py     # Priority management
│   ├── touch_detail.py       # Interaction tracking
│   └── __init__.py
├── repositories/
│   ├── train_repository.py   # Data access layer
│   └── __init__.py
├── services/
│   ├── train_route_service.py      # Route business logic
│   ├── station_service.py          # Station business logic
│   ├── train_schedule_service.py   # Schedule management
│   ├── train_priority_service.py   # Priority management
│   └── __init__.py
├── ui/
│   ├── views/
│   │   ├── dashboard_view.py       # Dashboard UI
│   │   ├── train_route_view.py     # Route search UI
│   │   ├── station_view.py         # Station search UI
│   │   └── __init__.py
│   ├── app_new.py                  # Main application
│   └── app_professional.py         # Full integration app
├── utils/
│   ├── data_validator.py   # Data validation utilities
│   └── __init__.py
└── __init__.py

data/
├── indian_stations.csv
└── trains_with_coaches.csv
```

---

## **Usage**

### Launch Professional App
```bash
python -m streamlit run src/ui/app_new.py
```

Open browser to: **http://localhost:8504**

### Use Services Programmatically
```python
from src.services import TrainRouteService, StationService

# Find trains between stations
route_service = TrainRouteService()
routes = route_service.get_routes_between_stations("NDLS", "BCT")

# Search stations
station_service = StationService()
stations = station_service.search_stations("Delhi")
```

---

## **Future Enhancements**

- Database integration (PostgreSQL/MongoDB)
- Real-time API integrations
- User authentication & booking system
- Machine learning for predictions
- Mobile app companion
- Advanced analytics dashboard

---

**Version:** 2.0  
**Last Updated:** January 22, 2026  
**Architecture:** Professional MVC with Clean Code principles
