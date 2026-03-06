# Indian Railways AI Detection System - PROJECT STRUCTURE

## 📁 Directory Organization

```
Indian Train/
├── 📚 DOCUMENTATION & SETUP
│   ├── SETUP_AND_LAUNCH.md          ← START HERE - Complete setup guide
│   ├── README.md                    ← Project overview & features
│   ├── startup_config.json          ← Application configuration
│   ├── requirements.txt             ← Python dependencies
│   └── .env                         ← Environment variables
│
├── 🚀 QUICK START
│   ├── launch_app.bat               ← One-click Windows launcher
│   ├── launch_app.ps1               ← PowerShell launcher
│   ├── CONTROL_PANEL.bat            ← Interactive control menu
│   └── PROJECT_CLEANUP.bat          ← Organize project files
│
├── 📖 DOCUMENTATION FOLDER
│   └── docs/                        ← All guides & documentation
│       ├── QUICK_START_GUIDE.md
│       ├── SYSTEM_OVERVIEW.md
│       ├── DEPLOYMENT_GUIDE.md
│       ├── ERROR_HANDLING_GUIDE.md
│       └── ... (other docs)
│
├── 💻 SOURCE CODE
│   └── src/
│       ├── ui/                      ← Streamlit UI modules
│       │   ├── app.py               ← Main application
│       │   ├── live_monitoring.py
│       │   ├── enhanced_coach_detection.py
│       │   ├── all_india_search.py
│       │   ├── journey_tracking.py
│       │   └── ... (other UI modules)
│       ├── agents/                  ← AI agent system
│       ├── detection/               ← Train detection models
│       ├── models/                  ← ML models & utilities
│       ├── realtime/                ← Real-time processing
│       ├── repositories/            ← Data access layer
│       ├── scheduling/              ← Schedule management
│       ├── services/                ← Business logic
│       ├── utils/                   ← Helper utilities
│       └── viewmodels/              ← Data models
│
├── 📊 DATA
│   └── data/                        ← Dataset files
│       ├── indian_stations.csv
│       ├── train_schedule.csv
│       ├── trains_with_coaches.csv
│       └── Train_details_22122017.csv
│
├── 🤖 MODELS
│   └── models/                      ← Pre-trained ML models
│
├── 🧪 TESTS
│   └── tests/                       ← Unit & integration tests
│
├── 🛠️ UTILITIES
│   └── utilities/                   ← Helper scripts & tools
│
└── 🔐 BACKUPS
    └── _backup/                     ← Automatic backup of original structure
```

## 🎯 Key Files Explained

### Entry Points
- **main.py** - Python entry point (alternative to launcher scripts)
- **launch_app.bat** - Windows batch launcher (recommended for Windows)
- **launch_app.ps1** - PowerShell launcher (alternative)
- **CONTROL_PANEL.bat** - Interactive menu with 16 options

### Main Application
- **src/ui/app.py** - Main Streamlit application (2,826+ lines, production-ready)
- **startup_config.json** - Complete application configuration
- **requirements.txt** - All Python dependencies

### Configuration
- **.env** - Environment variables (API keys, secrets)
- **startup_config.json** - Feature flags, settings, deployment options

## 🚀 Quick Start

### 1. First Time Setup
```bash
# Windows - double-click:
launch_app.bat

# Or manually run:
cd "E:\Indian Train"
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
streamlit run src/ui/app.py
```

### 2. Access Application
- **Local**: http://localhost:8501
- **Network**: http://[YOUR_IP]:8501

### 3. Control Menu
```bash
CONTROL_PANEL.bat    # Interactive menu with options
```

## 📚 Documentation Guide

### For Beginners
1. **SETUP_AND_LAUNCH.md** - Complete setup instructions
2. **QUICK_START_GUIDE.md** - Get running in 60 seconds
3. Run `launch_app.bat`

### For Developers
1. **README.md** - Project overview
2. **SYSTEM_OVERVIEW.md** - Architecture & design
3. **docs/MODULES_ORGANIZATION.md** - Code structure
4. **src/** - Source code exploration

### For Deployment
1. **DEPLOYMENT_GUIDE.md** - Production deployment
2. **ERROR_HANDLING_GUIDE.md** - Troubleshooting
3. **startup_config.json** - Configuration reference

## ✨ Features Included

### Core Features
✓ Real-time train detection using YOLO  
✓ Coach identification and numbering  
✓ Platform zone mapping  
✓ Advanced live train status (NTES integration)  
✓ Train search and route information  

### UI Components
✓ Professional Streamlit dashboard  
✓ Real-time live monitoring  
✓ Enhanced journey tracking  
✓ Coach detection & positioning  
✓ Platform management  
✓ All India train search  
✓ AI agent system  
✓ Advanced dashboard analytics  

### Integration
✓ Multiple railway API support  
✓ Automatic fallback system  
✓ Offline capabilities  
✓ Network accessibility  
✓ Mobile responsive design  

## 🔧 Configuration

### startup_config.json
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

### Environment Variables (.env)
```bash
# API Configuration
RAILWAY_API_KEY=your_key

# Application Settings
DEBUG=False
LOG_LEVEL=INFO
```

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| Main Application | 2,826+ lines |
| Professional CSS | 600+ lines |
| Documentation Files | 15+ files |
| Test Files | 6+ files |
| Source Modules | 20+ modules |
| Total Lines of Code | 10,000+ |

## 🎓 Learning Resources

- **Getting Started**: SETUP_AND_LAUNCH.md
- **System Design**: SYSTEM_OVERVIEW.md
- **Troubleshooting**: ERROR_HANDLING_GUIDE.md
- **API Reference**: docs/API_DOCUMENTATION_INDEX.md
- **Deployment**: DEPLOYMENT_GUIDE.md

## 🆘 Common Commands

```bash
# Activate virtual environment
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run src/ui/app.py

# Run tests
python -m pytest tests/

# Clear cache
streamlit cache clear

# Check system status
python main.py
```

## 📞 Support

For issues or questions:
1. Check **docs/ERROR_HANDLING_GUIDE.md**
2. Review **SETUP_AND_LAUNCH.md**
3. Check configuration in **startup_config.json**
4. Run **CONTROL_PANEL.bat** option 14 for system status

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment (.venv) working
- [ ] Requirements installed
- [ ] launch_app.bat runs successfully
- [ ] Access http://localhost:8501
- [ ] All tabs load without errors
- [ ] Dashboard displays data

## 📝 Notes

- Backup of original structure in `_backup/` folder
- All documentation moved to `docs/` folder
- All tests organized in `tests/` folder
- Utilities in `utilities/` folder
- Clean, professional root directory

---

**Version**: 1.0.0  
**Status**: Production Ready  
**Last Updated**: 2026-01-28
