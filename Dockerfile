FROM python:3.8

RUN apt-get update && apt-get install --assume-yes ffmpeg 

RUN mkdir /app

COPY pyproject.toml poetry.lock /app 


WORKDIR /app

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY mercator /app/mercator
ENV APP_MODULE=mercator

ENTRYPOINT [ \
    "gunicorn", \
    "--workers", "4", \
    "--bind", "0.0.0.0:8000", \
    "--access-logfile", "-", \
    "--chdir", "/app", \
    "mercator:create_app()" \ 
]
