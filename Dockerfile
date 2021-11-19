# syntax=docker/dockerfile:1

FROM python:3.8-slim

WORKDIR /bbot-ng

COPY . .

RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "./bot.py"]