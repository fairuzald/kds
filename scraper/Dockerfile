FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip

RUN pip install \
  --default-timeout=100 \
  --retries 5 \
  --no-cache-dir \
  -r requirements.txt

COPY . /app

