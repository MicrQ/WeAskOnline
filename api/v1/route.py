#!/usr/bin/env python3
from flask import Blueprint, jsonify

home = Blueprint('home', __name__)


@home.route('/api/v1/')
def index():
    """\
    Root directory and first page for the developer to find
    moveable routes which route to find resources and to develop the frontend

    Returns:
        JSON List[Dict] - list of keys and values (hyperlinks)
    """
    home_data = [
        {"message": "Hello, developer!"},
        {"login": "http://localhost:5000/api/v1/login"},
        {"register": "http://localhost:5000/api/register"},
        {"password_reset": "http://localhost:5000/api/password-reset"},
        {"user": "http://localhost:5000/api/users/<userid>"}
        ]
    return jsonify(home_data), 200
