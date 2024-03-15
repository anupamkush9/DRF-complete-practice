FROM python:3.8

RUN pip install --upgrade pip
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

