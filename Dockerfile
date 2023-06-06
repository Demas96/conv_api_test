FROM python:3

WORKDIR /Fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg

COPY . .

RUN mkdir -p ./app/sttatic/mp3