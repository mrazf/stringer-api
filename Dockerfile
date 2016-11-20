FROM tiangolo/uwsgi-nginx-flask:flask-index

COPY ./requirements.txt /app
RUN pip install -r requirements.txt --src /usr/local/src

COPY . /app