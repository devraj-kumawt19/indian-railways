# 🚂 Indian Railways AI Detection System

**Advanced Train Detection & Real-Time Scheduling Platform**

---

## ✨ Overview

A comprehensive AI-powered railway platform monitoring system that:
- 📊 Detects trains using dataset-based analysis
- 🚃 Identifies coach positions and compositions  
- 📍 Manages platform zones and tracking
- 🔍 Searches trains across all Indian Railways
- 📈 Provides real-time dashboards and analytics
- 🤖 Uses intelligent agent systems for advanced processing

---

## 🚀 Quick Start

### 1️⃣ **Windows - One-Click Launch**
```bash
# Double-click this file:
launch_app.bat
```

### 2️⃣ **PowerShell**
```powershell
& ".\launch_app.ps1"
```

### 3️⃣ **Manual Setup**
```bash
# Activate virtual environment
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run src/ui/app.py
```

### 📱 **Access the App**
- **Local Machine**: http://localhost:8501
- **Other Devices** (same network): http://[YOUR_IP]:8501

---

## 📁 Project Structure

```
Indian Train/
├── 📚 Documentation
│   ├── SETUP_AND_LAUNCH.md       ← START HERE
│   ├── README.md                 ← This file
│   ├── docs/                     ← All guides
│   └── PROJECT_STRUCTURE.md      ← Detailed structure
│
├── 🚀 Launchers
│   ├── launch_app.bat            ← Windows launcher
│   ├── launch_app.ps1            ← PowerShell launcher
│   └── CONTROL_PANEL.bat         ← Menu system
│
├── 💻 Source Code
│   ├── src/
│   │   ├── ui/                   ← Streamlit UI components
│   │   ├── repositories/         ← Data access layer
│   │   ├── services/             ← Business logic
│   │   ├── agents/               ← AI agent systems
│   │   ├── scheduling/           ← Train scheduling
│   │   ├── detection/            ← Detection models
│   │   ├── realtime/             ← Real-time processing
│   │   ├── models/               ← ML utilities
│   │   ├── utils/                ← Helper functions
│   │   └── viewmodels/           ← Data models
│   │
│   ├── data/                     ← Dataset files
│   ├── models/                   ← ML models
│   ├── tests/                    ← Test suite
│   └── utilities/                ← Helper scripts
│
├── ⚙️ Configuration
│   ├── startup_config.json       ← App settings
│   ├── requirements.txt          ← Dependencies
│   └── .env                      ← Environment variables
│
└── 🔐 Backup
    └── _backup/                  ← Original backup

```

---

## 🎯 Features

### 🚃 Dataset-Based Coach Detection
- ✅ Detect coaches from CSV dataset
- ✅ Analyze coach compositions
- ✅ Generate detection reports
- ✅ 100% accuracy with known data

### 📊 Live Monitoring Dashboard
- ✅ Real-time train status
- ✅ Platform occupancy tracking
- ✅ Coach detection analytics
- ✅ Live alerts & notifications

### 🔍 All India Train Search
- ✅ Search trains across all stations
- ✅ Find by route, station, or date
- ✅ Advanced filtering options
- ✅ Journey tracking & status

### 📈 Advanced Analytics
- ✅ Dashboard with charts & metrics
- ✅ Performance analytics
- ✅ Historical data analysis
- ✅ Predictive insights

### 🤖 AI Agent System
- ✅ Intelligent train tracking
- ✅ Automated coach detection
- ✅ Smart scheduling
- ✅ Multi-agent coordination

---

## 📊 Data Files

| File | Size | Purpose |
|------|------|---------|
| `Train_details_22122017.csv` | 15.93 MB | Complete train schedule |
| `trains_with_coaches.csv` | <1 MB | Coach compositions |
| `indian_stations.csv` | <1 MB | Station information |
| `train_schedule.csv` | <1 MB | Schedule data |

**Total Data**: ~16 MB  
**Trains Loaded**: 186,124+ schedules  
**Stations**: 60+  
**Coaches**: 31 types

---

## 🎨 Main Application Tabs

| Tab | Feature | Status |
|-----|---------|--------|
| 🚃 Dataset Coach Detection | Coach detection from CSV | ✅ Active |
| ⚡ Live Monitoring | Real-time dashboards | ✅ Active |
| 📊 Journey Tracking | Train journey analytics | ✅ Active |
| 🚆 Train Status | Current train status | ✅ Active |
| 🚃 Enhanced Coach Detection | Advanced coach analysis | ✅ Active |
| 📍 Platform Management | Platform operations | ✅ Active |
| 🇮🇳 All India Search | Train search engine | ✅ Active |
| 🤖 Agent System | AI-powered operations | ✅ Active |
| 📈 Dashboard | Analytics & reports | ✅ Active |

---

## 📋 Requirements

### System Requirements
- **OS**: Windows 7+ / Linux / macOS
- **Python**: 3.8+
- **RAM**: 4GB minimum
- **Disk**: 1GB free space

