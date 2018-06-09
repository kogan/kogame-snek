release: python manage.py migrate --noinput
web: daphne kogame.asgi:application --port $PORT --bind 0.0.0.0
worker: python manage.py runworker game_engine -v2
