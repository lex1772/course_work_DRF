FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev
ENV DOCKER_CONTAINER 1

WORKDIR /app
EXPOSE 8000

COPY requirements.txt .

RUN pip install -U pip && pip install -r requirements.txt

COPY . .
