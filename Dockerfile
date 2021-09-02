FROM python:3.9
RUN mkdir /mercator 
COPY /mercator /mercator
COPY pyproject.toml /mercator 
WORKDIR /mercator


ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY /opt/venv/lib/python3.9/site-packages/mercator

ENTRYPOINT [ \
    "gunicorn", \
    "--workers", "4", \
    "--bind", "0.0.0.0:8000", \
    "--access-logfile", "-", \
    "mercator:app" \
]
