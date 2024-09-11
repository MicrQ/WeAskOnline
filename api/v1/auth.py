#!/usr/bin/env python3
from datetime import datetime
from os import name
from flask import Blueprint, Response, jsonify, make_response, request
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash

from models.base import db
from models.country import Country
from models.user import User
from utils.email_controller import send_token, verify_token


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
    user = db.session.query(User).filter_by(username=username).first()
    if user is None:
        return jsonify({"error": "Invalid username"}), 400
    if check_password_hash(user.password, password):
        # store the token on the user cookie with key & token as value
        token: str = str(uuid4())
        res = jsonify({"message": "Success", "api-token": token})
        res.set_cookie('api-token', token, max_age=60 * 60 * 24)
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
        country: str = request.form.get("country").title()

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

        # Inputing user's data into database
        country_id = db.session.query(Country).filter_by(name=country).first()
        print(country_id.id)
        user_data: dict = {}
        user_data['username'] = username
        user_data['bio'] = ''
        user_data['firstname'] = first_name
        user_data['lastname'] = last_name
        user_data['password'] = generate_password_hash(password)
        user_data['email'] = email
        user_data['country_id'] = country_id.id
        user_data['created_at'] = datetime.now()
        user_data['updated_at'] = datetime.now()
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()

        # Send OTP to user email for verification
        OTP = send_token(email)
        if not OTP:
            return jsonify({'error': 'email not sent'}), 400
        resp = make_response('hello')
        resp.headers['auth'] = OTP
        return jsonify({
            "message": "Success,user created. Please verifiy your email",
            "data": user_data,
            "link": "http://localhost:5000/verify-email"
            }), 201
    except Exception as e:
        print(e)
        return jsonify({"error": "Server make_response('hello')error, empty data found"}), 500


@auth.route('/api/v1/verify-email', methods=['POST'])
def verify_email():
    """
    Route for handling and processing email
    """
    data = request.get_json()
    if not data or data['email']:
        return jsonify({"error": "Missing email address"}), 400
    otp = Response.auth
    result = verify_token(int(data['token']), int(otp))
    if result:
        return jsonify({'message': 'success, email verified'}), 200
    else:
        return jsonify({'error': 'email not verified'}), 401


@auth.route('/api/v1/logout', methods=['GET'])
def logout():
    """\
    Deletes the found token from the cookie stored in the user's browser and
    also logs out the user
    """
    res = jsonify({"message": "Logged out successfully"})
    res.delete_cookie('api-token')
    return res, 204


@auth.route('/api/v1/reset-password', methods=["POST"])
def reset_password():
    """\
    route for handling password reset for users that has forgotten their password
    and also checks if the email is stored in the database
    """
    data = request.get_json()
    password: str = str(data['password'])
    if not data['email']:
        return jsonify({"error": "Please provide email address"}), 400
    if not data['password']:
        return jsonify({"error": "provide password"}), 400
    try:
        user_email = db.session.query(User).filter_by(email=data['email']).first()
        user_email.password = generate_password_hash(password)
        db.session.commit()
        db.session.close()
        return jsonify({"message": "Success, password changed"}), 201
    except Exception as e:
        print(e)
        return jsonify({"error": e}), 500
    