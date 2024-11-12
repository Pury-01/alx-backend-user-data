#!/usr/bin/env python3
"""basic auth class that inherits from Auth.
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """basic auth class that inherits from auth.
    """
    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        """BasicAuth that returns Base64 part of the
         Authorization header for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[len("Basic "):]
