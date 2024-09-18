#!/usr/bin/env python3
from datetime import datetime
from flask import Blueprint, jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4
from base64 import b64decode, b64encode
from models import db, User
from models.country import Country
from utils.email_controller import send_token, verify_token
from redis_server import RedisServer

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
    username: str = request.form.get("username", None).lower()
    password: str = request.form.get("password", None)
    if username is None:
        return jsonify({"error": "Missing username"}), 400
    if password is None:
        return jsonify({"error": "Missing password"}), 400

    user = db.session.query(User).filter_by(username=username).first()
    if user is None:
        return jsonify({"error": "Invalid username"}), 401
    if check_password_hash(user.password, password):
        if not user.isActive:
            return jsonify({"error": "User account is inactive"}), 403

        token = str(uuid4())

        redisConnect = RedisServer()
        resp = redisConnect.set_token(token, username)

        # Check if token was stored in Redis server
        if not resp:
            return jsonify({"error": "Couldn't connect to Redis server"}), 500

        # Store the token in the cookie session & expire age at 5 days
        res = jsonify({"message": "Success", "api-token": token})
        res.set_cookie('api-token', token, max_age=60 * 60 * 24 * 5)
        return res, 200
    else:
        return jsonify({"error": "Incorrect password"}), 401


@auth.route('/api/v1/register', methods=['POST'])
def register():
    """
    Handles the registering of new users using the data gotten via the
    request.form

    Return:
        <Response 201> and redirects to the login page to confirm success
    """
    try:
        username = request.form.get("username").strip().lower()
        password = request.form.get("password")
        email = request.form.get("email").strip().lower()
        first_name = request.form.get("firstname").strip().lower()
        last_name = request.form.get("lastname").strip().lower()
        country = request.form.get("country").strip().title()

        if not all([
            username, password, email, first_name, last_name, country
        ]):
            return jsonify({"error": "Missing required fields"}), 400

        # Check if country exists in the database
        country_id = db.session.query(Country).filter_by(name=country).first()
        if not country_id:
            return jsonify({"error": "Country not found"}), 400

        # Create user instance
        user_data = {
            'username': username,
            'bio': '',
            'firstname': first_name,
            'lastname': last_name,
            'password': generate_password_hash(password),
            'email': email,
            'country_id': country_id.id,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }

        # Send OTP to user email for verification
        OTP = send_token(email)

        r = RedisServer()
        res = r.hset(email, OTP, user_data)
        if not res:
            return jsonify({'error': 'Email not sent'}), 400

        encoded_email = b64encode(email.encode()).decode()

        return jsonify({
            "message": "User created successfully. Please verify your email.",
            "data": user_data,
            "link": (
               f"http://localhost:5000/api/v1/verify-email?key={encoded_email}"
            )
        }), 201

    except Exception as e:
        print(f"Error: {e}", exc_info=True)
        return jsonify(
            {"error": "Server error, empty data found"}
            ), 500


@auth.route('/api/v1/verify-email', methods=['POST'])
def verify_email():
    """
    Route for handling and processing email
    """
    # Fetch data from redis
    if request.args:
        get_key = request.args.get("key")
        decoded = b64decode(get_key.encode()).decode()
        email_key = decoded
    else:
        email_key = request.form.get("email")

    user_otp = request.form.get("otp")

    if not email_key:
        return jsonify({"error": "Missing email address"}), 400

    # Check & validate if the user's OTP is an int
    try:
        if not user_otp or not isinstance(int(user_otp), int):
            return jsonify({"error": "Please, provide valid OTP"}), 400
    except ValueError:
        print("user provided a non integer parameter")
        return jsonify({"error": "Please, provide valid OTP"}), 400

    # Connect to redis and fetch token
    redis_otp = RedisServer()
    user_data = redis_otp.hgetall(email_key)

    # Convert dict[byte(str)] to dict[string] & add created date
    user_data = {k.decode(): v.decode() for k, v in user_data.items()}
    user_data['created_at'] = datetime.now()
    user_data['updated_at'] = datetime.now()
    print(user_data)
    print(type(user_data))

    otp = user_data.get('token')

    # Validate token
    if not otp:
        return jsonify({'error': 'Token expired or invalid'}), 401

    result = verify_token(int(user_otp), int(otp))
    if result:
        del user_data['token']
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Success, email verified'}), 200
    else:
        return jsonify({'error': 'Email not verified'}), 401


@auth.route('/api/v1/logout', methods=['GET'])
def logout():
    """
    Deletes the found token from the cookie stored in the user's browser and
    also logs out the user
    """
    redis = RedisServer()
    if not redis:
        return jsonify({"error": "Redis server is not running"}), 500

    # find the token and delete it & handle cases where the token is not in
    # the redis cache
    res = jsonify({"message": "Logged out successfully"})
    try:
        redis_value = redis.delete(res.cookies.get('api-token'))
        if not redis_value:
            return jsonify({'error': 'Token not found'}), 400
        res.delete_cookie('api-token')
        return res, 204
    except:
        return jsonify({'error': 'Token not found'}), 400


@auth.route('/api/v1/reset-password', methods=["POST"])
def reset_password():
    """
    Route for handling password reset for users that
    have forgotten their password
    and also checks if the email is stored in the database
    """
    data = request.get_json()
    password = data.get('password')
    email = data.get('email')

    if not email:
        return jsonify({"error": "Please provide email address"}), 400
    if not password:
        return jsonify({"error": "Provide password"}), 400

    try:
        user = db.session.query(User).filter_by(email=email).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        user.password = generate_password_hash(password)
        db.session.commit()
        return jsonify({"message": "Success, password changed"}), 201
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
