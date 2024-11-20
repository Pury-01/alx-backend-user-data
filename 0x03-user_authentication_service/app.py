#!/usr/bin/env python3
"""Flask Application
"""
from flask import Flask, jsonify, Response, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
