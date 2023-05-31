FROM debian:stable-slim as base
RUN apt-get install ffmpeg

# set work directory
WORKDIR /audio-pingerprint

# pull the official base image
FROM python:3.10.5

# set work directory
WORKDIR /audio-pingerprint

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /audio-pingerprint
RUN pip install -r requirements.txt


# copy config
COPY ./config /audio-pingerprint/config
COPY . /audio-pingerprint

EXPOSE 5000

CMD ["python", "server.py"]