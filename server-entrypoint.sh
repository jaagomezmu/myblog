#!/bin/bash

until cd /app/myblog
do
    echo "Waiting for server ..."
done

until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 5
done

DJANGO_SUPERUSER_PASSWORD=my_password \
DJANGO_SUPERUSER_USERNAME=my_user \
DJANGO_SUPERUSER_EMAIL=my_user@domain.com \
python manage.py createsuperuser \
--no-input

python manage.py runserver 0.0.0.0:8000

