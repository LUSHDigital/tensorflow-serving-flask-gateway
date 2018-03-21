FROM tiangolo/uwsgi-nginx-flask:python2.7

ENV APP_TFSERVING_HOST 0.0.0.0
ENV APP_TFSERVING_PORT 8080

COPY ./app /app

RUN pip install --upgrade pip
RUN /usr/local/bin/pip install -r /app/requirements.txt
