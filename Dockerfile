# syntax=docker/dockerfile:1

FROM python:3.8-slim

WORKDIR /

COPY . .

RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt

CMD python bot.py