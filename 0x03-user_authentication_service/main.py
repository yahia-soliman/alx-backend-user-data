#!/usr/bin/env python3
"""End-to-end integration test"""
import requests

BASEURL = "http://0.0.0.0:5000/"


def register_user(email: str, password: str) -> None:
    """doc doc u ment"""
    res = requests.post(
        BASEURL + "users",
        data={"email": email, "password": password},
    )
    assert res.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """doc doc u ment"""
    res = requests.post(
        BASEURL + "sessions",
        data={"email": email, "password": password},
    )
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """doc doc u ment"""
    res = requests.post(
        BASEURL + "sessions",
        data={"email": email, "password": password},
    )
    assert res.status_code == 200
    return res.cookies.get("session_id")


def profile_unlogged() -> None:
    """doc doc u ment"""
    res = requests.get(BASEURL + "profile")
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """doc doc u ment"""
    res = requests.get(BASEURL + "profile", cookies={"session_id": session_id})
    assert res.status_code == 200


def log_out(session_id: str) -> None:
    """doc doc u ment"""
    res = requests.delete(
        BASEURL + "sessions",
        cookies={"session_id": session_id},
    )
    assert res.status_code == 200


def reset_password_token(email: str) -> str:
    """doc doc u ment"""
    res = requests.post(BASEURL + "reset_password", data={"email": email})
    assert res.status_code == 200
    return res.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """doc doc u ment"""
    res = requests.put(
        BASEURL + "reset_password",
        data={
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password,
        },
    )
    assert res.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
