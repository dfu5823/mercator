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
from werkzeug.utils import secure_filename
import cv2 as cv


def create_app():

    UPLOAD_FOLDER = '/Users/zahza/mercator-files/'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    if __name__ != "__main__":
        gunicorn_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/health', methods=["GET"])
    def check_health():
        return "OK"

    @app.route('/map_interface', methods=["POST"])
    def map_interface() -> Response:
        if request.method == 'POST':
            if 'file' not in request.files:
                return "ERROR"
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filepath = app.config['UPLOAD_FOLDER'] + "/" + filename

                img = cv.imread(filepath, cv.IMREAD_GRAYSCALE)
                thresh = 127
                im_bw = cv.threshold(img, thresh, 255, cv.THRESH_BINARY)[1]
                cv.imwrite('bw_image.png', im_bw)
        coordinates = {"x": 1, "y": 2}
        return jsonify(data={"coordinates": coordinates})

    return app
