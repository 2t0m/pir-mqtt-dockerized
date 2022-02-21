FROM arm32v7/python:3.7-slim-buster

RUN apt-get update && apt-get install -y apt-utils python-dev python3-dev build-essential pkg-config
RUN pip3 install RPi.GPIO configparser paho-mqtt

RUN mkdir app

COPY /app /app
WORKDIR /app
CMD ["python", "./pir.py"]
