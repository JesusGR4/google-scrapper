FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /django_server
WORKDIR /django_server
COPY . /django_server/
RUN pip install --upgrade pip && apt-get upgrade && apt-get update && apt-get install -y gettext && pip install -r requirements.txt
EXPOSE 8000