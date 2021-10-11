#!/usr/bin/env bash
# start-server.sh
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (cd svdIris; python manage.py createsuperuser --no-input)
fi
(cd svdIris; gunicorn svdIris.wsgi --user www-data --bind 0.0.0.0:8010 --timeout 600 --workers 3) &
nginx -g "daemon off;"