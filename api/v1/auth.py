#!/usr/bin/env python3
from datetime import datetime, timezone
from os import name
from flask import Blueprint, jsonify, request
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash

from models.base import db
from models.country import Country
from models.user import User


auth = Blueprint('auth', __name__)


@auth.route('/api/v1/login', methods=['POST'])
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
    user = db.session.query(User).filter_by(username = username).first()
    if user is None:
        return jsonify({"error": "Invalid username"}), 400
    if check_password_hash(user.password, password):
        # store the token on the user cookie with key & token as value
        token: str = str(uuid4())
        res = jsonify({"message": "Success", "api-token": token})
        res.set_cookie('api-token', token, max_age = 60 * 60 * 24)
        return res, 200
    else:
        return jsonify({"error": "Incorrect password"})


@auth.route('/api/v1/register', methods=['POST'])
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
        email: str = request.form.get("email").lower()
        first_name: str = request.form.get("firstname").lower()
        last_name: str = request.form.get("lastname").lower()
        country: str = request.form.get("country").lower()

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

        FORMAT: str = "%Y-%m-%d %H:%M:%S"
        country_id = "2"
        user_data: dict = {}
        user_data['username'] = username
        user_data['bio'] = ''
        user_data['firstname'] = first_name
        user_data['lastname'] = last_name
        user_data['password'] = generate_password_hash(password)
        user_data['email'] = email
        user_data['country_id'] = 1
        user_data['created_at'] = datetime.now()
        user_data['updated_at'] = datetime.now()
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        return jsonify({
            "message": "Success,user created. Please verifiy your email",
            "data": user_data,
            "link": "http://localhost:5000/login"
            }), 201
    except Exception as e:
        print(e)
        return jsonify({"error": "Server error, empty data found"}), 500
