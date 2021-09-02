# Overly complicated multistage build to reduce incremental upload on push to
# *just* the files from this project, ie about 12 KiB. This could almost
# certainly be simpler.


# Export dependencies as requirements.txt
FROM ubuntu:21.04
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install --assume-yes python3-venv pipx ffmpeg libopencv-dev python3-opencv
#RUN python3 -m pip install --user pipx
#RUN python3 -m pipx ensurepath --force
RUN pipx install poetry

COPY pyproject.toml poetry.lock /src/
WORKDIR /src

RUN pipx run poetry install 

ENTRYPOINT [ \
    "gunicorn", \
    "--workers", "4", \
    "--bind", "0.0.0.0:8000", \
    "--access-logfile", "-", \
    "mercator:app" \
]
