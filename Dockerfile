FROM python:3.8

RUN pip install --upgrade pip

ENV PYTHONDONTWRITEBYTECODE 1
# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1


WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

