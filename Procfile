web: flask db upgrade; gunicorn  wsgi:app --preload --workers=5 --threads=10 --worker-class=gthread 