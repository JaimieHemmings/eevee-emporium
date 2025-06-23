release: python manage.py check_settings && python manage.py collectstatic --noinput && python manage.py migrate
web: gunicorn eeveeEmporium.wsgi:application