#!/usr/bin/env python3
"""Handling API Authentication based on the Basic scheme"""

from typing import Dict
from uuid import uuid4

from .auth import Auth


class SessionAuth(Auth):
    """Authentication handler for the Basic scheme"""

    user_id_by_session_id: Dict[str, str] = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a new session id"""
        if isinstance(user_id, str):
            s_id = str(uuid4())
            self.user_id_by_session_id[s_id] = user_id
            return s_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Get the user's id based on session id"""
        return self.user_id_by_session_id.get(session_id)