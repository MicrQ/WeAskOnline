#!/usr/bin/env python3
""" implementaion for Reply endpoints """
from crypt import methods
from api.v1 import comment
from models.reply import Reply
from models.comment import Comment
from flask import Blueprint, request, jsonify, abort
from models.base_redis import RedisServer
from models.base import db
from models.user import User
from datetime import datetime, timezone


reply = Blueprint('reply', __name__)


@reply.route('/api/v1/comments/<comment_id>/reply', methods=['POST'])
def create_reply(comment_id):
    """ Handles reply creation """
    token = request.cookies.get('api-token')
    if not token:
        abort(401)

    redis = RedisServer()
    if not redis:
        return jsonify({'Error': 'Redis server not available'}), 500

    username = redis.get(token)
    if username is None:
        abort(401)
    user = db.session.query(User).filter_by(
        username=username.decode('utf-8')).first()
    if not user:
        abort(401)

    comment = db.session.query(Comment).filter_by(id=comment_id).first()
    if not comment:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({'Error': 'Invalid JSON data'}), 400
    body = data.get('body')
    if not body:
        return jsonify({'Error': 'Missing body'}), 400

    reply = Reply(body=body, user_id=user.id, comment_id=comment_id)
    db.session.add(reply)
    db.session.commit()

    return jsonify({'message': "Reply created successfully."}), 201


@reply.route('/api/v1/comments/<comment_id>/reply/<reply_id>', methods=["PUT"])
def update_reply(comment_id, reply_id):
    """ update reply handler route """
    token = request.cookies.get('api-token')
    if not token:
        abort(401)

    redis = RedisServer()
    if not redis:
        return jsonify({'Error': 'Redis server not available'}), 500

    username = redis.get(token)
    if username is None:
        abort(401)
    user = db.session.query(User).filter_by(
        username=username.decode('utf-8')).first()
    if not user:
        abort(401)

    comment = db.session.query(Comment).filter_by(id=comment_id).first()
    if not comment:
        abort(404)

    reply = db.session.query(Reply).filter_by(
        id=reply_id, comment_id=comment_id).first()
    if not reply:
        abort(404)

    if reply.user_id != user.id:
        return jsonify(
            {'Error': 'You don\'t have permission to\
              update this reply.'}
            ), 403

    data = request.get_json()
    if not data:
        return jsonify({'Error': 'Invalid JSON data'}), 400
    body = data.get('body')
    if not body:
        return jsonify({'Error': 'Missing body'}), 400
    reply.body = body
    reply.isEdited = True
    db.session.commit()
    return jsonify({'message': "Reply updated successfully."}), 200
