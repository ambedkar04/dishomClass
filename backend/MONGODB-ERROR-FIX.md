# ⚠️ MongoDB Connection Error - Quick Fix

## Problem Detected

```
pymongo.errors.ServerSelectionTimeoutError: localhost:27017
Connection refused - target machine actively refused it
```

**Cause:** MongoDB service is not running on your system.

---

## Quick Fix (Windows)

### Option 1: Start MongoDB Service

```bash
# Open Command Prompt or PowerShell as Administrator
net start MongoDB
```

### Option 2: Check if MongoDB is Installed

```bash
# Check MongoDB version
mongod --version
```

If this command fails, MongoDB is not installed.

---

## Solution: Install MongoDB

### Step 1: Download MongoDB

1. Go to: https://www.mongodb.com/try/download/community
2. Select:
   - Version: 7.0 (or latest)
   - Platform: Windows
   - Package: MSI
3. Download the installer

### Step 2: Install MongoDB

1. Run the downloaded `.msi` file
2. Choose **"Complete"** installation
3. **Important:** Check "Install MongoDB as a Service"
4. **Important:** Check "Install MongoDB Compass" (GUI tool)
5. Complete the installation

### Step 3: Verify Installation

```bash
# Open new Command Prompt
mongod --version

# Should show: db version v7.0.x
```

### Step 4: Start MongoDB Service

```bash
# Start service
net start MongoDB

# Verify it's running
mongosh --eval "db.version()"
```

---

## Alternative: Use MongoDB Atlas (Cloud)

If you don't want to install MongoDB locally, use MongoDB Atlas (free tier):

### 1. Create Account
- Go to: https://www.mongodb.com/cloud/atlas/register
- Sign up for free

### 2. Create Cluster
- Choose FREE tier (M0)
- Select region closest to you
- Create cluster (takes 3-5 minutes)

### 3. Get Connection String
- Click "Connect" on your cluster
- Choose "Connect your application"
- Copy the connection string

### 4. Update .env

```env
# Instead of localhost, use Atlas connection
MONGO_HOST=cluster0.xxxxx.mongodb.net
MONGO_PORT=27017
MONGO_USER=your-atlas-username
MONGO_PASSWORD=your-atlas-password
MONGO_DB_NAME=safalclasses_db
```

Or update settings.py to use full URI:
```python
MONGO_URI = "mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/safalclasses_db?retryWrites=true&w=majority"
```

---

## Temporary Solution: Switch Back to SQLite

If you want to continue development without MongoDB right now:

### Update settings.py

```python
# Comment out MongoDB configuration
# DATABASES = {
#     'default': {
#         'ENGINE': 'djongo',
#         ...
#     }
# }

# Use SQLite temporarily
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

Then run:
```bash
python manage.py migrate
python manage.py runserver
```

---

## Verify MongoDB is Running

### Windows:

```bash
# Check service status
sc query MongoDB

# Or use Services app
# Press Win+R, type: services.msc
# Look for "MongoDB" service
```

### Test Connection:

```bash
# Connect to MongoDB shell
mongosh

# Should show: connecting to: mongodb://127.0.0.1:27017
```

---

## Next Steps

After MongoDB is running:

1. ✅ Start MongoDB service
2. ✅ Run migrations: `python manage.py migrate`
3. ✅ Create superuser: `python manage.py createsuperuser`
4. ✅ Start server: `python manage.py runserver`

---

## Need Help?

See full guide: [MONGODB-WINDOWS.md](./MONGODB-WINDOWS.md)
