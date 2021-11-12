FROM python:3.9-slim

ENV USER worker
ENV PATH "/home/${USER}/.local/bin:${PATH}"

RUN useradd -m $USER --shell /bin/bash

WORKDIR /home/$USER

COPY . .
RUN chown -R $USER:$USER "/home/$USER"

USER $USER

RUN pip install pip==21.3.1 poetry==1.1.11
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev

ENTRYPOINT ["notion-gcal-sync"]
