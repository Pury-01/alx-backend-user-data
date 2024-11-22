#!/usr/bin/env python3
"""Flask Application
"""
from flask import Flask, jsonify, Response, request, abort
from flask import make_response, redirect
from auth import Auth


# Initialize Flask app
app = Flask(__name__)
AUTH = Auth()


# define a single GET route
@app.route("/", methods=['GET'])
def payload() -> Response:
    """Returns a JSON payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users() -> Response:
    """endpoint to register a new user with provided email and
    pasword
    """

    email = request.form.get("email")
    password = request.form.get("password")

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'])
def login() -> str:
    """Handles user login via POST /sessions.

    Returns:
        JSON respone containing user email and success login
        Aborts with 401 status code if login is invalid
    """

    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)

    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)

    return response


@app.route("/sessions", methods=['DELETE'])
def logout():
    """
    DELETE /sessions endpoint to log out a user.
    """
    session_id = request.cookies.get('session_id')

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    AUTH.destroy_session(user.id)

    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile():
    """
    profile of the user
    """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=['POST'])
def get_reset_passsword_token():
    """route to reset the user's password
    """
    email = request.form.get("email")

    if not email:
        abort(403)
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": token}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
