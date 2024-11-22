#!/usr/bin/env python3
"""End-to-end intergration test
"""
import requests


BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """register new user by sending POST request to /users
    endpoint
    """
    url = f"{BASE_URL}/users"
    data = {
            "email": email,
            "password": password
            }
    response = requests.post(url, data=data)

    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_passsword(email: str, password: str) -> None:
    """Attempts to log in with a wrong password
    """
    url = f"{BASE_UR}/sessions"
    data = {
            "email": email,
            "password": password
            }
    response = requests.post(url, data=data)

    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Login user using email and password
    """
    pass


def profile_unlogged() -> None:
    """for users whose profiles is unlogged
    """
    pass


def profile_logged(session_id: str) -> None:
    """for users whose profile is logged in
    """
    pass


def log_out(session_id: str) -> None:
    """clears the session and logs out the user
    """
    pass


def reset_password_token(email: str) -> str:
    """Resets the user's password
    """
    pass


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """updates the password of the user
    """
    pass


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
