#!/usr/bin/env python3
""" Module for handling the comment logics C.R.U.D operations """
from flask import Blueprint, abort, jsonify, request

from models.base_redis import RedisServer
from models.comment import Comment
from models.question import Question
from models.base import db


comment = Blueprint('comment', __name__)


@comment.route('/questions/<int:id>/comments/<int:comment_id', methods=['PUT'])
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

    data = request.get_json()
    updated_comment = data.get("body")
    
    if not data or updated_comment:
        return jsonify({'error': 'Comment body is empty'}), 400

    # Check if the question is a valid question in the database & check if
    # the comment is also valid in the database related to the question
    question = db.session.query(Question).filter_by(id=id).first()
    if not question:
        abort(404)
    
    comment = db.session.query(Comment).filter_by(user_id=comment_id).first()
    if not comment:
        abort(404)
    comment.body = updated_comment
    comment.isEdited = True
    db.session.commit()  
    return jsonify({'message': 'Success, comment updated.'}), 201 
