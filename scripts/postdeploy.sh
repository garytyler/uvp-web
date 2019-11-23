#!/usr/bin/env bash

python manage.py makemigrations live
python manage.py migrate
python manage.py loaddata live



python manage.py makemigrations live && python manage.py migrate && python manage.py loaddata live