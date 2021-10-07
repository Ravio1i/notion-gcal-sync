FROM docker.io/python:latest

COPY . .

RUN pip install -r requirements.txt

RUN python main.py
