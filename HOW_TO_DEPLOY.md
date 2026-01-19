# 🚀 Complete Deployment Guide - Indian Railways AI System

## Overview

The Indian Railways AI Detection System is **production-ready** and can be deployed in multiple ways depending on your needs and infrastructure.

**Current Status:** ✅ Running Locally at http://localhost:8501

---

## 📋 Deployment Options

### Option 1: Local Deployment (Development/Testing)
**Status:** ✅ Currently Active  
**Best For:** Development, testing, small teams  
**Setup Time:** < 5 minutes  
**Cost:** Free

### Option 2: Cloud Deployment (Production)
**Best For:** Production, scalability, high availability  
**Platforms:** AWS, Azure, Google Cloud, Heroku  
**Setup Time:** 30-60 minutes  
**Cost:** Variable ($10-100+/month)

### Option 3: Server Deployment (Linux/Ubuntu)
**Best For:** On-premises, full control, custom setup  
**Setup Time:** 1-2 hours  
**Cost:** Server costs only

### Option 4: Docker Deployment
**Best For:** Containerization, consistency, easy scaling  
**Setup Time:** 20-30 minutes  
**Cost:** Depends on hosting

---

## 🚀 QUICK START - Local Deployment (Easiest)

### For Windows Users

**Method 1: Double-Click (Simplest)**
```
1. Navigate to: e:\Indian Train\
2. Double-click: launch_app.bat
3. Wait for message: "Streamlit app is running..."
4. Open browser: http://localhost:8501
5. Done! ✅
```

**Method 2: PowerShell**
```powershell
# Open PowerShell
cd e:\Indian Train
.\launch_app.ps1

# Then open: http://localhost:8501
```

**Method 3: Manual**
```powershell
cd e:\Indian Train
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run src/ui/app.py
```

### For Mac/Linux Users

```bash
# Navigate to project
cd /path/to/Indian\ Train

# Make launcher executable
chmod +x launch_app.sh

# Run
./launch_app.sh

# Or manual
source .venv/bin/activate
pip install -r requirements.txt
streamlit run src/ui/app.py
```

---

## ☁️ Cloud Deployment Guide

### AWS Elastic Beanstalk (Recommended)

**Step 1: Install AWS CLI**
```bash
pip install awsebcli
```

**Step 2: Initialize EB**
```bash
eb init -p python-3.9 indian-railways-ai
```

**Step 3: Create Environment**
```bash
eb create production --instance-type t3.medium
```

**Step 4: Deploy**
```bash
eb deploy
```

**Step 5: Access**
```
Your app will be available at:
https://indian-railways-ai.elasticbeanstalk.com
```

### Heroku Deployment

**Step 1: Install Heroku CLI**
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

**Step 2: Login**
```bash
heroku login
```

**Step 3: Create App**
```bash
heroku create indian-railways-ai
```

**Step 4: Add Buildpack**
```bash
heroku buildpacks:set heroku/python
```

**Step 5: Deploy**
```bash
git push heroku main
```

**Step 6: Access**
```
https://indian-railways-ai.herokuapp.com
```

### Azure App Service

**Step 1: Install Azure CLI**
```bash
# Download from https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
```

**Step 2: Login**
```bash
az login
```

**Step 3: Create Resource Group**
```bash
az group create --name indian-railways-rg --location eastus
```

**Step 4: Create App Service Plan**
```bash
az appservice plan create --name indian-railways-plan \
  --resource-group indian-railways-rg --sku B1 --is-linux
```

**Step 5: Create Web App**
```bash
az webapp create --resource-group indian-railways-rg \
  --plan indian-railways-plan --name indian-railways-app \
  --runtime "PYTHON|3.9"
```

**Step 6: Deploy**
```bash
az webapp up -n indian-railways-app -g indian-railways-rg
```

---

## 🐳 Docker Deployment

### Create Dockerfile

Create file `Dockerfile` in project root:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Set Streamlit config
RUN mkdir -p ~/.streamlit && \
    echo "[server]" > ~/.streamlit/config.toml && \
    echo "headless = true" >> ~/.streamlit/config.toml && \
    echo "port = 8501" >> ~/.streamlit/config.toml && \
    echo "enableXsrfProtection = false" >> ~/.streamlit/config.toml

