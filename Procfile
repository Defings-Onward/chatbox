  web: daphne chatproject.asgi:application --port $PORT
  worker: python manage.py runworker --clear-connections --settings chatproject.settings

