#!/usr/bin/env python3
"""Module to handle API Authentication based on the Basic scheme"""

import base64
from typing import Optional, Tuple

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
        self, base64_authorization_header: str
    ) -> Optional[str]:
        """Decode a base64 encoded string"""
        try:
            return base64.b64decode(base64_authorization_header).decode()
        except Exception:
            return

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> Tuple:
        """Get the username, password from a decoded authorization header"""
        if isinstance(decoded_base64_authorization_header, str):
            if ":" in decoded_base64_authorization_header:
                return tuple(decoded_base64_authorization_header.split(":", 1))
        return None, None
