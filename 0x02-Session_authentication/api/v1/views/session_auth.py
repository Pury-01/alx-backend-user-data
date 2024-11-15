#!/usr/bin/ env python3
"""
Flask view that handles all routes for the Session
authentication
"""
from models.user import User
from flask import request, jsonify, abort,  make_response
from os import getenv
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login():
    """POST /auth_session/login endpoints for Session Authentication
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password  missing"}), 400

    users = User.search({'email': email})

    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)

    if not session_id:
        abort(500)

    response = make_response(jsonify(user.to_json()))
    response.set_cookie(getenv("SESSION_NAME"), session_id)

    return response
