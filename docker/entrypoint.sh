#/bin/sh
cd srv/web/
gunicorn text-metrics-service:app -b 0.0.0.0:8000 --workers=2
