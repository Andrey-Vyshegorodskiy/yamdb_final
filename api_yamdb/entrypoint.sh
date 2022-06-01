#!/bin/sh
echo "Start makemigrations"
cd infra
python manage.py makemigrations /dev/null 2>&1;
echo "Start migrate"
python manage.py migrate /dev/null 2>&1;
echo "Start collectstatic"
python manage.py collectstatic --no-input /dev/null 2>&1;
echo "Start loaddata"
python manage.py loaddata dump.json /dev/null 2>&1;
echo "Start wsgi"
gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000
exec "$@"