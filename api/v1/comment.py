#!/usr/bin/env python3
""" Module for handling the comment logics C.R.U.D operations """
from api.v1 import question
from flask import Blueprint, abort, jsonify, request

from models.base_redis import RedisServer
from models.comment import Comment
from models.question import Question
from models.base import db
from models.user import User
from datetime import datetime, timezone


comment = Blueprint('comment', __name__)


@comment.route('/api/v1/questions/<int:id>/comments/<int:comment_id>',
               methods=['PUT'])
def update_comment(id, comment_id):
    """ Updates existing comment data """
    token = request.cookies.get('api-token')
    if not token:
        abort(401)

    redis = RedisServer()
    # Check if redis is connected to the database
    if not redis:
        return jsonify({'error': 'Redis is not running'}), 500

    username = redis.get(token)
    if not username:
        abort(401)

    user = db.session.query(User).filter_by(
        username=username.decode('utf-8')).first()
    if not user:
        abort(401)

    # Check if the question is a valid question in the database & check if
    # the comment is also valid in the database related to the question
    comment = db.session.query(Comment).filter_by(
        question_id=id, id=comment_id).first()
    if not comment:
        abort(404)

    if int(comment.user_id) != user.id:
        return jsonify(
            {'Error': 'You don\'t have permission to edit this comment'}
            ), 403

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400
    updated_comment = data.get("body")
    if not updated_comment:
        return jsonify({'error': 'Missing comment body'}), 400

    comment.body = updated_comment
    comment.isEdited = True
    db.session.commit()
    return jsonify({'message': 'Success, comment updated.'}), 200


# DELETE - /questions/<id>/comments/<id>
@comment.route('/api/v1/questions/<int:id>/comments/<int:comment_id>',
               methods=["DELETE"])
def delete_comment(id, comment_id):
    """ Deletes the comment based on the id of the comment and if the comment
    and if the comment is being posted by the owner of the comment """

    token = request.cookies.get('api-token')
    if not token:
        abort(401)

    redis = RedisServer()
    if not redis:
        return jsonify({'error': 'Redis is not running'}), 500
    username: str = redis.get(token)
    if not username:
        abort(401)
    try:
        user = db.session.query(User).filter_by(
            username=username.decode('utf-8')).first()
        if not user:
            abort(401)
        question = db.session.query(Question).filter_by(id=id).first()
        if not question:
            abort(404)
        comment = db.session.query(Comment).filter_by(
            question_id=id, id=comment_id).first()
        if not comment:
            abort(404)
        print("safe .......")
    except Exception as e:
        print("Error with fetching data from db: ", str(e))
        abort(404)

    # Check if the current user is the owner of the comment and have
    # access to delete the comment else abort 401
    if comment.user_id == user.id:
        db.session.delete(comment)
        db.session.commit()
        return jsonify({'message': 'Success, comment deleted'}), 200
    else:
        return jsonify(
            {'Error': 'You don\'t have permission to delete this comment'}
        ), 403


@comment.route('/api/v1/questions/<int:id>/comments', methods=['POST'])
def create_comment(id):
    """ route used to create a new comment """
    token = request.cookies.get('api-token')
    if not token:
        abort(401)

    redis = RedisServer()
    if not redis:
        return jsonify({'error': 'Redis is not running'}), 500
    username: str = redis.get(token)
    if not username:
        abort(401)

    user = db.session.query(User).filter_by(
        username=username.decode('utf-8')).first()
    if not user:
        abort(401)

    question = db.session.query(Question).filter_by(id=id).first()
    if not question:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400
    body = data.get("body")
    if not body:
        return jsonify({'error': 'Missing comment body'}), 400

    comment = Comment(
        body=body,
        created_at=datetime.now(timezone.utc),
        user_id=user.id,
        question_id=question.id
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify({'message': 'Success, comment created'}), 201
