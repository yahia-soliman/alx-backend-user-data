#!/usr/bin/env python3
"""User Authentication Module"""

import bcrypt
from sqlalchemy.exc import NoResultFound

from db import DB, User


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Create a new user if not exists"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_pw = _hash_password(password).decode()
            return self._db.add_user(email, hashed_pw)
