# 🎓 Safal Classes - Learning Management System

A complete Learning Management System (LMS) built with Django REST Framework and React, designed for online education platforms.

**Live Site**: [https://safalclasses.com](https://safalclasses.com)

---

## 🌟 Features

### For Students
- 📚 Access course materials and study resources
- 🎥 Watch live and recorded classes
- 📝 Track learning progress
- 👤 User authentication and profiles

### For Administrators
- 📊 Beautiful admin dashboard (Jazzmin)
- 👥 User management
- 📖 Course and batch management
- 📹 Live class scheduling
- 📄 Study material uploads

### Technical Features
- 🔐 JWT Authentication
- 🎨 Modern React UI with Tailwind CSS
- 📱 Responsive design
- 🚀 Production-ready deployment
- 🔒 HTTPS/SSL enabled
- 📊 RESTful API

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 5.2.1
- **API**: Django REST Framework
- **Authentication**: JWT (Simple JWT)
- **Database**: SQLite (Production-ready for PostgreSQL)
- **Admin**: Django Jazzmin
- **Server**: Gunicorn + Nginx

### Frontend
- **Framework**: React 19
- **Build Tool**: Vite
- **Styling**: Tailwind CSS 4
- **UI Components**: Radix UI
- **Routing**: React Router v7
- **Animations**: Framer Motion

---

## 🚀 Quick Start

### Development Setup

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

Access:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Admin Panel: http://localhost:8000/admin

---

## 🌐 Production Deployment

### Quick Deploy (Ubuntu Server)

```bash
# 1. Clone repository
git clone https://github.com/ambedkar04/DishomLMS.git
cd DishomLMS

# 2. Run setup script
chmod +x deployment/scripts/initial-setup.sh
sudo ./deployment/scripts/initial-setup.sh

# 3. Configure environment
sudo nano /home/deploy/safalclasses/backend/.env

# 4. Restart services
sudo systemctl restart safalclasses
```

**📖 Full Documentation**: [deployment/DEPLOYMENT.md](deployment/DEPLOYMENT.md)

---

## 📁 Project Structure

```
DishomLMS/
├── backend/                 # Django backend
│   ├── Dishom/             # Main project settings
│   ├── accounts/           # User management
│   ├── batch/              # Course batches
│   ├── study/              # Study materials
│   ├── live_class/         # Live classes
│   ├── media/              # Uploaded files
│   ├── static/             # Static files
│   └── requirements.txt    # Python dependencies
│
├── frontend/               # React frontend
│   ├── src/               # Source code
│   ├── public/            # Public assets
│   └── package.json       # Node dependencies
│
└── deployment/            # Production configs
    ├── nginx/            # Nginx configuration
    ├── systemd/          # Systemd services
    ├── scripts/          # Deployment scripts
    └── DEPLOYMENT.md     # Full deployment guide
```

---

## 🔧 Configuration

### Environment Variables

Create `.env` file in `backend/` directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=safalclasses.com,www.safalclasses.com

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

FRONTEND_BASE_URL=https://safalclasses.com
```

---

## 📚 API Endpoints

### Authentication
- `POST /api/accounts/register/` - User registration
- `POST /api/accounts/login/` - User login
- `POST /api/accounts/token/refresh/` - Refresh JWT token

### Batches & Courses
- `GET /api/batch/` - List all batches
- `GET /api/batch/{id}/` - Batch details

### Study Materials
- `GET /api/study/` - List study materials
- `GET /api/study/{id}/` - Material details

### Health Check
- `GET /health/` - Service health status
- `GET /api/` - API information

---

## 🔐 Security Features

- ✅ HTTPS/SSL encryption
- ✅ HSTS headers
- ✅ Secure cookies
- ✅ CSRF protection
- ✅ XSS protection
- ✅ Content Security Policy
- ✅ JWT authentication
- ✅ Password validation

---

## 📊 Monitoring

### Check Service Status
```bash
sudo systemctl status safalclasses
sudo systemctl status nginx
```

### View Logs
```bash
# Application logs
sudo journalctl -u safalclasses -f

# Nginx logs
sudo tail -f /var/log/nginx/safalclasses_access.log
```

---

## 🔄 Updates & Maintenance

### Deploy Updates
```bash
cd /home/deploy/safalclasses
./deployment/scripts/deploy.sh
```

### Backup Database
```bash
cd /home/deploy/safalclasses/backend
cp db.sqlite3 backup-$(date +%Y%m%d).db
```

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is private and proprietary.

---

## 👨‍💻 Developer

**Safal Classes Team**
- Website: [safalclasses.com](https://safalclasses.com)
- GitHub: [@ambedkar04](https://github.com/ambedkar04)

---

## 🆘 Support

For issues and questions:
1. Check [DEPLOYMENT.md](deployment/DEPLOYMENT.md)
2. Review logs
3. Open an issue on GitHub

---

**Made with ❤️ for education**
