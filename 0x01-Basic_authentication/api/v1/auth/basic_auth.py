#!/usr/bin/env python3
"""basic auth class that inherits from Auth.
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


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

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
        """returns decoded value of a Base64 string.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> (str, str):
        """returns the user email and password from Base64
        decoded value
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
            ) -> TypeVar('User'):
        """retrieves a User instance based on his email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User.search({"email": user_email})
        if not users:
            return None

        # verify password if user is found
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """retrieves the User instance for a request.
        """
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None

        b64_auth = self.extract_base64_authorization_header(auth_header)
        if not b64_auth:
            return None

        decoded_auth = self.decode_base64_authorization_header(b64_auth)
        if not decoded_auth:
            return None

        username, password = self.extract_user_credentials(decoded_auth)
        if username is None or password is None:
            return None

        user = self.user_object_from_credentials(username, password)
        return user
