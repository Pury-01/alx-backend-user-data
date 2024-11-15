#!/usr/bin/env python3
"""class Sessionauth that inherits from Auth
"""
from .auth import Auth
import uuid
import os
from models.user import User


class SessionAuth(Auth):
    """inherits from Auth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        instance method that creates Session ID.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """returns User instance based on a cookie.
        """

        session_id = self.session_cookie(request)

        if not session_id:
            return None

        user_id = self.user_id_for_session_id(session_id)

        if not user_id:
            return None

        user = User.get(user_id)

        if not user:
            return None

        return user

    def destroy_session(self, request=None):
        """deletes the user session/logout.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        delself.user_id_by_session_id[session_id]
        return True
