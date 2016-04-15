web: gunicorn askkit.wsgi --log-file -
celery: celery multi start -A askkit.celery default -c 2
flower: celery -A askkit.celery flower