# Run app
CMD ["streamlit", "run", "src/ui/app.py"]
```

### Build & Run

```bash
# Build Docker image
docker build -t indian-railways-ai:latest .

# Run container
docker run -p 8501:8501 indian-railways-ai:latest

# Access: http://localhost:8501
```

### Push to Docker Hub

```bash
# Login
docker login

# Tag image
docker tag indian-railways-ai:latest yourusername/indian-railways-ai:latest

# Push
docker push yourusername/indian-railways-ai:latest

# Others can run:
docker run -p 8501:8501 yourusername/indian-railways-ai:latest
```

---

## 🖥️ Linux Server Deployment (Ubuntu/Debian)

### Step 1: Update System
```bash
sudo apt update
sudo apt upgrade -y
```

### Step 2: Install Python & Dependencies
```bash
sudo apt install -y python3.9 python3-pip python3-venv
sudo apt install -y git curl wget
```

### Step 3: Clone Repository
```bash
cd /opt
sudo git clone https://your-repo-url.git indian-railways-ai
cd indian-railways-ai
```

### Step 4: Create Virtual Environment
```bash
python3.9 -m venv .venv
source .venv/bin/activate
```

### Step 5: Install Requirements
```bash
pip install -r requirements.txt
```

### Step 6: Create Systemd Service

Create `/etc/systemd/system/indian-railways.service`:

```ini
[Unit]
Description=Indian Railways AI Detection System
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/indian-railways-ai
Environment="PATH=/opt/indian-railways-ai/.venv/bin"
ExecStart=/opt/indian-railways-ai/.venv/bin/streamlit run src/ui/app.py \
  --server.port=8501 --server.address=0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Step 7: Enable & Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable indian-railways
sudo systemctl start indian-railways
```

### Step 8: Check Status
```bash
sudo systemctl status indian-railways
journalctl -u indian-railways -f
```

### Step 9: Setup Nginx Reverse Proxy

Install Nginx:
```bash
sudo apt install -y nginx
```

Create `/etc/nginx/sites-available/indian-railways`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/indian-railways \
  /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 10: Setup SSL (HTTPS)

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 🔐 Production Deployment Checklist

### Pre-Deployment
- [ ] Code tested locally
- [ ] All tests passing
- [ ] No hardcoded secrets in code
- [ ] `.env` file properly configured
- [ ] Database backups created
- [ ] API keys secured
- [ ] SSL certificate ready
- [ ] Domain DNS configured
- [ ] Firewall rules configured
- [ ] Monitoring setup complete

### During Deployment
- [ ] Database migrations run
- [ ] Cache cleared
- [ ] Old version backed up
- [ ] Health checks pass
- [ ] Logs monitored
- [ ] Error tracking enabled
- [ ] Performance monitored

### Post-Deployment
- [ ] All features tested
- [ ] API endpoints verified
- [ ] Database queries optimized
- [ ] Cache strategy verified
- [ ] Backups confirmed working
- [ ] Monitoring alerts active
- [ ] Team notified
- [ ] Documentation updated

---

## 🔧 Environment Configuration

### .env File Setup

Create `.env` file in project root:

```env
# Application
APP_ENV=production
APP_DEBUG=false
APP_HOST=0.0.0.0
APP_PORT=8501

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=railways_db
DB_USER=railways_user
DB_PASSWORD=your_secure_password

# API
API_KEY=your_api_key_here
API_SECRET=your_api_secret_here
API_TIMEOUT=30

# Security
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CSRF_TRUSTED_ORIGINS=https://your-domain.com
SECRET_KEY=your_django_secret_key

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/railways/app.log

# Features
ENABLE_REALTIME=true
ENABLE_NOTIFICATIONS=true
CACHE_ENABLED=true
CACHE_TTL=300
```

### Load Environment Variables

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Access variables
app_env = os.getenv('APP_ENV', 'development')
db_host = os.getenv('DB_HOST', 'localhost')
api_key = os.getenv('API_KEY')
```

---

## 📊 Monitoring & Logging

### Setup Application Logging

