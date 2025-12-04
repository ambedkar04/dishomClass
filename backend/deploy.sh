#!/bin/bash
# Deployment script for Linux/Mac

echo "Deploying Tailwind CSS..."

# Navigate to theme directory
cd theme

# Install dependencies
echo "Installing Node dependencies..."
npm install

# Build CSS
echo "Building Tailwind CSS..."
npm run build

# Return to backend directory
cd ..

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Deployment preparation complete!"
