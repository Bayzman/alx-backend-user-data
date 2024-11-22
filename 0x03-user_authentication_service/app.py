#!/usr/bin/env python3

""" Basic Flask app """

from flask import Flask, render_template
from flask import jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """ Returns a JSON response """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> str:
    """ Register user """
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already exists"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
