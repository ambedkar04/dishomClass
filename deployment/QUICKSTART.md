# 🚀 Quick Start - Production Deployment

## For Fresh Server (First Time Setup)

### 1️⃣ One-Command Setup
```bash
# Connect to your server
ssh root@your-server-ip

# Download and run setup
curl -o setup.sh https://raw.githubusercontent.com/ambedkar04/DishomLMS/main/deployment/scripts/initial-setup.sh
chmod +x setup.sh
sudo ./setup.sh
```

### 2️⃣ Configure Environment
```bash
sudo nano /home/deploy/safalclasses/backend/.env
```

Update these values:
- `SECRET_KEY` - Generate new one
- `EMAIL_HOST_USER` - Your Gmail
- `EMAIL_HOST_PASSWORD` - Gmail App Password

### 3️⃣ Restart & Go Live
```bash
sudo systemctl restart safalclasses
```

**Done! Visit: https://safalclasses.com** 🎉

---

## For Updates (After Initial Setup)

### Simple Update Command
```bash
cd /home/deploy/safalclasses
./deployment/scripts/deploy.sh
```

That's it! Your site is updated.

---

## Quick Commands

```bash
# View logs
sudo journalctl -u safalclasses -f

# Restart service
sudo systemctl restart safalclasses

# Check status
sudo systemctl status safalclasses

# Backup database
cd /home/deploy/safalclasses/backend
cp db.sqlite3 backup-$(date +%Y%m%d).db
```

---

## Need Help?

See full documentation: [DEPLOYMENT.md](./DEPLOYMENT.md)
