#!/bin/sh
echo "Start makemigrations"
python manage.py makemigrations /dev/null 2>&1;
echo "Start migrate"
python manage.py migrate /dev/null 2>&1;
echo "Start collectstatic"
python manage.py collectstatic --no-input /dev/null 2>&1;
echo "Start loaddata"
python manage.py loaddata dump.json /dev/null 2>&1;
echo "Start wsgi"
gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000 --error-logfile /code/logs/gunicorn.error.log --access-logfile /code/logs/gunicorn.access.log --capture-output --log-level debug

rm -f /app/pytest.ini
rm -rf /app/tests

cp pytest.ini /app/pytest.ini
cp -a tests/ /app/tests

cd /app
pip3 install -r requirements.txt
pytest --tb=line 1>&2

exec "$@"