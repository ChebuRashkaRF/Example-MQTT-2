FROM python:3.9-slim-buster
WORKDIR /
ADD publisher.py /
RUN pip install paho-mqtt

