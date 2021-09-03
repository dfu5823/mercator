__version__ = '0.1.0'

from dataclasses import dataclass
import flask
from flask.json import jsonify
import requests
from flask import Flask, Response, g, request
from http import HTTPStatus
import random
import logging
import os
import numpy
import cv2 as cv


def create_app():
    app = Flask(__name__)

    if __name__ != "__main__":
        gunicorn_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

    @app.errorhandler(400)
    def bad_request(e):
        """400 Errorhandler"""
        return jsonify(error=str(e)), 400

    @app.route('/health', methods=["GET"])
    def check_health():
        return flask.make_response("OK")

    @app.route('/map_interface', methods=["POST"])
    def map_interface() -> Response:
        """Map interface using image provided by request"""
        if request.method == 'POST':
            if 'file' not in request.files:
                return flask.abort(400)

            file = request.files['file']
            img = cv.imdecode(numpy.frombuffer(
                request.files['file'].read(), numpy.uint8), cv.IMREAD_UNCHANGED)

            thresh = 127
            im_bw = cv.threshold(img, thresh, 255, cv.THRESH_BINARY)[1]
            cv.imwrite('bw_image.png', im_bw)
        coordinates = {"x": 1, "y": 2}
        return jsonify(data={"coordinates": coordinates})

    return app
