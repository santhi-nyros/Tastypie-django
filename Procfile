#web: gunicorn tastypie_sample.wsgi:application --log-file=-

web: gunicorn -w 2 tastypie_sample.wsgi:application  -b 0.0.0.0:$PORT --log-file -
#web: gunicorn --pythonpath="$PWD/tastypie_sample" wsgi:application --log-file=-
heroku ps:scale web=1

/Applications
/Applications/Firefox.app

celery: python manage.py celeryd --events --loglevel=INFO -c 5 --settings=settings -B
