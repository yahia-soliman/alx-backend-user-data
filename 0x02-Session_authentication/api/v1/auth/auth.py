#!/usr/bin/env python3
"""Module for managing API Authentication
"""

from typing import List, TypeVar


class Auth:
    """Class for managing Authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if a URL path requires auth or not
        Returns:
            True  - requires authentication, when path is not excluded
            False - does not require auth, path is in the excluded_paths
        """
        if path is None or excluded_paths is None:
            return True
        if path in excluded_paths or path + "/" in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Get the Authorization Header from the request"""
        return request.headers.get("Authorization") if request else None

    def current_user(self, request=None) -> TypeVar("User"):
        """Get the current logged in user"""
        return None
