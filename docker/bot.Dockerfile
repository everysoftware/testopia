FROM python:3.12.3

ENV DOCKER_MODE 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python -m venv venv

RUN /bin/bash -c "source venv/bin/activate && pip install -r requirements.txt"

RUN chmod 755 .

COPY ./migrations ./migrations
COPY ./alembic.ini ./alembic.ini
COPY ./app ./app
