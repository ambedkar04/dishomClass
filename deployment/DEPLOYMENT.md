# 🚀 Safal Classes - Production Deployment Guide

Complete production deployment guide for **safalclasses.com**

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Server Setup](#initial-server-setup)
3. [Configuration](#configuration)
4. [Deployment](#deployment)
5. [Maintenance](#maintenance)
6. [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

### Server Requirements
- **OS**: Ubuntu 20.04 LTS or newer
- **RAM**: Minimum 2GB (4GB recommended)
- **Storage**: Minimum 20GB
- **Domain**: safalclasses.com pointing to your server IP

### Required Software
- Python 3.8+
- Node.js 18+
- Nginx
- Git
- Certbot (for SSL)

---

## 🎯 Initial Server Setup

### Step 1: Connect to Server
```bash
ssh root@your-server-ip
```

### Step 2: Clone Repository
```bash
cd /tmp
git clone https://github.com/ambedkar04/DishomLMS.git
cd DishomLMS
```

### Step 3: Run Initial Setup Script
```bash
chmod +x deployment/scripts/initial-setup.sh
sudo ./deployment/scripts/initial-setup.sh
```

This script will:
- ✅ Install all required packages
- ✅ Create deploy user
- ✅ Setup project directory
- ✅ Configure Nginx
- ✅ Setup systemd service
- ✅ Install SSL certificate
- ✅ Build frontend
- ✅ Run Django migrations

---

## ⚙️ Configuration

### 1. Environment Variables

Edit the production environment file:
```bash
sudo nano /home/deploy/safalclasses/backend/.env
```

**Required Settings:**
```env
# Django
SECRET_KEY=your-super-secret-key-min-50-chars-random-string
DEBUG=False

# Email (Gmail)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
DEFAULT_FROM_EMAIL=noreply@safalclasses.com

# Domain
FRONTEND_BASE_URL=https://safalclasses.com
ALLOWED_HOSTS=safalclasses.com,www.safalclasses.com,your-server-ip
```

### 2. Generate Secret Key

```bash
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 3. Gmail App Password

For email functionality:
1. Go to Google Account Settings
2. Enable 2-Factor Authentication
3. Generate App Password
4. Use that password in `EMAIL_HOST_PASSWORD`

---

## 🚀 Deployment

### First Time Deployment

After initial setup, create superuser:
```bash
cd /home/deploy/safalclasses/backend
source venv/bin/activate
python manage.py createsuperuser
deactivate
```

### Regular Deployments

For updates, use the deployment script:
```bash
cd /home/deploy/safalclasses
chmod +x deployment/scripts/deploy.sh
./deployment/scripts/deploy.sh
```

This will:
- ✅ Pull latest code
- ✅ Install dependencies
- ✅ Run migrations
- ✅ Build frontend
- ✅ Collect static files
- ✅ Restart services

---

## 🔄 Maintenance

### Check Service Status
```bash
# Check Gunicorn (Django)
sudo systemctl status safalclasses

# Check Nginx
sudo systemctl status nginx
```

### View Logs
```bash
# Django/Gunicorn logs
sudo journalctl -u safalclasses -f

# Nginx access logs
sudo tail -f /var/log/nginx/safalclasses_access.log

# Nginx error logs
sudo tail -f /var/log/nginx/safalclasses_error.log

# Django error logs
sudo tail -f /home/deploy/safalclasses/backend/logs/django_errors.log
```

### Restart Services
```bash
# Restart Django
sudo systemctl restart safalclasses

# Restart Nginx
sudo systemctl restart nginx

# Reload Nginx (without downtime)
sudo systemctl reload nginx
```

### SSL Certificate Renewal

Certbot auto-renews, but to manually renew:
```bash
sudo certbot renew
sudo systemctl reload nginx
```

### Database Backup
```bash
# Backup SQLite database
cd /home/deploy/safalclasses/backend
cp db.sqlite3 db.sqlite3.backup-$(date +%Y%m%d-%H%M%S)
```

### Media Files Backup
```bash
# Backup media files
cd /home/deploy/safalclasses/backend
tar -czf media-backup-$(date +%Y%m%d).tar.gz media/
```

---

## 🐛 Troubleshooting

### Issue: 502 Bad Gateway

**Solution:**
```bash
# Check if Gunicorn is running
sudo systemctl status safalclasses

# If not running, start it
sudo systemctl start safalclasses

# Check logs
sudo journalctl -u safalclasses -n 50
```

### Issue: Static files not loading

**Solution:**
```bash
cd /home/deploy/safalclasses/backend
source venv/bin/activate
python manage.py collectstatic --noinput
deactivate
sudo systemctl restart safalclasses
```

### Issue: Permission denied errors

**Solution:**
```bash
sudo chown -R deploy:www-data /home/deploy/safalclasses
sudo chmod -R 755 /home/deploy/safalclasses
sudo chmod -R 775 /home/deploy/safalclasses/backend/media
```

### Issue: Database locked

**Solution:**
```bash
# Stop the service
sudo systemctl stop safalclasses

# Wait a moment
sleep 5

# Start again
sudo systemctl start safalclasses
```

### Issue: Frontend not updating

**Solution:**
```bash
cd /home/deploy/safalclasses/frontend
npm run build
sudo systemctl reload nginx
```

---

## 📊 Performance Optimization

### Enable Nginx Caching
Already configured in nginx config with:
- Static files: 30 days cache
- Media files: 7 days cache
- HTML: No cache (for SPA)

### Database Optimization (Future)
For production with many users, consider migrating to PostgreSQL:
```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Update .env with PostgreSQL settings
# Update settings.py DATABASES configuration
```

### Monitor Resources
```bash
# Check disk usage
df -h

# Check memory
free -h

# Check CPU
top
```

---

## 🔐 Security Checklist

- ✅ DEBUG=False in production
- ✅ Strong SECRET_KEY (50+ characters)
- ✅ HTTPS enabled (SSL certificate)
- ✅ HSTS headers enabled
- ✅ Security headers configured
- ✅ Firewall enabled (UFW)
- ✅ Regular backups scheduled
- ✅ .env file not in Git
- ✅ Database file not in Git (after initial setup)
- ✅ Strong admin password

---

## 📞 Support

For issues or questions:
- Check logs first
- Review this documentation
- Check Django/Nginx documentation

---

## 🎉 Success!

Your application should now be live at:
- **Website**: https://safalclasses.com
- **Admin Panel**: https://safalclasses.com/admin
- **API**: https://safalclasses.com/api/

**Happy Teaching! 🎓**
