#!/usr/bin/env python3
"""Module for managing API Authentication
"""

from typing import List, Optional

from flask import Request


class Auth:
    """Class for managing Authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if a URL path requires auth or not"""
        return False

    def authorization_header(self, request: Optional[Request] = None) -> str:
        """Get the Authorization Header from the request"""
        return ""

    def current_user(self, request: Optional[Request] = None) -> TypeVar("User"):
        """Get the current logged in user"""
        return None
