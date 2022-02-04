FROM python:3.9.4-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

<<<<<<< HEAD
=======

>>>>>>> 881b1c7fc90a1e2862617ccbb668e8de3b115157
COPY ./requirements.txt /usr/src/app/requirements.txt


RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
        libressl-dev libffi-dev gcc musl-dev python3-dev \
        postgresql-dev bash \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /usr/src/app/requirements.txt \
    && rm -rf /root/.cache/pip


COPY . /usr/src/app/
