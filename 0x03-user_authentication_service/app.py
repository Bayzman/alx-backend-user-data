#!/usr/bin/env python3

""" Basic Flask app """

from flask import Flask, render_template
from flask import jsonify
from auth import Auth

app = Flask(__name__)
auth = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """ Returns a JSON response """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
