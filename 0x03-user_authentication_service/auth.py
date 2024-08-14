#!/usr/bin/env python3
"""User Authentication Module"""

import bcrypt
from sqlalchemy.exc import IntegrityError

from db import DB, User


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Get a new UUID4 string"""
    import uuid

    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Create a new user if not exists"""
        try:
            hashed_pw = _hash_password(password).decode()
            return self._db.add_user(email, hashed_pw)
        except IntegrityError:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Validate an email against a password"""
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return False
        return bcrypt.checkpw(password.encode(), user.hashed_password.encode())
