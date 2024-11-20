#!/usr/bin/env python3
"""hash password using bcrypt
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """hash password using bcrypt

    Args:
        password (str): password to hash
    Return:
        bytes: Salted hash of the password
    """
    # generate salt
    salt = bcrypt.gensalt()

    # hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database
    """

    def __init__(self):
        """Initialize an instance of database
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers a user using email and password
        """

        # check if user already exists
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:

            # hash password and create user
            hashed_pwd = _hash_password(password)
            user = self._db.add_user(email, hashed_pwd)
            return user
