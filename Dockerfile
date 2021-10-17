FROM docker.io/python:latest

COPY . .

RUN pip install .

ENTRYPOINT ["notion-gcal-sync"]
