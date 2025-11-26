# 🚀 Quick MongoDB Setup for Windows Development

## Install MongoDB on Windows

### Option 1: MongoDB Community Server (Recommended)

1. **Download MongoDB**
   - Go to: https://www.mongodb.com/try/download/community
   - Select: Windows, MSI package
   - Download and run installer

2. **Installation Steps**
   - Choose "Complete" installation
   - Install MongoDB as a Service (recommended)
   - Install MongoDB Compass (GUI tool)

3. **Verify Installation**
   ```bash
   # Open Command Prompt or PowerShell
   mongod --version
   ```

### Option 2: Using Chocolatey

```powershell
# Install Chocolatey first (if not installed)
# Then run:
choco install mongodb

# Start MongoDB service
net start MongoDB
```

---

## Configure Your Project

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Setup Environment File

```bash
# Copy example file
copy .env.example .env
```

Edit `.env` and set:
```env
# MongoDB Configuration
MONGO_DB_NAME=safalclasses_db
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_USER=
MONGO_PASSWORD=
```

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

### 5. Run Server

```bash
python manage.py runserver
```

---

## MongoDB Compass (GUI)

MongoDB Compass is automatically installed with MongoDB Community Server.

**Connect to local database:**
- Connection String: `mongodb://localhost:27017`
- Database: `safalclasses_db`

---

## Troubleshooting

### Issue: "MongoDB service not running"

**Solution:**
```bash
# Start MongoDB service
net start MongoDB

# Or run mongod manually
mongod --dbpath C:\data\db
```

### Issue: "Data directory not found"

**Solution:**
```bash
# Create data directory
mkdir C:\data\db
```

### Issue: "Port 27017 already in use"

**Solution:**
```bash
# Check what's using the port
netstat -ano | findstr :27017

# Kill the process or use different port in .env
MONGO_PORT=27018
```

---

## Quick Commands

```bash
# Start MongoDB service
net start MongoDB

# Stop MongoDB service
net stop MongoDB

# Connect to MongoDB shell
mongosh

# View databases
show dbs

# Use your database
use safalclasses_db

# View collections
show collections
```

---

## Next Steps

After MongoDB is running:

1. ✅ MongoDB installed and running
2. ✅ `.env` configured
3. ✅ Migrations run
4. ✅ Superuser created
5. ✅ Server running at http://localhost:8000

**You're ready to develop! 🎉**

---

## Resources

- [MongoDB Windows Installation Guide](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows/)
- [MongoDB Compass Documentation](https://www.mongodb.com/docs/compass/)
- [Full MongoDB Setup Guide](./MONGODB-SETUP.md)
