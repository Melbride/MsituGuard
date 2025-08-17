@echo off
REM Windows build script for MsituGuard

REM Install dependencies
python -m pip install -r requirements.txt

REM Collect static files
python manage.py collectstatic --noinput

REM Run migrations
python manage.py migrate --noinput