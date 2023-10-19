#!/bin/sh

backend npm run build
python manage.py collectstatic --no-input
gunicorn backend.wsgi:application --bind "0.0.0.0:8080"