```python
import logging
import logging.handlers

# Create logger
logger = logging.getLogger('railways_ai')
logger.setLevel(logging.INFO)

# File handler
file_handler = logging.handlers.RotatingFileHandler(
    '/var/log/railways/app.log',
    maxBytes=10485760,  # 10MB
    backupCount=10
)

# Formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Use logger
logger.info("Application started")
logger.error("An error occurred")
```

### Monitor Key Metrics

```
✓ CPU Usage: Keep below 80%
✓ Memory Usage: Keep below 85%
✓ Disk Usage: Keep below 90%
✓ Response Time: Keep below 2 seconds
✓ Error Rate: Keep below 1%
✓ API Uptime: Maintain 99.9%
```

---

## 🔄 Continuous Deployment (CI/CD)

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest tests/
    
    - name: Deploy to production
      run: |
        # Your deployment script here
        ./scripts/deploy.sh
```

---

## 🆘 Troubleshooting Deployment

### App Won't Start

```bash
# Check logs
journalctl -u indian-railways -f

# Check port
lsof -i :8501

# Restart service
sudo systemctl restart indian-railways
```

### Database Connection Issues

```bash
# Test connection
psql -h $DB_HOST -U $DB_USER -d $DB_NAME

# Check permissions
sudo -u www-data psql -h localhost -U railways_user -d railways_db
```

### Performance Issues

```bash
# Monitor resources
top
htop

# Check disk space
df -h

# Check logs for errors
grep ERROR /var/log/railways/app.log
```

### SSL Certificate Issues

```bash
# Renew certificate
sudo certbot renew

# Check certificate status
sudo certbot certificates
```

---

## 📚 Additional Resources

### Documentation
- [SETUP_AND_LAUNCH.md](SETUP_AND_LAUNCH.md) - Quick setup guide
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Extended deployment info
- [README.md](README.md) - Project overview
- [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md) - Getting started

### External Links
- [Streamlit Deployment Docs](https://docs.streamlit.io/deploy)
- [AWS Deployment Guide](https://docs.aws.amazon.com/)
- [Azure App Service Docs](https://docs.microsoft.com/en-us/azure/app-service/)
- [Docker Documentation](https://docs.docker.com/)

---

## 💡 Recommended Production Setup

```
┌─────────────────────────────────────┐
│      Client (Web Browser)            │
└──────────────┬──────────────────────┘
               │ HTTPS
┌──────────────▼──────────────────────┐
│  Cloudflare / CDN (Cache/DDoS)      │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  Load Balancer (AWS/Azure)           │
└──────────────┬──────────────────────┘
               │
     ┌─────────┴─────────┐
     │                   │
┌────▼────┐         ┌────▼────┐
│Instance │         │Instance │
│    1    │         │    2    │
└────┬────┘         └────┬────┘
     │                   │
     └─────────┬─────────┘
               │
┌──────────────▼──────────────────────┐
│  Database (PostgreSQL)               │
│  - Primary + Replica                 │
│  - Automated Backups                 │
└──────────────────────────────────────┘
```

---

## 🎯 Quick Reference

| Method | Cost | Setup Time | Best For |
|--------|------|-----------|----------|
| Local | Free | 5 min | Development |
| Heroku | $7-50/mo | 10 min | Small apps |
| AWS EB | $15-100/mo | 30 min | Scalable |
| Azure | $20-100/mo | 30 min | Enterprise |
| Docker | Free | 20 min | Containerized |
| Server | Varies | 2 hours | Full control |

---

## 📞 Support

- **Documentation:** Check DEPLOYMENT_GUIDE.md
- **Issues:** Review troubleshooting section above
- **Questions:** Contact development team
- **Emergency:** Follow incident response plan

---

## ✅ Deployment Validation

After deploying, verify:

```bash
# Check app is running
curl http://your-domain.com/health

# Check database
curl http://your-domain.com/api/status

# Check API endpoints
curl http://your-domain.com/api/trains

# Monitor logs
tail -f /var/log/railways/app.log
```

---

**Developed by:** Devraj Kumawat  
**Indian Railways AI Detection System © 2026**  
**Last Updated:** January 18, 2026  
**Status:** Production Ready ✅
