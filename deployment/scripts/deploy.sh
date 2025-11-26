#!/bin/bash

# Safal Classes - Production Deployment Script
# Run this script to deploy/update the application

set -e  # Exit on error

echo "======================================"
echo "Safal Classes - Deployment Script"
echo "======================================"

# Configuration
PROJECT_DIR="/home/deploy/safalclasses"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"
VENV_DIR="$BACKEND_DIR/venv"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Functions
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# 1. Pull latest code from GitHub
print_status "Pulling latest code from GitHub..."
cd $PROJECT_DIR
git pull origin main

# 2. Backend Deployment
print_status "Deploying Backend..."

cd $BACKEND_DIR

# Activate virtual environment
source $VENV_DIR/bin/activate

# Install/Update dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt --quiet

# Run migrations
print_status "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
print_status "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create logs directory if not exists
mkdir -p $BACKEND_DIR/logs

# 3. Frontend Deployment
print_status "Deploying Frontend..."

cd $FRONTEND_DIR

# Install dependencies
print_status "Installing Node dependencies..."
npm install --silent

# Build production bundle
print_status "Building React production bundle..."
npm run build

# 4. Restart services
print_status "Restarting services..."

# Restart Gunicorn
sudo systemctl restart safalclasses

# Reload Nginx
sudo systemctl reload nginx

# 5. Check service status
print_status "Checking service status..."
if systemctl is-active --quiet safalclasses; then
    print_status "Gunicorn service is running"
else
    print_error "Gunicorn service failed to start!"
    sudo systemctl status safalclasses
    exit 1
fi

if systemctl is-active --quiet nginx; then
    print_status "Nginx service is running"
else
    print_error "Nginx service failed to start!"
    sudo systemctl status nginx
    exit 1
fi

# 6. Cleanup
print_status "Cleaning up..."
deactivate

echo ""
print_status "======================================"
print_status "Deployment completed successfully! 🎉"
print_status "======================================"
echo ""
print_status "Your application is now live at:"
echo -e "  ${GREEN}https://safalclasses.com${NC}"
echo ""
print_status "Admin panel:"
echo -e "  ${GREEN}https://safalclasses.com/admin${NC}"
echo ""
