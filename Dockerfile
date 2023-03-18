FROM python:3.9-alpine
WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
