#!/usr/bin/env python3
"""hash password using bcrypt
"""
import bcrypt


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
