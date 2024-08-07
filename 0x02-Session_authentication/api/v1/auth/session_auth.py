#!/usr/bin/env python3
"""Handling API Authentication based on the Basic scheme"""

from uuid import uuid4

from .auth import Auth


class SessionAuth(Auth):
    """Authentication handler for the Basic scheme"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a new session id"""
        if isinstance(user_id, str):
            s_id = str(uuid4())
            self.user_id_by_session_id[s_id] = user_id
            return s_id
