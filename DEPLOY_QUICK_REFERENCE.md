# ⚡ Deployment Quick Reference

## 🚀 Fastest Deployment (Choose One)

### 1️⃣ Local (30 seconds) - Current Setup
```
✅ Double-click launch_app.bat
✅ Open http://localhost:8501
```

### 2️⃣ Heroku (5 minutes) - Cloud Beginner
```
heroku create my-railways-app
git push heroku main
# Access: https://my-railways-app.herokuapp.com
```

### 3️⃣ Docker (3 minutes) - Containerized
```
docker build -t my-railways .
docker run -p 8501:8501 my-railways
# Access: http://localhost:8501
```

### 4️⃣ AWS (10 minutes) - Professional
```
eb create production
eb deploy
# Access: https://your-app.elasticbeanstalk.com
```

---

## 📊 Comparison

| Method | Time | Cost | Scale | Best For |
|--------|------|------|-------|----------|
| **Local** | 30s | Free | 1 user | Dev/Test |
| **Docker** | 3m | Free | 100s | Testing |
| **Heroku** | 5m | $7-50 | 1000s | Startups |
| **AWS** | 10m | $15-100 | 10K+ | Production |
| **Server** | 2h | Varies | Custom | Enterprise |

---

## 🔧 All Startup Commands

### Windows
```powershell
# Option 1: Double-click
launch_app.bat

# Option 2: PowerShell
.\launch_app.ps1

# Option 3: Manual
.venv\Scripts\Activate.ps1
streamlit run src/ui/app.py
```

### Mac/Linux
```bash
# Activate
source .venv/bin/activate

# Run
streamlit run src/ui/app.py
```

### Docker
```bash
docker run -p 8501:8501 my-railways-app
```

---

## 📋 Production Checklist

Before deploying to production:

- [ ] All tests pass locally
- [ ] `.env` file configured
- [ ] Database backups created
- [ ] API keys secured
- [ ] SSL certificate ready
- [ ] Monitoring setup complete
- [ ] Error tracking enabled
- [ ] Logging configured

---

## 🌐 Access URLs

### Local
- **Main:** http://localhost:8501
- **Network:** http://192.168.x.x:8501

### Cloud (After Deployment)
- **Heroku:** https://your-app.herokuapp.com
- **AWS:** https://your-app.elasticbeanstalk.com
- **Azure:** https://your-app.azurewebsites.net
- **Custom:** https://your-domain.com

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 8501 in use | `lsof -i :8501` then kill process |
| Module not found | `pip install -r requirements.txt` |
| App won't start | Check logs: `journalctl -u app -f` |
| Database error | Verify `.env` configuration |
| Slow response | Check CPU/Memory usage |

---

## 📞 Need Help?

1. Read: [HOW_TO_DEPLOY.md](HOW_TO_DEPLOY.md) (This file in detail)
2. Check: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) (Extended guide)
3. Review: [SETUP_AND_LAUNCH.md](SETUP_AND_LAUNCH.md) (Setup guide)

---

## ✨ Recommended Path

**For Development:** Local deployment (30 sec)  
**For Testing:** Docker deployment (3 min)  
**For Production:** AWS or Azure (10-30 min)  

---

**Current Status:** ✅ App running at http://localhost:8501  
**Ready to Deploy:** YES  
**Production Ready:** YES  

**Developed by:** Devraj Kumawat  
**© 2026 Indian Railways AI**
