#!/bin/sh

gunicorn backend.wsgi:application --bind "0.0.0.0:8000"
