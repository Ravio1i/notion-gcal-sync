FROM python:3.9-slim

ENV USER worker
ENV PATH "/home/${USER}/.local/bin:${PATH}"

RUN useradd -m $USER --shell /bin/bash

WORKDIR /home/$USER

COPY . .
RUN chown -R $USER:$USER "/home/$USER"

USER $USER

RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r requirements.txt

ENV PYTHONPATH "/home/$USER"

ENTRYPOINT ["python", "notion_gcal_sync/__main__.py"]
