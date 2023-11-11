FROM python:3.9-slim

WORKDIR /app

# Install basic SO and Python
RUN apt-get update --fix-missing \
	&& apt-get install -y --no-install-recommends \
		build-essential \
		libpq-dev \
		python-dev-is-python3 \
        wget curl vim locales zip unzip apt-utils \
		wait-for-it \
	&& rm -rf /var/lib/apt/lists/* \
    && pip install uwsgi uwsgitop

#### Prepare BACKEND Django API
COPY requirements.txt ./
COPY requirements-dev.txt ./

RUN pip install -r requirements-dev.txt

ENV PYTHONUNBUFFERED=1 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONIOENCODING=UTF-8
ENV SHELL=/bin/bash LANG=en_US.UTF-8

COPY . ./

EXPOSE 8000