FROM python:3.10.7-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt install -y gcc \
                          libc-dev \
                          libffi-dev

COPY requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /usr/src/app
CMD gunicorn -b 0.0.0.0:80 main:server