#!/usr/bin/bash
pip install -r requirements.txt
rm db.sqlite3

./manage.py makemigrations
./manage.py migrate
