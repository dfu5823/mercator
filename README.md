# Mercator


## Installing Poetry (Mac)

    brew install poetry

## Development
This project uses [poetry][poetry-docs] to manage dependencies. Before anything else, install Poetry and then run

    poetry install

To run the server locally, run

    export PYTHONPATH="${PYTHONPATH}:Mercator/"

    poetry run env FLASK_APP=support FLASK_ENV=development flask run
