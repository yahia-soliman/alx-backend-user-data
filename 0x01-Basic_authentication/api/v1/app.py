#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from typing import Tuple

from flask import Flask, Response, jsonify
from flask_cors import CORS

from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.errorhandler(404)
def not_found(error) -> Tuple[Response, int]:
    """Not found handler"""
    print(error)
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> Tuple[Response, int]:
    """Not found handler"""
    print(error)
    return jsonify({"error": "Unauthorized"}), 401


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=int(port))
