import datetime
from flask import Blueprint, jsonify, request
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash

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


@auth.route('/register', methods=['POST'])
def register():
    """
    handles the registering of new users using the data gotten via the
    request.form

    Return:
        <Response 201> and redirects to the login page to confirm success
    """
    try:
        username: str = request.form.get("username").replace(" ", "").lower()
        password: str = request.form.get("password")
        email: str = request.form.get("email")
        first_name: str = request.form.get("firstname")
        last_name: str = request.form.get("lastname")
        country: str = request.form.get("country")

        if not username:
            return jsonify({"error": "Missing username"}), 400
        elif not password:
            return jsonify({"error": "Missing password"}), 400
        elif not email:
            return jsonify({"error": "Missing email address"}), 400
        elif not first_name:
            return jsonify({"error": "Missing first name"}), 400
        elif not last_name:
            return jsonify({"error": "Missing last name"}), 400
        elif not country:
            return jsonify({"error": "Missing country"}), 400

        user_data: dict = {}
        user_data['id'] = uuid4()
        user_data['username'] = username
        user_data['password'] = password
        user_data['email'] = email
        user_data['created_at'] = datetime.datetime.now()
        return jsonify({
            "message": "Success,user created",
            "data": user_data,
            "link": "http://localhost:5000/login"
            }), 201
    except Exception as e:
        print(e)
        return jsonify({"error": "Bad method, use POST"}), 500
