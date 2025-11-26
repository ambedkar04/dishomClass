# 🔧 Environment Configuration Guide

## Quick Setup

### For Development

1. **Copy the example file:**
   ```bash
   cd backend
   cp .env.example .env
   ```

2. **Edit `.env` and set:**
   ```env
   DEBUG=True
   SECRET_KEY=any-random-string-for-development
   FRONTEND_BASE_URL=http://localhost:5173
   CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
   ```

3. **Run the server:**
   ```bash
   python manage.py runserver
   ```

---

### For Production

1. **Copy the example file on server:**
   ```bash
   cd /home/deploy/safalclasses/backend
   cp .env.example .env
   ```

2. **Generate SECRET_KEY:**
   ```bash
   python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

3. **Edit `.env` and configure:**
   ```env
   # Core Settings
   SECRET_KEY=<paste-generated-key-here>
   DEBUG=False
   ALLOWED_HOSTS=safalclasses.com,www.safalclasses.com,your-server-ip
   
   # Email (Gmail)
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=<gmail-app-password>
   DEFAULT_FROM_EMAIL=noreply@safalclasses.com
   
   # Frontend
   FRONTEND_BASE_URL=https://safalclasses.com
   CORS_ALLOWED_ORIGINS=https://safalclasses.com,https://www.safalclasses.com
   ```

4. **Restart services:**
   ```bash
   sudo systemctl restart safalclasses
   ```

---

## Environment Variables Reference

### Required Variables

| Variable | Description | Development | Production |
|----------|-------------|-------------|------------|
| `SECRET_KEY` | Django secret key | Any string | 50+ char random |
| `DEBUG` | Debug mode | `True` | `False` |
| `ALLOWED_HOSTS` | Allowed domains | `localhost,127.0.0.1` | `safalclasses.com,www.safalclasses.com` |
| `FRONTEND_BASE_URL` | Frontend URL | `http://localhost:5173` | `https://safalclasses.com` |

### Email Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `EMAIL_HOST` | SMTP server | `smtp.gmail.com` |
| `EMAIL_PORT` | SMTP port | `587` |
| `EMAIL_HOST_USER` | Email address | `your-email@gmail.com` |
| `EMAIL_HOST_PASSWORD` | App password | `abcd efgh ijkl mnop` |
| `DEFAULT_FROM_EMAIL` | From address | `noreply@safalclasses.com` |

### CORS Settings

| Variable | Description | Example |
|----------|-------------|---------|
| `CORS_ALLOWED_ORIGINS` | Allowed origins (comma-separated) | `https://safalclasses.com,https://www.safalclasses.com` |

---

## Gmail App Password Setup

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification**
3. Go to [App Passwords](https://myaccount.google.com/apppasswords)
4. Select **Mail** and **Other (Custom name)**
5. Enter "Safal Classes" as name
6. Copy the generated 16-character password
7. Use this in `EMAIL_HOST_PASSWORD`

---

## Security Best Practices

### ✅ DO:
- Generate a new `SECRET_KEY` for production
- Set `DEBUG=False` in production
- Use strong, unique passwords
- Keep `.env` file out of Git (it's in `.gitignore`)
- Use environment-specific values

### ❌ DON'T:
- Commit `.env` file to Git
- Use the same `SECRET_KEY` in dev and prod
- Share your `.env` file
- Set `DEBUG=True` in production
- Hardcode sensitive values in code

---

## Troubleshooting

### Issue: "SECRET_KEY not set"
**Solution:** Make sure `.env` file exists and contains `SECRET_KEY=...`

### Issue: "CORS errors in browser"
**Solution:** Check `CORS_ALLOWED_ORIGINS` includes your frontend URL

### Issue: "Email not sending"
**Solution:** 
1. Verify Gmail App Password is correct
2. Check 2FA is enabled on Google Account
3. Verify `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD`

### Issue: "Static files not loading"
**Solution:** Run `python manage.py collectstatic` and restart server

---

## File Locations

- **Example file**: `backend/.env.example` (tracked in Git)
- **Actual config**: `backend/.env` (NOT in Git, created by you)
- **Production**: `/home/deploy/safalclasses/backend/.env`

---

## Quick Reference

```bash
# Copy example file
cp .env.example .env

# Generate secret key
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Test configuration
python manage.py check

# View current settings (development only!)
python manage.py diffsettings
```

---

**Need help?** Check the main [DEPLOYMENT.md](./DEPLOYMENT.md) guide.