### Python Packages
- streamlit (UI framework)
- pandas (Data processing)
- numpy (Numerical computing)
- requests (API calls)
- opencv-python (Image processing)
- ultralytics (YOLO models)
- And 6 more (see requirements.txt)

---

## ⚙️ Configuration

### Application Settings (`startup_config.json`)
```json
{
    "application": {
        "name": "Indian Railways AI Detection System",
        "version": "1.0.0",
        "status": "Production"
    },
    "features": {
        "live_monitoring": true,
        "train_tracking": true,
        "coach_detection": true,
        "platform_management": true
    }
}
```

### Environment Variables (`.env`)
```bash
# Optional: Set custom API keys
RAILWAY_API_KEY=your_key_here
RAPIDAPI_KEY=your_key_here

# Debug mode
DEBUG=False
LOG_LEVEL=INFO
```

---

## 🧪 Testing

### Run Health Check
```bash
python PROJECT_HEALTH_CHECK.py
```

### Run Unit Tests
```bash
python -m pytest tests/
```

### Test Data Loading
```python
from src.repositories.train_repository import TrainRepository
repo = TrainRepository()
print(f"Loaded {len(repo.schedule_df)} train schedules")
```

---

## 🔧 Troubleshooting

### Issue: App Won't Start
1. Check Python: `python --version` (should be 3.8+)
2. Verify venv: `.\.venv\Scripts\activate`
3. Install deps: `pip install -r requirements.txt`
4. Run: `streamlit run src/ui/app.py`

### Issue: Data Not Loading
1. Check data folder exists: `data/`
2. Verify CSV files present
3. Run: `python PROJECT_HEALTH_CHECK.py`
4. Check file permissions

### Issue: Port Already in Use
```bash
# Use different port
streamlit run src/ui/app.py --server.port=8502
```

### Issue: API Errors
- Check `.env` file for API keys
- Verify internet connection
- Check API rate limits
- Review error logs

---

## 📖 Documentation

| Guide | Purpose |
|-------|---------|
| [SETUP_AND_LAUNCH.md](docs/SETUP_AND_LAUNCH.md) | Complete setup guide |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | Detailed file structure |
| [VIDEO_REMOVAL_COMPLETE.md](docs/VIDEO_REMOVAL_COMPLETE.md) | System changes |
| [docs/](docs/) | All other documentation |

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| Total Code Lines | 10,000+ |
| Python Modules | 50+ |
| UI Components | 9 tabs |
| Data Records | 186,124+ |
| Documentation Files | 15+ |
| Test Coverage | Included |

---

## 🔐 Security

- ✅ No hardcoded credentials
- ✅ Environment-based configuration
- ✅ API key support
- ✅ SSL/TLS ready
- ✅ Data validation
- ✅ Error handling

---

## 🚀 Deployment

### Local Server
```bash
streamlit run src/ui/app.py --server.address=0.0.0.0
```

### Docker (if needed)
```bash
# Build: docker build -t trains-ai .
# Run: docker run -p 8501:8501 trains-ai
```

### Cloud Deployment
- AWS ElasticBeanstalk compatible
- Azure App Service ready
- GCP Cloud Run compatible
- Heroku deployable

---

## 📞 Support

### Getting Help
1. Check [docs/](docs/) folder
2. Read [SETUP_AND_LAUNCH.md](docs/SETUP_AND_LAUNCH.md)
3. Run `PROJECT_HEALTH_CHECK.py`
4. Check browser console for errors

### Common Issues
- **Won't launch?** → Run `launch_app.bat`
- **Data missing?** → Check `data/` folder
- **Port error?** → Change port: `--server.port=8502`
- **API issues?** → Verify `.env` file

---

## 📈 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-28 | ✅ Production release |
| 0.9.0 | 2026-01-27 | Video detection removed |
| 0.8.0 | 2026-01-26 | Platform detection removed |

---

## ✅ Verification Checklist

Before using the application:
- [ ] Python 3.8+ installed
- [ ] `.venv` folder exists
- [ ] `data/` folder has CSV files
- [ ] `pip install -r requirements.txt` completed
- [ ] `streamlit run src/ui/app.py` runs without errors
- [ ] Browser opens to http://localhost:8501
- [ ] All 9 tabs load without errors
- [ ] Data appears in dashboard

---

## 📝 Notes

- **Data Source**: Dataset-based analysis only
- **Real-Time**: Uses API fallback for live updates
- **Platform**: Windows/Linux/macOS compatible
- **Performance**: Optimized for 4GB+ RAM
- **Updates**: Check `docs/` for latest changes

---

## 📄 License

Indian Railways AI Detection System v1.0.0  
© 2026 | Enterprise Platform | All Rights Reserved

---

## 🎉 Ready to Launch?

```bash
# Windows
launch_app.bat

# PowerShell
& ".\launch_app.ps1"

# Manual
streamlit run src/ui/app.py
```

**Access**: http://localhost:8501  
**Status**: ✅ Production Ready

---

*Last Updated: 2026-01-28*  
*Project Status: ✅ STABLE*  
*All Systems: ✅ OPERATIONAL*
