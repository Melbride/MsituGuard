#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

# Reset database and apply fresh migrations
python manage.py migrate --run-syncdb