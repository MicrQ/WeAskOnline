#!/usr/bin/env python3
""" Handles user-related operations """

from flask import Blueprint, request, jsonify, abort
from models.base_redis import RedisServer
from models.base import db
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta

user = Blueprint('user', __name__)

SECRET_KEY = 'your_secret_key'
TOKEN_EXPIRATION = 3600

def generate_token(username):
    """ Generate a JWT token for the given username """
    expiration = datetime.utcnow() + timedelta(seconds=TOKEN_EXPIRATION)
    payload = {
        'username': username,
        'exp': expiration
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

@user.route('/api/v1/register', methods=['POST'])
def register():
    """ Handle user registration """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    if db.session.query(User).filter_by(username=username).first():
        return jsonify({'error': 'User already exists'}), 400

    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@user.route('/api/v1/login', methods=['POST'])
def login():
    """ Handle user login """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = db.session.query(User).filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid username or password'}), 401

    # Generate a token and save it in Redis
    redis = RedisServer()
    token = generate_token(username)
    redis.set(token, username)

    return jsonify({'token': token}), 200

@user.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """ Get user details """
    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        abort(404)

    return jsonify(user.to_dict()), 200

@user.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """ Update user details """
    token = request.cookies.get('api-token')
    if not token:
        abort(401)

    redis = RedisServer()
    username = redis.get(token)
    if not username:
        abort(401)
    
    user = db.session.query(User).filter_by(username=username.decode('utf-8')).first()
    if not user:
        abort(401)

    if user.id != user_id:
        return jsonify({'error': 'You do not have permission to update this user'}), 403

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400
    
    password = data.get('password')
    if password:
        user.password = generate_password_hash(password)
    
    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200

@user.route('/api/v1/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ Delete a user """
    token = request.cookies.get('api-token')
    if not token:
        abort(401)

    redis = RedisServer()
    username = redis.get(token)
    if not username:
        abort(401)
    
    user = db.session.query(User).filter_by(username=username.decode('utf-8')).first()
    if not user:
        abort(401)

    if user.id != user_id:
        return jsonify({'error': 'You do not have permission to delete this user'}), 403

    user_to_delete = db.session.query(User).filter_by(id=user_id).first()
    if not user_to_delete:
        abort(404)

    db.session.delete(user_to_delete)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200
