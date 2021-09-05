# TO DO: Reduce size of container image (average 500-600mb)

# Define container build environment. In this case, a DEBIAN environment running python 3.8
FROM python:3.8 

# Update build enviornment and install OpenCV linux dependencies
RUN apt-get update && apt-get install --assume-yes ffmpeg tesseract-ocr

# Build the container's work directory
RUN mkdir /Mercator

# Copy project files (this example assumes these are at root dir) to cotainer work directory
COPY pyproject.toml poetry.lock /Mercator 

WORKDIR /Mercator

# Install poetry and install python dependencies
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-root

# Copy application files to /mercator dir (Should mirror file structure local/repo directory)
COPY mercator /Mercator/mercator
# Set environment variable to point to local/repo dir application dir
ENV APP_MODULE=mercator
ENV PYTHONPATH=mercator
# Define entrypoint, in this case running gunicorn on container start up
ENTRYPOINT [ \
    "gunicorn", \
    "--workers", "4", \
    "--bind", "0.0.0.0:8000", \
    "--access-logfile", "-", \
    "--chdir", "/Mercator", \
    "mercator:create_app()" \ 
]
