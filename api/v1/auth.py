from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4

user: dict = {
    "username": "lawsonredeye",
    "password": generate_password_hash("Iam groot")
    }

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    """
    Handles the login feature of the User to check if the user has access
    to the api and returns a string

    Return:
        string token and a response status to indicate a successful
        login of the user
    """
    username: str = request.form.get("username", None)
    password: str = request.form.get("password", None)
    if username is None:
        return jsonify({"error": "Missing username"}), 400
    if password is None:
        return jsonify({"error": "Missing password"}), 400
    # make call to database to fetch user data and compare it
    if check_password_hash(user["password"], password):
        token: str = str(uuid4())
        return jsonify({"message": "Success", "api-token": token}), 200
    else:
        return jsonify({"error": "Incorrect password"})
