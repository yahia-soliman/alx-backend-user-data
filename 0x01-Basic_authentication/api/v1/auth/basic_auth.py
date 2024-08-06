#!/usr/bin/env python3
"""Module to handle API Authentication based on the Basic scheme"""

import base64
from typing import Optional, Tuple

from flask import Request

from models.user import User

from .auth import Auth


class BasicAuth(Auth):
    """Authentication handler for the Basic scheme"""

    def extract_base64_authorization_header(
        self, authorization_header: Optional[str]
    ) -> Optional[str]:
        """Get the base64 encoded string from the authorization header"""
        if isinstance(authorization_header, str):
            if authorization_header.startswith("Basic "):
                return authorization_header.rstrip()[6:]

    def decode_base64_authorization_header(
        self, base64_authorization_header: Optional[str]
    ) -> Optional[str]:
        """Decode a base64 encoded string"""
        try:
            return base64.b64decode(base64_authorization_header).decode()
        except Exception:
            return

    def extract_user_credentials(
        self, decoded_base64_authorization_header: Optional[str]
    ) -> Tuple:
        """Get the username, password from a decoded authorization header"""
        if isinstance(decoded_base64_authorization_header, str):
            if ":" in decoded_base64_authorization_header:
                return tuple(decoded_base64_authorization_header.split(":", 1))
        return None, None

    def user_object_from_credentials(
        self, user_email: Optional[str], user_pwd: Optional[str]
    ) -> Optional[User]:
        """Get the user object based on his email and password"""
        if isinstance(user_email, str) and isinstance(user_pwd, str):
            users = User.search({"email": user_email})
            if len(users) > 0 and users[0].is_valid_password(user_pwd):
                return users[0]

    def current_user(
        self, request: Optional[Request] = None
    ) -> Optional[User]:
        """Get the current logged in user, Basic Authentication shceme"""
        ah = self.authorization_header(request)
        b64 = self.extract_base64_authorization_header(ah)
        b64_decoded = self.decode_base64_authorization_header(b64)
        email, pwd = self.extract_user_credentials(b64_decoded)
        return self.user_object_from_credentials(email, pwd)