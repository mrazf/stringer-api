FROM tiangolo/uwsgi-nginx-flask

COPY . /app

RUN pip install -r requirements.txt --src /usr/local/src