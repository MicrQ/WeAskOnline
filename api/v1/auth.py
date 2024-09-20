#!/usr/bin/env python3
from base64 import b64decode, b64encode
from datetime import datetime
from os import name
from flask import Blueprint, Response, jsonify, make_response, request
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash

from models.base import db
from models.base_redis import RedisServer
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

    username = username.strip().lower()
    # make call to database to fetch user data and compare it
    user = db.session.query(User).filter_by(username=username).first()
    if user is None:
        return jsonify({"error": "Invalid username"}), 401
    if check_password_hash(user.password, password):
        # store the token on the user cookie with key & token as value
        if not user.isActive:
            return jsonify({"error": "User account is inactive"}), 403

        token: str = str(uuid4())

        redisConnect = RedisServer()
        resp = redisConnect.set_token(token, username)

        # Check if token was stored in redis server
        if not resp:
            return jsonify({"error": "Couldn't  connect to Redis server"}), 500

        # Store the token in the cookie session & expire age at 5 days
        res = jsonify({"message": "Success", "api-token": token})
        res.set_cookie('api-token', token, max_age=60 * 60 * 24 * 5)
        return res, 200
    else:
        return jsonify({"error": "Incorrect password"}), 401


@auth.route('/api/v1/register', methods=['POST'])
def register():
    """
    handles the registering of new users using the data gotten via the
    request.form

    Return:
        <Response 201> and redirects to the login page to confirm success
    """
    try:
        username: str = request.form.get("username").strip().lower()
        password: str = request.form.get("password")
        email: str = request.form.get("email").strip().lower()
        first_name: str = request.form.get("firstname").strip().lower()
        last_name: str = request.form.get("lastname").strip().lower()
        country: str = request.form.get("country").strip().title()

        if not username:
            return jsonify({"error": "Missing username"}), 400
        if not password:
            return jsonify({"error": "Missing password"}), 400
        if not email:
            return jsonify({"error": "Missing email address"}), 400
        if not first_name:
            return jsonify({"error": "Missing first name"}), 400
        if not last_name:
            return jsonify({"error": "Missing last name"}), 400
        if not country:
            return jsonify({"error": "Missing country"}), 400

        # Inputing user's data into database
        country_id = db.session.query(Country).filter_by(name=country).first()
        if not country_id:
            return jsonify({"error": "Country not found"}), 400

        # Create user instance
        user_data: dict = {}
        user_data['username'] = username
        user_data['bio'] = ''
        user_data['firstname'] = first_name
        user_data['lastname'] = last_name
        user_data['password'] = generate_password_hash(password)
        user_data['email'] = email
        user_data['country_id'] = country_id.id

        # Send OTP to user email for verification
        OTP = send_token(email)
        if not OTP:
            return jsonify({'error': 'email not valid'}), 400

        r = RedisServer()
        res = r.hset(email, OTP, user_data)
        if not res:
            return jsonify({'error': 'email not sent'}), 400

        encoded_email = b64encode(bytes(email.encode())).decode()

        return jsonify({
            "message": "Success,user created. Please verifiy your email",
            "data": user_data,
            "link": f"http://localhost:5000/api/v1/verify-email?key={encoded_email}"
            }), 201
    except Exception as e:
        return jsonify(
            {"error": "Server error, empty data found"}
            ), 500


@auth.route('/api/v1/verify-email', methods=['POST'])
def verify_email():
    """
    Route for handling and processing email
    """
    # Fetch data from redis
    # Validate the user token from redis and create the user in the database
    if request.args:
        get_key: str = request.args.get("key")
        decoded: bytes = get_key.encode()
        email_key: str = b64decode(decoded).decode()
    else:
        email_key: str = request.form.get("email")
    user_otp = request.form.get("otp")

    if not email_key:
        return jsonify({"error": "Missing email address"}), 400

    # Check & validate if the user's OTP is an int
    try:
        if not user_otp or not isinstance(int(user_otp), int):
            return jsonify({"error": "Please, provide valid OTP"}), 400
    except ValueError:
        return jsonify({"error": "Please, provide valid OTP"}), 400

    # Connect to redis and fetch token
    redis_otp = RedisServer()
    user_data = redis_otp.hgetall(email_key)

    # Convert dict[byte(str)] to dict[string] & add created date
    user_data = {k.decode(): v.decode() for k, v in user_data.items()}
    user_data['created_at'] = datetime.now()
    user_data['updated_at'] = datetime.now()
    
    otp = user_data.get('token')

    # validate token
    if not otp:
        return jsonify({'error': 'token expired or invalid'}), 401
    result = verify_token(int(user_otp), int(otp))
    if result:
        del user_data['token']
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'success, email verified'}), 200
    else:
        return jsonify({'error': 'email not verified'}), 401


@auth.route('/api/v1/logout', methods=['GET'])
def logout():
    """\
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
    """\
    route for handling password reset for users that has
    forgotten their password
    and also checks if the email is stored in the database
    """
    # check if the user is logged in before fetching
    # the data or the access token or if token is valid
    # Retrieve the token from the redis server and send the OTP to the
    data = request.get_json()
    password: str = str(data.get('password'))
    if not data.get('email'):
        return jsonify({"error": "Please provide email address"}), 400
    if not password:
        return jsonify({"error": "provide password"}), 400
    try:
        user_email = db.session.query(User).filter_by(
            email=data['email']).first()
        user_email.password = generate_password_hash(password)
        db.session.commit()
        db.session.close()
        return jsonify({"message": "Success, password changed"}), 201
    except Exception as e:
        print(e)
        return jsonify({"error": e}), 500
