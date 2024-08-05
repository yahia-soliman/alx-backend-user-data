#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from typing import Tuple

from flask import Flask, Response, abort, jsonify, request
from flask_cors import CORS

from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
if getenv("AUTH_TYPE") == "auth":
    from api.v1.auth.auth import Auth

    auth = Auth()


@app.before_request
def before_request():
    """Handle the Authentication before any request"""
    if not auth or not auth.require_auth(
        request.path,
        ["/api/v1/status/", "/api/v1/unauthorized/", "/api/v1/forbidden/"],
    ):
        return
    if auth.authorization_header(request) is None:
        return abort(401)
    if auth.current_user(request) is None:
        return abort(403)


@app.errorhandler(404)
def not_found(_) -> Tuple[Response, int]:
    """Not found handler"""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(_) -> Tuple[Response, int]:
    """Not found handler"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(_) -> Tuple[Response, int]:
    """Not found handler"""
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=int(port))
