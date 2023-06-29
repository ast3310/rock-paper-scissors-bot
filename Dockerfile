FROM python:3.8
WORKDIR /home/bot

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /home/bot/requirements.txt
RUN pip install -r requirements.txt

COPY . /home/bot