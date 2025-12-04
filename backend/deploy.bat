@echo off
echo Deploying Tailwind CSS...

REM Navigate to theme directory
cd theme

REM Install dependencies
echo Installing Node dependencies...
call npm install

REM Build CSS
echo Building Tailwind CSS...
call npm run build

REM Return to backend directory
cd ..

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

echo Deployment preparation complete!
pause
