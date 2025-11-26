# 🔍 Database Configuration - Problem & Solution

## ❌ Problem Found

**Error:** `pymongo.errors.ServerSelectionTimeoutError`
```
Connection refused to localhost:27017
The target machine actively refused the connection
```

**Root Cause:** MongoDB service is not running on the development machine.

---

## ✅ Solutions Provided

### Solution 1: Install & Start MongoDB (Recommended for Production)

#### For Windows:
```bash
# Download from: https://www.mongodb.com/try/download/community
# Install as Windows Service
# Then start:
net start MongoDB
```

#### For Linux/Ubuntu:
```bash
# Install MongoDB
sudo apt install -y mongodb-org

# Start service
sudo systemctl start mongod
sudo systemctl enable mongod
```

**See:** `MONGODB-WINDOWS.md` or `MONGODB-SETUP.md` for detailed instructions

---

### Solution 2: Use SQLite (Quick Development Fix) ⭐ **EASIEST**

**No MongoDB installation needed!**

Just update your `.env` file:

```env
# Change this line:
USE_MONGODB=False

# That's it! Now using SQLite
```

Then run:
```bash
python manage.py migrate
python manage.py runserver
```

---

### Solution 3: Use MongoDB Atlas (Cloud)

Free cloud MongoDB - no local installation needed!

1. Create account: https://www.mongodb.com/cloud/atlas/register
2. Create free cluster (M0)
3. Get connection string
4. Update `.env`:
```env
USE_MONGODB=True
MONGO_HOST=cluster0.xxxxx.mongodb.net
MONGO_USER=your-username
MONGO_PASSWORD=your-password
```

---

## 🎯 Quick Fix (Right Now)

**To get your server running immediately:**

1. **Edit `.env` file:**
   ```env
   USE_MONGODB=False
   ```

2. **Run migrations:**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

3. **Start server:**
   ```bash
   python manage.py runserver
   ```

**Done! Server will run with SQLite.**

---

## 🔄 Switching Between Databases

### Use MongoDB:
```env
USE_MONGODB=True
```

### Use SQLite:
```env
USE_MONGODB=False
```

**That's it!** No code changes needed.

---

## 📊 Database Comparison

| Feature | MongoDB | SQLite |
|---------|---------|--------|
| **Installation** | Required | Built-in |
| **Setup Time** | 10-15 min | 0 min |
| **Performance** | Excellent | Good |
| **Scalability** | High | Limited |
| **Best For** | Production | Development |
| **Cloud Option** | MongoDB Atlas | N/A |

---

## 🚀 Recommended Workflow

### For Development:
```env
USE_MONGODB=False  # Use SQLite - no setup needed
```

### For Production:
```env
USE_MONGODB=True   # Use MongoDB - better performance
```

---

## ✅ Changes Made to Fix This

### 1. Updated `settings.py`
- Added `USE_MONGODB` environment variable
- Automatic fallback to SQLite if MongoDB not available
- No code changes needed to switch databases

### 2. Updated `.env.example`
- Added `USE_MONGODB=True` option
- Clear documentation for both options

### 3. Created Documentation
- `MONGODB-ERROR-FIX.md` - This file
- `MONGODB-WINDOWS.md` - Windows installation guide
- `MONGODB-SETUP.md` - Complete setup guide

---

## 🧪 Test Database Connection

```bash
# Test current database
python manage.py shell

# In shell:
from django.db import connection
connection.ensure_connection()
print("Connected to:", connection.settings_dict['ENGINE'])
exit()
```

---

## 📝 Summary

**Problem:** MongoDB not installed/running
**Solution:** Added database toggle - can use SQLite or MongoDB
**Quick Fix:** Set `USE_MONGODB=False` in `.env`

**No more connection errors!** ✅

---

## 🆘 Still Having Issues?

1. Check `.env` file exists (copy from `.env.example`)
2. Verify `USE_MONGODB` setting
3. Run `python manage.py check`
4. Check error logs

**Need help?** See:
- `MONGODB-ERROR-FIX.md` - Detailed troubleshooting
- `MONGODB-WINDOWS.md` - Windows setup
- `MONGODB-SETUP.md` - Complete guide
