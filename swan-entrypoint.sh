#!/bin/bash

while ! python manage.py makemigrations  2>&1; do
   sleep 3
done

while ! python manage.py migrate  2>&1; do
   sleep 3
done

exec "$@"