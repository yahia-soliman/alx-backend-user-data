#!/usr/bin/env python3
"""Module for managing API Authentication
"""

from typing import List, Optional

from flask import Request

from models.user import User


class Auth:
    """Class for managing Authentication"""

    def require_auth(
        self, path: Optional[str], excluded_paths: Optional[List[str]]
    ) -> bool:
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

    def authorization_header(
        self, request: Optional[Request] = None
    ) -> Optional[str]:
        """Get the Authorization Header from the request"""
        return request.headers.get("Authorization") if request else None

    def current_user(
        self, request: Optional[Request] = None
    ) -> Optional[User]:
        """Get the current logged in user"""
        return None
