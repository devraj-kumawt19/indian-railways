# Indian Railways AI System - Error Handling & Health Check Guide

## 🔧 Error Handling System

### Error Categories

#### 1. Connection Errors
**Cause:** Network connectivity issues  
**Status Code:** 503, Connection Refused  
**Solution:** 
- Check internet connection
- Verify API server status
- Check firewall settings
- Try again in 30 seconds

**Example Error Display:**
```
❌ Connection Error
Unable to connect to API. Please check your internet connection.
```

#### 2. Validation Errors
**Cause:** Invalid input data  
**Status Code:** 400, Bad Request  
**Solution:**
- Check input format
- Verify required fields
- Review error details
- Re-enter correct data

**Example Error Display:**
```
❌ Invalid Format
Train number must be numeric and at least 4 digits
```

#### 3. Timeout Errors
**Cause:** Server response taking too long  
**Status Code:** 408, Request Timeout  
**Solution:**
- Wait and retry
- Check server load
- Reduce data range
- Clear browser cache

**Example Error Display:**
```
❌ Timeout Error
API request timed out. Please try again.
```

#### 4. Authorization Errors
**Cause:** Invalid credentials or permissions  
**Status Code:** 401, 403 Unauthorized  
**Solution:**
- Verify credentials
- Check user permissions
- Log out and log in again
- Contact administrator

**Example Error Display:**
```
❌ Authorization Failed
You don't have permission to access this resource
```

#### 5. Data Errors
**Cause:** Invalid or missing data  
**Status Code:** 422, Unprocessable Entity  
**Solution:**
- Verify data source
- Check data format
- Review data validation rules
- Report to support

**Example Error Display:**
```
❌ Data Error
The requested train number doesn't exist in our database
```

---

## 🏥 System Health Check

### Health Check Endpoints

| Component | Endpoint | Method | Expected | Check Interval |
|-----------|----------|--------|----------|-----------------|
| API Server | /health | GET | 200 OK | 30s |
| Database | /db/health | GET | Connected | 60s |
| Cache | /cache/health | GET | Running | 45s |
| Auth | /auth/health | GET | OK | 120s |

### Health Monitoring

```python
# Check system health
GET /api/health
Response: {
    "status": "healthy",
    "timestamp": "2026-01-18T21:12:14Z",
    "components": {
        "api": "operational",
        "database": "operational",
        "cache": "operational",
        "auth": "operational"
    },
    "uptime": "99.8%",
    "response_time": "45ms"
}
```

---

## 📊 Performance Monitoring

### Key Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| API Response Time | < 500ms | 45ms | ✅ Good |
| Database Query Time | < 200ms | 35ms | ✅ Good |
| Cache Hit Rate | > 80% | 92% | ✅ Excellent |
| Error Rate | < 1% | 0.2% | ✅ Excellent |
| System Uptime | > 99% | 99.8% | ✅ Excellent |

### Performance Alerts

**Critical Thresholds:**
- Response Time > 2000ms → Send Alert
- Error Rate > 5% → Send Alert
- Uptime < 95% → Send Alert
- Memory Usage > 90% → Send Alert

---

## 🔍 Debugging Guide

### Enable Debug Logging

```python
# In src/ui/app.py
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Log important events
logger.debug("Train search initiated for: 12267")
logger.info("API response received successfully")
logger.warning("Slow response detected: 1500ms")
logger.error("Connection failed to API server")
```

### Common Debug Steps

1. **Check Browser Console**
   - Open: F12 or Ctrl+Shift+I
   - Go to Console tab
   - Look for JavaScript errors

2. **Review Server Logs**
   - Check terminal output
   - Review error messages
   - Note timestamps

3. **Test API Manually**
   ```bash
   curl -X GET "http://localhost:8501/api/trains/12267"
   ```

4. **Clear Cache & Cookies**
   - Ctrl+Shift+Delete
   - Clear browsing data
   - Restart application

