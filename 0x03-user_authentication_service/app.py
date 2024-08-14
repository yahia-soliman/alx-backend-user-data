#!/usr/bin/env python3
"""Flask app for the authentication service"""

from flask import Flask, abort, jsonify, redirect, request, url_for

from auth import Auth

AUTH = Auth()
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/")
def get_root():
    """basic flask json"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """Register new user"""
    email = request.form.get("email")
    password = request.form.get("password")
    if not (email and password):
        return jsonify({"message": "email and password required"}), 400
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """Register new user"""
    email = request.form.get("email")
    password = request.form.get("password")
    if not (email and password and AUTH.valid_login(email, password)):
        return abort(401)
    session_id = AUTH.create_session(email)
    res = jsonify({"email": email, "message": "logged in"})
    res.set_cookie("session_id", session_id)
    return res if session_id else abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout():
    """Logout and delete session"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect("/")
    else:
        return abort(403)


@app.route("/profile")
def profile():
    """Get current user's profile"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email})
    else:
        return abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
