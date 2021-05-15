#!/bin/bash

while ! python manage.py makemigrations  2>&1; do
   sleep 3
done

while ! python manage.py migrate  2>&1; do
   sleep 3
done

service cron start && python manage.py crontab add
mkdir  -p ~/swan/scheduler/logs
exec "$@"