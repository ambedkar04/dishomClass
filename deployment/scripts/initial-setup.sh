#!/bin/bash

# Safal Classes - Initial Server Setup Script
# Run this ONCE on a fresh server to set up everything

set -e

echo "======================================"
echo "Safal Classes - Initial Setup"
echo "======================================"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# 1. Update system
print_status "Updating system packages..."
apt update && apt upgrade -y

# 2. Install required packages
print_status "Installing required packages..."
apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    nginx \
    git \
    curl \
    certbot \
    python3-certbot-nginx \
    nodejs \
    npm

# 3. Create deploy user
print_status "Creating deploy user..."
if ! id "deploy" &>/dev/null; then
    useradd -m -s /bin/bash deploy
    usermod -aG www-data deploy
    print_status "User 'deploy' created"
else
    print_warning "User 'deploy' already exists"
fi

# 4. Create project directory
print_status "Setting up project directory..."
PROJECT_DIR="/home/deploy/safalclasses"
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# 5. Clone repository (if not exists)
if [ ! -d "$PROJECT_DIR/.git" ]; then
    print_status "Cloning repository..."
    print_warning "Please enter your GitHub repository URL:"
    read REPO_URL
    git clone $REPO_URL .
else
    print_warning "Repository already cloned"
fi

# 6. Setup Python virtual environment
print_status "Creating Python virtual environment..."
cd $PROJECT_DIR/backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

# 7. Create necessary directories
print_status "Creating necessary directories..."
mkdir -p $PROJECT_DIR/backend/logs
mkdir -p $PROJECT_DIR/backend/media
mkdir -p $PROJECT_DIR/backend/staticfiles
mkdir -p /var/log/gunicorn

# 8. Set permissions
print_status "Setting permissions..."
chown -R deploy:www-data $PROJECT_DIR
chmod -R 755 $PROJECT_DIR
chmod -R 775 $PROJECT_DIR/backend/media
chmod -R 775 $PROJECT_DIR/backend/logs

# 9. Copy environment file
print_status "Setting up environment file..."
if [ ! -f "$PROJECT_DIR/backend/.env" ]; then
    cp $PROJECT_DIR/backend/.env.production $PROJECT_DIR/backend/.env
    print_warning "Please edit /home/deploy/safalclasses/backend/.env with your settings"
fi

# 10. Install Nginx configuration
print_status "Installing Nginx configuration..."
cp $PROJECT_DIR/deployment/nginx/safalclasses.conf /etc/nginx/sites-available/safalclasses.com
ln -sf /etc/nginx/sites-available/safalclasses.com /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
nginx -t

# 11. Install systemd service
print_status "Installing systemd service..."
cp $PROJECT_DIR/deployment/systemd/safalclasses.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable safalclasses

# 12. Build frontend
print_status "Building frontend..."
cd $PROJECT_DIR/frontend
npm install
npm run build

# 13. Run Django setup
print_status "Running Django setup..."
cd $PROJECT_DIR/backend
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput

# Create superuser
print_warning "Creating Django superuser..."
python manage.py createsuperuser

deactivate

# 14. Setup SSL with Let's Encrypt
print_status "Setting up SSL certificate..."
print_warning "Make sure your domain is pointing to this server!"
read -p "Press Enter to continue with SSL setup (or Ctrl+C to skip)..."

certbot --nginx -d safalclasses.com -d www.safalclasses.com

# 15. Start services
print_status "Starting services..."
systemctl start safalclasses
systemctl restart nginx

# 16. Enable firewall
print_status "Configuring firewall..."
ufw allow 'Nginx Full'
ufw allow OpenSSH
ufw --force enable

echo ""
print_status "======================================"
print_status "Setup completed successfully! 🎉"
print_status "======================================"
echo ""
print_status "Next steps:"
echo "1. Edit /home/deploy/safalclasses/backend/.env with your settings"
echo "2. Update SECRET_KEY, EMAIL settings, etc."
echo "3. Run: sudo systemctl restart safalclasses"
echo ""
print_status "Your site should be live at:"
echo -e "  ${GREEN}https://safalclasses.com${NC}"
echo ""
