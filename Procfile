web: flask db upgrade; gunicorn  quiniela:app --preload 
--workers=5 --threads=10 --worker-class=gthread 