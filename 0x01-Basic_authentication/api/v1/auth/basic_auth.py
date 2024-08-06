#!/usr/bin/env python3
"""Handling API Authentication based on the Basic scheme"""

import base64


from .auth import Auth


class BasicAuth(Auth):
    """Authentication handler for the Basic scheme"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:  # nopep8
        """Get the base64 encoded string from the authorization header"""
        if isinstance(authorization_header, str):
            if authorization_header.startswith("Basic "):
                return authorization_header.rstrip()[6:]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:  # nopep8
        """Decode a base64 encoded string"""
        try:
            return base64.b64decode(base64_authorization_header).decode()
        except Exception:
            return
