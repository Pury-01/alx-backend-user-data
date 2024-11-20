#!/usr/bin/env  python3
"""Flask Application
"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/", methods=['GET'])
def payload():
    """payload method that returns a dict in json
    """
    return jsonify({"message": "Bievenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
