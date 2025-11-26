# ✅ Production Deployment Checklist

Use this checklist before going live with safalclasses.com

---

## 🔧 Pre-Deployment

### Server Setup
- [ ] Ubuntu 20.04+ server ready
- [ ] Domain (safalclasses.com) pointing to server IP
- [ ] SSH access configured
- [ ] Firewall configured (UFW)
- [ ] Server has minimum 2GB RAM

### DNS Configuration
- [ ] A record: safalclasses.com → Server IP
- [ ] A record: www.safalclasses.com → Server IP
- [ ] DNS propagated (check with `dig safalclasses.com`)

---

## 🚀 Deployment Steps

### 1. Initial Setup
- [ ] Run `initial-setup.sh` script
- [ ] All dependencies installed
- [ ] Deploy user created
- [ ] Project cloned to `/home/deploy/safalclasses`

### 2. Configuration
- [ ] `.env` file created and configured
- [ ] `SECRET_KEY` generated (50+ characters)
- [ ] `DEBUG=False` set
- [ ] `ALLOWED_HOSTS` configured
- [ ] Email settings configured (Gmail App Password)
- [ ] `FRONTEND_BASE_URL` set to https://safalclasses.com

### 3. Database
- [ ] Migrations run (`python manage.py migrate`)
- [ ] Superuser created
- [ ] Initial data loaded (if any)

### 4. Static Files
- [ ] Frontend built (`npm run build`)
- [ ] Static files collected (`python manage.py collectstatic`)
- [ ] Media directory created with proper permissions

### 5. Services
- [ ] Gunicorn service installed
- [ ] Gunicorn service enabled
- [ ] Gunicorn service running
- [ ] Nginx installed and configured
- [ ] Nginx service running

### 6. SSL/HTTPS
- [ ] Certbot installed
- [ ] SSL certificate obtained
- [ ] SSL certificate auto-renewal configured
- [ ] HTTPS redirect working
- [ ] SSL test passed (https://www.ssllabs.com/ssltest/)

---

## 🔐 Security Checklist

### Django Settings
- [ ] `DEBUG = False`
- [ ] Strong `SECRET_KEY` (not in Git)
- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `CSRF_COOKIE_SECURE = True`
- [ ] `SECURE_HSTS_SECONDS` set
- [ ] `ALLOWED_HOSTS` properly configured
- [ ] CORS settings configured

### Server Security
- [ ] Firewall enabled (UFW)
- [ ] Only ports 80, 443, 22 open
- [ ] SSH key authentication (password disabled)
- [ ] Regular security updates enabled
- [ ] Fail2ban installed (optional but recommended)

### Files & Permissions
- [ ] `.env` file not in Git
- [ ] `.env` file permissions: 600
- [ ] Database file not tracked in Git (after initial push)
- [ ] Media folder: 775 permissions
- [ ] Logs folder: 775 permissions
- [ ] Owner: deploy:www-data

---

## 🧪 Testing

### Functionality Tests
- [ ] Homepage loads (https://safalclasses.com)
- [ ] Admin panel accessible (https://safalclasses.com/admin)
- [ ] Can login to admin
- [ ] API endpoints working
- [ ] Health check working (https://safalclasses.com/health)
- [ ] Static files loading
- [ ] Media uploads working

### Performance Tests
- [ ] Page load time < 3 seconds
- [ ] Images optimized
- [ ] Gzip compression enabled
- [ ] Browser caching working

### Security Tests
- [ ] HTTPS working
- [ ] HTTP redirects to HTTPS
- [ ] Security headers present
- [ ] No sensitive data in responses
- [ ] CORS properly configured

---

## 📊 Monitoring Setup

### Logging
- [ ] Django error logs configured
- [ ] Gunicorn logs accessible
- [ ] Nginx logs accessible
- [ ] Log rotation configured

### Monitoring
- [ ] Service status checks working
- [ ] Disk space monitoring
- [ ] Memory usage monitoring
- [ ] SSL expiry monitoring

---

## 🔄 Backup Strategy

### Automated Backups
- [ ] Database backup script created
- [ ] Media files backup script created
- [ ] Backup cron jobs configured
- [ ] Backup storage location configured
- [ ] Backup retention policy defined

### Manual Backup Test
- [ ] Database backup tested
- [ ] Database restore tested
- [ ] Media backup tested

---

## 📱 Post-Deployment

### Verification
- [ ] Site accessible from different devices
- [ ] Site accessible from different networks
- [ ] Mobile responsive
- [ ] All pages working
- [ ] Forms submitting correctly
- [ ] Email sending working

### Documentation
- [ ] Deployment documentation reviewed
- [ ] Admin credentials documented (securely)
- [ ] Emergency procedures documented
- [ ] Team trained on deployment process

### Monitoring
- [ ] Set up uptime monitoring (UptimeRobot, etc.)
- [ ] Set up error tracking (Sentry, etc.) - optional
- [ ] Google Analytics added - optional
- [ ] Search Console configured - optional

---

## 🎯 Go-Live Checklist

### Final Checks (Day Before)
- [ ] All tests passed
- [ ] Backup created
- [ ] Team notified
- [ ] Rollback plan ready
- [ ] Support team ready

### Launch Day
- [ ] Final deployment run
- [ ] Services restarted
- [ ] Smoke tests passed
- [ ] Monitoring active
- [ ] Team on standby

### Post-Launch (First 24 Hours)
- [ ] Monitor error logs
- [ ] Check performance metrics
- [ ] Verify user registrations working
- [ ] Check email delivery
- [ ] Monitor server resources

---

## 🆘 Emergency Contacts

```
Server Provider: __________________
Domain Registrar: __________________
SSL Provider: Let's Encrypt (auto-renew)
Email Provider: Gmail
```

---

## 📝 Notes

```
Deployment Date: __________________
Deployed By: __________________
Server IP: __________________
Database: SQLite (path: /home/deploy/safalclasses/backend/db.sqlite3)
```

---

## ✅ Sign-Off

- [ ] Technical Lead Approval
- [ ] Security Review Complete
- [ ] Performance Review Complete
- [ ] Ready for Production

**Signed**: __________________ **Date**: __________________

---

**🎉 Once all items are checked, you're ready to go live!**
