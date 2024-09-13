#!/usr/bin/env python3
from datetime import datetime
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4  # Add this import
from models.base import db
from models.country import Country
from models.user import User
from flask_sqlalchemy import SQLAlchemy


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
    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    user = db.session.query(User).filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 400

    token = str(uuid4())
    res = jsonify({"message": "Success", "api-token": token})
    res.set_cookie('api-token', token, max_age=60 * 60 * 24)
    return res, 200

@auth.route('/api/v1/register', methods=['POST'])
def register():
    """
    Handles the registering of new users using the data gotten via the
    request.form

    Return:
        <Response 201> and redirects to the login page to confirm success
    """
    try:
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password")
        email = request.form.get("email", "").lower()
        first_name = request.form.get("firstname", "").lower()
        last_name = request.form.get("lastname", "").lower()
        country = request.form.get("country", "").lower()

        if not all([username, password, email, first_name, last_name, country]):
            return jsonify({"error": "Missing required fields"}), 400

        user_data = {
            'username': username,
            'bio': '',
            'firstname': first_name,
            'lastname': last_name,
            'password': generate_password_hash(password),
            'email': email,
            'country_id': 1,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()

        return jsonify({
            "message": "User created successfully. Please verify your email.",
            "data": user_data,
            "link": "http://localhost:5000/login"
        }), 201
    except Exception as e:
        print(e)
        return jsonify({"error": "Server error"}), 500

@auth.route('/api/v1/logout', methods=['GET'])
def logout():
    """
    Deletes the found token from the cookie stored in the user's browser and
    also logs out the user
    """
    res = jsonify({"message": "Logged out successfully"})
    res.delete_cookie('api-token')
    return res, 204