---

## 🚨 Emergency Procedures

### System Down

**Step 1: Verify Issue**
- Check internet connection
- Verify API server status
- Check system resources

**Step 2: Try Recovery**
- Restart application
- Clear browser cache
- Check firewall settings

**Step 3: Contact Support**
- Call: +91-XXXX-XXXX-XXXX
- Email: emergency@example.com
- Include: Timestamp, error message, screenshots

### Database Connection Lost

**Procedure:**
1. Check database status: `systemctl status postgresql`
2. Restart database: `systemctl restart postgresql`
3. Verify connection: `psql -U user -d railway_db`
4. Check logs: `/var/log/postgresql/`

### High Memory Usage

**Procedure:**
1. Stop application gracefully
2. Check process: `ps aux | grep streamlit`
3. Kill if needed: `kill -9 PID`
4. Restart application
5. Monitor memory: `top` or `htop`

### API Rate Limiting

**Situation:** Getting 429 Too Many Requests  
**Solution:**
1. Implement request queuing
2. Add exponential backoff
3. Increase cache TTL
4. Request rate limit increase from provider

---

## ✅ Health Check Checklist

### Daily Checks
- [ ] System uptime status
- [ ] API response times
- [ ] Error rate monitoring
- [ ] Database connectivity
- [ ] Cache performance

### Weekly Checks
- [ ] Security audit logs
- [ ] Performance trends
- [ ] Disk space usage
- [ ] Backup verification
- [ ] User access logs

### Monthly Checks
- [ ] Full system audit
- [ ] Compliance verification
- [ ] Performance optimization
- [ ] Disaster recovery test
- [ ] Security assessment

---

## 📝 Logging Best Practices

### Log Levels

```python
logger.debug("Detailed info for developers")      # DEBUG
logger.info("General informational messages")     # INFO
logger.warning("Something unexpected occurred")   # WARNING
logger.error("A serious problem, function failed") # ERROR
logger.critical("System may be unstable")         # CRITICAL
```

### Log Format
```
[2026-01-18 21:12:14] [INFO] Train search: 12267
[2026-01-18 21:12:15] [DEBUG] API response received
[2026-01-18 21:12:16] [ERROR] Database connection failed
```

---

## 🔒 Security Error Handling

### Never Log
- Passwords or tokens
- Personal information
- Credit card numbers
- API secrets
- User session data

### Always Verify
- Input validation
- SQL injection prevention
- XSS attack prevention
- CSRF token verification
- API authentication

---

## 📞 Support Contacts

### Escalation Levels

**Level 1: General Support**
- Email: support@example.com
- Response Time: 4 hours
- Hours: 9 AM - 6 PM IST

**Level 2: Technical Support**
- Email: technical@example.com
- Response Time: 1 hour
- Hours: 24/7

**Level 3: Emergency Support**
- Phone: +91-XXXX-XXXX-XXXX
- Response Time: 15 minutes
- Hours: 24/7/365

---

## 📚 Additional Resources

### Documentation
- User Guide: https://docs.example.com/user-guide
- API Reference: https://docs.example.com/api
- Troubleshooting: https://docs.example.com/troubleshoot

### Tools
- Status Dashboard: https://status.example.com
- Performance Monitor: https://monitor.example.com
- Error Tracking: https://errors.example.com

---

## 🎯 Error Prevention Strategy

### Input Validation
✅ Always validate user input  
✅ Check data types and ranges  
✅ Sanitize strings and commands  
✅ Handle null/empty values  

### API Integration
✅ Implement timeout handling  
✅ Use retry mechanism  
✅ Check response codes  
✅ Validate response data  

### Error Recovery
✅ Graceful degradation  
✅ Fallback mechanisms  
✅ Auto-recovery attempts  
✅ User-friendly messages  

---

**Last Updated:** January 18, 2026  
**Next Review:** January 25, 2026  
**Maintained By:** System Operations Team
