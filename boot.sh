#!/bin/bash
source venv/bin/activate
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done
exec gunicorn -b :8080 --access-logfile - --error-logfile - quiniela:app --workers=3 --threads=8 --worker-class=gthread
