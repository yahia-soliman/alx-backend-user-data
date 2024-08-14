#!/usr/bin/env python3
"""User Authentication Module"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
