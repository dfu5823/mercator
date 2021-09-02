# Overly complicated multistage build to reduce incremental upload on push to
# *just* the files from this project, ie about 12 KiB. This could almost
# certainly be simpler.


# Export dependencies as requirements.txt
FROM ubuntu:21.04 as gen-requirements
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install --assume-yes python3-venv pipx ffmpeg
#RUN python3 -m pip install --user pipx
#RUN python3 -m pipx ensurepath --force
RUN pipx install poetry

COPY pyproject.toml poetry.lock /src/
WORKDIR /src

RUN pipx run poetry export --output requirements.txt


# Install dependencies
FROM python:3.9-alpine as deps-installer

COPY --from=gen-requirements /src/requirements.txt /tmp/requirements.txt
RUN python -m venv /opt/venv \
    && . /opt/venv/bin/activate \
    && pip install -r /tmp/requirements.txt


# Minimal image with dependencies installed
FROM python:3.9-alpine as deps
COPY --from=deps-installer /opt/venv /opt/venv


# Build this project
FROM deps as build
RUN . /opt/venv/bin/activate && pip install poetry-core>=1.0.0

COPY pyproject.toml poetry.lock /src/
COPY mercator/*.py /src/mercator/
WORKDIR /src

RUN . /opt/venv/bin/activate && pip install .


# Finally just copy this project's package on top of the deps image.
FROM deps
COPY --from=build \
    /opt/venv/lib/python3.9/site-packages/mercator \
    /opt/venv/lib/python3.9/site-packages/mercator

ENTRYPOINT [ \
    "/opt/venv/bin/gunicorn", \
    "--workers", "4", \
    "--bind", "0.0.0.0:8000", \
    "--access-logfile", "-", \
    "mercator:app" \
]
