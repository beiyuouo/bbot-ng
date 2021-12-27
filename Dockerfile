# syntax=docker/dockerfile:1

FROM python:3.8

WORKDIR /bbot-ng

COPY . .

RUN python -m pip install --upgrade pip \
    && pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "./bot.py"]