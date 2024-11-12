#!/usr/bin/env python3
"""Class auth to manage API authentication.
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """manages  the API authentication.
    """

    def require_auth(self, path: str, excluded_path: List[str]) -> bool:
        """Returns False."""
        return False

    def authorization_header(self, request=None) -> str:
        """returns None. request are Flask request object.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None.
        """
