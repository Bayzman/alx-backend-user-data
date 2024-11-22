#!/usr/bin/env python3

""" Basic Flask app """

from flask import Flask, render_template
from flask import jsonify, request, abort
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


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ Login """
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)
            return jsonify({"email": email, "message": "logged in",
                            "session_id": session_id}), 200
        else:
            abort(401, description="Invalid login")
    except Exception:
        abort(401, description="Invalid login")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
