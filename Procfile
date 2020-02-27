release: python manage.py makemigrations live && python manage.py migrate && python manage.py loaddata live
web: daphne backend.asgi:application --port $PORT --bind 0.0.0.0