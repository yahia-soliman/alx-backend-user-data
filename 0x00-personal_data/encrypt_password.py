#!/usr/bin/env python3
"""Personal data
Password Encryption
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """encrypt a password with bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if a password is valid or not"""
    return bcrypt.checkpw(password.encode(), hashed_password)
