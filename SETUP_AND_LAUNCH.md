# 🚀 Indian Railways AI - Complete Setup & Deployment Guide

## ✅ Quick Access

### **Windows Users - Quick Launch**
1. **Double-click** `launch_app.bat` (Automatic Setup & Launch)
   - Auto-activates virtual environment
   - Installs dependencies
   - Clears cache
   - Launches app at http://localhost:8501

2. **PowerShell Users**
   - Right-click `launch_app.ps1` → Run with PowerShell
   - Or: `.\launch_app.ps1` in PowerShell

### **Open in Browser**
- **Local Access:** [http://localhost:8501](http://localhost:8501)
- **Network Access:** [http://192.168.29.171:8501](http://192.168.29.171:8501)
- **Dashboard:** [index.html](index.html)

---

## 📋 Pre-Launch Checklist

### System Requirements
- ✅ Python 3.8 or higher
- ✅ Windows 10/11 OR Linux/Mac with Python installed
- ✅ Virtual Environment (.venv folder)
- ✅ 2GB RAM minimum
- ✅ 500MB free disk space

### Check Installation
```bash
# Open Command Prompt or PowerShell
python --version        # Should show Python 3.8+
pip --version          # Should show pip version
```

---

## 🎯 Startup Methods

### Method 1: Windows Batch (EASIEST ⭐)
```bash
double-click: launch_app.bat
```
✅ Auto-setup  
✅ One-click  
✅ Includes all configuration  

### Method 2: PowerShell (With Color Output)
```powershell
.\launch_app.ps1
```
✅ Colored status messages  
✅ Professional output  
✅ Same as batch functionality  

### Method 3: Manual Command Line
```bash
# Activate virtual environment
.venv\Scripts\activate

# Install dependencies (if needed)
pip install -r requirements.txt

# Clear Streamlit cache (optional)
streamlit cache clear

# Launch application
streamlit run src/ui/app.py
```

### Method 4: Docker (Production)
```bash
# Build image
docker build -t indian-railways-ai .

# Run container
docker run -p 8501:8501 indian-railways-ai
```

---

## 📱 Access Points

| Method | URL | Platform | Speed | Notes |
|--------|-----|----------|-------|-------|
| **Local** | http://localhost:8501 | Windows, Mac, Linux | Fastest | Default, localhost only |
| **Network** | http://192.168.29.171:8501 | Same network | Fast | Share with colleagues |
| **Dashboard** | [index.html](index.html) | All | Instant | Landing page with links |
| **Mobile** | http://192.168.29.171:8501 | Smartphone | Good | Responsive design |

---

## 🔧 Configuration

### Application Settings (startup_config.json)
```json
{
    "access": {
        "local": "http://localhost:8501",
        "network": "http://192.168.1.1:8501"
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
RAILWAY_API_KEY=your_api_key
API_BASE_URL=https://api.railways.example.com

# Application Settings
DEBUG=False
LOG_LEVEL=INFO
CACHE_TTL=300

# Database (optional)
DATABASE_URL=sqlite:///data/app.db
```

---

## 📚 Documentation Guide

| Document | Purpose | Quick Access |
|----------|---------|--------------|
| **README.md** | Project overview & features | [View](README.md) |
| **SYSTEM_OVERVIEW.md** | Architecture & technology stack | [View](SYSTEM_OVERVIEW.md) |
| **QUICK_START_GUIDE.md** | Getting started in 60 seconds | [View](QUICK_START_GUIDE.md) |
| **DEPLOYMENT_GUIDE.md** | Production deployment instructions | [View](DEPLOYMENT_GUIDE.md) |
| **ERROR_HANDLING_GUIDE.md** | Troubleshooting & debugging | [View](ERROR_HANDLING_GUIDE.md) |
| **LINKS.md** | Quick links & resources | [View](LINKS.md) |

---

## 🎮 Application Features

### 🎥 Live Monitoring
- Real-time train detection
- Camera feed integration
- Live coach identification
- System health status

### 🚆 Train Status
- Live train location tracking
- Station-by-station journey
- Delay information
- Platform predictions

### 🚃 Coach Analysis
- AI-powered coach detection
- Platform positioning
- Capacity planning
- Detailed coach information

### 📍 Platform Management
- Platform configuration
- Coach positioning visualization
- Real-time updates
- Management dashboard

### 🔍 Advanced Search
- Filter by train, date, route
- Schedule search
- Status history
- Analytics reports

---

## 🚀 Deployment Options

### Quick Deployment (5 Minutes)
```bash
# Windows: Double-click launch_app.bat
# Or PowerShell: .\launch_app.ps1
# Open http://localhost:8501
```

### Docker Deployment (10 Minutes)
See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for full Docker setup

### Cloud Deployment
- **AWS:** Elastic Beanstalk, EC2
- **Azure:** App Service
- **GCP:** Cloud Run
- **Heroku:** Buildpack compatible

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

---

## 🆘 Troubleshooting

### Issue: App won't start
```bash
# Solution 1: Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Solution 2: Clear Streamlit cache
streamlit cache clear

# Solution 3: Check Python version
python --version
```

### Issue: Port 8501 already in use
```bash
# Solution: Use different port
streamlit run src/ui/app.py --server.port 8502
```

### Issue: Virtual environment not activating
```bash
# Solution: Recreate venv
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: API connection errors
```bash
# Check API configuration in .env file
# Verify RAILWAY_API_KEY is set
# Check internet connection
# See ERROR_HANDLING_GUIDE.md for detailed debugging
```

---

## 📊 Performance Tips

1. **Clear Cache Regularly**
   ```bash
   streamlit cache clear
   ```

2. **Update Dependencies**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

3. **Monitor Resources**
   - Check Task Manager (Windows)
   - Monitor CPU & Memory usage
   - Restart if memory > 80%

4. **Optimize Video Feed**
   - Reduce camera resolution
   - Lower FPS if needed
   - Use hardware acceleration

---

## 🔒 Security Checklist

- ✅ Environment variables in .env (not committed to git)
- ✅ API keys properly configured
- ✅ HTTPS for production deployment
- ✅ Regular backups of data folder
- ✅ Monitor access logs
- ✅ Keep dependencies updated

---

## 📞 Support & Contact

### Need Help?
- 📧 **Email:** support@example.com
- 📞 **Phone:** +91-XXXX-XXXX-XXXX
- 🌐 **Website:** https://example.com
- 💬 **Chat:** https://example.com/chat
- 🐛 **Report Bug:** https://github.com/example/issues

### Quick Links
- [Application Dashboard](http://localhost:8501)
- [Landing Page](index.html)
- [System Configuration](startup_config.json)
- [All Documentation](LINKS.md)

---

## 🎓 Learning Resources

1. **Get Started:** Read [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)
2. **Understand System:** Read [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md)
3. **Deploy Production:** Read [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
4. **Fix Issues:** Read [ERROR_HANDLING_GUIDE.md](ERROR_HANDLING_GUIDE.md)
5. **Find Resources:** Read [LINKS.md](LINKS.md)

---

## 🎉 Success!

Once you see this message:
```
Local URL: http://localhost:8501
```

Your application is ready! Open the URL in your browser to begin.

---

**Version:** 1.0.0  
**Status:** ✅ Production Ready  
**Developed by:** Devraj Kumawat  
**Last Updated:** 2026  
**License:** © 2026 Indian Railways

---

### 🚀 Ready to Launch?

**Windows:** Double-click `launch_app.bat`  
**PowerShell:** Run `.\launch_app.ps1`  
**Browser:** Open http://localhost:8501
