FROM python:3.7

WORKDIR /usr/src

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN apt-get upgrade && apt-get update && pip install --upgrade pip && pip install -r requirements.txt