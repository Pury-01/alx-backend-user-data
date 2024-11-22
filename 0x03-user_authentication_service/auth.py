#!/usr/bin/env python3
"""hash password using bcrypt
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Optional


def _generate_uuid() -> str:
    """returns a string representation of a new UUID
    """
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """validates user's login credentials
        """
        try:
            user = self._db.find_user_by(email=email)

            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
        except NoResultFound:
            pass
        return False

    def create_session(self, email: str) -> str:
        """Returns session ID as a string
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()

            self._db.update_user(user.id, session_id=session_id)

            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(
            self,
            session_id: Optional[str]
            ) -> Optional[User]:
        """Returns a corresponding user of session ID

        Args:
            session_id (str): session ID
        Returns:
            None: if None or no user found
            user (str): corresponding user to the session ID
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """updates the corresponding user's session ID to None
        """
        try:
            user = self._db.find_user_by(id=user_id)

            self._db.update_user(user.id, session_id=None)

        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """resets password token, returns the reset token
        """

        try:
            user = self._db.find_user_by(email=email)
        except ValueError:
            raise ValueError()

        reset_token = _generate_uuid()

        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """update the password and returns None
        """
        user = self._db.find_user_by(reset_token)

        if not user:
            raise ValueError()

        hashed_password = _hash_password(password)

        self._db.update_user(
                user.id,
                hashed_password=hashed_pasword,
                reset_token=None
                )
