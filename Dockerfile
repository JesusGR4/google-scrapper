FROM python:3.7
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY ./requirements.txt /app/
RUN pip install --upgrade pip
RUN apt-get upgrade && apt-get update && pip install --upgrade pip && pip install -r requirements.txt