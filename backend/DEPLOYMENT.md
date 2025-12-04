# Deployment Guide

## Prerequisites
- Node.js & npm
- Python & pip

## Production Build Steps

1. **Install Node Dependencies**:
   Navigate to the theme directory and install dependencies.
   ```bash
   cd theme
   npm install
   ```

2. **Build Tailwind CSS**:
   Run the build script to generate the minified CSS.
   ```bash
   npm run build
   ```

3. **Collect Static Files**:
   Collect all static files to the static root directory.
   ```bash
   cd ..
   python manage.py collectstatic
   ```

## Automation
You can use the provided scripts:
- Windows: `deploy.bat`
- Linux/Mac: `deploy.sh`
