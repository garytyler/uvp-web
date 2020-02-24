release: python manage.py migrate --noinput
web: daphne backend.asgi:application --port $PORT --bind 0.0.0.0