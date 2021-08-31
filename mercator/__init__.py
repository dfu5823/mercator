__version__ = '0.1.0'

from dataclasses import dataclass
import flask
from flask.json import jsonify
import requests
from flask import Flask, Response, g, request
from http import HTTPStatus
import random
import logging

app = Flask(__name__)
if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


@app.route('/health', methods=["GET"])
def check_health():
    return "ok"


@app.route('/map_interface', methods=["POST"])
def map_interface():
    return "ok"
