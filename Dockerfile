FROM python:3.9

ENV USER worker
ENV WORKDIR /app
ENV PATH "${WORKDIR}/${USER}/.local/bin:${PATH}"


RUN useradd -m $USER -b $WORKDIR --shell /bin/bash

WORKDIR $WORKDIR

COPY . .
RUN chown -R $USER:$USER $WORKDIR


USER $USER

RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r requirements.txt

ENV PYTHONPATH $WORKDIR

ENTRYPOINT ["python", "notion_gcal_sync/__main__.py"]
