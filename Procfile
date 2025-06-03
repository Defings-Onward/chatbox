  web: daphne chatproject.asgi:application --host 0.0.0.0 --port $PORT
  worker: python manage.py runworker --clear-connections --settings chatproject.settings

