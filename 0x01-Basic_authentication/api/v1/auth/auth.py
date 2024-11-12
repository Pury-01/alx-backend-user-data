#!/usr/bin/env python3
"""Class auth to manage API authentication.
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """manages  the API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns False."""
        if path is None:
            return True

        if not excluded_paths:
            return True

        normalized_path = path if path.endswith('/') else path + '/'

        for excluded_path in excluded_paths:
            normalized_excluded_path = excluded_path if\
                    excluded_path.endswith('/') else excluded_path + '/'
            if normalized_path == normalized_excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """returns None. request are Flask request object.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None.
        """
        return None
