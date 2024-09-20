#!/usr/bin/env python3
"""Handles user-related operations"""

from flask import Blueprint, request, jsonify, abort
from models.base import db
from models.country import Country
from models.base import db
from models.user import User
from werkzeug.security import generate_password_hash
from models.base_redis import RedisServer

user = Blueprint('user', __name__)


@user.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user details"""
    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        abort(404)
    return jsonify(user.to_dict()), 200


@user.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user details"""
    token = request.cookies.get('api-token')
    if not token:
        abort(401)

    redis = RedisServer()
    username = redis.get(token)
    if not username:
        abort(401)

    user = db.session.query(User).filter_by(
        username=username.decode('utf-8')
    ).first()
    if not user:
        abort(401)

    if user.id != user_id:
        return jsonify({
            'error': 'You do not have permission to update this user'
        }), 403

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
    """Delete a user"""
    token = request.cookies.get('api-token')
    if not token:
        abort(401)

    redis = RedisServer()
    username = redis.get(token)
    if not username:
        abort(401)

    user = db.session.query(User).filter_by(
        username=username.decode('utf-8')
    ).first()
    if not user:
        abort(401)

    if user.id != user_id:
        return jsonify({
            'error': 'You do not have permission to delete this user'
        }), 403

    user_to_delete = db.session.query(User).filter_by(id=user_id).first()
    if not user_to_delete:
        abort(404)


    db.session.delete(user_to_delete)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200
