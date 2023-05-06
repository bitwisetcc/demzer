#!/usr/bin/bash
pip freeze | xargs pip uninstall -y
pip install -r requirements.txt

rm db.sqlite3
./manage.py makemigrations
./manage.py migrate
