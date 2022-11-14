FROM python:3.9.5-slim

RUN useradd quiniela

WORKDIR /home/quiniela

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN apt-get update && apt-get -y install libpq-dev gcc && venv/bin/pip install psycopg2
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql cryptography


COPY app app
COPY migrations migrations
COPY quiniela.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP quiniela.py
RUN chown -R quiniela:quiniela ./
USER quiniela

EXPOSE 8080
ENTRYPOINT ["./boot.sh"]