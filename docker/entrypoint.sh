#/bin/sh
cd srv/web/
mkdir -p /var/log/style-checker/
gunicorn style-service:app -b 0.0.0.0:8000 --error-logfile /var/log/style-checker/gnuicorn.log --workers=2
