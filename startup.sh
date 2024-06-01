#!/bin/sh
# exit on error
set -o errexit

cp /data/settings.py /app/core/

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files for nginx
python manage.py collectstatic --no-input

# Startup webapp
gunicorn --config /data/gunicorn-cfg.py core.wsgi
