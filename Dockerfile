FROM python:3.9
RUN mkdir /src 
COPY /mercator /src
COPY pyproject.toml /src 
WORKDIR /src


ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

ENTRYPOINT [ \
    "gunicorn", \
    "--workers", "4", \
    "--bind", "0.0.0.0:8000", \
    "--access-logfile", "-", \
    "mercator:app" \
]
