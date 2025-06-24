release: python manage.py migrate --noinput && python manage.py setup_cache && python manage.py collectstatic --noinput
web: gunicorn eeveeEmporium.wsgi:application