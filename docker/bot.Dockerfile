ARG PYTHON_VERSION=3.12.3
ARG VOSK_MODEL=vosk-model-small-ru-0.4

FROM python:$PYTHON_VERSION

ARG VOSK_MODEL

ENV PIP_NO_CACHE_DIR=on
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV DOCKER_MODE 1

WORKDIR /opt/app

RUN apt update && apt install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Download and extract the model
RUN mkdir -p /opt/app/models && \
    curl -L https://alphacephei.com/vosk/models/$VOSK_MODEL.zip -o /opt/app/models/$VOSK_MODEL.zip && \
    unzip /opt/app/models/$VOSK_MODEL.zip -d /opt/app/models && \
    rm /opt/app/models/$VOSK_MODEL.zip

#RUN /bin/bash -c "pip install torch==2.5.1 -f https://download.pytorch.org/whl/torch_stable.html"

COPY requirements.txt requirements.txt
RUN /bin/bash -c "pip install -r requirements.txt"

RUN chmod 755 .

COPY ./migrations ./migrations
COPY ./alembic.ini ./alembic.ini
COPY ./app ./app
