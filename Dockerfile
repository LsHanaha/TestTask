FROM --platform=linux/amd64 python:3.10

LABEL "author"="Trishin"

RUN apt-get update
RUN mkdir /Alar

COPY requirements.txt /Alar
WORKDIR /Alar
RUN pip install --no-cache-dir -r requirements.txt

COPY /app /Alar/app
COPY start.py /Alar
EXPOSE 8888