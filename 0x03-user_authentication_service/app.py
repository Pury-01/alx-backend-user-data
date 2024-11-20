#!/usr/bin/env python3
"""Flask Application
"""
from flask import Flask, jsonify, Response


# Initialize Flask app
app = Flask(__name__)


# define a single GET route
@app.route("/", methods=['GET'])
def payload() -> Response:
    """Returns a JSON payload
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
