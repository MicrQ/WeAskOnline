#!/usr/bin/env python3
from flask import Blueprint, request, jsonify
from models.user import User
from models.base import db
from werkzeug.security import generate_password_hash

user_routes = Blueprint('user_routes', __name__)


@user_routes.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.get_json()
    required_fields = [
        'firstname', 'lastname', 'username', 'email', 'password'
        ]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=data['email']).first() is not None:
        return jsonify({"error": "Email already exists"}), 400

    if User.query.filter_by(username=data['username']).first() is not None:
        return jsonify({"error": "Username already exists"}), 400

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(
        firstname=data['firstname'],
        lastname=data['lastname'],
        username=data['username'],
        email=data['email'],
        password=hashed_password,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201


@user_routes.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieve a user by ID"""
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "username": user.username,
        "email": user.email,
        "bio": user.bio,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat(),
    }), 200
