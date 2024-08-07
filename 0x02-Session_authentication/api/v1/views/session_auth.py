#!/usr/bin/env python3
"""All route handlers for the Session authentication."""

from flask import jsonify, request

from api.v1.views import app_views
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"])
def login():
    """Create a new user session"""
    email = request.form.get("email")
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get("password")
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 401
    user: User = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    else:
        from api.v1.app import auth

        session_id = auth.create_session(user.id)
        res = jsonify(user.to_json())
        res.set_cookie(auth.SESSION_NAME, session_id)
        return res, 200
