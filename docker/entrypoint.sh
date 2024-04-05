#/bin/sh
cd srv/web/
gunicorn style-service:app -b 0.0.0.0:8000 --workers=1 --threads=1 --graceful-timeout 0 --timeout 0 --log-level=debug
