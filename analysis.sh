#!/bin/bash

GREEN=`tput setaf 2`
banner () {
    echo "+------------------------------------------+"
    printf "| %-40s |\n" "`date`"
    echo "|                                          |"
    printf "|`tput bold` ${GREEN}%-40s `tput sgr0`|\n" "$@"
    echo "+------------------------------------------+"
}


measure_coverage () {
    coverage erase

    coverage run --source='.' manage.py test "$1" || true

    coverage report
}


django_apps () {
    local apps=`echo 'from django.conf import settings;apps = settings.INSTALLED_APPS; \
        apps = [x for x in apps if "django" not in x];exci = ["rest_framework", "corsheaders"]; \
        apps=list(set(apps) - set(exci));[print(x) for x in apps]' | ./manage.py shell`
    
    echo "$apps"
}


apps="$(django_apps)"
echo $apps

for app in $apps
do
    echo -e '\n\n'
    banner "Coverage of $app"
    measure_coverage $app
done
